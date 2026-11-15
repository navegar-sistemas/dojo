"""Leitura da renderização do labirinto no terminal (I02, I03, I04, I21).

A saída padrão é dividida em blocos de 2 × HEIGHT + 1 linhas desenhadas
(as que têm ESC). As sequências SGR são lidas como uma máquina de estado:
``38;2;R;G;B`` troca a cor do texto, ``48;2;R;G;B`` a do fundo e o reset
(``0`` ou vazio) volta as duas a None, "sem cor". Cada linha vira uma
lista de caracteres com o texto e o fundo em vigor, e o bloco, uma grade
de (2H + 1) linhas por (4W + 1) colunas: o canto (i, j) fica na linha 2j,
coluna 4i; a célula (x, y) ocupa a linha 2y + 1, colunas 4x + 1 a 4x + 3,
com o centro na 4x + 2; a parede oeste dela é a coluna 4x dessa linha e a
norte, as colunas 4x + 1 a 4x + 3 da linha 2y. As paredes são lidas pelos
caracteres ``┃`` e ``━``; o caminho, pelos caracteres de texto ciano.
"""

import re
from collections import deque
from dataclasses import dataclass
from typing import NamedTuple

from suporte.labirinto import (
    DESLOCAMENTOS,
    DIRECOES,
    FECHADA,
    NOMES,
    Celula,
    Labirinto,
)
from suporte.sessao import PROMPT

Rgb = tuple[int, int, int]
Cor = Rgb | None
Posicao = tuple[int, int]

CORES: dict[str, Rgb] = {
    "branco": (255, 255, 255),
    "grafite": (31, 41, 55),
    "laranja": (194, 65, 12),
    "verde": (21, 128, 61),
    "azul": (29, 78, 216),
    "magenta": (217, 70, 239),
    "vermelho": (239, 68, 68),
    "ciano": (34, 211, 238),
    "cinza": (156, 163, 175),
}
NOMES_DAS_CORES = {rgb: nome for nome, rgb in CORES.items()}
BRANCO = CORES["branco"]
CIANO = CORES["ciano"]
RODIZIO = (CORES["grafite"], CORES["laranja"], CORES["verde"], CORES["azul"])
RESET = "\x1b[0m"
ESCAPE = "\x1b"
# O menu da figura do subject (I03), como o .feature 15 cita, antes do prompt.
MENU = (
    "=== A-Maze-ing ===",
    "1. Re-generate a new maze",
    "2. Show / Hide the shortest path",
    "3. Rotate the wall colours",
    "4. Quit",
)
ACOES_QUE_DESENHAM = ("1", "2", "3")
TROCA_DE_COR = "3"
SEQUENCIA = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
SGR = re.compile(r"\x1b\[[0-9;]*m")
# Qualquer sequência ESC: CSI, ou ESC seguido de um caractere (ex.: ESC c).
QUALQUER_ESC = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|.?)", re.DOTALL)
# Texto e fundo de 24 bits numa sequência só, como a I02 escreve.
PAR = re.compile(r"\x1b\[38;2;(\d+);(\d+);(\d+);48;2;(\d+);(\d+);(\d+)m")
# Caractere de caixa de cada soma de braços N=1, E=2, S=4, W=8 (I02).
GLIFOS = " ╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"
HORIZONTAL = GLIFOS[DIRECOES["E"] | DIRECOES["W"]]
VERTICAL = GLIFOS[DIRECOES["N"] | DIRECOES["S"]]
PERMITIDOS = frozenset(GLIFOS)
COLUNAS_POR_CELULA = 4
TEXTO = "texto"
FUNDO = "fundo"
# Camada da cor de cada elemento, nas regras da renderização do vocabulário.
CAMADAS = {
    "entrada": FUNDO,
    "saída": FUNDO,
    "células do caminho": TEXTO,
    "passagens do caminho": TEXTO,
    "42": FUNDO,
    "paredes": TEXTO,
}
ELEMENTOS = tuple(CAMADAS)
NOMES_DAS_DIRECOES = {"Norte": "N", "Leste": "E", "Sul": "S", "Oeste": "W"}
NENHUMA = "nenhuma"


class Caractere(NamedTuple):
    """Caractere impresso com as cores em vigor.

    Attributes:
        simbolo: O caractere.
        texto: Cor do texto, ou None sem cor.
        fundo: Cor do fundo, ou None sem cor.
    """

    simbolo: str
    texto: Cor
    fundo: Cor


Tela = list[list[Caractere]]


@dataclass
class Renderizacao:
    """Bloco de linhas desenhadas e as linhas impressas até o próximo."""

    linhas: list[str]
    seguinte: list[str]


