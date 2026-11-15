"""Testes do maze_analyzer: execução, leitura do relatório e passos."""

import pytest

from step_defs.analyzer import (
    eu_analiso,
    eu_analiso_com_opcoes,
    eu_gero_e_analiso,
    linha_do_analyzer,
    numero_do_analyzer,
    veredito_do_perfect,
)
from suporte.analyzer import (
    ROTULOS,
    analisar,
    analise_atual,
    arquivo_atual,
    primeiro_inteiro,
    valor_da_linha,
)
from suporte.config import CONFIG_BASE, Config
from suporte.estado import Estado, Execucao
from suporte.labirinto import Labirinto, ler_saida

# Labirinto 2x1 com uma passagem entre as duas células: perfeito.
LABIRINTO = "d7\n\n0,0\n1,0\nE\n"
RELATORIO = """\
Maze size        : 20 x 15 (300 cells)
Entry            : (0, 0)   Exit: (19, 14) (reachable)
Reachable region : 282 cells (0 corridor(s) unreachable)
Independent loops: 32 / 228 possible (path ratio 14%)
Dead-ends        : 2 real + 2 enclosed by the '42' (tolerated)
Corners + centre : all reachable
Wall coherence   : OK (all shared walls match)

Verdict: Pac-Man-USABLE: fully connected, 32 independent routes.
"""
PROGRAMA = (
    "from pathlib import Path\n"
    f"Path('maze.txt').write_text({LABIRINTO!r})\n"
)


def com_analise(cenario: Estado, saida: str = RELATORIO) -> Estado:
    """Põe no cenário uma análise já feita.

    Args:
        cenario: Estado numa pasta temporária.
        saida: Saída padrão do analyzer.

    Returns:
        O mesmo estado.
    """
    cenario.analise = Execucao("analyzer", 0, saida, "")
    return cenario


def com_labirinto_em_arquivo(cenario: Estado) -> Execucao:
    """Grava um OUTPUT_FILE e registra a execução que o produziu.

    Args:
        cenario: Estado numa pasta temporária.

    Returns:
        A execução, com o labirinto registrado no cenário.
    """
    saida = cenario.cwd / "maze.txt"
    saida.write_text(LABIRINTO, encoding="utf-8")
    execucao = Execucao(
        "python3 a_maze_ing.py cfg.txt", 0, "", "", False, saida, LABIRINTO
    )
    cenario.registrar_labirinto(execucao)
    cenario.resultados.append(execucao)
    return execucao


def test_arquivo_atual_exige_um_labirinto(cenario: Estado) -> None:
    """Sem labirinto no cenário não há arquivo a analisar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhum labirinto"):
        arquivo_atual(cenario)


def test_arquivo_atual_recusa_o_labirinto_da_classe(cenario: Estado) -> None:
    """O labirinto de generate() não tem arquivo de saída.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(Labirinto([[13, 7]], (0, 0), (1, 0), "E"))
    with pytest.raises(pytest.fail.Exception, match="classe geradora"):
        arquivo_atual(cenario)


def test_arquivo_atual_e_o_output_file_da_execucao(cenario: Estado) -> None:
    """O labirinto vindo de uma execução usa o OUTPUT_FILE dela.

    Args:
        cenario: Estado numa pasta temporária.
    """
    execucao = com_labirinto_em_arquivo(cenario)
    assert arquivo_atual(cenario) == execucao.arquivo_saida


@pytest.mark.parametrize(
    "regravado", [True, False], ids=["arquivo regravado", "labirinto de teste"]
)
def test_arquivo_atual_copia_o_texto(cenario: Estado, regravado: bool) -> None:
    """Sem arquivo com o mesmo conteúdo, o texto vai para um temporário.

    Args:
        cenario: Estado numa pasta temporária.
        regravado: Se o OUTPUT_FILE mudou depois da execução.
    """
    if regravado:
        execucao = com_labirinto_em_arquivo(cenario)
        assert execucao.arquivo_saida is not None
        execucao.arquivo_saida.write_text("outro", encoding="utf-8")
    else:
        cenario.labirintos.append(ler_saida(LABIRINTO))
    arquivo = arquivo_atual(cenario)
    assert arquivo.parent != cenario.cwd
    assert arquivo.read_text(encoding="utf-8") == LABIRINTO
    cenario.restaurar()
    assert not arquivo.parent.exists()


def test_analisar_roda_o_analyzer(cenario: Estado) -> None:
    """A execução fica em resultados e em analise, com as opções.

    Args:
        cenario: Estado numa pasta temporária.
    """
    arquivo = cenario.cwd / "maze.txt"
    arquivo.write_text(LABIRINTO, encoding="utf-8")
    execucao = analisar(cenario, arquivo, ["--max-dead-ends", "0"])
    assert cenario.analise is execucao
    assert cenario.resultados == [execucao]
    assert execucao.codigo == 0
    assert "--max-dead-ends 0" in execucao.comando
    assert valor_da_linha(execucao.saida_padrao, "Verdict:").startswith(
        "PERFECT maze"
    )


