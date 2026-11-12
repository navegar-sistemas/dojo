"""Testes dos passos que executam comandos e conferem a saída."""

import pytest

from step_defs.execucao import (
    codigo_de_saida,
    comando_termina_com,
    conferir_mensagem_de_erro,
    conferir_motivo,
    eu_executo,
    eu_executo_com_entrada,
    linha_da_saida_contem,
    resultado_da_execucao,
    saida_contem,
    saida_do_comando_contem,
    saida_do_comando_igual,
    saida_igual,
    termina_no_tempo,
)
from suporte.config import Config
from suporte.estado import Estado, Execucao

ERRO = "Error: cfg.txt, line 3: expected KEY=VALUE, got 'abc'\n"


def com_resultado(
    cenario: Estado,
    codigo: int = 0,
    saida_padrao: str = "",
    saida_erro: str = "",
    estourou: bool = False,
) -> Execucao:
    """Põe no cenário uma execução já terminada.

    Args:
        cenario: Estado numa pasta temporária.
        codigo: Código de saída.
        saida_padrao: Texto do stdout.
        saida_erro: Texto do stderr.
        estourou: Se o comando passou do tempo limite.

    Returns:
        A execução guardada no cenário.
    """
    execucao = Execucao("comando", codigo, saida_padrao, saida_erro, estourou)
    cenario.resultados.append(execucao)
    return execucao


def test_mensagem_de_erro_valida() -> None:
    """Uma linha com "Error: " e os itens na ordem devolve a mensagem."""
    execucao = Execucao("comando", 1, "", ERRO)
    mensagem = conferir_mensagem_de_erro(execucao, ["cfg.txt", "3", "abc"])
    assert mensagem == ERRO.strip()


@pytest.mark.parametrize(
    ("saida_erro", "itens"),
    [
        ("", []),
        ("cfg.txt not found\n", ["cfg.txt"]),
        (ERRO + "Error: outra linha\n", ["cfg.txt"]),
        (ERRO, ["3", "cfg.txt"]),
        (ERRO, ["WIDTH"]),
    ],
    ids=["vazia", "sem prefixo", "duas linhas", "fora de ordem", "ausente"],
)
def test_mensagem_de_erro_invalida(saida_erro: str, itens: list[str]) -> None:
    """Sem a linha única, sem o prefixo ou sem um item, o passo falha.

    Args:
        saida_erro: Texto do stderr.
        itens: Textos que a mensagem deveria citar, na ordem.
    """
    execucao = Execucao("comando", 1, "", saida_erro)
    with pytest.raises(pytest.fail.Exception):
        conferir_mensagem_de_erro(execucao, itens)


def test_motivo_aceita_a_palavra_chave_em_qualquer_caixa() -> None:
    """A palavra-chave do motivo é procurada sem diferenciar maiúsculas."""
    conferir_motivo("Error: cfg.txt NOT FOUND", "arquivo não encontrado")
    conferir_motivo('Error: ENTRY is in the "42"', "coordenada no padrão 42")


@pytest.mark.parametrize(
    ("mensagem", "motivo"),
    [
        ("Error: cfg.txt is unreadable", "arquivo não encontrado"),
        ("Error: cfg.txt not found", "motivo que não existe"),
    ],
    ids=["sem a palavra-chave", "motivo desconhecido"],
)
def test_motivo_invalido(mensagem: str, motivo: str) -> None:
    """Mensagem sem a palavra-chave ou motivo fora da lista falham.

    Args:
        mensagem: Linha da mensagem de erro.
        motivo: Motivo pedido pelo passo.
    """
    with pytest.raises(pytest.fail.Exception):
        conferir_motivo(mensagem, motivo)


def test_eu_executo_grava_o_config_e_roda_cada_comando(
    cenario: Estado,
) -> None:
    """O config vai para o disco antes do primeiro comando.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(["WIDTH=20"])
    eu_executo(cenario, ["cat cfg.txt", "echo fim"])
    assert [execucao.saida_padrao for execucao in cenario.resultados] == [
        "WIDTH=20\n",
        "fim\n",
    ]


def test_eu_executo_com_entrada_termina_cada_linha(cenario: Estado) -> None:
    """Cada linha da entrada chega ao stdin terminada em quebra de linha.

    Args:
        cenario: Estado numa pasta temporária.
    """
    eu_executo_com_entrada(cenario, ["cat"], ["1", "4"])
    assert cenario.resultado.saida_padrao == "1\n4\n"


def test_codigo_de_saida(cenario: Estado) -> None:
    """O passo compara o código da última execução.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, codigo=1)
    codigo_de_saida(cenario, 1)
    with pytest.raises(AssertionError, match="terminou com código 1"):
        codigo_de_saida(cenario, 0)


def test_comando_termina_com(cenario: Estado) -> None:
    """O passo roda o comando na hora e compara o código.

    Args:
        cenario: Estado numa pasta temporária.
    """
    comando_termina_com(cenario, "exit 7", 7)
    with pytest.raises(AssertionError, match="terminou com código 7"):
        comando_termina_com(cenario, "exit 7", 0)