def nome_da_cor(cor: Cor) -> str:
    """Nome da cor para as mensagens.

    Args:
        cor: RGB, ou None.

    Returns:
        O nome da I21, "sem cor" ou "RGB r,g,b".
    """
    if cor is None:
        return "sem cor"
    return NOMES_DAS_CORES.get(cor, "RGB {},{},{}".format(*cor))


def onde(posicao: Posicao) -> str:
    """Descreve a posição do desenho para as mensagens.

    Args:
        posicao: (linha, coluna) do desenho, a partir de 0.

    Returns:
        O texto "linha l, coluna c".
    """
    linha, coluna = posicao
    return f"linha {linha}, coluna {coluna}"


def descrever(caractere: Caractere) -> str:
    """Caractere e cores para as mensagens.

    Args:
        caractere: Caractere do desenho.

    Returns:
        O texto "'c' texto t, fundo f".
    """
    return (
        f"{caractere.simbolo!r} texto {nome_da_cor(caractere.texto)}, "
        f"fundo {nome_da_cor(caractere.fundo)}"
    )


def renderizacoes(saida: str, altura: int) -> list[Renderizacao]:
    """Divide a saída padrão em blocos de 2 × altura + 1 linhas desenhadas.

    Uma sequência de linhas desenhadas seguidas maior que o bloco vira
    vários blocos; o último pode ficar mais curto.

    Args:
        saida: Saída padrão inteira.
        altura: HEIGHT do config.

    Returns:
        Os blocos, na ordem em que foram impressos.
    """
    linhas = saida.split("\n")
    tamanho = 2 * altura + 1
    limites: list[tuple[int, int]] = []
    indice = 0
    while indice < len(linhas):
        if ESCAPE not in linhas[indice]:
            indice += 1
            continue
        fim = indice
        while fim < len(linhas) and ESCAPE in linhas[fim]:
            fim += 1
        for inicio in range(indice, fim, tamanho):
            limites.append((inicio, min(inicio + tamanho, fim)))
        indice = fim
    blocos: list[Renderizacao] = []
    for numero, (inicio, fim) in enumerate(limites):
        proximo = (
            limites[numero + 1][0] if numero + 1 < len(limites)
            else len(linhas)
        )
        blocos.append(Renderizacao(linhas[inicio:fim], linhas[fim:proximo]))
    return blocos


def seguida_do_menu(renderizacao: Renderizacao) -> bool:
    """Diz se as linhas logo depois do bloco são o menu e o prompt (I03).

    Args:
        renderizacao: Bloco desenhado.

    Returns:
        True quando as 5 linhas seguintes são as do menu e a sexta começa
        com o prompt.
    """
    seguinte = renderizacao.seguinte
    return (
        tuple(seguinte[:len(MENU)]) == MENU
        and len(seguinte) > len(MENU)
        and seguinte[len(MENU)].startswith(PROMPT)
    )


def _rgb(partes: list[str]) -> Cor:
    """Lê o "2;R;G;B" que segue um 38 ou um 48.

    Args:
        partes: Os parâmetros seguintes da sequência.

    Returns:
        A cor, ou None quando as partes não são 2 e três números de 0 a
        255.
    """
    if len(partes) < 4 or partes[0] != "2":
        return None
    canais = partes[1:4]
    if not all(canal.isdigit() and int(canal) <= 255 for canal in canais):
        return None
    vermelho, verde, azul = (int(canal) for canal in canais)
    return vermelho, verde, azul


def _aplicar_sgr(
    parametros: str, texto: Cor, fundo: Cor
) -> tuple[Cor, Cor, list[str]]:
    """Aplica os parâmetros de uma sequência SGR às cores em vigor.

    Args:
        parametros: Texto entre "ESC[" e "m".
        texto: Cor do texto antes da sequência.
        fundo: Cor do fundo antes dela.

    Returns:
        (texto, fundo, problemas): as cores depois da sequência e a
        descrição de cada parâmetro que não é reset nem cor de 24 bits.
    """
    partes = parametros.split(";")
    problemas: list[str] = []
    indice = 0
    while indice < len(partes):
        parametro = partes[indice]
        if parametro == "" or (parametro.isdigit() and int(parametro) == 0):
            texto = fundo = None
            indice += 1
            continue
        if parametro in ("38", "48"):
            cor = _rgb(partes[indice + 1:indice + 5])
            if cor is not None:
                if parametro == "38":
                    texto = cor
                else:
                    fundo = cor
                indice += 5
                continue
            problemas.append(f"parâmetro {parametro!r} sem 2;R;G;B de 0 a 255")
        else:
            problemas.append(
                f"parâmetro {parametro!r} não é cor de 24 bits nem reset"
            )
        indice += 1
    return texto, fundo, problemas


