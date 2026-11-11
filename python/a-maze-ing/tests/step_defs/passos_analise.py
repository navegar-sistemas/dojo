"""Passos da análise estática do código-fonte (ast)."""

import ast
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, when

from conftest import TIPOS, Estado, propriedade

FORA_DA_ANALISE = {".venv", "build", "dist", "__pycache__"}
FRAMEWORKS_DE_TESTE = {"pytest", "pytest_bdd", "unittest"}


def arquivos_python(alvo: Path) -> list[Path]:
    """Lista os .py de um arquivo ou pasta, sem venv nem artefatos de build.

    Args:
        alvo: Arquivo .py ou pasta.

    Returns:
        Os arquivos .py, em ordem.
    """
    if alvo.is_file():
        return [alvo]
    return sorted(
        arquivo for arquivo in alvo.rglob("*.py")
        if not FORA_DA_ANALISE.intersection(arquivo.relative_to(alvo).parts)
    )


@given(parsers.parse("o código-fonte de {alvos:L}", extra_types=TIPOS))
def codigo_fonte_de(estado: Estado, alvos: list[str]) -> None:
    """V06: lista os .py dos alvos.

    Args:
        estado: Estado do cenário.
        alvos: Caminhos relativos ao repositório; "." é o repositório todo.
    """
    for nome in alvos:
        alvo = (estado.cwd / nome).resolve()
        if not alvo.exists():
            pytest.fail(f'"{nome}" não existe em {estado.cwd}')
        estado.fontes.extend(arquivos_python(alvo))
    if not estado.fontes:
        pytest.fail(f"nenhum arquivo .py em {alvos}")


@when("a análise estática percorre o código-fonte")
def analise_percorre(estado: Estado) -> None:
    """V41: faz o ast.parse de cada fonte.

    Args:
        estado: Estado do cenário.
    """
    for fonte in estado.fontes:
        estado.arvores[fonte] = ast.parse(
            fonte.read_text(encoding="utf-8"), filename=str(fonte)
        )


def modulos_importados(arvore: ast.Module) -> set[str]:
    """Pacotes de primeiro nível importados em qualquer ponto do módulo.

    Args:
        arvore: Módulo já analisado.

    Returns:
        Os nomes de primeiro nível ("pytest_bdd" para
        "from pytest_bdd.parsers import parse").
    """
    nomes: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes.update(apelido.name.split(".")[0] for apelido in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module and not no.level:
            nomes.add(no.module.split(".")[0])
    return nomes


def eh_arquivo_de_teste(caminho: Path) -> bool:
    """Diz se o nome segue a convenção de coleta do pytest e do unittest.

    Args:
        caminho: Arquivo .py.

    Returns:
        True para test_*.py e *_test.py.
    """
    return caminho.name.startswith("test_") or caminho.stem.endswith("_test")


def usa_framework_de_teste(arvore: ast.Module) -> bool:
    """Diz se o módulo de teste usa pytest ou unittest.

    Args:
        arvore: Módulo de teste já analisado.

    Returns:
        True se importa pytest, pytest_bdd ou unittest, ou se define
        funções test_* no nível do módulo, que o pytest coleta sem import.
    """
    if FRAMEWORKS_DE_TESTE & modulos_importados(arvore):
        return True
    return any(
        isinstance(no, ast.FunctionDef) and no.name.startswith("test_")
        for no in arvore.body
    )


@propriedade("a análise estática", "testes usam pytest ou unittest")
def testes_usam_framework(estado: Estado) -> None:
    """Há arquivos de teste, e todos usam pytest ou unittest.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    testes = [
        caminho for caminho in estado.arvores if eh_arquivo_de_teste(caminho)
    ]
    assert testes, "nenhum arquivo test_*.py ou *_test.py no código-fonte"
    sem_framework = [
        caminho for caminho in testes
        if not usa_framework_de_teste(estado.arvores[caminho])
    ]
    assert not sem_framework, f"testes sem pytest ou unittest: {sem_framework}"
