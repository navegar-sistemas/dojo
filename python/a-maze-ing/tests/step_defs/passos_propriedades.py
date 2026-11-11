"""Passo V72, que confere as propriedades registradas com @propriedade."""

import pytest
from pytest_bdd import parsers, then

from conftest import PROPRIEDADES, TIPOS, Estado


@then(
    parsers.parse(
        '{sujeito:Sujeito} confirma "{nome:Q}"', extra_types=TIPOS
    )
)
def sujeito_confirma(estado: Estado, sujeito: str, nome: str) -> None:
    """V72: roda a verificação registrada para o sujeito e a propriedade.

    Args:
        estado: Estado do cenário.
        sujeito: Valor do tipo Sujeito.
        nome: Propriedade da lista fechada do sujeito.
    """
    verificacao = PROPRIEDADES.get((sujeito, nome))
    if verificacao is None:
        pytest.fail(
            f'propriedade "{nome}" de "{sujeito}" ainda não implementada '
            "(V72 no README)"
        )
    verificacao(estado)