def visiveis(linha: str) -> list[Caractere]:
    """Caracteres impressos da linha, cada um com as cores em vigor.

    As sequências CSI não ocupam lugar; um ESC solto conta como caractere.
    A linha começa sem cor.

    Args:
        linha: Linha desenhada.

    Returns:
        Os caracteres, na ordem.
    """
    impressos: list[Caractere] = []
    texto: Cor = None
    fundo: Cor = None
    posicao = 0
    for casado in SEQUENCIA.finditer(linha):
        impressos.extend(
            Caractere(simbolo, texto, fundo)
            for simbolo in linha[posicao:casado.start()]
        )
        sequencia = casado.group()
        if sequencia.endswith("m"):
            texto, fundo, _ = _aplicar_sgr(sequencia[2:-1], texto, fundo)
        posicao = casado.end()
    impressos.extend(
        Caractere(simbolo, texto, fundo) for simbolo in linha[posicao:]
    )
    return impressos


def problemas_de_sgr(linha: str) -> list[str]:
    """Sequências da linha que não são cor de 24 bits nem reset, e ESC soltos.

    Args:
        linha: Linha desenhada.

    Returns:
        A descrição de cada problema, vazia quando a linha só usa as cores
        de 24 bits e o reset.
    """
    problemas: list[str] = []
    for casado in SEQUENCIA.finditer(linha):
        sequencia = casado.group()
        if not sequencia.endswith("m"):
            problemas.append(f"sequência que não é SGR: {sequencia!r}")
            continue
        _, _, achados = _aplicar_sgr(sequencia[2:-1], None, None)
        problemas.extend(f"{achado} em {sequencia!r}" for achado in achados)
    if ESCAPE in SEQUENCIA.sub("", linha):
        problemas.append("ESC fora de uma sequência CSI")
    return problemas


def problemas_do_formato(linha: str) -> list[str]:
    """Desvios da forma das sequências que a I02 fixa para cada linha.

    A linha abre com ``ESC[38;2;R;G;B;48;2;R;G;Bm``, só usa essa forma até
    o fim e termina com o reset, o único da linha.

    Args:
        linha: Linha desenhada.

    Returns:
        A descrição de cada desvio, vazia quando a linha segue a forma.
    """
    sequencias = list(SEQUENCIA.finditer(linha))
    if not sequencias:
        return ["a linha não tem sequência"]
    problemas: list[str] = []
    primeira = sequencias[0]
    if primeira.start() != 0 or not PAR.fullmatch(primeira.group()):
        problemas.append(
            f"a linha não abre com texto e fundo numa sequência só: "
            f"{linha[:40]!r}"
        )
    ultima = sequencias[-1]
    if ultima.group() != RESET or ultima.end() != len(linha):
        problemas.append(f"a linha não termina com o reset: {linha[-40:]!r}")
    for casado in sequencias[1:-1]:
        if not PAR.fullmatch(casado.group()):
            problemas.append(
                f"{casado.group()!r} no meio da linha não é texto e fundo "
                f"numa sequência só"
            )
    return problemas


def trocas_sem_mudanca(linha: str) -> list[str]:
    """Sequências da linha que não mudam o par de cores do caractere seguinte.

    Uma sequência repete o par em vigor, ou é seguida de outra sem nenhum
    caractere no meio; a última sequência da linha não conta.

    Args:
        linha: Linha desenhada.

    Returns:
        A descrição de cada sequência sobrando.
    """
    problemas: list[str] = []
    sequencias = list(SEQUENCIA.finditer(linha))
    atual: tuple[str, ...] | None = None
    for numero, casado in enumerate(sequencias[:-1]):
        seguinte = sequencias[numero + 1]
        if seguinte.start() == casado.end():
            problemas.append(
                f"{casado.group()!r} vem logo antes de {seguinte.group()!r}, "
                f"sem caractere no meio"
            )
        par = PAR.fullmatch(casado.group())
        cores = par.groups() if par else (casado.group(),)
        if cores == atual:
            problemas.append(
                f"{casado.group()!r} repete o par de cores em vigor"
            )
        atual = cores
    return problemas


def sequencias_que_nao_sao_sgr(texto: str) -> list[str]:
    """Sequências ESC do texto que não são SGR, CSI ou não.

    Args:
        texto: Saída padrão.

    Returns:
        As sequências, sem repetir, na ordem do texto.
    """
    achadas: list[str] = []
    for casado in QUALQUER_ESC.finditer(texto):
        sequencia = casado.group()
        if not SGR.fullmatch(sequencia) and sequencia not in achadas:
            achadas.append(sequencia)
    return achadas


