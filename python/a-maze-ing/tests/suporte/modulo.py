"""Acesso da suíte à classe MazeGenerator do módulo mazegen."""

import ast
import importlib
import textwrap
from collections.abc import Callable
from typing import Any

from suporte.labirinto import Labirinto, coordenada

# O mazegen vem de ../project pelo pythonpath do pytest; o import dinâmico
# evita que o mypy da suíte exija o pacote, que não fica em tests/.
MODULO = "mazegen"
CLASSE = "MazeGenerator"
# Assinatura da I09, na ordem dos parâmetros posicionais.
PARAMETROS = ("width", "height", "entry", "exit", "perfect", "seed")
ENTRADA_PADRAO = (0, 0)
SECAO_DO_EXEMPLO = "Example:"

# Argumentos que o construtor recusa (D05, I09): valores impossíveis e tipos
# errados. Cada caso parte de um tamanho válido e troca o que diz.
_TAMANHO = {"width": 20, "height": 15}
INVALIDOS: tuple[dict[str, object], ...] = (
    {"width": -5, "height": 15},
    {"width": 20, "height": -1},
    {"width": 0, "height": 0},
    {"width": 101, "height": 15},
    {"width": 20, "height": 1000000},
    {**_TAMANHO, "entry": (20, 0)},
    {**_TAMANHO, "exit": (19, 15)},
    {**_TAMANHO, "entry": (-1, 0)},
    {**_TAMANHO, "entry": (5, 5), "exit": (5, 5)},
    {**_TAMANHO, "entry": (6, 5)},
    {"width": 2, "height": 2, "perfect": False},
    {"width": "20", "height": 15},
    {"width": 20, "height": "15"},
    {"width": 2.5, "height": 15},
    {"width": True, "height": 15},
    {"width": 20, "height": None},
    {**_TAMANHO, "entry": (0,)},
    {**_TAMANHO, "entry": (0, 0, 0)},
    {**_TAMANHO, "entry": [0, 0]},
    {**_TAMANHO, "entry": (0, "0")},
    {**_TAMANHO, "entry": None},
    {**_TAMANHO, "exit": "19,14"},
    {**_TAMANHO, "exit": (1.5, 2)},
    {**_TAMANHO, "perfect": "no"},
    {**_TAMANHO, "perfect": 1},
    {**_TAMANHO, "perfect": None},
    {**_TAMANHO, "seed": "x"},
    {**_TAMANHO, "seed": 4.2},
)


def argumentos(expressao: str) -> dict[str, object]:
    """Argumentos de uma expressão ``MazeGenerator(...)`` só com literais.

    Args:
        expressao: Texto como escrito no .feature.

    Returns:
        Nome do parâmetro (I09) para valor; os posicionais recebem o nome
        pela ordem da assinatura.

    Raises:
        ValueError: A expressão não é uma chamada a MazeGenerator com
            literais e parâmetros da I09.
    """
    try:
        arvore = ast.parse(expressao.strip(), mode="eval")
    except SyntaxError as erro:
        raise ValueError(f"não é Python válido: {erro.msg}") from erro
    chamada = arvore.body
    if not (
        isinstance(chamada, ast.Call)
        and isinstance(chamada.func, ast.Name)
        and chamada.func.id == CLASSE
    ):
        raise ValueError(f"não é uma chamada a {CLASSE}(...)")
    if len(chamada.args) > len(PARAMETROS):
        raise ValueError(f"mais de {len(PARAMETROS)} argumentos posicionais")
    nomes = list(PARAMETROS[:len(chamada.args)])
    for palavra in chamada.keywords:
        if palavra.arg not in PARAMETROS:
            raise ValueError(
                f"parâmetro {palavra.arg!r} fora da assinatura da I09: "
                f"{', '.join(PARAMETROS)}"
            )
        nomes.append(palavra.arg)
    nos = [*chamada.args, *(palavra.value for palavra in chamada.keywords)]
    valores: dict[str, object] = {}
    for nome, no in zip(nomes, nos):
        try:
            valores[nome] = ast.literal_eval(no)
        except ValueError as erro:
            raise ValueError(
                f"o valor de {nome} não é literal: {ast.unparse(no)}"
            ) from erro
    return valores


def avaliar(expressao: str) -> Any:
    """Avalia a expressão com só a classe MazeGenerator no escopo.

    Args:
        expressao: Chamada a MazeGenerator com literais.

    Returns:
        A instância criada; a exceção do construtor se propaga.

    Raises:
        ValueError: A expressão não passa em ``argumentos``.
    """
    argumentos(expressao)
    # O eval roda só depois de ``argumentos`` confirmar uma única chamada a
    # MazeGenerator com literais; ele mantém os argumentos posicionais como
    # o .feature os escreveu.
    escopo = {CLASSE: classe_geradora()}
    return eval(expressao.strip(), {"__builtins__": {}}, escopo)


