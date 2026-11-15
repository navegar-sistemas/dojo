"""Renderizações e arquivos de saída montados à mão para os autotestes.

O labirinto de exemplo tem 3x2 células: a entrada (0,0) e a saída (2,0)
ligadas pela célula (1,0), caminho "EE"; a célula (0,1) é fechada (o "42");
(1,1) e (2,1) são corredor ligado a (1,0).
"""

from suporte.render import MENU, RESET, Cor
from suporte.sessao import PROMPT

BRANCO, AMARELO, VERDE, AZUL = 47, 43, 42, 44
MAGENTA, VERMELHO, CIANO, CINZA = 45, 41, 46, 100
ARQUIVO = "d17\nfc7\n\n0,0\n2,0\nEE\n"
CONFIG = ["WIDTH=3", "HEIGHT=2"]
TEXTO_DO_MENU = "\n".join(MENU) + "\n" + PROMPT


def grade(parede: int = BRANCO, caminho: bool = True) -> list[list[Cor]]:
    """Fundos das posições do labirinto de exemplo.

    Args:
        parede: Código da cor das paredes.
        caminho: Se o caminho aparece em ciano.

    Returns:
        As 5 linhas de 7 posições.
    """
    marca = CIANO if caminho else None
    return [
        [parede] * 7,
        [parede, MAGENTA, marca, marca, marca, VERMELHO, parede],
        [parede, parede, parede, None, parede, parede, parede],
        [parede, CINZA, parede, None, None, None, parede],
        [parede] * 7,
    ]


def desenhar(fundos: list[list[Cor]]) -> str:
    """Escreve as linhas com uma sequência de fundo antes de cada posição.

    Args:
        fundos: Código de cada posição; None vira o fundo padrão 49.

    Returns:
        As linhas, cada uma terminada no reset, sem quebra no fim.
    """
    return "\n".join(
        "".join(
            f"\x1b[{49 if fundo is None else fundo}m  " for fundo in linha
        )
        + RESET
        for linha in fundos
    )


def tela_com_menu(fundos: list[list[Cor]]) -> str:
    """Uma exibição do programa: linha vazia, desenho, menu e prompt.

    Args:
        fundos: Código de cada posição.

    Returns:
        O texto, terminado no prompt.
    """
    return f"\n{desenhar(fundos)}\n{TEXTO_DO_MENU}"


def saida(*telas: list[list[Cor]]) -> str:
    """Saída padrão de uma sessão com uma exibição por grade de fundos.

    Args:
        *telas: Grades de fundos, na ordem em que são exibidas.

    Returns:
        As exibições concatenadas.
    """
    return "".join(tela_com_menu(fundos) for fundos in telas)