def test_analise_atual_reaproveita_ou_roda(cenario: Estado) -> None:
    """A análise já feita é reaproveitada; sem ela, o analyzer roda.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(ler_saida(LABIRINTO))
    execucao = analise_atual(cenario)
    assert "Wall coherence" in execucao.saida_padrao
    assert analise_atual(cenario) is execucao
    assert len(cenario.resultados) == 1


def test_eu_analiso_com_e_sem_opcoes(cenario: Estado) -> None:
    """Os dois passos analisam o arquivo atual; as opções são separadas.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_labirinto_em_arquivo(cenario)
    eu_analiso(cenario)
    eu_analiso_com_opcoes(cenario, "--max-dead-ends 0 --min-loops 0")
    assert cenario.analise is not None
    assert cenario.analise.comando.endswith(
        "maze.txt --max-dead-ends 0 --min-loops 0"
    )
    assert len(cenario.resultados) == 3


def test_eu_gero_e_analiso(cenario: Estado) -> None:
    """Gera pelo programa e analisa o OUTPUT_FILE gravado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "a_maze_ing.py").write_text(PROGRAMA, encoding="utf-8")
    cenario.config = Config(list(CONFIG_BASE))
    eu_gero_e_analiso(cenario)
    assert cenario.analise is not None
    assert str(cenario.cwd / "maze.txt") in cenario.analise.comando
    linha_do_analyzer(cenario, "Reachable region", "começa com", ["2 cells"])


def test_eu_gero_e_analiso_exige_o_labirinto(cenario: Estado) -> None:
    """Geração que falha não deixa analisar o labirinto anterior.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "a_maze_ing.py").write_text(
        "raise SystemExit(1)\n", encoding="utf-8"
    )
    cenario.config = Config(list(CONFIG_BASE))
    cenario.labirintos.append(ler_saida(LABIRINTO))
    with pytest.raises(pytest.fail.Exception, match="não gerou"):
        eu_gero_e_analiso(cenario)
    assert cenario.analise is None


@pytest.mark.parametrize(
    ("rotulo", "valor"),
    [
        (
            "Verdict:",
            "Pac-Man-USABLE: fully connected, 32 independent routes.",
        ),
        ("Reachable region", "282 cells (0 corridor(s) unreachable)"),
        ("Independent loops", "32 / 228 possible (path ratio 14%)"),
        ("Dead-ends", "2 real + 2 enclosed by the '42' (tolerated)"),
        ("Corners + centre", "all reachable"),
        ("Wall coherence", "OK (all shared walls match)"),
        ("Entry", "(0, 0)   Exit: (19, 14) (reachable)"),
    ],
    ids=list(ROTULOS),
)
def test_valor_da_linha(rotulo: str, valor: str) -> None:
    """O valor é o que vem depois do rótulo, dos espaços e do ":".

    Args:
        rotulo: Rótulo da linha.
        valor: Valor esperado.
    """
    assert valor_da_linha(RELATORIO, rotulo) == valor


