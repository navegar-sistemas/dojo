"""Testes do catálogo de casos de erro e dos passos que o usam."""

import os
import re
from collections.abc import Callable
from dataclasses import replace

import pytest

from step_defs.catalogo import (
    NOME_DE_EXCECAO,
    casos_do_catalogo,
    casos_executados,
    cada_caso_executado,
    depende_de_permissao,
    executar_caso,
    mensagem_cita_a_causa,
    mensagem_comeca_com_error,
    mensagem_sem_excecao,
    nenhum_estouro,
    nenhum_traceback,
)
from step_defs.repositorio import CONTEUDOS, ESPECIAIS, SITUACOES
from suporte.catalogo import CATALOGO, Caso
from suporte.estado import TESTS_DIR, Estado, Execucao

FEATURES_DE_ERRO = ("03", "04", "05", "07", "08", "13")
PASSO_DE_ERRO = re.compile(
    r"^(?:Então|E|Mas) (?:o código de saída é 1$|a mensagem de erro |"
    r'o resultado da execução é "<resultado>")'
)
ERRO = "Error: cfg.txt: WIDTH must be an integer, got 'abc'\n"


def celulas(linha: str) -> list[str]:
    """Valores de uma linha de tabela de exemplos do .feature.

    Args:
        linha: Linha "| a | b |", já sem espaços nas pontas.

    Returns:
        Os valores, sem os espaços em volta.
    """
    return [valor.strip() for valor in linha.strip("|").split("|")]


def exemplos_de_erro() -> set[tuple[str, str, tuple[str, ...]]]:
    """Cenários e linhas de exemplo de erro dos .feature cobertos.

    Um cenário é de erro quando um passo Então confere o código 1, a
    mensagem de erro ou um resultado "erro citando ..." (só as linhas cujo
    resultado começa com "erro").

    Returns:
        (número do .feature, título, valores da linha de exemplo).
    """
    achados: set[tuple[str, str, tuple[str, ...]]] = set()
    for numero in FEATURES_DE_ERRO:
        (arquivo,) = (TESTS_DIR / "features").glob(f"{numero}-*.feature")
        with arquivo.open(encoding="utf-8") as feature:
            texto = feature.read()
        blocos = re.split(r"^\s*(?:Esquema do )?Cenário: ", texto, flags=re.M)
        for bloco in blocos[1:]:
            titulo, *linhas = [linha.strip() for linha in bloco.splitlines()]
            if not any(PASSO_DE_ERRO.match(linha) for linha in linhas):
                continue
            tabela = [celulas(linha) for linha in linhas if linha[:1] == "|"]
            if not tabela:
                achados.add((numero, titulo, ()))
                continue
            cabecalho, *exemplos = tabela
            for valores in exemplos:
                resultado = dict(zip(cabecalho, valores)).get("resultado")
                if resultado is None or resultado.startswith("erro"):
                    achados.add((numero, titulo, tuple(valores)))
    return achados


def test_ha_exemplos_de_erro_para_conferir() -> None:
    """A leitura dos .feature encontra os cenários de erro."""
    assert len(exemplos_de_erro()) > 80


def test_um_caso_por_exemplo_de_erro() -> None:
    """O catálogo tem exatamente um caso por exemplo de cenário de erro."""
    catalogados = [
        (caso.feature, caso.cenario, caso.exemplo) for caso in CATALOGO
    ]
    assert len(catalogados) == len(set(catalogados))
    esperados = exemplos_de_erro()
    assert sorted(esperados - set(catalogados)) == []
    assert sorted(set(catalogados) - esperados) == []


@pytest.mark.parametrize("caso", CATALOGO, ids=lambda caso: caso.nome)
def test_caso_bem_formado(caso: Caso) -> None:
    """Cada caso usa valores existentes e diz o que a mensagem cita.

    Args:
        caso: Caso do catálogo.
    """
    assert caso.uso or caso.cita
    assert caso.config in (None, "base", "do repositório")
    assert caso.situacao is None or caso.situacao in SITUACOES
    if caso.preparado is not None:
        assert caso.preparado[1] in ESPECIAIS or caso.preparado[1] in CONTEUDOS
    assert caso.comando.startswith("python3 a_maze_ing.py")