def exemplo_da_docstring(docstring: str) -> str:
    """Bloco de código da seção ``Example:`` de uma docstring (I22).

    A seção vai da linha ``Example:`` até a primeira linha não vazia com
    recuo igual ou menor que o dela.

    Args:
        docstring: Docstring já limpa por ``ast.get_docstring``.

    Returns:
        O código, sem o recuo comum e terminado em quebra de linha.

    Raises:
        ValueError: A docstring não tem a seção ou a seção está vazia.
    """
    linhas = docstring.splitlines()
    for indice, linha in enumerate(linhas):
        if linha.strip() != SECAO_DO_EXEMPLO:
            continue
        recuo = len(linha) - len(linha.lstrip())
        corpo: list[str] = []
        for seguinte in linhas[indice + 1:]:
            if seguinte.strip() and (
                len(seguinte) - len(seguinte.lstrip()) <= recuo
            ):
                break
            corpo.append(seguinte)
        codigo = textwrap.dedent("\n".join(corpo)).strip("\n")
        if not codigo:
            raise ValueError(f"a seção {SECAO_DO_EXEMPLO} está vazia")
        return codigo + "\n"
    raise ValueError(f"a docstring não tem a seção {SECAO_DO_EXEMPLO}")


def classe_geradora() -> Callable[..., Any]:
    """A classe MazeGenerator do mazegen instalado ou de ../project.

    Returns:
        A classe.
    """
    classe: Callable[..., Any] = getattr(
        importlib.import_module(MODULO), "MazeGenerator"
    )
    return classe


def classe_de_erro() -> type[Exception]:
    """A exceção pública MazeError do mazegen.

    Returns:
        A classe da exceção.
    """
    erro: type[Exception] = getattr(
        importlib.import_module(MODULO), "MazeError"
    )
    return erro


def parametros_do_config(chaves: dict[str, str]) -> dict[str, object]:
    """Argumentos de MazeGenerator equivalentes a um config (I09).

    Args:
        chaves: Chave em maiúsculas para valor, como ``ler_chaves``.

    Returns:
        width, height, entry, exit, perfect e, se houver, seed.

    Raises:
        ValueError: Quando o config não tem um valor que o módulo aceita.
    """
    entrada = coordenada(chaves["ENTRY"])
    saida = coordenada(chaves["EXIT"])
    if entrada is None or saida is None:
        raise ValueError("ENTRY e EXIT precisam ser x,y")
    parametros: dict[str, object] = {
        "width": int(chaves["WIDTH"]),
        "height": int(chaves["HEIGHT"]),
        "entry": entrada,
        "exit": saida,
        "perfect": chaves["PERFECT"].lower() == "true",
    }
    if "SEED" in chaves:
        parametros["seed"] = int(chaves["SEED"])
    return parametros


def labirinto_do_gerador(
    gerador: Any, entrada: tuple[int, int], saida: tuple[int, int] | None
) -> Labirinto:
    """Labirinto que a classe deixou depois de ``generate()``.

    A classe não expõe entrada e saída (I09); elas vêm dos argumentos
    passados ao construtor.

    Args:
        gerador: Instância de MazeGenerator já gerada.
        entrada: ``entry`` passado ao construtor.
        saida: ``exit`` passado ao construtor; None é o canto inferior
            direito.

    Returns:
        O labirinto com ``grid``, ``solution`` e ``pattern`` da classe.
    """
    grade = [list(linha) for linha in gerador.grid]
    if saida is None:
        saida = (len(grade[0]) - 1, len(grade) - 1)
    return Labirinto(
        grade,
        entrada,
        saida,
        str(gerador.solution),
        None,
        [],
        frozenset(tuple(celula) for celula in gerador.pattern),
    )


def _ponto(nome: str, valor: object) -> tuple[int, int]:
    """Confere que o valor é uma coordenada (x, y) de inteiros.

    Args:
        nome: Nome do parâmetro, para a mensagem.
        valor: Valor passado ao construtor.

    Returns:
        A coordenada.

    Raises:
        ValueError: O valor não é uma tupla de dois inteiros.
    """
    if (
        isinstance(valor, tuple)
        and len(valor) == 2
        and all(isinstance(item, int) for item in valor)
    ):
        return (valor[0], valor[1])
    raise ValueError(f"{nome} não é uma tupla (x, y) de inteiros: {valor!r}")


def extremos(
    valores: dict[str, object],
) -> tuple[tuple[int, int], tuple[int, int] | None]:
    """Entrada e saída que o construtor recebeu, com os padrões da I09.

    Args:
        valores: Argumentos do construtor, como ``argumentos`` devolve.

    Returns:
        ``entry`` (ausente = (0, 0)) e ``exit`` (ausente ou None = None, o
        canto inferior direito).

    Raises:
        ValueError: Uma coordenada passada não é (x, y) de inteiros.
    """
    entrada = _ponto("entry", valores.get("entry", ENTRADA_PADRAO))
    saida = valores.get("exit")
    return entrada, None if saida is None else _ponto("exit", saida)


def dimensoes(valores: dict[str, object]) -> tuple[int, int]:
    """Largura e altura que o construtor recebeu.

    Args:
        valores: Argumentos do construtor, como ``argumentos`` devolve.

    Returns:
        ``width`` e ``height``.

    Raises:
        ValueError: Um dos dois falta ou não é inteiro.
    """
    largura = valores.get("width")
    altura = valores.get("height")
    if not isinstance(largura, int) or not isinstance(altura, int):
        raise ValueError(
            f"width e height precisam ser inteiros: {largura!r}, {altura!r}"
        )
    return largura, altura
