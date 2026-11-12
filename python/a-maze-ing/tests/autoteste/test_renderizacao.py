"""Testes dos passos que conferem a renderização no terminal."""

import pytest

from step_defs.renderizacao import linhas_com_reset
from suporte.estado import Estado, Execucao

PAREDE = "\x1b[47m  \x1b[0m"


def com_saida(cenario: Estado, saida_padrao: str) -> Estado:
    """Põe no cenário uma execução com a saída padrão dada.

    Args:
        cenario: Estado numa pasta temporária.
        saida_padrao: Texto do stdout.

    Returns:
        O cenário.
    """
    cenario.resultados.append(Execucao("comando", 0, saida_padrao, ""))
    return cenario


def test_linhas_coloridas_terminam_com_reset(cenario: Estado) -> None:
    """Linhas sem cor, como o menu, não precisam do reset.

    Args:
        cenario: Estado numa pasta temporária.
    """
    saida = f"{PAREDE}{PAREDE}\n{PAREDE}\n1. Regenerate\nChoice? (1-4): "
    linhas_com_reset(com_saida(cenario, saida))


@pytest.mark.parametrize(
    "linha",
    ["\x1b[47m  ", f"{PAREDE} ", f"{PAREDE}\x1b[47m  "],
    ids=["sem reset", "espaço depois do reset", "cor aberta no fim"],
)
def test_linha_colorida_sem_reset_no_fim(cenario: Estado, linha: str) -> None:
    """Uma única linha colorida que não termina no reset derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        linha: Linha renderizada com defeito.
    """
    with pytest.raises(pytest.fail.Exception, match="1 de 2 linhas"):
        linhas_com_reset(com_saida(cenario, f"{PAREDE}\n{linha}\n"))


def test_saida_sem_renderizacao(cenario: Estado) -> None:
    """Sem nenhuma linha colorida não houve renderização.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhuma linha"):
        linhas_com_reset(com_saida(cenario, "teste\n"))