@pytest.mark.parametrize(
    ("caso", "nome"),
    [
        (Caso("05", "Título", (), "c", ("X",)), "05 Título"),
        (Caso("05", "Título", ("a", ""), "c", ("X",)), "05 Título | a |  |"),
    ],
    ids=["cenário", "linha de exemplo"],
)
def test_nome_do_caso(caso: Caso, nome: str) -> None:
    """O nome junta o .feature, o título e os valores do exemplo.

    Args:
        caso: Caso montado no teste.
        nome: Nome esperado.
    """
    assert caso.nome == nome


@pytest.mark.parametrize(
    ("caso", "depende"),
    [
        (Caso("04", "t", (), "c", ("a",), preparado=("a", "vazio")), False),
        (
            Caso(
                "04", "t", (), "c", ("a",),
                preparado=("a", "sem permissão de leitura"),
            ),
            True,
        ),
        (
            Caso(
                "13", "t", (), "c", ("a",),
                preparado=("a", "diretório sem permissão de escrita"),
            ),
            True,
        ),
        (
            Caso(
                "03", "t", (), "c", ("a",),
                situacao="arquivo de configuração sem permissão de leitura",
            ),
            True,
        ),
        (Caso("03", "t", (), "c", ("a",), situacao="valor inválido"), False),
    ],
    ids=[
        "vazio", "sem leitura", "sem escrita", "situação sem leitura",
        "valor inválido",
    ],
)
def test_depende_de_permissao(caso: Caso, depende: bool) -> None:
    """Só os casos que dependem de chmod são marcados.

    Args:
        caso: Caso montado no teste.
        depende: Resposta esperada.
    """
    assert depende_de_permissao(caso) is depende


def test_casos_do_catalogo_carrega_todos(estado: Estado) -> None:
    """Fora do root, o passo carrega o catálogo inteiro.

    Args:
        estado: Estado do cenário.
    """
    casos_do_catalogo(estado)
    if os.geteuid() == 0:
        assert estado.catalogo == [
            caso for caso in CATALOGO if not depende_de_permissao(caso)
        ]
    else:
        assert estado.catalogo == list(CATALOGO)


def caso_de(comando: str) -> Caso:
    """Caso de teste que roda um comando qualquer sobre o config base.

    Args:
        comando: Comando do caso.

    Returns:
        O caso.
    """
    return Caso("05", "teste", (), comando, ("cfg.txt",))


CAT = caso_de("cat cfg.txt")


@pytest.mark.parametrize(
    ("caso", "esperado"),
    [
        (replace(CAT, pares=("WIDTH=abc",)), "WIDTH=abc\nHEIGHT=15\n"),
        (replace(CAT, sem="WIDTH"), "HEIGHT=15\nENTRY=0,0\n"),
        (replace(CAT, linha=(2, "HEIGHT 15")), "WIDTH=20\nHEIGHT 15\n"),
        (
            replace(CAT, linha_da_chave=("WIDTH", "")),
            "HEIGHT=15\nENTRY=0,0\n",
        ),
        (replace(CAT, linha_da_chave=("WIDTH", "W=1")), "W=1\nHEIGHT=15\n"),
        (replace(CAT, situacao="valor inválido"), "WIDTH=abc\nHEIGHT=15\n"),
        (replace(CAT, config="do repositório"), "# repositório\nWIDTH=9\n"),
    ],
    ids=[
        "pares", "sem a chave", "linha trocada", "linha da chave removida",
        "linha da chave trocada", "situação", "config do repositório",
    ],
)
def test_executar_caso_monta_o_config(
    cenario: Estado, caso: Caso, esperado: str
) -> None:
    """O config do caso vai para cfg.txt com os ajustes, e some no fim.

    Args:
        cenario: Estado numa pasta temporária.
        caso: Caso com os ajustes do config.
        esperado: Começo do cfg.txt que o comando vê.
    """
    (cenario.cwd / "config.txt").write_text(
        "# repositório\nWIDTH=9\n", encoding="utf-8"
    )
    execucao = executar_caso(cenario, caso, 0)
    assert execucao.saida_padrao.startswith(esperado)
    assert not (cenario.cwd / "cfg.txt").exists()
    assert cenario.resultados == []


