"""Passos da análise estática do código-fonte (ast)."""

import ast
import re
import sys
import tokenize
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from suporte.estado import Estado
from suporte.tipos import TIPOS

FORA_DA_ANALISE = {".venv", "build", "dist", "__pycache__"}
FRAMEWORKS_DE_TESTE = {"pytest", "pytest_bdd", "unittest"}
COLECOES = {"list", "dict", "set"}
SECOES_GOOGLE = {
    "Args:", "Returns:", "Yields:", "Raises:", "Example:", "Examples:",
    "Note:", "Notes:", "Attributes:", "Todo:",
}
SEM_RETORNO = {"None", "NoReturn", "Never"}
DEFINICOES = ("módulo", "função", "método", "classe")
SUPRESSAO = re.compile(
    r"(?i)#\s*noqa\b|#\s*flake8[:=]\s*noqa|#\s*type:\s*ignore|#\s*mypy:"
)
PACOTE_DO_MODULO = "mazegen"

Definicao = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
Documentavel = Definicao | ast.Module


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
    """Lista os .py dos alvos.

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
    """Faz o ast.parse de cada fonte.

    A leitura com utf-8-sig aceita o BOM, que o Python também aceita.

    Args:
        estado: Estado do cenário.
    """
    for fonte in estado.fontes:
        estado.arvores[fonte] = ast.parse(
            fonte.read_text(encoding="utf-8-sig"), filename=str(fonte)
        )


def importacoes(arvore: ast.Module) -> list[tuple[str, int]]:
    """Módulos importados de forma absoluta em qualquer ponto do módulo.

    Args:
        arvore: Módulo já analisado.

    Returns:
        Nome completo e linha de cada import; imports relativos
        ("from . import x") ficam de fora.
    """
    achados: list[tuple[str, int]] = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            achados += [(apelido.name, no.lineno) for apelido in no.names]
        elif isinstance(no, ast.ImportFrom) and no.module and not no.level:
            achados.append((no.module, no.lineno))
    return achados


def modulos_importados(arvore: ast.Module) -> set[str]:
    """Pacotes de primeiro nível importados em qualquer ponto do módulo.

    Args:
        arvore: Módulo já analisado.

    Returns:
        Os nomes de primeiro nível ("pytest_bdd" para
        "from pytest_bdd.parsers import parse").
    """
    return {nome.split(".")[0] for nome, _ in importacoes(arvore)}


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


@then('a análise estática confirma "testes usam pytest ou unittest"')
def todo_teste_usa_framework(estado: Estado) -> None:
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


def local(estado: Estado, arquivo: Path) -> str:
    """Caminho do arquivo relativo à raiz do repositório, quando possível.

    Args:
        estado: Estado do cenário.
        arquivo: Arquivo analisado.

    Returns:
        O caminho para as mensagens de falha.
    """
    try:
        return str(arquivo.resolve().relative_to(estado.cwd.resolve()))
    except ValueError:
        return str(arquivo)


def falhar_se(estado: Estado, violacoes: list[tuple[Path, int, str]],
              regra: str) -> None:
    """Falha o teste listando as violações da regra.

    Args:
        estado: Estado do cenário.
        violacoes: Arquivo, linha e descrição de cada violação.
        regra: Regra violada, para a mensagem.
    """
    if violacoes:
        lista = "\n".join(
            f"  {local(estado, arquivo)}:{linha} {descricao}"
            for arquivo, linha, descricao in violacoes
        )
        pytest.fail(f"{regra}:\n{lista}")


def definicoes(estado: Estado) -> list[tuple[Path, Definicao, str]]:
    """Funções, métodos e classes de todas as árvores analisadas.

    Args:
        estado: Estado do cenário, com as árvores da análise.

    Returns:
        Arquivo, nó e tipo ("função", "método" ou "classe"); método é a
        definição feita direto no corpo de uma classe.
    """
    achadas: list[tuple[Path, Definicao, str]] = []

    def visitar(no: ast.AST, em_classe: bool, arquivo: Path) -> None:
        """Guarda as definições abaixo do nó, na ordem do arquivo.

        Args:
            no: Nó cujos filhos são percorridos.
            em_classe: Se o nó é o corpo de uma classe.
            arquivo: Arquivo a que o nó pertence.
        """
        for filho in ast.iter_child_nodes(no):
            if isinstance(filho, ast.ClassDef):
                achadas.append((arquivo, filho, "classe"))
                visitar(filho, True, arquivo)
            elif isinstance(filho, (ast.FunctionDef, ast.AsyncFunctionDef)):
                tipo = "método" if em_classe else "função"
                achadas.append((arquivo, filho, tipo))
                visitar(filho, False, arquivo)
            else:
                visitar(filho, em_classe, arquivo)

    for arquivo, arvore in estado.arvores.items():
        visitar(arvore, False, arquivo)
    return achadas


def funcoes(
    estado: Estado,
) -> list[tuple[Path, ast.FunctionDef | ast.AsyncFunctionDef, str]]:
    """Só as funções e os métodos de definicoes().

    Args:
        estado: Estado do cenário, com as árvores da análise.

    Returns:
        Arquivo, nó e tipo de cada função ou método.
    """
    return [
        (arquivo, no, tipo) for arquivo, no, tipo in definicoes(estado)
        if not isinstance(no, ast.ClassDef)
    ]


def documentaveis(estado: Estado) -> list[tuple[Path, Documentavel]]:
    """Módulos, classes, funções e métodos que têm docstring.

    Args:
        estado: Estado do cenário, com as árvores da análise.

    Returns:
        Arquivo e nó de cada docstring existente.
    """
    nos: list[tuple[Path, Documentavel]] = [
        (arquivo, arvore) for arquivo, arvore in estado.arvores.items()
    ]
    nos += [(arquivo, no) for arquivo, no, _ in definicoes(estado)]
    return [
        (arquivo, no) for arquivo, no in nos if ast.get_docstring(no)
    ]


def nome_de(no: Documentavel) -> str:
    """Nome do nó para as mensagens ("módulo" para o arquivo).

    Args:
        no: Nó com docstring.

    Returns:
        O nome.
    """
    return "módulo" if isinstance(no, ast.Module) else no.name


def linha_de(no: Documentavel) -> int:
    """Linha do nó para as mensagens (1 para o módulo).

    Args:
        no: Nó com docstring.

    Returns:
        O número da linha.
    """
    return 1 if isinstance(no, ast.Module) else no.lineno


@then('a análise estática confirma "open sempre dentro de with"')
def open_dentro_de_with(estado: Estado) -> None:
    """Toda chamada open() ou x.open() é a expressão de um with.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, arvore in estado.arvores.items():
        em_with = {
            id(item.context_expr)
            for no in ast.walk(arvore)
            if isinstance(no, (ast.With, ast.AsyncWith))
            for item in no.items
        }
        for no in ast.walk(arvore):
            if not isinstance(no, ast.Call) or id(no) in em_with:
                continue
            funcao = no.func
            if (isinstance(funcao, ast.Name) and funcao.id == "open") or (
                isinstance(funcao, ast.Attribute) and funcao.attr == "open"
            ):
                violacoes.append((arquivo, no.lineno, "open fora de with"))
    falhar_se(estado, violacoes, "open fora de with")


