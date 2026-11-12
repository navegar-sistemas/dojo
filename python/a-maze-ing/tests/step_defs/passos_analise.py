"""Passos da análise estática do código-fonte (ast)."""

import ast
import re
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from conftest import TIPOS, Estado, propriedade

FORA_DA_ANALISE = {".venv", "build", "dist", "__pycache__"}
FRAMEWORKS_DE_TESTE = {"pytest", "pytest_bdd", "unittest"}
COLECOES = {"list", "dict", "set"}
SECOES_GOOGLE = {
    "Args:", "Returns:", "Yields:", "Raises:", "Example:", "Examples:",
    "Note:", "Notes:", "Attributes:", "Todo:",
}
SEM_RETORNO = {"None", "NoReturn", "Never"}

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


@then(
    parsers.parse(
        'nenhum arquivo .py do projeto contém "{texto:Q}"', extra_types=TIPOS
    )
)
def nenhum_py_contem(estado: Estado, texto: str) -> None:
    """V63: procura o texto nos .py do repositório.

    Args:
        estado: Estado do cenário.
        texto: Texto proibido.
    """
    achados = [
        f"{local(estado, arquivo)}:{numero}"
        for arquivo in arquivos_python(estado.cwd)
        for numero, linha in enumerate(
            arquivo.read_text(encoding="utf-8", errors="replace")
            .splitlines(),
            start=1,
        )
        if texto in linha
    ]
    if achados:
        pytest.fail(f"{texto!r} aparece em: {', '.join(achados)}")


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


@propriedade("a análise estática", "open sempre dentro de with")
def open_dentro_de_with(estado: Estado) -> None:
    """Toda chamada open() ou x.open() é a expressão de um with."""
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


@propriedade("a análise estática", "anotação de retorno em toda definição")
def retorno_anotado(estado: Estado) -> None:
    """Todo def tem anotação de retorno."""
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, f"{no.name} sem ->")
            for arquivo, no, _ in funcoes(estado)
            if no.returns is None
        ],
        "definições sem anotação de retorno",
    )


def _docstring_em(tipo: str) -> None:
    """Registra a propriedade "docstring em cada <tipo>".

    Args:
        tipo: "função", "método" ou "classe".
    """

    @propriedade("a análise estática", f"docstring em cada {tipo}")
    def verificar(estado: Estado) -> None:
        falhar_se(
            estado,
            [
                (arquivo, no.lineno, f"{no.name} sem docstring")
                for arquivo, no, achado in definicoes(estado)
                if achado == tipo and not ast.get_docstring(no)
            ],
            f"{tipo} sem docstring",
        )


for _tipo in ("função", "método", "classe"):
    _docstring_em(_tipo)


@propriedade("a análise estática", "docstrings com aspas triplas duplas")
def aspas_triplas_duplas(estado: Estado) -> None:
    """Toda docstring é escrita com três aspas duplas."""
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no in documentaveis(estado):
        fonte = arquivo.read_text(encoding="utf-8")
        expressao = no.body[0]
        assert isinstance(expressao, ast.Expr)
        trecho = ast.get_source_segment(fonte, expressao.value) or ""
        if not re.match(r'[rR]?"""', trecho):
            violacoes.append(
                (arquivo, linha_de(no), f"{nome_de(no)}: {trecho[:10]!r}")
            )
    falhar_se(estado, violacoes, "docstrings sem aspas triplas duplas")


@propriedade("a análise estática", "resumo de uma frase terminado em ponto")
def resumo_com_ponto(estado: Estado) -> None:
    """O primeiro parágrafo da docstring é uma linha terminada em ponto."""
    violacoes: list[tuple[Path, int, str]] = []
    for arquivo, no in documentaveis(estado):
        linhas = (ast.get_docstring(no) or "").splitlines()
        paragrafo = []
        for linha in linhas:
            if not linha.strip():
                break
            paragrafo.append(linha)
        if len(paragrafo) != 1 or not paragrafo[0].rstrip().endswith("."):
            violacoes.append(
                (arquivo, linha_de(no), f"{nome_de(no)}: {paragrafo!r}")
            )
    falhar_se(estado, violacoes, "resumo que não é uma frase com ponto")


@propriedade("a análise estática", "linha em branco entre resumo e descrição")
def linha_em_branco(estado: Estado) -> None:
    """Docstring de várias linhas tem a segunda linha vazia."""
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
            corpo = []
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


@propriedade("a análise estática", "seção Args: nas funções com parâmetros")
def secao_args(estado: Estado) -> None:
    """Função com parâmetros tem Args: citando cada um."""
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


@propriedade(
    "a análise estática", "seção Returns: nas funções que retornam valor"
)
def secao_returns(estado: Estado) -> None:
    """Função com retorno anotado diferente de None tem Returns: ou Yields:."""
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


@propriedade("a análise estática", "coleções vazias com tipo anotado")
def colecoes_anotadas(estado: Estado) -> None:
    """Coleção vazia só é atribuída com anotação (x: list[int] = [])."""
    falhar_se(
        estado,
        [
            (arquivo, no.lineno, ast.unparse(no))
            for arquivo, arvore in estado.arvores.items()
            for no in ast.walk(arvore)
            if isinstance(no, ast.Assign) and colecao_vazia(no.value)
        ],
        "coleções vazias sem anotação de tipo",
    )