@pytest.mark.parametrize(
    ("caso", "saida"),
    [
        (
            replace(
                caso_de("wc -c < cfg.txt"),
                config=None,
                preparado=("cfg.txt", "vazio"),
            ),
            "0",
        ),
        (
            replace(
                caso_de("test -e cfg.txt; echo $?"),
                preparado=("cfg.txt", "inexistente"),
            ),
            "1",
        ),
        (
            replace(
                caso_de("test -e cfg.txt; echo $?"),
                situacao="arquivo de configuração inexistente",
            ),
            "1",
        ),
        (
            replace(
                caso_de("test -d a/b; echo $?"),
                preparado=("a/b", "diretório"),
            ),
            "0",
        ),
    ],
    ids=["vazio sem config", "inexistente", "situação", "pasta nova"],
)
def test_executar_caso_prepara_e_desfaz_o_caminho(
    cenario: Estado, caso: Caso, saida: str
) -> None:
    """O caminho preparado vale durante o comando e some no fim.

    Args:
        cenario: Estado numa pasta temporária.
        caso: Caso que prepara um caminho e o inspeciona.
        saida: Saída esperada do comando.
    """
    execucao = executar_caso(cenario, caso, 0)
    assert execucao.saida_padrao.strip() == saida
    assert sorted(cenario.cwd.iterdir()) == []


def test_executar_caso_exige_reserva() -> None:
    """Sem pasta de reserva, o caso não roda."""
    with pytest.raises(pytest.fail.Exception, match="reserva"):
        executar_caso(Estado(), caso_de("true"), 0)


def test_cada_caso_executado_troca_as_execucoes(cenario: Estado) -> None:
    """Cada caso vira uma execução, na ordem do catálogo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.execucoes = [Execucao("antiga", 0, "", "")]
    cenario.catalogo = [caso_de("echo um"), caso_de("echo dois")]
    cada_caso_executado(cenario)
    assert [
        execucao.saida_padrao for execucao in cenario.execucoes
    ] == ["um\n", "dois\n"]


def test_cada_caso_executado_exige_o_catalogo(cenario: Estado) -> None:
    """Sem o catálogo carregado, o passo falha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não foi carregado"):
        cada_caso_executado(cenario)