def tela(renderizacao: Renderizacao) -> Tela:
    """Caracteres e cores de cada linha do bloco.

    Args:
        renderizacao: Bloco desenhado.

    Returns:
        Uma lista de caracteres por linha do bloco.

    Raises:
        ValueError: Quando as linhas têm números diferentes de caracteres.
    """
    desenho = [visiveis(linha) for linha in renderizacao.linhas]
    tamanhos = sorted({len(linha) for linha in desenho})
    if len(tamanhos) > 1:
        raise ValueError(
            f"as linhas do desenho têm números diferentes de caracteres: "
            f"{tamanhos}"
        )
    return desenho


def dimensoes(desenho: Tela) -> tuple[int, int]:
    """Largura e altura em células da grade desenhada.

    Args:
        desenho: Caracteres do bloco.

    Returns:
        (largura, altura).

    Raises:
        ValueError: Quando o desenho não tem 2n + 1 linhas de 4m + 1
            caracteres.
    """
    linhas = len(desenho)
    colunas = len(desenho[0]) if desenho else 0
    if (
        linhas < 3 or not linhas % 2
        or colunas < COLUNAS_POR_CELULA + 1
        or colunas % COLUNAS_POR_CELULA != 1
    ):
        raise ValueError(
            f"o desenho tem {linhas} linhas e {colunas} caracteres por "
            f"linha; uma grade precisa de 2n + 1 linhas de 4m + 1 "
            f"caracteres, com n e m >= 1"
        )
    return (colunas - 1) // COLUNAS_POR_CELULA, (linhas - 1) // 2


def da_celula(celula: Celula) -> Posicao:
    """Posição do centro da célula no desenho.

    Args:
        celula: Coordenada (x, y).

    Returns:
        (2y + 1, 4x + 2).
    """
    x, y = celula
    return 2 * y + 1, COLUNAS_POR_CELULA * x + 2


def interior(celula: Celula) -> set[Posicao]:
    """As 3 colunas do interior da célula.

    Args:
        celula: Coordenada (x, y).

    Returns:
        A linha 2y + 1, colunas 4x + 1 a 4x + 3.
    """
    linha, centro = da_celula(celula)
    return {(linha, centro - 1), (linha, centro), (linha, centro + 1)}


def da_passagem(celula: Celula, direcao: str) -> set[Posicao]:
    """Posições da parede da célula na direção.

    Args:
        celula: Coordenada (x, y).
        direcao: "N", "E", "S" ou "W".

    Returns:
        Uma posição na vertical (Leste, Oeste) e três na horizontal (Norte,
        Sul).
    """
    linha, centro = da_celula(celula)
    dx, dy = DESLOCAMENTOS[direcao]
    if dy:
        return {(linha + dy, centro + coluna) for coluna in (-1, 0, 1)}
    return {(linha, centro + 2 * dx)}


def glifo_da_parede(direcao: str) -> str:
    """Caractere da parede fechada na direção (I02).

    Args:
        direcao: "N", "E", "S" ou "W".

    Returns:
        ``━`` no Norte e no Sul, ``┃`` no Leste e no Oeste.
    """
    return HORIZONTAL if direcao in ("N", "S") else VERTICAL


def direcao_entre(primeira: Celula, segunda: Celula) -> str:
    """Direção que leva de uma célula à vizinha.

    Args:
        primeira: Coordenada (x, y).
        segunda: Coordenada vizinha.

    Returns:
        "N", "E", "S" ou "W".

    Raises:
        ValueError: Quando as células não são vizinhas.
    """
    deslocamento = (segunda[0] - primeira[0], segunda[1] - primeira[1])
    for direcao, passo in DESLOCAMENTOS.items():
        if passo == deslocamento:
            return direcao
    raise ValueError(f"{primeira} e {segunda} não são vizinhas")


def entre(primeira: Celula, segunda: Celula) -> set[Posicao]:
    """Posições da passagem do caminho entre duas células vizinhas.

    Args:
        primeira: Coordenada (x, y).
        segunda: Coordenada vizinha.

    Returns:
        As colunas 4x + 3 a 4x + 5 entre (x, y) e (x + 1, y), ou a linha
        2y + 2 entre (x, y) e (x, y + 1).
    """
    (x1, y1), (x2, y2) = primeira, segunda
    if y1 == y2:
        linha, centro = da_celula((min(x1, x2), y1))
        return {(linha, centro + coluna) for coluna in (1, 2, 3)}
    linha, centro = da_celula((x1, min(y1, y2)))
    return {(linha + 1, centro)}


