"""Renderizações e arquivos de saída montados à mão para os autotestes.

O labirinto de exemplo tem 3x2 células: a entrada (0,0) e a saída (2,0)
ligadas pela célula (1,0), caminho "EE"; a célula (0,1) é fechada (o "42");
(1,1) e (2,1) são corredor ligado a (1,0). O desenho dele está escrito
caractere a caractere em PAREDES e CAMINHO, sem passar pelo código que a
suíte confere.
"""

from suporte.render import MENU, RESET, Caractere, Cor, Posicao, Rgb, Tela
from suporte.sessao import PROMPT

BRANCO: Rgb = (255, 255, 255)
GRAFITE: Rgb = (31, 41, 55)
LARANJA: Rgb = (194, 65, 12)
VERDE: Rgb = (21, 128, 61)
AZUL: Rgb = (29, 78, 216)
MAGENTA: Rgb = (217, 70, 239)
VERMELHO: Rgb = (239, 68, 68)
CIANO: Rgb = (34, 211, 238)
CINZA: Rgb = (156, 163, 175)
ARQUIVO = "d17\nfc7\n\n0,0\n2,0\nEE\n"
CONFIG = ["WIDTH=3", "HEIGHT=2"]
TEXTO_DO_MENU = "\n".join(MENU) + "\n" + PROMPT
PAREDES = (
    "┏━━━━━━━━━━━┓",
    "┃           ┃",
    "┣━━━┓   ╺━━━┫",
    "┃   ┃       ┃",
    "┗━━━┻━━━━━━━┛",
)
CAMINHO: dict[Posicao, str] = {
    (1, coluna): simbolo
    for coluna, simbolo in enumerate("╺━━━━━━━╸", start=2)
}
FUNDOS: dict[Posicao, Rgb] = {
    **{(1, coluna): MAGENTA for coluna in (1, 2, 3)},
    **{(1, coluna): VERMELHO for coluna in (9, 10, 11)},
    **{(3, coluna): CINZA for coluna in (1, 2, 3)},
}
# Labirinto 2x2 todo aberto: a BFS vai direto de (0,0) a (1,0), e o ciano
# de volta() dá a volta por baixo, com 3 passos.
ANEL = "93\nc6\n\n0,0\n1,0\nE\n"
PAREDES_DO_ANEL = (
    "┏━━━━━━━┓",
    "┃       ┃",
    "┃       ┃",
    "┃       ┃",
    "┗━━━━━━━┛",
)
VOLTA: dict[Posicao, str] = {
    (1, 2): "╻", (2, 2): "┃", (3, 2): "┗", (3, 3): "━", (3, 4): "━",
    (3, 5): "━", (3, 6): "┛", (2, 6): "┃", (1, 6): "╻",
}


def montar(
    linhas: tuple[str, ...], parede: Rgb, fundos: dict[Posicao, Rgb]
) -> Tela:
    """Caracteres de um desenho, com o texto na cor das paredes.

    Args:
        linhas: Texto de cada linha.
        parede: Cor do texto de todos os caracteres.
        fundos: Fundo de cada posição que não é branca.

    Returns:
        A grade de caracteres.
    """
    return [
        [
            Caractere(simbolo, parede, fundos.get((linha, coluna), BRANCO))
            for coluna, simbolo in enumerate(texto)
        ]
        for linha, texto in enumerate(linhas)
    ]


def com_caminho(desenho: Tela, simbolos: dict[Posicao, str]) -> Tela:
    """Cópia do desenho com caracteres ciano nas posições dadas.

    Args:
        desenho: Grade original.
        simbolos: Caractere de cada posição do caminho.

    Returns:
        A grade nova, com o fundo de cada posição mantido.
    """
    copia = [list(linha) for linha in desenho]
    for (linha, coluna), simbolo in simbolos.items():
        copia[linha][coluna] = copia[linha][coluna]._replace(
            simbolo=simbolo, texto=CIANO
        )
    return copia


