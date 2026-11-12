"""Propriedades da V72 sobre a renderização do labirinto no terminal."""

import pytest

from conftest import Estado, propriedade

ANSI = "\x1b["
RESET = "\x1b[0m"


@propriedade("a renderização", "cada linha termina com o reset ANSI")
def linhas_com_reset(estado: Estado) -> None:
    """Toda linha colorida da saída padrão termina com o reset ANSI (I02).

    Sem nenhuma linha colorida não houve renderização, e o teste falha.

    Args:
        estado: Estado do cenário.
    """
    coloridas = [
        linha for linha in estado.resultado.saida_padrao.splitlines()
        if ANSI in linha
    ]
    if not coloridas:
        pytest.fail("a saída padrão não tem nenhuma linha renderizada")
    sem_reset = [
        numero for numero, linha in enumerate(coloridas, start=1)
        if not linha.endswith(RESET)
    ]
    if sem_reset:
        pytest.fail(
            f"{len(sem_reset)} de {len(coloridas)} linhas renderizadas sem "
            f"o reset no fim (primeira: {coloridas[sem_reset[0] - 1]!r})"
        )