def cantos(largura: int, altura: int) -> set[Posicao]:
    """Posições dos cantos entre as células: linha 2j, coluna 4i.

    Args:
        largura: WIDTH em células.
        altura: HEIGHT em células.

    Returns:
        As posições dos cantos.
    """
    return {
        (linha, coluna)
        for linha in range(0, 2 * altura + 1, 2)
        for coluna in range(0, COLUNAS_POR_CELULA * largura + 1,
                            COLUNAS_POR_CELULA)
    }


def bracos(fechadas: set[Posicao], canto: Posicao) -> int:
    """Soma dos braços que saem do canto para as paredes fechadas.

    Args:
        fechadas: Posições de parede fechada.
        canto: Posição do canto.

    Returns:
        O índice em GLIFOS: N=1, E=2, S=4, W=8.
    """
    linha, coluna = canto
    vizinhas = {
        "N": (linha - 1, coluna),
        "E": (linha, coluna + 1),
        "S": (linha + 1, coluna),
        "W": (linha, coluna - 1),
    }
    return sum(
        DIRECOES[direcao] for direcao, posicao in vizinhas.items()
        if posicao in fechadas
    )


def paredes_na_tela(desenho: Tela) -> set[Posicao]:
    """Posições de parede fechada do desenho, lidas pelos caracteres.

    São as colunas 4i das linhas ímpares com ``┃`` e as colunas fora dos
    cantos das linhas pares com ``━``.

    Args:
        desenho: Caracteres do bloco.

    Returns:
        As posições de parede fechada, sem os cantos.
    """
    fechadas: set[Posicao] = set()
    for linha, caracteres in enumerate(desenho):
        for coluna, caractere in enumerate(caracteres):
            vertical = coluna % COLUNAS_POR_CELULA == 0
            if linha % 2 and vertical and caractere.simbolo == VERTICAL:
                fechadas.add((linha, coluna))
            elif (
                not linha % 2 and not vertical
                and caractere.simbolo == HORIZONTAL
            ):
                fechadas.add((linha, coluna))
    return fechadas


def cor_das_paredes(desenho: Tela) -> Cor:
    """Cor das paredes, lida no texto do canto superior esquerdo.

    Args:
        desenho: Caracteres do bloco.

    Returns:
        O texto do caractere (0, 0).
    """
    return desenho[0][0].texto


def paredes_desenhadas(desenho: Tela, celula: Celula) -> set[str]:
    """Direções em que a célula aparece com parede.

    Args:
        desenho: Caracteres do bloco.
        celula: Coordenada (x, y).

    Returns:
        As direções cujas posições têm todas o caractere da parede.

    Raises:
        ValueError: Quando só parte das posições de uma parede tem o
            caractere dela.
    """
    fechadas: set[str] = set()
    for direcao in DIRECOES:
        glifo = glifo_da_parede(direcao)
        simbolos = [
            desenho[linha][coluna].simbolo
            for linha, coluna in sorted(da_passagem(celula, direcao))
        ]
        if all(simbolo == glifo for simbolo in simbolos):
            fechadas.add(direcao)
        elif glifo in simbolos:
            raise ValueError(
                f"a parede {NOMES[direcao]} da célula {celula} está "
                f"desenhada só em parte: {''.join(simbolos)!r}"
            )
    return fechadas


def grade_desenhada(desenho: Tela) -> list[list[int]]:
    """Bits de parede de cada célula, como o desenho mostra.

    Args:
        desenho: Caracteres do bloco.

    Returns:
        Uma linha de valores de 0 a 15 por linha de células.
    """
    largura, altura = dimensoes(desenho)
    return [
        [
            sum(
                DIRECOES[direcao]
                for direcao in paredes_desenhadas(desenho, (x, y))
            )
            for x in range(largura)
        ]
        for y in range(altura)
    ]


def cor_em(caractere: Caractere, camada: str) -> Cor:
    """Cor do caractere na camada do elemento.

    O texto de um espaço não aparece, e conta como sem cor.

    Args:
        caractere: Caractere do desenho.
        camada: TEXTO ou FUNDO.

    Returns:
        A cor da camada, ou None.
    """
    if camada == FUNDO:
        return caractere.fundo
    return caractere.texto if caractere.simbolo != " " else None


