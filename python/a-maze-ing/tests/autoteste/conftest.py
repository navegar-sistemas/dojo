"""Fixtures dos testes da própria suíte."""

from pathlib import Path

import pytest

from suporte.estado import Estado


@pytest.fixture
def cenario(estado: Estado, tmp_path: Path) -> Estado:
    """Estado de cenário que roda numa pasta temporária, fora de project/.

    Args:
        estado: Estado novo, com a pasta de reserva.
        tmp_path: Pasta temporária do teste.

    Returns:
        O estado com ``cwd`` na pasta temporária.
    """
    estado.cwd = tmp_path
    return estado
