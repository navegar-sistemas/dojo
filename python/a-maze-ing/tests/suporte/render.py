"""Leitura da renderização do labirinto no terminal (I02, I03, I04, I21).

A saída padrão é dividida em blocos de 2 × HEIGHT + 1 linhas desenhadas
(as que têm ESC). Cada linha vira uma lista de posições de 2 caracteres, e
cada posição guarda o código SGR do fundo; o fundo padrão (``49`` ou o
reset) é ``None``, "sem cor". Na grade de (2H + 1) × (2W + 1) posições, a
célula (x, y) fica em (2y + 1, 2x + 1); a passagem entre duas células fica
entre elas; as posições (par, par) são cantos, sempre parede.
"""

import re
from collections import deque
from dataclasses import dataclass

from suporte.labirinto import (
    DESLOCAMENTOS,
    DIRECOES,
    FECHADA,
    Celula,
    Labirinto,
)
from suporte.sessao import PROMPT

CORES = {
    "branco": 47,
    "amarelo": 43,
    "verde": 42,
    "azul": 44,
    "magenta": 45,
    "vermelho": 41,
    "ciano": 46,
    "cinza": 100,
}
NOMES_DAS_CORES = {codigo: nome for nome, codigo in CORES.items()}
CIANO = CORES["ciano"]
RODIZIO = (CORES["branco"], CORES["amarelo"], CORES["verde"], CORES["azul"])
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
FUNDOS = frozenset((*range(40, 48), *range(100, 108)))
FUNDO_PADRAO = 49
SGR_PERMITIDOS = frozenset((0, FUNDO_PADRAO, *FUNDOS))
SEQUENCIA = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
ELEMENTOS = (
    "entrada",
    "saída",
    "células do caminho",
    "passagens do caminho",
    "células do 42",
    "paredes",
)
NOMES_DAS_DIRECOES = {"Norte": "N", "Leste": "E", "Sul": "S", "Oeste": "W"}
NENHUMA = "nenhuma"

Cor = int | None
Posicao = tuple[int, int]
Tela = list[list[Cor]]


@dataclass
class Renderizacao:
    """Bloco de linhas desenhadas e as linhas impressas até o próximo."""

    linhas: list[str]
    seguinte: list[str]


def nome_da_cor(cor: Cor) -> str:
    """Nome da cor para as mensagens.

    Args:
        cor: Código SGR do fundo, ou None.

    Returns:
        O nome da I21, "sem cor" ou "SGR n".
    """
    if cor is None:
        return "sem cor"
    return NOMES_DAS_CORES.get(cor, f"SGR {cor}")


def onde(posicao: Posicao) -> str:
    """Descreve a posição do desenho para as mensagens.

    Args:
        posicao: (linha, coluna) do desenho, a partir de 0.

    Returns:
        O texto "linha l, coluna c".
    """
    linha, coluna = posicao
    return f"linha {linha}, coluna {coluna}"


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


def _fundo(parametros: str, atual: Cor) -> Cor:
    """Aplica os parâmetros de uma sequência SGR ao fundo atual.

    Args:
        parametros: Texto entre "ESC[" e "m".
        atual: Fundo antes da sequência.

    Returns:
        O fundo depois dela; o reset e o 49 voltam ao padrão.
    """
    for parametro in parametros.split(";"):
        codigo = int(parametro) if parametro.isdigit() else 0
        if codigo in (0, FUNDO_PADRAO):
            atual = None
        elif codigo in FUNDOS:
            atual = codigo
    return atual


def visiveis(linha: str) -> list[tuple[str, Cor]]:
    """Caracteres impressos da linha, cada um com o fundo em vigor.

    As sequências CSI não ocupam lugar; um ESC solto conta como caractere.

    Args:
        linha: Linha desenhada.

    Returns:
        Pares (caractere, fundo).
    """
    impressos: list[tuple[str, Cor]] = []
    fundo: Cor = None
    posicao = 0
    for casado in SEQUENCIA.finditer(linha):
        impressos.extend(
            (caractere, fundo) for caractere in linha[posicao:casado.start()]
        )
        sequencia = casado.group()
        if sequencia.endswith("m"):
            fundo = _fundo(sequencia[2:-1], fundo)
        posicao = casado.end()
    impressos.extend((caractere, fundo) for caractere in linha[posicao:])
    return impressos


def problemas_de_sgr(linha: str) -> list[str]:
    """Sequências da linha que não são fundo SGR nem reset, e ESC soltos.

    Args:
        linha: Linha desenhada.

    Returns:
        A descrição de cada problema, vazia quando a linha só usa fundos.
    """
    problemas: list[str] = []
    for casado in SEQUENCIA.finditer(linha):
        sequencia = casado.group()
        if not sequencia.endswith("m"):
            problemas.append(f"sequência que não é SGR: {sequencia!r}")
            continue
        for parametro in sequencia[2:-1].split(";"):
            codigo = int(parametro) if parametro.isdigit() else None
            if parametro and codigo not in SGR_PERMITIDOS:
                problemas.append(
                    f"parâmetro {parametro!r} não é fundo nem reset em "
                    f"{sequencia!r}"
                )
    if ESCAPE in SEQUENCIA.sub("", linha):
        problemas.append("ESC fora de uma sequência CSI")
    return problemas


