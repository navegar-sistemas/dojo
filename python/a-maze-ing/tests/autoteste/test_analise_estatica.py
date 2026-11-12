"""Testes dos passos da análise estática, com trechos bons e ruins."""

from collections.abc import Callable

import pytest

from step_defs.analise_estatica import (
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
from suporte.estado import Estado

Passo = Callable[[Estado], None]

COMPLETA = '''
def somar(a: int, *resto: int, **opcoes: int) -> int:
    """Soma os números.

    Args:
        a: Primeiro número.
        *resto: Outros números.
        **opcoes (int): Números com nome.

    Returns:
        A soma.
    """
    return a + sum(resto) + sum(opcoes.values())
'''

CASOS: list[tuple[Passo, str, str]] = [
    (
        open_dentro_de_with,
        'with open("a") as arquivo:\n    pass\n',
        'arquivo = open("a")\n',
    ),
    (
        open_dentro_de_with,
        'with caminho.open(encoding="utf-8") as arquivo:\n    pass\n',
        "texto = caminho.open().read()\n",
    ),
    (
        retorno_anotado,
        "def f() -> None:\n    pass\n",
        "class C:\n    def f(self):\n        pass\n",
    ),
    (
        lambda estado: docstring_em_cada(estado, "função"),
        'def f() -> None:\n    """Faz."""\n',
        'def f() -> None:\n    def g() -> None:\n        """Faz."""\n',
    ),
    (
        lambda estado: docstring_em_cada(estado, "método"),
        'class C:\n    def f(self) -> None:\n        """Faz."""\n',
        'class C:\n    """Classe."""\n    def f(self) -> None:\n        ...\n',
    ),
    (
        lambda estado: docstring_em_cada(estado, "classe"),
        'class C:\n    """Classe."""\n',
        'class C:\n    def f(self) -> None:\n        """Faz."""\n',
    ),
    (
        aspas_triplas_duplas,
        'r"""Módulo."""\n\ndef f() -> None:\n    """Faz."""\n',
        "def f() -> None:\n    '''Faz.'''\n",
    ),
    (
        aspas_triplas_duplas,
        '"""Módulo."""\n',
        'def f() -> None:\n    "Faz."\n',
    ),
    (
        resumo_com_ponto,
        'def f() -> None:\n    """Faz.\n\n    Detalhe sem ponto\n    """\n',
        'def f() -> None:\n    """Faz"""\n',
    ),
    (
        resumo_com_ponto,
        '"""Módulo."""\n',
        'def f() -> None:\n    """Faz uma coisa\n    e outra.\n    """\n',
    ),
    (
        linha_em_branco,
        'def f() -> None:\n    """Faz.\n\n    Detalhe.\n    """\n',
        'def f() -> None:\n    """Faz.\n    Detalhe.\n    """\n',
    ),
    (
        secao_args,
        COMPLETA,
        'def f(a: int) -> None:\n    """Faz."""\n',
    ),
    (
        secao_args,
        'class C:\n    def f(self) -> None:\n        """Faz."""\n',
        'def f(a: int, b: int) -> None:\n'
        '    """Faz.\n\n    Args:\n        a: Um.\n    """\n',
    ),
    (
        secao_returns,
        COMPLETA,
        'def f() -> int:\n    """Faz."""\n    return 1\n',
    ),
    (
        secao_returns,
        'def f() -> None:\n    """Faz."""\n',
        'def f() -> list[int]:\n    """Faz.\n\n    Note:\n        X.\n    """',
    ),
    (
        secao_returns,
        'def f() -> Iterator[int]:\n'
        '    """Faz.\n\n    Yields:\n        Números.\n    """\n    yield 1\n',
        'def f() -> typing.Any:\n    """Faz."""\n',
    ),
    (
        colecoes_anotadas,
        "itens: list[int] = []\nmapa: dict[str, int] = dict()\ncheio = [1]\n",
        "itens = []\n",
    ),
    (
        colecoes_anotadas,
        "conjunto: set[int] = set()\ncopia = list(conjunto)\n",
        "mapa = dict()\n",
    ),
]

IDS = [
    "open-fora-de-with",
    "caminho-open-fora-de-with",
    "retorno",
    "docstring-funcao",
    "docstring-metodo",
    "docstring-classe",
    "aspas-simples-triplas",
    "aspas-duplas-simples",
    "resumo-sem-ponto",
    "resumo-em-duas-linhas",
    "linha-em-branco",
    "args-ausente",
    "args-incompleto",
    "returns-ausente",
    "returns-de-colecao",
    "returns-de-atributo",
    "lista-vazia",
    "dict-vazio",
]


def analisar(cenario: Estado, fonte: str, nome: str = "modulo.py") -> Estado:
    """Grava a fonte na pasta do cenário e roda a análise sobre ela.

    Args:
        cenario: Estado numa pasta temporária.
        fonte: Código Python.
        nome: Nome do arquivo gravado.

    Returns:
        O cenário, com as árvores da análise.
    """
    (cenario.cwd / nome).write_text(fonte, encoding="utf-8")
    codigo_fonte_de(cenario, ["."])
    analise_percorre(cenario)
    return cenario


@pytest.mark.parametrize(
    ("passo", "bom", "ruim"),
    CASOS,
    ids=IDS,
)
def test_propriedade_aceita_e_recusa(
    cenario: Estado, passo: Passo, bom: str, ruim: str
) -> None:
    """Cada propriedade passa no trecho bom e falha no trecho ruim.

    Args:
        cenario: Estado numa pasta temporária.
        passo: Função do passo que confere a propriedade.
        bom: Código que cumpre a regra.
        ruim: Código que quebra a regra.
    """
    passo(analisar(cenario, bom))
    with pytest.raises(pytest.fail.Exception, match="ruim.py"):
        passo(analisar(cenario, ruim, "ruim.py"))


def test_docstring_de_definicao_desconhecida(cenario: Estado) -> None:
    """Só função, método e classe são tipos de definição.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        docstring_em_cada(analisar(cenario, "x = 1\n"), "módulo")


def test_arquivos_de_teste_usam_framework(cenario: Estado) -> None:
    """Import de pytest ou unittest, ou função test_ no módulo, bastam.

    Args:
        cenario: Estado numa pasta temporária.
    """
    analisar(cenario, "import pytest\n", "test_a.py")
    analisar(cenario, "from unittest import TestCase\n", "b_test.py")
    analisar(cenario, "def test_c() -> None:\n    pass\n", "test_c.py")
    todo_teste_usa_framework(analisar(cenario, "print(1)\n", "prog.py"))


def test_arquivo_de_teste_sem_framework(cenario: Estado) -> None:
    """Arquivo test_ que só imprime não é teste de pytest nem de unittest.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(AssertionError, match="test_solto.py"):
        todo_teste_usa_framework(
            analisar(cenario, "print(1)\n", "test_solto.py")
        )


def test_codigo_sem_arquivo_de_teste(cenario: Estado) -> None:
    """Sem nenhum arquivo de teste a propriedade falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(AssertionError, match="nenhum arquivo"):
        todo_teste_usa_framework(analisar(cenario, "print(1)\n"))


def test_codigo_fonte_ignora_venv_e_build(cenario: Estado) -> None:
    """Só entram os .py do projeto; venv, build, dist e caches ficam fora.

    Args:
        cenario: Estado numa pasta temporária.
    """
    for pasta in (".venv/lib", "build", "dist", "pacote/__pycache__"):
        (cenario.cwd / pasta).mkdir(parents=True)
        (cenario.cwd / pasta / "fora.py").write_text("", encoding="utf-8")
    (cenario.cwd / "pacote" / "dentro.py").write_text("", encoding="utf-8")
    (cenario.cwd / "raiz.py").write_text("", encoding="utf-8")
    codigo_fonte_de(cenario, [".", "raiz.py"])
    assert [fonte.name for fonte in cenario.fontes] == [
        "dentro.py",
        "raiz.py",
        "raiz.py",
    ]


def test_codigo_fonte_inexistente_ou_vazio(cenario: Estado) -> None:
    """Alvo que não existe ou pasta sem .py derrubam o cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        codigo_fonte_de(cenario, ["mazegen"])
    with pytest.raises(pytest.fail.Exception, match="nenhum arquivo"):
        codigo_fonte_de(cenario, ["."])


def test_nenhum_py_contem(cenario: Estado) -> None:
    """O texto proibido é procurado linha a linha nos .py do repositório.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "limpo.py").write_text("x = 1\n", encoding="utf-8")
    nenhum_py_contem(cenario, "TODO")
    (cenario.cwd / "sujo.py").write_text("x = 1\n# TODO\n", encoding="utf-8")
    with pytest.raises(pytest.fail.Exception, match="sujo.py:2"):
        nenhum_py_contem(cenario, "TODO")
