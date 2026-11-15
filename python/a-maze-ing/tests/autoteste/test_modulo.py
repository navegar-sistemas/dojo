"""Testes dos passos da classe MazeGenerator, com um mazegen falso."""

import random
import sys
import types
from collections.abc import Callable

import pytest

from step_defs.modulo import (
    construtor_levanta,
    exemplo_salvo,
    gerador_gera,
    gero_com_instancias,
    grade_igual_ao_arquivo,
    grid_e_solution_preenchidos,
    grid_publico,
    mensagem_cita,
    mesmos_parametros,
    o_gerador,
    so_maze_error,
    solution_documentada,
    tento_criar,
    uma_unica_classe,
)
from suporte.estado import Estado, Execucao
from suporte.labirinto import Labirinto
from suporte.modulo import (
    argumentos,
    dimensoes,
    exemplo_da_docstring,
    extremos,
)

DOCUMENTACAO = "Gerador falso.\n\nAfter generate(), grid and solution.\n"


class Erro(Exception):
    """MazeError do mazegen falso."""


class Gerador:
    """MazeGenerator falso, com a assinatura e os atributos da I09."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] | None = None,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """Recusa largura menor que 2 e guarda o resto.

        Args:
            width: Colunas.
            height: Linhas.
            entry: Entrada (x, y).
            exit: Saída (x, y), ou None.
            perfect: Modo perfeito.
            seed: Seed do sorteio.

        Raises:
            Erro: width menor que 2.
        """
        if width < 2:
            raise Erro(f"width must be at least 2, got {width}")
        self.largura = width
        self.altura = height
        self.sorteio = random.Random(seed)
        self.grid: list[list[int]] = []
        self.solution = ""
        self.pattern: set[tuple[int, int]] = set()

    def generate(self) -> None:
        """Sorteia as paredes e anda até o canto inferior direito."""
        self.grid = [
            [self.sorteio.randrange(16) for _ in range(self.largura)]
            for _ in range(self.altura)
        ]
        self.solution = "E" * (self.largura - 1) + "S" * (self.altura - 1)


class Recusa:
    """Gerador que recusa qualquer argumento com a exceção do módulo."""

    def __init__(self, **valores: object) -> None:
        """Levanta Erro sempre.

        Args:
            **valores: Ignorados.

        Raises:
            Erro: Sempre.
        """
        raise Erro("refused")


class DeixaPassar:
    """Gerador que aceita qualquer argumento sem conferir."""

    def __init__(self, **valores: object) -> None:
        """Não confere nada.

        Args:
            **valores: Ignorados.
        """


class TipoErrado:
    """Gerador cujo construtor deixa escapar TypeError."""

    def __init__(self, **valores: object) -> None:
        """Levanta TypeError sempre.

        Args:
            **valores: Ignorados.

        Raises:
            TypeError: Sempre.
        """
        raise TypeError("'<' not supported")


@pytest.fixture
def falso(monkeypatch: pytest.MonkeyPatch) -> types.ModuleType:
    """Troca o mazegen importado por um módulo falso.

    Args:
        monkeypatch: Fixture do pytest, que desfaz a troca no fim.

    Returns:
        O módulo falso, com MazeGenerator e MazeError.
    """
    modulo = types.ModuleType("mazegen", DOCUMENTACAO)
    setattr(modulo, "MazeGenerator", Gerador)
    setattr(modulo, "MazeError", Erro)
    monkeypatch.setitem(sys.modules, "mazegen", modulo)
    return modulo


@pytest.mark.parametrize(
    ("expressao", "esperado"),
    [
        ("MazeGenerator(4, 3)", {"width": 4, "height": 3}),
        (
            " MazeGenerator(width=4, height=3, entry=(1, 0), exit=None, "
            "perfect=True, seed=-2) ",
            {
                "width": 4,
                "height": 3,
                "entry": (1, 0),
                "exit": None,
                "perfect": True,
                "seed": -2,
            },
        ),
        ('MazeGenerator(width="20", height=1)', {"width": "20", "height": 1}),
    ],
    ids=["posicionais", "nomeados", "tipo-errado-e-literal"],
)
def test_argumentos_da_expressao(
    expressao: str, esperado: dict[str, object]
) -> None:
    """Posicionais recebem o nome da I09 e os valores são os literais.

    Args:
        expressao: Chamada a MazeGenerator.
        esperado: Argumentos por nome.
    """
    assert argumentos(expressao) == esperado


@pytest.mark.parametrize(
    ("expressao", "motivo"),
    [
        ("MazeGenerator(", "não é Python válido"),
        ("print(1)", "não é uma chamada"),
        ("MazeGenerator", "não é uma chamada"),
        ("MazeGenerator(width=len('ab'), height=1)", "não é literal"),
        ("MazeGenerator(1, 2, (0, 0), None, True, 1, 9)", "posicionais"),
        ("MazeGenerator(width=1, size=2)", "fora da assinatura"),
        ("MazeGenerator(**{'width': 1})", "fora da assinatura"),
    ],
    ids=[
        "sintaxe",
        "outra-funcao",
        "sem-chamada",
        "nao-literal",
        "posicionais-demais",
        "parametro-desconhecido",
        "kwargs",
    ],
)
def test_argumentos_recusa(expressao: str, motivo: str) -> None:
    """Só chamada a MazeGenerator com literais da assinatura da I09.

    Args:
        expressao: Expressão fora da regra.
        motivo: Trecho esperado na mensagem.
    """
    with pytest.raises(ValueError, match=motivo):
        argumentos(expressao)


def test_extremos_e_dimensoes() -> None:
    """Entrada ausente é (0, 0); saída ausente ou None é o canto."""
    assert extremos({}) == ((0, 0), None)
    assert extremos({"entry": (1, 2), "exit": (3, 4)}) == ((1, 2), (3, 4))
    assert dimensoes({"width": 4, "height": 3}) == (4, 3)
    with pytest.raises(ValueError, match="entry"):
        extremos({"entry": [0, 0]})
    with pytest.raises(ValueError, match="width"):
        dimensoes({"height": 3})


def test_exemplo_da_docstring() -> None:
    """O bloco recuado depois de Example: vira o código, sem recuo."""
    docstring = (
        "Resumo.\n\nExample:\n    from x import y\n\n    print(y)\n"
        "\nFim do texto.\n"
    )
    assert exemplo_da_docstring(docstring) == "from x import y\n\nprint(y)\n"
    with pytest.raises(ValueError, match="não tem a seção"):
        exemplo_da_docstring("Resumo.\n\nExamples:\n    x = 1\n")
    with pytest.raises(ValueError, match="vazia"):
        exemplo_da_docstring("Resumo.\n\nExample:\nTexto.\n")


@pytest.mark.usefixtures("falso")
def test_gerador_gera_com_entrada_e_saida(cenario: Estado) -> None:
    """O labirinto usa a entrada e a saída da expressão.

    Args:
        cenario: Estado numa pasta temporária.
    """
    o_gerador(cenario, "MazeGenerator(4, 3, entry=(1, 0), seed=1)")
    gerador_gera(cenario)
    labirinto = cenario.labirintos[-1]
    assert (labirinto.entrada, labirinto.saida) == ((1, 0), (3, 2))
    assert labirinto.caminho == "EEESS"
    assert labirinto.largura == 4 and labirinto.altura == 3
    o_gerador(cenario, "MazeGenerator(width=4, height=3, exit=(2, 2))")
    gerador_gera(cenario)
    assert cenario.labirintos[-1].entrada == (0, 0)
    assert cenario.labirintos[-1].saida == (2, 2)


@pytest.mark.usefixtures("falso")
def test_gerador_recusado(cenario: Estado) -> None:
    """Expressão fora da regra ou construtor com erro derrubam o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não é literal"):
        o_gerador(cenario, "MazeGenerator(width=x, height=3)")
    with pytest.raises(pytest.fail.Exception, match="levantou Erro"):
        o_gerador(cenario, "MazeGenerator(width=1, height=3)")
    with pytest.raises(pytest.fail.Exception, match="nenhum MazeGenerator"):
        gerador_gera(cenario)