def posicoes_da_cor(desenho: Tela, cor: Cor) -> set[Posicao]:
    """Posições onde a cor aparece: no fundo ou no texto de um não espaço.

    Args:
        desenho: Caracteres do bloco.
        cor: RGB procurado.

    Returns:
        As posições com essa cor.
    """
    return {
        (linha, coluna)
        for linha, caracteres in enumerate(desenho)
        for coluna, caractere in enumerate(caracteres)
        if cor in (caractere.fundo, cor_em(caractere, TEXTO))
    }


def caminho_do_arquivo(labirinto: Labirinto) -> list[Celula]:
    """Células do caminho do rodapé, da entrada em diante.

    Args:
        labirinto: Labirinto lido do arquivo de saída.

    Returns:
        A entrada seguida da célula de cada letra do caminho.

    Raises:
        ValueError: Quando falta a entrada ou o caminho, uma letra não é
            N, E, S ou W ou o caminho sai da grade.
    """
    if labirinto.entrada is None:
        raise ValueError(f"o rodapé não tem a entrada: {labirinto.rodape}")
    if not labirinto.caminho:
        raise ValueError(f"o rodapé não tem o caminho: {labirinto.rodape}")
    celulas = [labirinto.entrada]
    for numero, letra in enumerate(labirinto.caminho, start=1):
        if letra not in DESLOCAMENTOS:
            raise ValueError(
                f"a letra {numero} do caminho é {letra!r}, não N, E, S ou W"
            )
        x, y = celulas[-1]
        dx, dy = DESLOCAMENTOS[letra]
        proxima = (x + dx, y + dy)
        if not labirinto.dentro(proxima):
            raise ValueError(
                f"a letra {numero} do caminho leva a {proxima}, fora da grade"
            )
        celulas.append(proxima)
    return celulas


def desenho_do_caminho(celulas: list[Celula]) -> dict[Posicao, str]:
    """Caractere ciano esperado em cada posição do caminho (I02).

    Cada centro tem o caractere dos braços que levam à célula anterior e à
    seguinte; cada passagem, ``━`` ou ``┃``.

    Args:
        celulas: Células do caminho, da entrada à saída.

    Returns:
        O caractere de cada posição do caminho.
    """
    esperado: dict[Posicao, str] = {}
    for indice, celula in enumerate(celulas):
        vizinhas = celulas[max(indice - 1, 0):indice] + celulas[
            indice + 1:indice + 2
        ]
        soma = sum(
            DIRECOES[direcao_entre(celula, vizinha)] for vizinha in vizinhas
        )
        esperado[da_celula(celula)] = GLIFOS[soma]
    for primeira, segunda in zip(celulas, celulas[1:]):
        glifo = HORIZONTAL if primeira[1] == segunda[1] else VERTICAL
        for posicao in entre(primeira, segunda):
            esperado[posicao] = glifo
    return esperado


def paredes_do_arquivo(labirinto: Labirinto) -> set[Posicao]:
    """Posições das paredes fechadas e dos cantos de onde sai alguma.

    Args:
        labirinto: Labirinto lido do arquivo de saída.

    Returns:
        As posições do elemento "paredes".
    """
    fechadas = {
        posicao
        for celula in labirinto.celulas()
        for direcao in DIRECOES
        if not labirinto.aberta(celula, direcao)
        for posicao in da_passagem(celula, direcao)
    }
    return fechadas | {
        canto for canto in cantos(labirinto.largura, labirinto.altura)
        if bracos(fechadas, canto)
    }


def posicoes_do_42(labirinto: Labirinto) -> set[Posicao]:
    """Interior das células F e paredes entre duas delas.

    Args:
        labirinto: Labirinto lido do arquivo de saída.

    Returns:
        As posições do elemento "42".
    """
    padrao = {
        celula for celula in labirinto.celulas()
        if labirinto.valor(celula) == FECHADA
    }
    posicoes: set[Posicao] = set()
    for x, y in padrao:
        posicoes |= interior((x, y))
        if (x + 1, y) in padrao:
            posicoes |= da_passagem((x, y), "E")
        if (x, y + 1) in padrao:
            posicoes |= da_passagem((x, y), "S")
    return posicoes


