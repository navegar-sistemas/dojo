"""Ligação da suíte com o pytest: passos, tags, python3 e estado."""

from collections.abc import Callable, Iterator

import pytest

from suporte.ambiente import problema_do_python3
from suporte.estado import Estado

pytest_plugins = [
    "step_defs.execucao",
    "step_defs.repositorio",
    "step_defs.analise_estatica",
    "step_defs.renderizacao",
]

REFERENCIAS = ("pdf-", "md-", "regua-", "decisao-")


def pytest_bdd_apply_tag(tag: str, function: Callable[..., object]) -> object:
    """Converte as tags dos .feature em marcadores do pytest.

    Args:
        tag: Tag do cenário, sem o "@".
        function: Função de teste gerada pelo pytest-bdd.

    Returns:
        True quando a tag foi tratada aqui; None para o pytest-bdd criar o
        marcador registrado no pyproject.toml.
    """
    if tag == "manual":
        pytest.mark.manual(function)
        pytest.mark.skip(reason="verificação manual")(function)
        return True
    if tag == "decisao-I19":
        pytest.mark.adiado(function)
        pytest.mark.skip(reason="fora da primeira versão (I19)")(function)
        return True
    if tag.startswith(REFERENCIAS):
        return True
    return None


@pytest.fixture(scope="session", autouse=True)
def python3_do_path() -> None:
    """Encerra a rodada quando o python3 do PATH não serve aos cenários."""
    problema = problema_do_python3()
    if problema is not None:
        pytest.exit(problema, returncode=pytest.ExitCode.USAGE_ERROR)


@pytest.fixture
def estado(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Estado]:
    """Estado novo para cada cenário; desfaz os caminhos preparados no fim.

    Args:
        tmp_path_factory: Fábrica de pastas temporárias do pytest.

    Yields:
        O estado, com uma pasta de reserva própria.
    """
    novo = Estado(reserva=tmp_path_factory.mktemp("reserva"))
    yield novo
    novo.restaurar()