def test_casos_executados_exige_as_execucoes(cenario: Estado) -> None:
    """Catálogo sem execuções correspondentes derruba as propriedades.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não foi carregado"):
        casos_executados(cenario)
    cenario.catalogo = [caso_de("true")]
    with pytest.raises(pytest.fail.Exception, match="não foram executados"):
        casos_executados(cenario)


def com_execucoes(
    cenario: Estado, *execucoes: tuple[Caso, Execucao]
) -> Estado:
    """Põe no cenário um catálogo já executado.

    Args:
        cenario: Estado numa pasta temporária.
        *execucoes: Pares (caso, execução).

    Returns:
        O mesmo estado.
    """
    cenario.catalogo = [caso for caso, _ in execucoes]
    cenario.execucoes = [execucao for _, execucao in execucoes]
    return cenario


USO = Caso("04", "uso", ("",), "python3 a_maze_ing.py", (), uso=True)
WIDTH = Caso("05", "width", ("abc",), "c", ("cfg.txt", "WIDTH"))
MENSAGEM_DE_USO = "Usage: python3 a_maze_ing.py <config_file>\n"
PROPRIEDADES: dict[str, Callable[[Estado], None]] = {
    "Traceback": nenhum_traceback,
    "tempo limite": nenhum_estouro,
    "Error:": mensagem_comeca_com_error,
    "cita": mensagem_cita_a_causa,
    "exceção": mensagem_sem_excecao,
}


@pytest.mark.parametrize("propriedade", PROPRIEDADES)
def test_propriedades_aceitam_o_catalogo_certo(
    cenario: Estado, propriedade: str
) -> None:
    """Mensagem da D01 certa e uso com a mensagem da I12 passam em todas.

    Args:
        cenario: Estado numa pasta temporária.
        propriedade: Chave de PROPRIEDADES.
    """
    com_execucoes(
        cenario,
        (WIDTH, Execucao("c", 1, "", ERRO)),
        (USO, Execucao("c", 1, "", MENSAGEM_DE_USO)),
    )
    PROPRIEDADES[propriedade](cenario)


@pytest.mark.parametrize(
    ("propriedade", "execucao", "caso"),
    [
        (
            "Traceback",
            Execucao("c", 1, "Traceback (most recent call last):\n", ERRO),
            WIDTH,
        ),
        (
            "Traceback",
            Execucao("c", 1, "", "Traceback (most recent call last):\n"),
            USO,
        ),
        ("tempo limite", Execucao("c", -9, "", "", True), USO),
        ("Error:", Execucao("c", 1, "", "WIDTH inválido\n"), WIDTH),
        ("Error:", Execucao("c", 1, "", ERRO + ERRO), WIDTH),
        ("Error:", Execucao("c", 0, "", ""), WIDTH),
        ("cita", Execucao("c", 1, "", "Error: WIDTH is bad\n"), WIDTH),
        (
            "cita",
            Execucao("c", 1, "", "Error: WIDTH in cfg.txt is bad\n"),
            WIDTH,
        ),
        (
            "exceção",
            Execucao("c", 1, "", "Error: ValueError: invalid literal\n"),
            WIDTH,
        ),
        (
            "exceção",
            Execucao("c", 1, "", "Error: MazeError('width')\n"),
            WIDTH,
        ),
        (
            "exceção",
            Execucao("c", 1, "", "Error: KeyboardInterrupt\n"),
            WIDTH,
        ),
    ],
    ids=[
        "Traceback no stdout", "Traceback no uso", "estouro", "sem prefixo",
        "duas linhas", "sem mensagem", "sem o arquivo", "fora de ordem",
        "ValueError", "exceção do projeto", "KeyboardInterrupt",
    ],
)
def test_propriedades_recusam_o_defeito(
    cenario: Estado, propriedade: str, execucao: Execucao, caso: Caso
) -> None:
    """Cada propriedade falha citando o caso que não a cumpre.

    Args:
        cenario: Estado numa pasta temporária.
        propriedade: Chave de PROPRIEDADES.
        execucao: Execução com o defeito.
        caso: Caso a que a execução pertence.
    """
    com_execucoes(
        cenario, (WIDTH, Execucao("c", 1, "", ERRO)), (caso, execucao)
    )
    with pytest.raises(pytest.fail.Exception, match=re.escape(caso.nome)):
        PROPRIEDADES[propriedade](cenario)


@pytest.mark.parametrize("propriedade", ["Error:", "cita", "exceção"])
def test_propriedades_da_mensagem_pulam_o_uso(
    cenario: Estado, propriedade: str
) -> None:
    """O uso errado da linha de comando (I12) não segue a D01.

    Args:
        cenario: Estado numa pasta temporária.
        propriedade: Chave de PROPRIEDADES.
    """
    com_execucoes(
        cenario, (USO, Execucao("c", 1, "", "Usage: ValueError\nlinha 2\n"))
    )
    PROPRIEDADES[propriedade](cenario)


@pytest.mark.parametrize(
    ("texto", "nome"),
    [
        ("Error: cfg.txt: x", None),
        ("Error: cannot read pasta: Is a directory", None),
        ("Error: cfg.txt: SEED must be an integer", None),
        ("Error: OSError", "OSError"),
        ("Error: UnicodeDecodeError: x", "UnicodeDecodeError"),
        ("Error: ConfigError: x", "ConfigError"),
        ("Error: SystemExit", "SystemExit"),
        ("Error: StopIteration", "StopIteration"),
    ],
    ids=[
        "D01", "strerror", "palavra Error no meio", "OSError", "Unicode",
        "do projeto", "SystemExit", "StopIteration",
    ],
)
def test_nome_de_excecao(texto: str, nome: str | None) -> None:
    """O prefixo "Error:" não conta; nomes de exceção contam.

    Args:
        texto: Mensagem de erro.
        nome: Nome achado, ou None.
    """
    achado = NOME_DE_EXCECAO.search(texto)
    assert (achado.group(0) if achado else None) == nome