@then(
    'a análise estática confirma "anotação de retorno em toda definição"'
)
def retorno_anotado(estado: Estado) -> None:
    """Todo def tem anotação de retorno.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, f"{no.name} sem ->")
            for arquivo, no, _ in funcoes(estado)
            if no.returns is None
        ],
        "definições sem anotação de retorno",
    )


@then(
    parsers.parse(
        'a análise estática confirma "docstring em cada {definicao:Q}"',
        extra_types=TIPOS,
    )
)
def docstring_em_cada(estado: Estado, definicao: str) -> None:
    """Toda definição do tipo pedido tem docstring.

    Args:
        estado: Estado do cenário, com as árvores da análise.
        definicao: "módulo", "função", "método" ou "classe".
    """
    if definicao not in DEFINICOES:
        pytest.fail(
            f'definição "{definicao}" não existe; as válidas são: '
            f"{', '.join(DEFINICOES)}"
        )
    if definicao == "módulo":
        falhar_se(
            estado,
            [
                (arquivo, 1, "sem docstring")
                for arquivo, arvore in estado.arvores.items()
                if not ast.get_docstring(arvore)
            ],
            "módulo sem docstring",
        )
        return
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, f"{no.name} sem docstring")
            for arquivo, no, achado in definicoes(estado)
            if achado == definicao and not ast.get_docstring(no)
        ],
        f"{definicao} sem docstring",
    )


@then('a análise estática confirma "docstrings com aspas triplas duplas"')
def aspas_triplas_duplas(estado: Estado) -> None:
    """Toda docstring é escrita com três aspas duplas.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no in documentaveis(estado):
        fonte = arquivo.read_text(encoding="utf-8-sig")
        expressao = no.body[0]
        assert isinstance(expressao, ast.Expr)
        trecho = ast.get_source_segment(fonte, expressao.value) or ""
        if not re.match(r'[rR]?"""', trecho):
            violacoes.append(
                (arquivo, linha_de(no), f"{nome_de(no)}: {trecho[:10]!r}")
            )
    falhar_se(estado, violacoes, "docstrings sem aspas triplas duplas")