def posicoes_de(labirinto: Labirinto, nome: str) -> set[Posicao]:
    """Posições de um elemento do desenho, segundo o arquivo de saída.

    Args:
        labirinto: Labirinto lido do arquivo de saída.
        nome: Um dos ELEMENTOS.

    Returns:
        As posições do elemento.

    Raises:
        ValueError: Quando o nome não está em ELEMENTOS ou o rodapé não
            tem o que o elemento precisa.
    """
    if nome not in ELEMENTOS:
        raise ValueError(
            f'"{nome}" não existe; os válidos são: {", ".join(ELEMENTOS)}'
        )
    if nome == "paredes":
        return paredes_do_arquivo(labirinto)
    if nome == "42":
        return posicoes_do_42(labirinto)
    if labirinto.entrada is None or labirinto.saida is None:
        raise ValueError(
            f"o rodapé não tem a entrada e a saída: {labirinto.rodape}"
        )
    if nome == "entrada":
        return interior(labirinto.entrada)
    if nome == "saída":
        return interior(labirinto.saida)
    celulas = caminho_do_arquivo(labirinto)
    if nome == "passagens do caminho":
        return {
            posicao
            for primeira, segunda in zip(celulas, celulas[1:])
            for posicao in entre(primeira, segunda)
        }
    pontas = {labirinto.entrada, labirinto.saida}
    return {da_celula(celula) for celula in celulas if celula not in pontas}


def _passagem_ciano(posicao: Posicao) -> tuple[Celula, Celula, str]:
    """Células ligadas por uma posição ciano fora dos centros e dos cantos.

    Args:
        posicao: (linha, coluna) de uma passagem do caminho.

    Returns:
        (primeira, segunda, caractere esperado) da passagem.

    Raises:
        ValueError: Quando a posição não pode ser de uma passagem.
    """
    linha, coluna = posicao
    resto = coluna % COLUNAS_POR_CELULA
    if linha % 2:
        x, y = (coluna - 3) // COLUNAS_POR_CELULA, (linha - 1) // 2
        return (x, y), (x + 1, y), HORIZONTAL
    if resto == 0:
        raise ValueError(f"o canto da {onde(posicao)} é ciano")
    if resto != 2:
        raise ValueError(
            f"a {onde(posicao)}, numa parede horizontal fora do meio, é ciano"
        )
    x, y = (coluna - 2) // COLUNAS_POR_CELULA, (linha - 2) // 2
    return (x, y), (x, y + 1), VERTICAL


