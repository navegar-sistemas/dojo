"""A suíte cumpre as regras do subject que ela cobra do projeto."""

from collections.abc import Callable

import pytest

from step_defs.analise_estatica import (
    DEFINICOES,
    analise_percorre,
    aspas_triplas_duplas,
    codigo_fonte_de,
    colecoes_anotadas,
    docstring_em_cada,
    linha_em_branco,
    nenhum_py_contem,
    open_dentro_de_with,
    resumo_com_ponto,
    retorno_anotado,
    secao_args,
    secao_returns,
    todo_teste_usa_framework,
)
from suporte.estado import TESTS_DIR, Estado

REGRAS: list[Callable[[Estado], None]] = [
    open_dentro_de_with,
    retorno_anotado,
    aspas_triplas_duplas,
    resumo_com_ponto,
    linha_em_branco,
    secao_args,
    secao_returns,
    colecoes_anotadas,
    todo_teste_usa_framework,
]

# Montadas em pedaços: escritas por inteiro, este arquivo conteria os
# próprios textos que procura.
SUPRESSOES = ["# " + "noqa", "# type" + ": ignore"]


@pytest.mark.parametrize("regra", REGRAS, ids=lambda regra: regra.__name__)
def test_a_suite_cumpre_a_regra(
    estado: Estado, regra: Callable[[Estado], None]
) -> None:
    """Todo .py da suíte passa na propriedade da análise estática.

    Args:
        estado: Estado do cenário.
        regra: Passo que confere uma propriedade do Capítulo III.1.
    """
    estado.cwd = TESTS_DIR
    codigo_fonte_de(estado, ["."])
    analise_percorre(estado)
    regra(estado)


@pytest.mark.parametrize("definicao", DEFINICOES)
def test_a_suite_tem_docstring_em_cada(estado: Estado, definicao: str) -> None:
    """Toda função, todo método e toda classe da suíte têm docstring.

    Args:
        estado: Estado do cenário.
        definicao: "função", "método" ou "classe".
    """
    estado.cwd = TESTS_DIR
    codigo_fonte_de(estado, ["."])
    analise_percorre(estado)
    docstring_em_cada(estado, definicao)


@pytest.mark.parametrize("supressao", SUPRESSOES)
def test_a_suite_nao_suprime_o_lint(estado: Estado, supressao: str) -> None:
    """Nenhum .py da suíte desliga o flake8 ou o mypy numa linha.

    Args:
        estado: Estado do cenário.
        supressao: Comentário que desliga uma verificação.
    """
    estado.cwd = TESTS_DIR
    nenhum_py_contem(estado, supressao)
