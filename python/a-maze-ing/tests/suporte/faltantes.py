"""Frases dos .feature sem função em step_defs/, com os exemplos aplicados.

O ``--generate-missing`` do pytest-bdd confere a frase de um Esquema do
Cenário com o ``<coluna>`` ainda no texto: um ``<n>`` não casa com
``{n:d}``, e a frase sai como faltante mesmo tendo função. Aqui cada
Esquema é conferido com cada linha de Exemplos já aplicada, como o
pytest-bdd faz ao rodar o cenário.
"""

import importlib
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from pytest_bdd.feature import get_features
from pytest_bdd.parser import ScenarioTemplate
from pytest_bdd.steps import (
    StepFunctionContext,
    step_function_context_registry,
)

TESTS_DIR = Path(__file__).resolve().parent.parent
FEATURES = TESTS_DIR / "features"
CENARIOS = TESTS_DIR / "cenarios"


@dataclass(frozen=True)
class Faltante:
    """Frase de um passo sem função que case com ela."""

    tipo: str
    frase: str
    local: str


def carregar_passos() -> list[StepFunctionContext]:
    """Importa os módulos de passos do conftest.py e devolve os registrados.

    Returns:
        O contexto de cada passo: tipo e parser da frase.
    """
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    conftest = importlib.import_module("conftest")
    for modulo in getattr(conftest, "pytest_plugins"):
        importlib.import_module(modulo)
    return list(step_function_context_registry.values())


def contextos(cenario: ScenarioTemplate) -> list[dict[str, str]]:
    """Linhas de Exemplos do cenário; um contexto vazio se não houver.

    Args:
        cenario: Cenário ou Esquema do Cenário lido do .feature.

    Returns:
        Um dicionário coluna → valor por linha de Exemplos.
    """
    linhas = [
        contexto
        for exemplos in cenario.examples
        for contexto in exemplos.as_contexts()
    ]
    return linhas or [{}]


def faltantes(
    arquivos: Iterable[Path], passos: list[StepFunctionContext]
) -> list[Faltante]:
    """Passos dos cenários que nenhuma função casa, sem repetição.

    Args:
        arquivos: Arquivos .feature.
        passos: Passos registrados, de ``carregar_passos``.

    Returns:
        Cada frase sem função, no primeiro lugar em que aparece.
    """
    achados: dict[tuple[str, str], Faltante] = {}
    caminhos = [str(arquivo) for arquivo in sorted(arquivos)]
    for feature in get_features(caminhos):
        for cenario in feature.scenarios.values():
            for contexto in contextos(cenario):
                for passo in cenario.render(contexto).steps:
                    if any(
                        contexto_do_passo.type in (None, passo.type)
                        and contexto_do_passo.parser.is_matching(passo.name)
                        for contexto_do_passo in passos
                    ):
                        continue
                    chave = (passo.type, passo.name)
                    achados.setdefault(chave, Faltante(
                        passo.type,
                        passo.name,
                        f"{Path(feature.filename).name}:{passo.line_number}",
                    ))
    return list(achados.values())


def soltos(arquivos: Iterable[Path]) -> list[str]:
    """Arquivos .feature sem o cenarios/test_NN_nome.py correspondente.

    Args:
        arquivos: Arquivos .feature, com nome NN-nome.feature.

    Returns:
        Os nomes dos .feature sem arquivo de teste.
    """
    return [
        arquivo.name for arquivo in sorted(arquivos)
        if not (
            CENARIOS / f"test_{arquivo.stem.replace('-', '_')}.py"
        ).is_file()
    ]


def main() -> int:
    """Lista as frases sem função e os .feature sem arquivo de teste.

    Returns:
        0 quando não falta nada; 1 quando falta.
    """
    arquivos = list(FEATURES.glob("*.feature"))
    sem_funcao = faltantes(arquivos, carregar_passos())
    sem_teste = soltos(arquivos)
    for faltante in sem_funcao:
        print(
            f"{faltante.local}: {faltante.tipo} sem função: "
            f"{faltante.frase}"
        )
    for nome in sem_teste:
        print(f"{nome}: sem cenarios/test_*.py")
    if sem_funcao or sem_teste:
        return 1
    print("nenhuma frase sem função; todo .feature tem arquivo de teste")
    return 0


if __name__ == "__main__":
    sys.exit(main())