def grade(parede: Rgb = GRAFITE, caminho: bool = True) -> Tela:
    """Caracteres do labirinto de exemplo.

    Args:
        parede: Cor das paredes.
        caminho: Se o caminho aparece em ciano.

    Returns:
        As 5 linhas de 13 caracteres.
    """
    desenho = montar(PAREDES, parede, FUNDOS)
    return com_caminho(desenho, CAMINHO) if caminho else desenho


def volta() -> Tela:
    """O labirinto ANEL com o ciano dando a volta por baixo.

    Returns:
        As 5 linhas de 9 caracteres.
    """
    fundos = {
        **{(1, coluna): MAGENTA for coluna in (1, 2, 3)},
        **{(1, coluna): VERMELHO for coluna in (5, 6, 7)},
    }
    return com_caminho(montar(PAREDES_DO_ANEL, GRAFITE, fundos), VOLTA)


def com_simbolo(
    desenho: Tela, posicoes: list[Posicao], simbolo: str
) -> Tela:
    """Cópia do desenho com outro caractere nas posições, mesmas cores.

    Args:
        desenho: Grade original.
        posicoes: (linha, coluna) a trocar.
        simbolo: Caractere novo.

    Returns:
        A grade nova.
    """
    copia = [list(linha) for linha in desenho]
    for linha, coluna in posicoes:
        copia[linha][coluna] = copia[linha][coluna]._replace(simbolo=simbolo)
    return copia


def com_texto(desenho: Tela, linha: int, coluna: int, cor: Cor) -> Tela:
    """Cópia do desenho com outra cor de texto numa posição.

    Args:
        desenho: Grade original.
        linha: Linha da posição.
        coluna: Coluna da posição.
        cor: Cor nova do texto.

    Returns:
        A grade nova.
    """
    copia = [list(caracteres) for caracteres in desenho]
    copia[linha][coluna] = copia[linha][coluna]._replace(texto=cor)
    return copia


def com_fundo(desenho: Tela, linha: int, coluna: int, cor: Cor) -> Tela:
    """Cópia do desenho com outro fundo numa posição.

    Args:
        desenho: Grade original.
        linha: Linha da posição.
        coluna: Coluna da posição.
        cor: Cor nova do fundo.

    Returns:
        A grade nova.
    """
    copia = [list(caracteres) for caracteres in desenho]
    copia[linha][coluna] = copia[linha][coluna]._replace(fundo=cor)
    return copia


def sgr(texto: Cor, fundo: Cor) -> str:
    """Sequência que põe as duas cores, como a I02 escreve.

    Uma cor ausente vira um reset antes da outra.

    Args:
        texto: Cor do texto, ou None.
        fundo: Cor do fundo, ou None.

    Returns:
        A sequência SGR.
    """
    partes = ["0"] if texto is None or fundo is None else []
    if texto is not None:
        partes.append("38;2;{};{};{}".format(*texto))
    if fundo is not None:
        partes.append("48;2;{};{};{}".format(*fundo))
    return "\x1b[" + ";".join(partes) + "m"


def desenhar(desenho: Tela) -> str:
    """Escreve as linhas com uma sequência a cada troca do par de cores.

    Args:
        desenho: Caracteres e cores.

    Returns:
        As linhas, cada uma terminada no reset, sem quebra no fim.
    """
    linhas: list[str] = []
    for caracteres in desenho:
        partes: list[str] = []
        atual: tuple[Cor, Cor] | None = None
        for caractere in caracteres:
            par = (caractere.texto, caractere.fundo)
            if par != atual:
                partes.append(sgr(*par))
                atual = par
            partes.append(caractere.simbolo)
        linhas.append("".join(partes) + RESET)
    return "\n".join(linhas)


def tela_com_menu(desenho: Tela) -> str:
    """Uma exibição do programa: linha vazia, desenho, menu e prompt.

    Args:
        desenho: Caracteres e cores.

    Returns:
        O texto, terminado no prompt.
    """
    return f"\n{desenhar(desenho)}\n{TEXTO_DO_MENU}"


def saida(*telas: Tela) -> str:
    """Saída padrão de uma sessão com uma exibição por desenho.

    Args:
        *telas: Desenhos, na ordem em que são exibidos.

    Returns:
        As exibições concatenadas.
    """
    return "".join(tela_com_menu(desenho) for desenho in telas)