def caminho_marcado(
    desenho: Tela, entrada: Celula, saida: Celula
) -> list[Celula]:
    """Lê o caminho ciano do desenho, da entrada até a saída.

    Os centros ciano formam uma corrente ligada pelas passagens ciano
    completas: a entrada e a saída com uma ligação, cada outra célula com
    duas, cada centro com o caractere dos braços das suas ligações, e
    nenhuma posição ciano fora dessa corrente.

    Args:
        desenho: Caracteres do bloco.
        entrada: Célula de entrada do rodapé.
        saida: Célula de saída do rodapé.

    Returns:
        As células do caminho, da entrada até a saída.

    Raises:
        ValueError: Quando o ciano não forma essa corrente.
    """
    centros: dict[Celula, str] = {}
    passagens: dict[tuple[Celula, Celula], list[Posicao]] = {}
    for posicao in sorted(posicoes_da_cor(desenho, CIANO)):
        linha, coluna = posicao
        simbolo = desenho[linha][coluna].simbolo
        if linha % 2 and coluna % COLUNAS_POR_CELULA == 2:
            x = (coluna - 2) // COLUNAS_POR_CELULA
            centros[(x, (linha - 1) // 2)] = simbolo
            continue
        primeira, segunda, glifo = _passagem_ciano(posicao)
        if simbolo != glifo:
            raise ValueError(
                f"a passagem ciano da {onde(posicao)} é {simbolo!r}, não "
                f"{glifo!r}"
            )
        passagens.setdefault((primeira, segunda), []).append(posicao)
    for nome, ponta in (("entrada", entrada), ("saída", saida)):
        if ponta not in centros:
            raise ValueError(f"o centro da {nome} {ponta} não é ciano")
    ligacoes: dict[Celula, list[Celula]] = {}
    for (primeira, segunda), posicoes in sorted(passagens.items()):
        esperadas = len(entre(primeira, segunda))
        if len(posicoes) != esperadas:
            raise ValueError(
                f"a passagem ciano entre {primeira} e {segunda} tem "
                f"{len(posicoes)} dos {esperadas} caracteres"
            )
        fora = [ponta for ponta in (primeira, segunda) if ponta not in centros]
        if fora:
            raise ValueError(
                f"a passagem ciano da {onde(posicoes[0])} liga a célula "
                f"{fora[0]}, que não tem o centro ciano"
            )
        ligacoes.setdefault(primeira, []).append(segunda)
        ligacoes.setdefault(segunda, []).append(primeira)
    for celula, simbolo in sorted(centros.items()):
        vizinhas = ligacoes.get(celula, [])
        esperadas = 1 if celula in (entrada, saida) else 2
        if len(vizinhas) != esperadas:
            raise ValueError(
                f"a célula {celula} do caminho marcado tem {len(vizinhas)} "
                f"passagens ciano, esperadas {esperadas}"
            )
        glifo = GLIFOS[sum(
            DIRECOES[direcao_entre(celula, vizinha)] for vizinha in vizinhas
        )]
        if simbolo != glifo:
            raise ValueError(
                f"o centro da célula {celula} é {simbolo!r}; as passagens "
                f"ciano dela pedem {glifo!r}"
            )
    caminho = [entrada]
    anterior: Celula | None = None
    while caminho[-1] != saida:
        atual = caminho[-1]
        proxima = [
            vizinha for vizinha in ligacoes[atual] if vizinha != anterior
        ][0]
        anterior = atual
        caminho.append(proxima)
    if len(caminho) != len(centros):
        soltas = sorted(set(centros) - set(caminho))
        raise ValueError(
            f"células ciano fora da corrente entre a entrada e a saída: "
            f"{soltas}"
        )
    return caminho


def distancia(labirinto: Labirinto, origem: Celula, destino: Celula) -> int:
    """Número de passos da busca em largura entre duas células.

    Args:
        labirinto: Labirinto lido do arquivo de saída.
        origem: Célula de partida.
        destino: Célula de chegada.

    Returns:
        A distância pelas paredes abertas.

    Raises:
        ValueError: Quando o destino não é alcançável.
    """
    distancias = {origem: 0}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        if atual == destino:
            return distancias[atual]
        for vizinha in labirinto.vizinhas(atual):
            if vizinha not in distancias:
                distancias[vizinha] = distancias[atual] + 1
                fila.append(vizinha)
    raise ValueError(f"{destino} não é alcançável a partir de {origem}")


def conferir_rodizio(cores: list[Cor], acoes: list[str]) -> None:
    """Confere a cor das paredes de cada renderização contra as ações (I04).

    A primeira renderização é grafite; cada ação que desenha (``1``, ``2``
    ou ``3``) produz uma renderização, e só a ``3`` passa para a próxima
    cor de grafite → laranja → verde → azul → grafite.

    Args:
        cores: Cor das paredes de cada renderização, na ordem.
        acoes: Linhas enviadas ao menu, na ordem.

    Raises:
        ValueError: Quando o número de renderizações não bate com as
            ações, nenhuma ação troca a cor ou uma cor sai do rodízio.
    """
    desenham = [acao for acao in acoes if acao in ACOES_QUE_DESENHAM]
    if TROCA_DE_COR not in desenham:
        raise ValueError(
            f"nenhuma opção {TROCA_DE_COR} foi enviada ao menu: {acoes}"
        )
    if len(cores) != len(desenham) + 1:
        raise ValueError(
            f"{len(cores)} renderizações para {len(desenham)} ações que "
            f"desenham ({desenham}); esperadas {len(desenham) + 1}"
        )
    esperada = 0
    for numero, cor in enumerate(cores):
        if numero and desenham[numero - 1] == TROCA_DE_COR:
            esperada = (esperada + 1) % len(RODIZIO)
        if cor != RODIZIO[esperada]:
            momento = (
                f"depois de {desenham[numero - 1]!r}" if numero
                else "a primeira"
            )
            raise ValueError(
                f"a renderização {numero} ({momento}) tem paredes "
                f"{nome_da_cor(cor)}, esperado "
                f"{nome_da_cor(RODIZIO[esperada])}"
            )


def direcoes(texto: str) -> set[str]:
    """Converte "Norte, Leste e Sul" (ou "nenhuma") em direções.

    Args:
        texto: Paredes como escritas no passo.

    Returns:
        As letras N, E, S e W citadas.

    Raises:
        ValueError: Quando um nome não é uma das direções.
    """
    if texto == NENHUMA:
        return set()
    nomes = re.split(r", | e ", texto)
    desconhecidos = [nome for nome in nomes if nome not in NOMES_DAS_DIRECOES]
    if desconhecidos:
        raise ValueError(
            f'"{desconhecidos[0]}" não existe; os válidos são: {NENHUMA} ou '
            f'{", ".join(NOMES_DAS_DIRECOES)} em lista com vírgulas e "e"'
        )
    return {NOMES_DAS_DIRECOES[nome] for nome in nomes}


def nomes_das_direcoes(letras: set[str]) -> str:
    """Escreve direções na ordem Norte, Leste, Sul, Oeste.

    Args:
        letras: Letras N, E, S e W.

    Returns:
        Os nomes separados por vírgula, ou "nenhuma".
    """
    nomes = [
        nome for nome, letra in NOMES_DAS_DIRECOES.items() if letra in letras
    ]
    return ", ".join(nomes) if nomes else NENHUMA