def tela(renderizacao: Renderizacao) -> Tela:
    """Fundo de cada posição de 2 caracteres do bloco.

    Args:
        renderizacao: Bloco desenhado.

    Returns:
        Uma lista de fundos por linha do bloco.

    Raises:
        ValueError: Quando uma linha tem número ímpar de caracteres, uma
            posição tem dois fundos ou as linhas têm tamanhos diferentes.
    """
    desenho: Tela = []
    for numero, linha in enumerate(renderizacao.linhas):
        impressos = visiveis(linha)
        if len(impressos) % 2:
            raise ValueError(
                f"a linha {numero} do desenho tem {len(impressos)} "
                f"caracteres visíveis, número ímpar: {linha!r}"
            )
        posicoes: list[Cor] = []
        for coluna in range(0, len(impressos), 2):
            primeiro = impressos[coluna][1]
            segundo = impressos[coluna + 1][1]
            if primeiro != segundo:
                raise ValueError(
                    f"a posição da {onde((numero, coluna // 2))} tem dois "
                    f"fundos: {nome_da_cor(primeiro)} e "
                    f"{nome_da_cor(segundo)}"
                )
            posicoes.append(primeiro)
        desenho.append(posicoes)
    tamanhos = sorted({len(linha) for linha in desenho})
    if len(tamanhos) > 1:
        raise ValueError(
            f"as linhas do desenho têm números diferentes de posições: "
            f"{tamanhos}"
        )
    return desenho


def dimensoes(desenho: Tela) -> tuple[int, int]:
    """Largura e altura em células da grade desenhada.

    Args:
        desenho: Fundos das posições.

    Returns:
        (largura, altura).

    Raises:
        ValueError: Quando a grade não tem 2n + 1 linhas e colunas.
    """
    linhas = len(desenho)
    colunas = len(desenho[0]) if desenho else 0
    if linhas < 3 or colunas < 3 or not linhas % 2 or not colunas % 2:
        raise ValueError(
            f"o desenho tem {linhas} linhas e {colunas} posições por linha; "
            f"uma grade precisa de 2n + 1 de cada, com n >= 1"
        )
    return (colunas - 1) // 2, (linhas - 1) // 2


def da_celula(celula: Celula) -> Posicao:
    """Posição do desenho onde fica a célula.

    Args:
        celula: Coordenada (x, y).

    Returns:
        (2y + 1, 2x + 1).
    """
    x, y = celula
    return 2 * y + 1, 2 * x + 1


def da_passagem(celula: Celula, direcao: str) -> Posicao:
    """Posição do desenho da parede da célula na direção.

    Args:
        celula: Coordenada (x, y).
        direcao: "N", "E", "S" ou "W".

    Returns:
        A posição vizinha à da célula, nessa direção.
    """
    linha, coluna = da_celula(celula)
    dx, dy = DESLOCAMENTOS[direcao]
    return linha + dy, coluna + dx


def entre(primeira: Celula, segunda: Celula) -> Posicao:
    """Posição da passagem entre duas células vizinhas.

    Args:
        primeira: Coordenada (x, y).
        segunda: Coordenada vizinha.

    Returns:
        A posição no meio das duas.
    """
    (x1, y1), (x2, y2) = primeira, segunda
    return y1 + y2 + 1, x1 + x2 + 1


def cantos(largura: int, altura: int) -> set[Posicao]:
    """Posições (par, par) da grade: os cantos entre as células.

    Args:
        largura: WIDTH em células.
        altura: HEIGHT em células.

    Returns:
        As posições dos cantos.
    """
    return {
        (linha, coluna)
        for linha in range(0, 2 * altura + 1, 2)
        for coluna in range(0, 2 * largura + 1, 2)
    }


def cor_das_paredes(desenho: Tela) -> Cor:
    """Cor das paredes, lida no canto superior esquerdo.

    Args:
        desenho: Fundos das posições.

    Returns:
        O fundo da posição (0, 0).
    """
    return desenho[0][0]


def paredes_desenhadas(desenho: Tela, celula: Celula) -> set[str]:
    """Direções em que a célula aparece com parede.

    Args:
        desenho: Fundos das posições.
        celula: Coordenada (x, y).

    Returns:
        As direções cuja posição tem a cor das paredes.
    """
    parede = cor_das_paredes(desenho)
    fechadas: set[str] = set()
    for direcao in DIRECOES:
        linha, coluna = da_passagem(celula, direcao)
        if desenho[linha][coluna] == parede:
            fechadas.add(direcao)
    return fechadas


