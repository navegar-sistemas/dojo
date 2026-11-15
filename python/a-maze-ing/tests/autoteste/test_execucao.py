"""Testes dos passos que executam comandos e conferem a saída."""

import pytest

from step_defs.execucao import (
    AVISO_DO_42,
    alvo_casa_com,
    codigo_de_saida,
    comando_termina_com,
    conferir_mensagem_de_erro,
    conferir_motivo,
    eu_executo,
    eu_executo_com_entrada,
    linha_da_saida_contem,
    resultado_da_execucao,
    resultados_comparados,
    saida_contem,
    saida_do_comando_contem,
    saida_do_comando_igual,
    saida_igual,
    termina_no_tempo,
)
from suporte.config import Config
from suporte.estado import Estado, Execucao
from suporte.labirinto import Labirinto, ler_saida

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


def test_resultado_sucesso_aceita_o_aviso_do_42(cenario: Estado) -> None:
    """O aviso do "42" omitido (D06, I10) não tira o sucesso.

    Args:
        cenario: Estado numa pasta temporária.
    """
    execucao = com_resultado(cenario, saida_erro=f"{AVISO_DO_42}\n")
    execucao.arquivo_saida = cenario.cwd / "maze.txt"
    execucao.arquivo_saida.write_text("9\n", encoding="utf-8")
    resultado_da_execucao(cenario, "sucesso")