@pytest.mark.usefixtures("falso")
def test_instancias_novas(cenario: Estado) -> None:
    """Cada instância vira uma execução com o próprio labirinto.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="o gerador"):
        gero_com_instancias(cenario, 2)
    o_gerador(cenario, "MazeGenerator(width=5, height=4, seed=7)")
    gero_com_instancias(cenario, 3)
    grades = [
        execucao.labirinto.grade
        for execucao in cenario.execucoes
        if execucao.labirinto is not None
    ]
    assert len(grades) == 3 and grades[0] == grades[1] == grades[2]
    assert len(cenario.labirintos) == 3


@pytest.mark.usefixtures("falso")
def test_excecao_do_construtor(cenario: Estado) -> None:
    """A exceção fica guardada e os passos Então conferem tipo e texto.

    Args:
        cenario: Estado numa pasta temporária.
    """
    tento_criar(cenario, "MazeGenerator(width=1, height=3)")
    construtor_levanta(cenario, "MazeError")
    mensagem_cita(cenario, ["width", "2"])
    with pytest.raises(pytest.fail.Exception, match="não cita"):
        mensagem_cita(cenario, ["height"])
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        construtor_levanta(cenario, "ValueError")
    tento_criar(cenario, "MazeGenerator(width=3, height=3)")
    assert cenario.excecao is None and cenario.gerador is not None
    with pytest.raises(pytest.fail.Exception, match="não levantou"):
        construtor_levanta(cenario, "MazeError")
    with pytest.raises(pytest.fail.Exception, match="não levantou"):
        mensagem_cita(cenario, ["width"])


def test_excecao_de_outro_tipo(
    cenario: Estado, falso: types.ModuleType
) -> None:
    """Exceção que não é MazeError derruba o passo do tipo.

    Args:
        cenario: Estado numa pasta temporária.
        falso: Módulo mazegen falso.
    """
    setattr(falso, "MazeGenerator", TipoErrado)
    tento_criar(cenario, "MazeGenerator(width=1, height=3)")
    with pytest.raises(pytest.fail.Exception, match="TypeError"):
        construtor_levanta(cenario, "MazeError")


def gravar_mazegen(cenario: Estado, corpo: str) -> None:
    """Grava um pacote mazegen na pasta do cenário.

    Args:
        cenario: Estado numa pasta temporária.
        corpo: Código do __init__.py.
    """
    pasta = cenario.cwd / "mazegen"
    pasta.mkdir(exist_ok=True)
    (pasta / "__init__.py").write_text(corpo, encoding="utf-8")


CLASSES = '''
class MazeError(Exception):
    """Erro."""


class MazeGenerator:
    """Gerador."""

    def generate(self) -> None:
        """Gera."""
'''


def test_uma_unica_classe_publica(cenario: Estado) -> None:
    """__all__ com MazeGenerator e MazeError passa.

    Args:
        cenario: Estado numa pasta temporária.
    """
    gravar_mazegen(
        cenario,
        CLASSES + '\n\nclass _Interna:\n    """Interna."""\n\n'
        '__all__ = ["MazeGenerator", "MazeError"]\n',
    )
    uma_unica_classe(cenario)


@pytest.mark.parametrize(
    ("corpo", "motivo"),
    [
        (CLASSES, "não define __all__"),
        (
            CLASSES + '\n\nclass Cell:\n    """Célula."""\n\n'
            '__all__ = ["MazeGenerator", "MazeError", "Cell"]\n',
            "__all__ é",
        ),
        (
            CLASSES + '\n\nMazeError = MazeGenerator\n\n'
            '__all__ = ["MazeGenerator", "MazeError"]\n',
            "generate",
        ),
        (
            CLASSES + '\n\nMazeError = 1\n\n'
            '__all__ = ["MazeGenerator", "MazeError"]\n',
            "não é uma classe de exceção",
        ),
        ("import inexistente\n", "terminou com código"),
    ],
    ids=["sem-all", "classe-extra", "duas-geradoras", "erro-nao-e-classe",
         "import-quebrado"],
)
def test_classe_publica_recusada(
    cenario: Estado, corpo: str, motivo: str
) -> None:
    """Outra exportação ou import quebrado derrubam a propriedade.

    Args:
        cenario: Estado numa pasta temporária.
        corpo: __init__.py do mazegen gravado.
        motivo: Trecho esperado na mensagem.
    """
    gravar_mazegen(cenario, corpo)
    with pytest.raises(pytest.fail.Exception, match=motivo):
        uma_unica_classe(cenario)


@pytest.mark.usefixtures("falso")
def test_grid_e_solution(cenario: Estado) -> None:
    """Depois de generate() passa; antes, ou com valor fora de 0..15, não.

    Args:
        cenario: Estado numa pasta temporária.
    """
    o_gerador(cenario, "MazeGenerator(width=4, height=3, seed=2)")
    with pytest.raises(pytest.fail.Exception, match="grid tem 0 linhas"):
        grid_e_solution_preenchidos(cenario)
    gerador_gera(cenario)
    grid_e_solution_preenchidos(cenario)
    grid_publico(cenario)
    solution_documentada(cenario)
    assert isinstance(cenario.gerador, Gerador)
    cenario.gerador.grid[1][2] = 16
    with pytest.raises(pytest.fail.Exception, match=r"grid\[1\]\[2\]"):
        grid_publico(cenario)
    setattr(cenario.gerador, "grid", [(1, 2, 3, 4)] * 3)
    with pytest.raises(pytest.fail.Exception, match=r"grid\[0\] não é"):
        grid_publico(cenario)
    cenario.gerador.solution = ""
    with pytest.raises(pytest.fail.Exception, match="solution"):
        solution_documentada(cenario)


def test_solution_sem_documentacao(
    cenario: Estado, falso: types.ModuleType
) -> None:
    """A docstring do módulo precisa citar solution.

    Args:
        cenario: Estado numa pasta temporária.
        falso: Módulo mazegen falso.
    """
    falso.__doc__ = "Gerador sem a palavra."
    o_gerador(cenario, "MazeGenerator(width=4, height=3)")
    gerador_gera(cenario)
    with pytest.raises(pytest.fail.Exception, match="não cita solution"):
        solution_documentada(cenario)


@pytest.mark.usefixtures("falso")
def test_mesmos_parametros(cenario: Estado) -> None:
    """Com seed a grade se repete; sem seed, não.

    Args:
        cenario: Estado numa pasta temporária.
    """
    o_gerador(cenario, "MazeGenerator(width=6, height=5, seed=3)")
    with pytest.raises(pytest.fail.Exception, match="ainda não gerou"):
        mesmos_parametros(cenario)
    gerador_gera(cenario)
    mesmos_parametros(cenario)
    o_gerador(cenario, "MazeGenerator(width=6, height=5)")
    gerador_gera(cenario)
    with pytest.raises(pytest.fail.Exception, match="outra grade"):
        mesmos_parametros(cenario)


@pytest.mark.usefixtures("falso")
def test_grade_igual_ao_arquivo(cenario: Estado) -> None:
    """O grid precisa ser a grade do OUTPUT_FILE da última execução.

    Args:
        cenario: Estado numa pasta temporária.
    """
    o_gerador(cenario, "MazeGenerator(width=3, height=2, seed=4)")
    gerador_gera(cenario)
    assert isinstance(cenario.gerador, Gerador)
    grade = [list(linha) for linha in cenario.gerador.grid]
    arquivo = Labirinto(grade, (0, 0), (2, 1), "EES")
    cenario.resultados.append(Execucao("prog", 0, "", "", labirinto=arquivo))
    grade_igual_ao_arquivo(cenario)
    grade[1][1] = (grade[1][1] + 1) % 16
    with pytest.raises(pytest.fail.Exception, match=r"célula \(1, 1\)"):
        grade_igual_ao_arquivo(cenario)
    cenario.resultados.append(Execucao("prog", 1, "", "erro"))
    with pytest.raises(pytest.fail.Exception, match="não gravou"):
        grade_igual_ao_arquivo(cenario)


@pytest.mark.parametrize(
    ("classe", "motivo"),
    [
        (DeixaPassar, "não levantou exceção"),
        (TipoErrado, "levantou TypeError"),
    ],
    ids=["sem-excecao", "outra-excecao"],
)
def test_so_maze_error_recusa(
    cenario: Estado,
    falso: types.ModuleType,
    classe: Callable[..., object],
    motivo: str,
) -> None:
    """Construtor que aceita tudo ou deixa escapar outra exceção falha.

    Args:
        cenario: Estado numa pasta temporária.
        falso: Módulo mazegen falso.
        classe: Gerador falso do caso.
        motivo: Trecho esperado na mensagem.
    """
    setattr(falso, "MazeGenerator", classe)
    with pytest.raises(pytest.fail.Exception, match=motivo):
        so_maze_error(cenario)


def test_so_maze_error_aceita(
    cenario: Estado, falso: types.ModuleType
) -> None:
    """Construtor que recusa tudo com MazeError passa, com e sem expressão.

    Args:
        cenario: Estado numa pasta temporária.
        falso: Módulo mazegen falso.
    """
    setattr(falso, "MazeGenerator", Recusa)
    so_maze_error(cenario)
    tento_criar(cenario, "MazeGenerator(width=1, height=1)")
    so_maze_error(cenario)


def test_so_maze_error_confere_a_expressao(
    cenario: Estado, falso: types.ModuleType
) -> None:
    """A expressão do cenário também entra nos casos conferidos.

    Args:
        cenario: Estado numa pasta temporária.
        falso: Módulo mazegen falso.
    """
    tento_criar(cenario, "MazeGenerator(width=3, height=1)")
    setattr(falso, "MazeGenerator", Recusa)
    so_maze_error(cenario)
    setattr(falso, "MazeGenerator", Gerador)
    with pytest.raises(
        pytest.fail.Exception,
        match=r"MazeGenerator\(width=3, height=1\) não levantou",
    ):
        so_maze_error(cenario)


def test_exemplo_salvo(cenario: Estado) -> None:
    """O código de Example: vai para o arquivo e some no fim do cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    gravar_mazegen(
        cenario,
        '"""Gerador.\n\nExample:\n    gen = 1\n    print(gen)\n"""\n',
    )
    exemplo_salvo(cenario, "mazegen", "exemplo/novo/exemplo.py")
    destino = cenario.cwd / "exemplo" / "novo" / "exemplo.py"
    assert destino.read_text(encoding="utf-8") == "gen = 1\nprint(gen)\n"
    cenario.restaurar()
    assert not (cenario.cwd / "exemplo").exists()


@pytest.mark.parametrize(
    ("arquivos", "modulo", "motivo"),
    [
        ({}, "mazegen", "não existe"),
        ({"mazegen.py": "x = 1\n"}, "mazegen", "não tem docstring"),
        (
            {"mazegen.py": '"""Gerador.\n\nExamples:\n    x = 1\n"""\n'},
            "mazegen",
            "não tem a seção Example:",
        ),
    ],
    ids=["sem-modulo", "sem-docstring", "sem-example"],
)
def test_exemplo_recusado(
    cenario: Estado, arquivos: dict[str, str], modulo: str, motivo: str
) -> None:
    """Módulo ausente, sem docstring ou sem Example: derrubam o passo.

    Args:
        cenario: Estado numa pasta temporária.
        arquivos: Nome relativo para conteúdo, gravados antes.
        modulo: Módulo pedido ao passo.
        motivo: Trecho esperado na mensagem.
    """
    for nome, conteudo in arquivos.items():
        (cenario.cwd / nome).write_text(conteudo, encoding="utf-8")
    with pytest.raises(pytest.fail.Exception, match=motivo):
        exemplo_salvo(cenario, modulo, "exemplo.py")