@pytest.mark.parametrize(
    ("saida", "rotulo", "mensagem"),
    [
        (RELATORIO, "Maze size", "não existe"),
        ("Malformed maze file: x\n", "Verdict:", "vieram 0"),
        ("Entry : a\nEntry : b\n", "Entry", "vieram 2"),
    ],
    ids=["rótulo fora da lista", "sem a linha", "linha repetida"],
)
def test_valor_da_linha_invalido(
    saida: str, rotulo: str, mensagem: str
) -> None:
    """Rótulo desconhecido, ausente ou repetido derruba o passo.

    Args:
        saida: Saída do analyzer.
        rotulo: Rótulo pedido.
        mensagem: Trecho da mensagem de falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        valor_da_linha(saida, rotulo)


def test_primeiro_inteiro() -> None:
    """O primeiro inteiro do valor é o número da linha."""
    assert primeiro_inteiro("32 / 228 possible", "Independent loops") == 32
    with pytest.raises(pytest.fail.Exception, match="não tem número"):
        primeiro_inteiro("all reachable", "Corners + centre")


@pytest.mark.parametrize(
    ("rotulo", "op", "textos"),
    [
        ("Verdict:", "começa com", ["Pac-Man-USABLE"]),
        ("Independent loops", "começa com", ["32 /"]),
        ("Entry", "contém", ["(0, 0)", "Exit: (19, 14) (reachable)"]),
        ("Wall coherence", "contém", ["OK (all shared walls match)"]),
    ],
    ids=["veredito", "loops", "entrada e saída", "coerência"],
)
def test_linha_do_analyzer_aceita(
    cenario: Estado, rotulo: str, op: str, textos: list[str]
) -> None:
    """Valor que começa com o texto, ou que contém todos, passa.

    Args:
        cenario: Estado numa pasta temporária.
        rotulo: Rótulo da linha.
        op: "começa com" ou "contém".
        textos: Textos procurados.
    """
    linha_do_analyzer(com_analise(cenario), rotulo, op, textos)


@pytest.mark.parametrize(
    ("rotulo", "op", "textos"),
    [
        ("Verdict:", "começa com", ["PERFECT maze"]),
        ("Verdict:", "começa com", ["fully connected"]),
        ("Entry", "contém", ["(0, 0)", "(1, 1)"]),
        ("Wall coherence", "contém", ["mismatching"]),
        ("Verdict:", "termina com", ["."]),
    ],
    ids=[
        "outro veredito", "texto do meio", "um dos textos falta",
        "coerência", "operação desconhecida",
    ],
)
def test_linha_do_analyzer_recusa(
    cenario: Estado, rotulo: str, op: str, textos: list[str]
) -> None:
    """Valor que não começa com o texto, ou sem um dos textos, falha.

    Args:
        cenario: Estado numa pasta temporária.
        rotulo: Rótulo da linha.
        op: Operação pedida.
        textos: Textos procurados.
    """
    with pytest.raises(pytest.fail.Exception):
        linha_do_analyzer(com_analise(cenario), rotulo, op, textos)


def test_linha_do_analyzer_roda_o_analyzer(cenario: Estado) -> None:
    """Sem análise no cenário, o passo roda o analyzer sobre o labirinto.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(ler_saida("f7\n\n0,0\n1,0\n\n"))
    linha_do_analyzer(
        cenario,
        "Wall coherence",
        "contém",
        ["2 mismatching cell(s) -> (0, 0), (1, 0)"],
    )
    assert cenario.analise is not None


@pytest.mark.parametrize(
    ("rotulo", "cmp", "n", "certo"),
    [
        ("Independent loops", "pelo menos", 2, True),
        ("Independent loops", "pelo menos", 33, False),
        ("Dead-ends", "no máximo", 2, True),
        ("Dead-ends", "no máximo", 1, False),
    ],
    ids=["pelo menos", "menos que", "no máximo", "mais que"],
)
def test_numero_do_analyzer(
    cenario: Estado, rotulo: str, cmp: str, n: int, certo: bool
) -> None:
    """O primeiro inteiro da linha é comparado com o limite.

    Args:
        cenario: Estado numa pasta temporária.
        rotulo: Rótulo da linha.
        cmp: "pelo menos" ou "no máximo".
        n: Limite.
        certo: Se a comparação deve passar.
    """
    com_analise(cenario)
    if certo:
        numero_do_analyzer(cenario, rotulo, cmp, n)
    else:
        with pytest.raises(pytest.fail.Exception, match="esperado"):
            numero_do_analyzer(cenario, rotulo, cmp, n)


def test_numero_do_analyzer_com_comparacao_desconhecida(
    cenario: Estado,
) -> None:
    """Comparação fora da lista fechada derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        numero_do_analyzer(com_analise(cenario), "Dead-ends", "igual a", 2)


@pytest.mark.parametrize(
    ("perfeito", "veredito", "certo"),
    [
        ("True", "Verdict: PERFECT maze: a single path.", True),
        ("true", "Verdict: PERFECT maze: a single path.", True),
        ("False", "Verdict: Pac-Man-USABLE: fully connected.", True),
        ("False", "Verdict: PERFECT maze: a single path.", False),
        ("True", "Verdict: Pac-Man-USABLE: fully connected.", False),
        ("True", "Verdict: Not Pac-Man-ready: only 1 route.", False),
        ("talvez", "Verdict: PERFECT maze: a single path.", False),
    ],
    ids=[
        "True perfeito", "true minúsculo", "False Pac-Man", "False perfeito",
        "True Pac-Man", "veredito ruim", "PERFECT inválido",
    ],
)
def test_veredito_do_perfect(
    cenario: Estado, perfeito: str, veredito: str, certo: bool
) -> None:
    """O veredito precisa corresponder ao PERFECT do config.

    Args:
        cenario: Estado numa pasta temporária.
        perfeito: Valor de PERFECT no config.
        veredito: Linha Verdict: do analyzer.
        certo: Se o passo deve passar.
    """
    cenario.config = Config([f"PERFECT={perfeito}"])
    com_analise(cenario, f"{veredito}\n")
    if certo:
        veredito_do_perfect(cenario)
    else:
        with pytest.raises(pytest.fail.Exception):
            veredito_do_perfect(cenario)


def test_veredito_exige_o_perfect(cenario: Estado) -> None:
    """Config sem PERFECT não diz qual veredito esperar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(["WIDTH=20"])
    with pytest.raises(pytest.fail.Exception, match="PERFECT"):
        veredito_do_perfect(com_analise(cenario))