@then('a análise estática confirma "resumo de uma frase terminado em ponto"')
def resumo_com_ponto(estado: Estado) -> None:
    """O primeiro parágrafo da docstring é uma linha terminada em ponto.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no in documentaveis(estado):
        linhas = (ast.get_docstring(no) or "").splitlines()
        paragrafo: list[str] = []
        for linha in linhas:
            if not linha.strip():
                break
            paragrafo.append(linha)
        if len(paragrafo) != 1 or not paragrafo[0].rstrip().endswith("."):
            violacoes.append(
                (arquivo, linha_de(no), f"{nome_de(no)}: {paragrafo!r}")
            )
    falhar_se(estado, violacoes, "resumo que não é uma frase com ponto")


@then(
    'a análise estática confirma '
    + '"linha em branco entre resumo e descrição"'
)
def linha_em_branco(estado: Estado) -> None:
    """Docstring de várias linhas tem a segunda linha vazia.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no in documentaveis(estado):
        linhas = (ast.get_docstring(no) or "").splitlines()
        if len(linhas) > 1 and linhas[1].strip():
            violacoes.append((arquivo, linha_de(no), nome_de(no)))
    falhar_se(estado, violacoes, "sem linha em branco depois do resumo")


def secao(docstring: str, titulo: str) -> str | None:
    """Texto de uma seção estilo Google, até a próxima seção.

    Args:
        docstring: Docstring já limpa por ast.get_docstring.
        titulo: Título da seção, com os dois-pontos.

    Returns:
        O corpo da seção, ou None se ela não existe.
    """
    linhas = docstring.splitlines()
    for indice, linha in enumerate(linhas):
        if linha.strip() == titulo:
            corpo: list[str] = []
            for seguinte in linhas[indice + 1:]:
                if seguinte.strip() in SECOES_GOOGLE:
                    break
                corpo.append(seguinte)
            return "\n".join(corpo)
    return None


def parametros(no: ast.FunctionDef | ast.AsyncFunctionDef,
               metodo: bool) -> list[str]:
    """Nomes dos parâmetros como aparecem na seção Args.

    Args:
        no: Função ou método.
        metodo: Se é método, o primeiro parâmetro self ou cls fica de fora.

    Returns:
        Os nomes, com "*" e "**" em *args e **kwargs.
    """
    argumentos = no.args
    nomes = [
        argumento.arg for argumento in (
            *argumentos.posonlyargs, *argumentos.args, *argumentos.kwonlyargs
        )
    ]
    if metodo and nomes and nomes[0] in ("self", "cls"):
        nomes = nomes[1:]
    if argumentos.vararg:
        nomes.append(f"*{argumentos.vararg.arg}")
    if argumentos.kwarg:
        nomes.append(f"**{argumentos.kwarg.arg}")
    return nomes


@then(
    'a análise estática confirma "seção Args: nas funções com parâmetros"'
)
def secao_args(estado: Estado) -> None:
    """Função com parâmetros tem Args: citando cada um.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no, tipo in funcoes(estado):
        nomes = parametros(no, tipo == "método")
        if not nomes:
            continue
        corpo = secao(ast.get_docstring(no) or "", "Args:")
        if corpo is None:
            violacoes.append((arquivo, no.lineno, f"{no.name} sem Args:"))
            continue
        faltando = [
            nome for nome in nomes
            if not re.search(
                rf"^\s*{re.escape(nome)}\s*(\([^)]*\))?:", corpo, re.M
            )
        ]
        if faltando:
            violacoes.append(
                (arquivo, no.lineno, f"{no.name}: Args: sem {faltando}")
            )
    falhar_se(estado, violacoes, "seção Args: incompleta")


def retorna_valor(no: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Diz se a anotação de retorno indica um valor.

    Args:
        no: Função ou método.

    Returns:
        False sem anotação ou com None, NoReturn ou Never.
    """
    retorno = no.returns
    if retorno is None:
        return False
    if isinstance(retorno, ast.Constant) and retorno.value is None:
        return False
    if isinstance(retorno, ast.Name) and retorno.id in SEM_RETORNO:
        return False
    return not (
        isinstance(retorno, ast.Attribute) and retorno.attr in SEM_RETORNO
    )


