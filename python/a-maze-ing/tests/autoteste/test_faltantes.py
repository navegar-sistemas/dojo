"""Testes da lista de frases sem função (make faltantes)."""

from pathlib import Path
from typing import Literal

from pytest_bdd import parsers
from pytest_bdd.steps import StepFunctionContext

from suporte.faltantes import FEATURES, faltantes, soltos

FEATURE = """\
# language: pt
Funcionalidade: Exemplo

  Esquema do Cenário: Contagem
    Dado o config base
    Então a grade tem <n> colunas

    Exemplos:
      | n  |
      | 20 |
      | 25 |

  Cenário: Frase sem função
    Dado o config base
    Então nada casa com esta frase
"""


def passo(
    tipo: Literal["given", "when", "then"], frase: str
) -> StepFunctionContext:
    """Contexto de passo como o decorador do pytest-bdd registra.

    Args:
        tipo: "given", "when" ou "then".
        frase: Frase no formato de parsers.parse.

    Returns:
        O contexto do passo.
    """
    return StepFunctionContext(
        type=tipo, step_func=lambda: None, parser=parsers.parse(frase)
    )


def gravar(pasta: Path, nome: str) -> Path:
    """Grava o .feature de exemplo na pasta.

    Args:
        pasta: Pasta temporária.
        nome: Nome do arquivo.

    Returns:
        O caminho gravado.
    """
    arquivo = pasta / nome
    arquivo.write_text(FEATURE, encoding="utf-8")
    return arquivo


def test_esquema_com_inteiro_nao_e_falso_faltante(tmp_path: Path) -> None:
    """{n:d} casa com cada linha de Exemplos, não com o <n> do modelo.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = gravar(tmp_path, "01-exemplo.feature")
    achados = faltantes(
        [arquivo],
        [
            passo("given", "o config base"),
            passo("then", "a grade tem {n:d} colunas"),
        ],
    )
    assert [faltante.frase for faltante in achados] == [
        "nada casa com esta frase"
    ]
    assert achados[0].tipo == "then"
    assert achados[0].local == "01-exemplo.feature:15"


def test_tipo_do_passo_conta(tmp_path: Path) -> None:
    """Uma função given não serve a um passo Então com a mesma frase.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = gravar(tmp_path, "01-exemplo.feature")
    achados = faltantes(
        [arquivo],
        [
            passo("given", "o config base"),
            passo("given", "a grade tem {n:d} colunas"),
            passo("then", "nada casa com esta frase"),
        ],
    )
    assert {faltante.frase for faltante in achados} == {
        "a grade tem 20 colunas",
        "a grade tem 25 colunas",
    }


def test_passo_sem_tipo_serve_a_todos(tmp_path: Path) -> None:
    """O passo registrado sem tipo casa com Dado, Quando e Então.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = gravar(tmp_path, "01-exemplo.feature")
    achados = faltantes(
        [arquivo],
        [
            passo("given", "o config base"),
            passo("then", "a grade tem {n:d} colunas"),
            StepFunctionContext(
                type=None,
                step_func=lambda: None,
                parser=parsers.parse("nada casa com esta frase"),
            ),
        ],
    )
    assert achados == []


def test_feature_sem_arquivo_de_teste(tmp_path: Path) -> None:
    """Um .feature sem cenarios/test_NN_nome.py aparece como solto.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = gravar(tmp_path, "99-sem-teste.feature")
    assert soltos([arquivo]) == ["99-sem-teste.feature"]


def test_features_da_suite_tem_arquivo_de_teste() -> None:
    """Todo .feature da suíte tem o seu cenarios/test_NN_nome.py."""
    assert soltos(FEATURES.glob("*.feature")) == []