@pytest.mark.parametrize(
    ("codigo", "saida_erro", "estourou", "arquivo"),
    [
        (1, "", False, "9\n"),
        (0, "Error: aviso\n", False, "9\n"),
        (0, f"{AVISO_DO_42}\nError: aviso\n", False, "9\n"),
        (0, f"{AVISO_DO_42} e mais\n", False, "9\n"),
        (0, "", True, "9\n"),
        (0, "", False, ""),
        (0, "", False, None),
    ],
    ids=[
        "código 1",
        "Error:",
        "aviso do 42 e outro Error:",
        "aviso do 42 alterado",
        "tempo limite",
        "arquivo vazio",
        "sem arquivo",
    ],
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


ARQUIVO = "d7\n\n0,0\n1,0\nE\n"
README = "*This project has been created by eu.*\r\n# A-Maze-ing\n"


def com_labirintos(cenario: Estado, *textos: str) -> Estado:
    """Põe no cenário labirintos lidos de arquivos de saída.

    Args:
        cenario: Estado numa pasta temporária.
        *textos: Conteúdo de cada arquivo de saída.

    Returns:
        O mesmo estado.
    """
    cenario.labirintos += [ler_saida(texto) for texto in textos]
    return cenario


@pytest.mark.parametrize(
    ("alvo", "regex"),
    [
        ("a solução", "^[NESW]+$"),
        ("cada linha da grade", "^[0-9a-f]{2}$"),
        ("cada linha de coordenadas do rodapé", r"^\d+,\d+$"),
        ("a linha 3 do rodapé", "^E$"),
    ],
    ids=["solução", "grade", "coordenadas", "linha 3"],
)
def test_alvo_do_labirinto_casa(
    cenario: Estado, alvo: str, regex: str
) -> None:
    """Os alvos de labirinto passam quando todo item casa.

    Args:
        cenario: Estado numa pasta temporária.
        alvo: Alvo da V67.
        regex: Expressão que todo item cumpre.
    """
    com_labirintos(cenario, ARQUIVO, "b7\n\n0,0\n1,0\nE\n")
    alvo_casa_com(cenario, alvo, regex)


@pytest.mark.parametrize(
    ("alvo", "texto", "regex"),
    [
        ("a solução", "d7\n\n0,0\n1,0\nX\n", "^[NESW]+$"),
        ("cada linha da grade", "D7\n\n0,0\n1,0\nE\n", "^[0-9a-f]+$"),
        ("cada linha da grade", ARQUIVO, "^[0-9a-f]{3}$"),
        (
            "cada linha de coordenadas do rodapé",
            "d7\n\n# entry (0,0)\n1,0\nE\n",
            r"^\d+,\d+$",
        ),
        ("a linha 3 do rodapé", "d7\n\n0,0\n1,0\nE \n", "^[NESW]+$"),
    ],
    ids=[
        "letra fora", "maiúscula", "largura", "anotação", "espaço no fim",
    ],
)
def test_alvo_do_labirinto_nao_casa(
    cenario: Estado, alvo: str, texto: str, regex: str
) -> None:
    """Um item que não casa, em qualquer labirinto do cenário, falha.

    Args:
        cenario: Estado numa pasta temporária.
        alvo: Alvo da V67.
        texto: Arquivo de saída do segundo labirinto.
        regex: Expressão pedida.
    """
    com_labirintos(cenario, ARQUIVO, texto)
    with pytest.raises(pytest.fail.Exception, match="não casa"):
        alvo_casa_com(cenario, alvo, regex)


def test_grade_do_labirinto_da_classe_em_hexadecimal(cenario: Estado) -> None:
    """Sem texto, a grade da classe é escrita em hexadecimal minúsculo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.labirintos.append(Labirinto([[13, 7], [10, 15]], None, None, ""))
    alvo_casa_com(cenario, "cada linha da grade", "^(d7|af)$")
    with pytest.raises(pytest.fail.Exception, match="'af'"):
        alvo_casa_com(cenario, "cada linha da grade", "^d7$")


@pytest.mark.parametrize(
    ("alvo", "mensagem"),
    [
        ("a solução", "nenhum labirinto"),
        ("cada linha de coordenadas do rodapé", "rodapé tem 1"),
        ("a linha 3 do rodapé", "rodapé tem 1"),
        ("a primeira linha do README", "README.md não existe"),
        ("o nome de cada arquivo selecionado", "nenhum arquivo"),
        ("a última linha da saída padrão", "nenhum comando"),
        ("a grade inteira", "não existe"),
    ],
    ids=[
        "sem labirinto", "rodapé curto", "sem linha 3", "sem README",
        "sem seleção", "sem execução", "alvo desconhecido",
    ],
)
def test_alvo_sem_itens(cenario: Estado, alvo: str, mensagem: str) -> None:
    """Alvo sem os itens que ele confere derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        alvo: Alvo pedido.
        mensagem: Trecho da mensagem de falha.
    """
    if alvo != "a solução":
        com_labirintos(cenario, "d7\n\n0,0\n")
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        alvo_casa_com(cenario, alvo, ".")


def test_solucao_ausente(cenario: Estado) -> None:
    """Labirinto sem a linha do caminho não tem solução a conferir.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_labirintos(cenario, "d7\n\n0,0\n1,0\n")
    with pytest.raises(pytest.fail.Exception, match="não tem solução"):
        alvo_casa_com(cenario, "a solução", ".")


def test_primeira_linha_do_readme_sem_converter_quebras(
    cenario: Estado,
) -> None:
    """A primeira linha mantém o \\r do CRLF, que o $ não aceita.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "README.md").write_bytes(README.encode("utf-8"))
    alvo_casa_com(cenario, "a primeira linha do README", r"^\*This")
    with pytest.raises(pytest.fail.Exception, match="não casa"):
        alvo_casa_com(cenario, "a primeira linha do README", r"\.\*$")


def test_nome_de_cada_arquivo_selecionado(cenario: Estado) -> None:
    """A expressão vale para o nome, sem a pasta, de cada arquivo lido.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.lido = [
        cenario.cwd / "mazegen-1.0.0-py3-none-any.whl",
        cenario.cwd / "mazegen-1.0.0.tar.gz",
    ]
    alvo_casa_com(
        cenario,
        "o nome de cada arquivo selecionado",
        r"^mazegen-.+(\.whl|\.tar\.gz)$",
    )
    with pytest.raises(pytest.fail.Exception, match="tar.gz"):
        alvo_casa_com(cenario, "o nome de cada arquivo selecionado", r"\.whl$")


def test_ultima_linha_da_saida_padrao(cenario: Estado) -> None:
    """Só a última linha do stdout é conferida.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_resultado(cenario, saida_padrao="1 2\nNESW\n", saida_erro="x\n")
    alvo_casa_com(cenario, "a última linha da saída padrão", "^[NESW]+$")
    with pytest.raises(pytest.fail.Exception, match="não casa"):
        alvo_casa_com(cenario, "a última linha da saída padrão", "^1")
    com_resultado(cenario, saida_padrao="")
    with pytest.raises(pytest.fail.Exception, match="não imprimiu"):
        alvo_casa_com(cenario, "a última linha da saída padrão", ".")


def test_expressao_invalida(cenario: Estado) -> None:
    """Uma expressão que não compila derruba o passo citando-a.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_labirintos(cenario, ARQUIVO)
    with pytest.raises(pytest.fail.Exception, match="inválida"):
        alvo_casa_com(cenario, "a solução", "^[NESW")


def execucao_de(texto: str, saida_padrao: str = "") -> Execucao:
    """Execução com código 0 e o labirinto do arquivo de saída.

    Args:
        texto: Conteúdo do OUTPUT_FILE.
        saida_padrao: O que a execução mostrou.

    Returns:
        A execução.
    """
    return Execucao(
        "python3 a_maze_ing.py cfg.txt", 0, saida_padrao, "", False, None,
        texto, ler_saida(texto),
    )


# Pares de labirintos que só diferem num aspecto: (aspecto, outro arquivo).
OUTROS = [
    ("arquivo de saída", "d7\n\n0,0\n1,0\nE\n\n"),
    ("grade", "b7\n\n0,0\n1,0\nE\n"),
    ("solução", "d7\n\n0,0\n1,0\nEW\n"),
    ("células de valor F", "df\n\n0,0\n1,0\nE\n"),
]


@pytest.mark.parametrize(
    ("aspecto", "outro"), OUTROS, ids=[aspecto for aspecto, _ in OUTROS]
)
def test_resultados_comparados(
    cenario: Estado, aspecto: str, outro: str
) -> None:
    """Iguais no aspecto são idênticos; um diferente quebra a igualdade.

    Args:
        cenario: Estado numa pasta temporária.
        aspecto: Aspecto da V71.
        outro: Arquivo de saída diferente do ARQUIVO nesse aspecto.
    """
    cenario.execucoes = [execucao_de(ARQUIVO), execucao_de(ARQUIVO)]
    resultados_comparados(cenario, "idênticos", aspecto)
    with pytest.raises(pytest.fail.Exception, match="1 e 2"):
        resultados_comparados(cenario, "diferentes entre si", aspecto)
    cenario.execucoes = [
        execucao_de(ARQUIVO), execucao_de(outro), execucao_de(ARQUIVO)
    ]
    with pytest.raises(pytest.fail.Exception, match="1 e 2, 2 e 3"):
        resultados_comparados(cenario, "idênticos", aspecto)
    with pytest.raises(pytest.fail.Exception, match="1 e 3"):
        resultados_comparados(cenario, "diferentes entre si", aspecto)
    cenario.execucoes = [execucao_de(ARQUIVO), execucao_de(outro)]
    resultados_comparados(cenario, "diferentes entre si", aspecto)


def test_saida_exibida_comparada(cenario: Estado) -> None:
    """A saída exibida é o stdout de cada execução.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.execucoes = [
        execucao_de(ARQUIVO, "um"), execucao_de("b7\n\n0,0\n1,0\nE\n", "um")
    ]
    resultados_comparados(cenario, "idênticos", "saída exibida")
    cenario.execucoes.append(execucao_de(ARQUIVO, "dois"))
    with pytest.raises(pytest.fail.Exception, match="diferem"):
        resultados_comparados(cenario, "idênticos", "saída exibida")


@pytest.mark.parametrize(
    ("execucoes", "relacao", "aspecto", "mensagem"),
    [
        ([], "idênticos", "grade", "pelo menos 2"),
        ([execucao_de(ARQUIVO)], "idênticos", "grade", "pelo menos 2"),
        (
            [Execucao("c", 1, "", "Error: x\n")] * 2,
            "idênticos",
            "grade",
            "não produziu labirinto",
        ),
        (
            [Execucao("c", 1, "", "Error: x\n")] * 2,
            "idênticos",
            "arquivo de saída",
            "não gravou",
        ),
        (
            [execucao_de("d7\n\n0,0\n1,0\n")] * 2,
            "idênticos",
            "solução",
            "não tem solução",
        ),
        ([execucao_de(ARQUIVO)] * 2, "idênticos", "cor", "não existe"),
        ([execucao_de(ARQUIVO)] * 2, "iguais", "grade", "não existe"),
    ],
    ids=[
        "nenhuma", "uma só", "sem labirinto", "sem arquivo", "sem solução",
        "aspecto desconhecido", "relação desconhecida",
    ],
)
def test_resultados_comparados_invalido(
    cenario: Estado,
    execucoes: list[Execucao],
    relacao: str,
    aspecto: str,
    mensagem: str,
) -> None:
    """Menos de 2 execuções, aspecto ausente ou valor fora da lista falham.

    Args:
        cenario: Estado numa pasta temporária.
        execucoes: Execuções do cenário.
        relacao: Relação pedida.
        aspecto: Aspecto pedido.
        mensagem: Trecho da mensagem de falha.
    """
    cenario.execucoes = execucoes
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        resultados_comparados(cenario, relacao, aspecto)