def grade_desenhada(desenho: Tela) -> list[list[int]]:
    """Bits de parede de cada célula, como o desenho mostra.

    Args:
        desenho: Fundos das posições.

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


def posicoes_da_cor(desenho: Tela, cor: Cor) -> set[Posicao]:
    """Posições do desenho com o fundo dado.

    Args:
        desenho: Fundos das posições.
        cor: Código SGR, ou None para "sem cor".

    Returns:
        As posições com esse fundo.
    """
    return {
        (linha, coluna)
        for linha, fundos in enumerate(desenho)
        for coluna, fundo in enumerate(fundos)
        if fundo == cor
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


def posicoes_de(labirinto: Labirinto, nome: str) -> set[Posicao]:
    """Posições de um elemento do desenho, segundo o arquivo de saída.

    Entrada e saída têm prioridade sobre o caminho (I02); as células do 42
    são as de valor F; as paredes são os cantos e toda parede fechada.

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
        return cantos(labirinto.largura, labirinto.altura) | {
            da_passagem(celula, direcao)
            for celula in labirinto.celulas()
            for direcao in DIRECOES
            if not labirinto.aberta(celula, direcao)
        }
    if nome == "células do 42":
        return {
            da_celula(celula) for celula in labirinto.celulas()
            if labirinto.valor(celula) == FECHADA
        }
    if labirinto.entrada is None or labirinto.saida is None:
        raise ValueError(
            f"o rodapé não tem a entrada e a saída: {labirinto.rodape}"
        )
    if nome == "entrada":
        return {da_celula(labirinto.entrada)}
    if nome == "saída":
        return {da_celula(labirinto.saida)}
    celulas = caminho_do_arquivo(labirinto)
    if nome == "passagens do caminho":
        return {
            entre(primeira, segunda)
            for primeira, segunda in zip(celulas, celulas[1:])
        }
    pontas = {labirinto.entrada, labirinto.saida}
    return {da_celula(celula) for celula in celulas if celula not in pontas}


def caminho_marcado(
    desenho: Tela, entrada: Celula, saida: Celula
) -> list[Celula]:
    """Lê o caminho ciano do desenho, da entrada até a saída.

    As células ciano, a entrada e a saída formam uma corrente ligada pelas
    passagens ciano: a entrada e a saída com uma ligação, cada célula ciano
    com duas, e nenhuma posição ciano fora dessa corrente.

    Args:
        desenho: Fundos das posições.
        entrada: Célula de entrada do rodapé.
        saida: Célula de saída do rodapé.

    Returns:
        As células do caminho, da entrada até a saída.

    Raises:
        ValueError: Quando o ciano não forma essa corrente.
    """
    largura, altura = dimensoes(desenho)
    marcadas = {entrada, saida}
    ligacoes: dict[Celula, list[Celula]] = {}
    for linha, coluna in sorted(posicoes_da_cor(desenho, CIANO)):
        if linha % 2 and coluna % 2:
            marcadas.add(((coluna - 1) // 2, (linha - 1) // 2))
        elif not linha % 2 and not coluna % 2:
            raise ValueError(f"o canto da {onde((linha, coluna))} é ciano")
    for linha, coluna in sorted(posicoes_da_cor(desenho, CIANO)):
        if linha % 2 == coluna % 2:
            continue
        if linha % 2:
            pontas = [((coluna - 2) // 2, (linha - 1) // 2),
                      (coluna // 2, (linha - 1) // 2)]
        else:
            pontas = [((coluna - 1) // 2, (linha - 2) // 2),
                      ((coluna - 1) // 2, linha // 2)]
        fora = [
            ponta for ponta in pontas
            if not (0 <= ponta[0] < largura and 0 <= ponta[1] < altura)
            or ponta not in marcadas
        ]
        if fora:
            raise ValueError(
                f"a passagem ciano da {onde((linha, coluna))} liga a célula "
                f"{fora[0]}, que não é do caminho marcado"
            )
        primeira, segunda = pontas
        ligacoes.setdefault(primeira, []).append(segunda)
        ligacoes.setdefault(segunda, []).append(primeira)
    for celula in sorted(marcadas):
        esperadas = 1 if celula in (entrada, saida) else 2
        achadas = len(ligacoes.get(celula, []))
        if achadas != esperadas:
            raise ValueError(
                f"a célula {celula} do caminho marcado tem {achadas} "
                f"passagens ciano, esperadas {esperadas}"
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
    if len(caminho) != len(marcadas):
        soltas = sorted(marcadas - set(caminho))
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

    A primeira renderização é branca; cada ação que desenha (``1``, ``2``
    ou ``3``) produz uma renderização, e só a ``3`` passa para a próxima
    cor de branco → amarelo → verde → azul → branco.

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