def test_saida_contem_e_nao_contem(cenario: Estado) -> None:
    """O verbo "contém" exige todos os textos; "não contém" proíbe todos.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, saida_padrao="um dois", saida_erro="tres")
    saida_contem(cenario, "a saída", "contém", ["um", "tres"])
    saida_contem(cenario, "a saída padrão", "não contém", ["tres", "x"])
    with pytest.raises(AssertionError):
        saida_contem(cenario, "a saída padrão", "contém", ["um", "tres"])
    with pytest.raises(AssertionError):
        saida_contem(cenario, "a saída de erro", "não contém", ["x", "tres"])


def test_saida_igual_ignora_espacos_nas_pontas(cenario: Estado) -> None:
    """A comparação do fluxo inteiro descarta espaços e quebras nas pontas.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, saida_padrao="  True\n")
    saida_igual(cenario, "a saída padrão", "True")
    with pytest.raises(AssertionError):
        saida_igual(cenario, "a saída padrão", "False")


def test_saida_do_comando_reaproveita_a_execucao(cenario: Estado) -> None:
    """A saída vem da execução do cenário, sem rodar o comando de novo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.executar("echo um; echo dois >&2")
    saida_do_comando_igual(cenario, "echo um; echo dois >&2", "um\ndois")
    saida_do_comando_contem(cenario, "echo um; echo dois >&2", "dois")
    assert len(cenario.resultados) == 1
    with pytest.raises(AssertionError):
        saida_do_comando_contem(cenario, "echo tres", "quatro")
    assert len(cenario.resultados) == 2


def test_linha_da_saida_contem(cenario: Estado) -> None:
    """Toda linha com o primeiro texto precisa ter o segundo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, saida_padrao="a: 1\nb: 2\na: 1 de novo\n")
    linha_da_saida_contem(cenario, "a:", "1")
    with pytest.raises(AssertionError, match="nenhuma linha"):
        linha_da_saida_contem(cenario, "c:", "1")
    with pytest.raises(AssertionError, match="sem 'de novo'"):
        linha_da_saida_contem(cenario, "a:", "de novo")


def test_termina_no_tempo(cenario: Estado) -> None:
    """O passo falha quando a última execução estourou o tempo limite.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario)
    termina_no_tempo(cenario)
    com_resultado(cenario, estourou=True)
    with pytest.raises(pytest.fail.Exception, match="tempo limite"):
        termina_no_tempo(cenario)


def test_resultado_sucesso(cenario: Estado) -> None:
    """Sucesso é código 0, sem "Error:" e com o arquivo de saída gravado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    execucao = com_resultado(cenario)
    execucao.arquivo_saida = cenario.cwd / "maze.txt"
    execucao.arquivo_saida.write_text("9\n", encoding="utf-8")
    resultado_da_execucao(cenario, "sucesso")


@pytest.mark.parametrize(
    ("codigo", "saida_erro", "estourou", "arquivo"),
    [
        (1, "", False, "9\n"),
        (0, "Error: aviso\n", False, "9\n"),
        (0, "", True, "9\n"),
        (0, "", False, ""),
        (0, "", False, None),
    ],
    ids=["código 1", "Error:", "tempo limite", "arquivo vazio", "sem arquivo"],
)
def test_resultado_que_nao_e_sucesso(
    cenario: Estado,
    codigo: int,
    saida_erro: str,
    estourou: bool,
    arquivo: str | None,
) -> None:
    """Cada condição do sucesso, quando falta, derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        codigo: Código de saída da execução.
        saida_erro: Texto do stderr.
        estourou: Se o comando passou do tempo limite.
        arquivo: Conteúdo do arquivo de saída; None quando não foi gravado.
    """
    execucao = com_resultado(cenario, codigo, "", saida_erro, estourou)
    execucao.arquivo_saida = cenario.cwd / "maze.txt"
    if arquivo is not None:
        execucao.arquivo_saida.write_text(arquivo, encoding="utf-8")
    with pytest.raises(pytest.fail.Exception):
        resultado_da_execucao(cenario, "sucesso")


def test_resultado_sucesso_exige_config_com_output_file(
    cenario: Estado,
) -> None:
    """Comando que não passa um config com OUTPUT_FILE não é sucesso.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario)
    with pytest.raises(pytest.fail.Exception, match="OUTPUT_FILE"):
        resultado_da_execucao(cenario, "sucesso")


def test_resultado_erro_citando(cenario: Estado) -> None:
    """O erro exige código 1, a mensagem com os itens e o motivo pedido.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, 1, "", "Error: cfg.txt not found\n")
    resultado_da_execucao(cenario, "erro citando cfg.txt")
    resultado_da_execucao(
        cenario, "erro citando cfg.txt; motivo: arquivo não encontrado"
    )
    with pytest.raises(pytest.fail.Exception):
        resultado_da_execucao(cenario, "erro citando WIDTH")
    with pytest.raises(pytest.fail.Exception):
        resultado_da_execucao(
            cenario, "erro citando cfg.txt; motivo: arquivo não é UTF-8"
        )


@pytest.mark.parametrize(
    ("codigo", "resultado"),
    [(2, "erro citando cfg.txt"), (0, "erro citando cfg.txt"), (1, "falha")],
    ids=["código 2", "código 0", "formato desconhecido"],
)
def test_resultado_erro_invalido(
    cenario: Estado, codigo: int, resultado: str
) -> None:
    """Código diferente de 1 ou resultado fora do formato derrubam o passo.

    Args:
        cenario: Estado numa pasta temporária.
        codigo: Código de saída da execução.
        resultado: Resultado pedido pelo passo.
    """
    com_resultado(cenario, codigo, "", "Error: cfg.txt not found\n")
    with pytest.raises(pytest.fail.Exception):
        resultado_da_execucao(cenario, resultado)