@then(
    'a análise estática confirma '
    + '"seção Returns: nas funções que retornam valor"'
)
def secao_returns(estado: Estado) -> None:
    """Função com retorno anotado diferente de None tem Returns: ou Yields:.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, f"{no.name} sem Returns:")
            for arquivo, no, _ in funcoes(estado)
            if retorna_valor(no)
            and secao(ast.get_docstring(no) or "", "Returns:") is None
            and secao(ast.get_docstring(no) or "", "Yields:") is None
        ],
        "funções que retornam valor sem Returns:",
    )


def colecao_vazia(valor: ast.expr) -> bool:
    """Diz se a expressão é [], {} ou list(), dict(), set() sem argumentos.

    Args:
        valor: Lado direito de uma atribuição.

    Returns:
        True para coleção mutável vazia, cujo tipo o mypy não infere.
    """
    if isinstance(valor, ast.List | ast.Set) and not valor.elts:
        return True
    if isinstance(valor, ast.Dict) and not valor.keys:
        return True
    return (
        isinstance(valor, ast.Call)
        and isinstance(valor.func, ast.Name)
        and valor.func.id in COLECOES
        and not valor.args
        and not valor.keywords
    )


def atribui_colecao_vazia(alvo: ast.expr, valor: ast.expr) -> bool:
    """Diz se a atribuição põe uma coleção vazia em algum nome.

    Args:
        alvo: Lado esquerdo; tupla ou lista é desempacotada.
        valor: Lado direito.

    Returns:
        True para ``x = []`` e para ``a, b = [], []``, em qualquer
        profundidade do desempacotamento.
    """
    if (
        isinstance(alvo, ast.Tuple | ast.List)
        and isinstance(valor, ast.Tuple | ast.List)
        and len(alvo.elts) == len(valor.elts)
    ):
        return any(
            atribui_colecao_vazia(parte, item)
            for parte, item in zip(alvo.elts, valor.elts)
        )
    return colecao_vazia(valor)


@then('a análise estática confirma "coleções vazias com tipo anotado"')
def colecoes_anotadas(estado: Estado) -> None:
    """Coleção vazia só é atribuída com anotação (x: list[int] = []).

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, ast.unparse(no))
            for arquivo, arvore in estado.arvores.items()
            for no in ast.walk(arvore)
            if isinstance(no, ast.Assign)
            and any(
                atribui_colecao_vazia(alvo, no.value) for alvo in no.targets
            )
        ],
        "coleções vazias sem anotação de tipo",
    )


@then('a análise estática confirma "sem supressão de flake8 nem mypy"')
def sem_supressao(estado: Estado) -> None:
    """Nenhum comentário desliga o flake8 ou o mypy.

    Lê os comentários pelo tokenize, de modo que o texto dentro de uma
    string não conta; casa ``# noqa``, ``# flake8: noqa``, ``# type:
    ignore`` e ``# mypy:`` em qualquer caixa e espaçamento.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo in estado.arvores:
        with arquivo.open("rb") as fonte:
            violacoes += [
                (arquivo, token.start[0], token.string)
                for token in tokenize.tokenize(fonte.readline)
                if token.type == tokenize.COMMENT
                and SUPRESSAO.search(token.string)
            ]
    falhar_se(estado, violacoes, "comentários que desligam o flake8 ou o mypy")


@then('a análise estática confirma "mazegen só importa a biblioteca padrão"')
def so_biblioteca_padrao(estado: Estado) -> None:
    """Todo import absoluto é da biblioteca padrão ou do próprio mazegen.

    Args:
        estado: Estado do cenário, com as árvores da análise.
    """
    falhar_se(
        estado,
        [
            (arquivo, linha, f"importa {nome}")
            for arquivo, arvore in estado.arvores.items()
            for nome, linha in importacoes(arvore)
            if nome.split(".")[0] != PACOTE_DO_MODULO
            and nome.split(".")[0] not in sys.stdlib_module_names
        ],
        "imports de fora da biblioteca padrão",
    )
