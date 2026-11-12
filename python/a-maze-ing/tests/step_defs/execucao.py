"""Passos que executam comandos e conferem a saída."""

import re

import pytest
from pytest_bdd import parsers, then, when

from suporte.estado import Estado, Execucao
from suporte.tipos import TIPOS

# Palavra-chave que a mensagem de erro traz para cada motivo (I21).
MOTIVOS = {
    "arquivo não encontrado": "not found",
    "arquivo não é UTF-8": "UTF-8",
    "chave obrigatória ausente": "missing",
    "entrada igual à saída": "differ",
    "tamanho sem tabuleiro Pac-Man": "Pac-Man",
    "coordenada no padrão 42": '"42"',
}


def conferir_mensagem_de_erro(execucao: Execucao, itens: list[str]) -> str:
    """Confere a mensagem de erro da D01 e os itens citados, na ordem.

    Args:
        execucao: Execução que deveria terminar em erro.
        itens: Textos que a mensagem cita, na ordem.

    Returns:
        A linha da mensagem.
    """
    linhas = execucao.saida_erro.strip().splitlines()
    if len(linhas) != 1 or not linhas[0].startswith("Error: "):
        pytest.fail(
            "a saída de erro deveria ser uma única linha começando com "
            f"'Error: ', mas foi:\n{execucao.saida_erro!r}"
        )
    mensagem = linhas[0]
    inicio = 0
    for item in itens:
        posicao = mensagem.find(item, inicio)
        if posicao < 0:
            pytest.fail(
                f"a mensagem não cita {item!r} depois de "
                f"{mensagem[:inicio]!r}: {mensagem!r}"
            )
        inicio = posicao + len(item)
    return mensagem


def conferir_motivo(mensagem: str, motivo: str) -> None:
    """Confere a palavra-chave do motivo (I21), sem diferenciar caixa.

    Args:
        mensagem: Linha da mensagem de erro.
        motivo: Uma das chaves de MOTIVOS.
    """
    chave = MOTIVOS.get(motivo)
    if chave is None:
        pytest.fail(
            f'motivo "{motivo}" não existe; os válidos são: '
            f"{', '.join(MOTIVOS)}"
        )
    if not re.search(re.escape(chave), mensagem, re.IGNORECASE):
        pytest.fail(f"a mensagem não contém {chave!r}: {mensagem!r}")


@when(parsers.parse("eu executo {comandos:L}", extra_types=TIPOS))
def eu_executo(estado: Estado, comandos: list[str]) -> None:
    """Grava o config e roda cada comando, com stdin vazio.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
    """
    estado.gravar_config()
    for comando in comandos:
        estado.executar(comando)


@when(
    parsers.parse(
        "eu executo {comandos:L} com a entrada {linhas:L}", extra_types=TIPOS
    )
)
def eu_executo_com_entrada(
    estado: Estado, comandos: list[str], linhas: list[str]
) -> None:
    """Grava o config e roda cada comando com as linhas no stdin.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
        linhas: Linhas enviadas ao stdin, cada uma terminada em "\\n".
    """
    entrada = "".join(f"{linha}\n" for linha in linhas)
    estado.gravar_config()
    for comando in comandos:
        estado.executar(comando, entrada)


@then(
    parsers.parse(
        "{fluxo:Fluxo} {verbo:Contem} {textos:L}", extra_types=TIPOS
    )
)
def saida_contem(
    estado: Estado, fluxo: str, verbo: str, textos: list[str]
) -> None:
    """Confere se o fluxo contém (ou não) cada texto.

    Args:
        estado: Estado do cenário.
        fluxo: "a saída", "a saída padrão" ou "a saída de erro".
        verbo: "contém" ou "não contém".
        textos: Textos procurados.
    """
    saida = estado.resultado.fluxo(fluxo)
    for texto in textos:
        if verbo == "contém":
            assert texto in saida, f"{fluxo} não contém {texto!r}:\n{saida}"
        else:
            assert texto not in saida, f"{fluxo} contém {texto!r}:\n{saida}"


@then(parsers.parse("o código de saída é {codigo:d}"))
def codigo_de_saida(estado: Estado, codigo: int) -> None:
    """Confere o código de saída do último comando.

    Args:
        estado: Estado do cenário.
        codigo: Código esperado.
    """
    resultado = estado.resultado
    assert resultado.codigo == codigo, (
        f"'{resultado.comando}' terminou com código {resultado.codigo}, "
        f"esperado {codigo}\n{resultado.saida_padrao}{resultado.saida_erro}"
    )


@then(
    parsers.parse(
        'o comando "{comando:Q}" termina com código {codigo:d}',
        extra_types=TIPOS,
    )
)
def comando_termina_com(estado: Estado, comando: str, codigo: int) -> None:
    """Roda o comando agora e confere o código de saída.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando.
        codigo: Código esperado.
    """
    resultado = estado.executar(comando)
    assert resultado.codigo == codigo, (
        f"'{comando}' terminou com código {resultado.codigo}, esperado "
        f"{codigo}\n{resultado.saida_padrao}{resultado.saida_erro}"
    )


@then(
    parsers.parse(
        'a saída de "{comando:Q}" é "{texto:Q}"', extra_types=TIPOS
    )
)
def saida_do_comando_igual(estado: Estado, comando: str, texto: str) -> None:
    """Compara a saída do comando, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando; usa a execução do cenário ou roda agora.
        texto: Saída esperada (stdout e stderr juntos).
    """
    saida = estado.resultado_de(comando).fluxo("a saída").strip()
    assert saida == texto, f"'{comando}' mostrou {saida!r}, esperado {texto!r}"


@then(
    parsers.parse(
        'a saída de "{comando:Q}" contém "{texto:Q}"', extra_types=TIPOS
    )
)
def saida_do_comando_contem(estado: Estado, comando: str, texto: str) -> None:
    """Confere que a saída do comando contém o texto.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando; usa a execução do cenário ou roda agora.
        texto: Texto procurado (em stdout e stderr juntos).
    """
    saida = estado.resultado_de(comando).fluxo("a saída")
    assert texto in saida, f"'{comando}' não mostrou {texto!r}:\n{saida}"


@then(
    parsers.parse(
        'a linha da saída que contém "{a:Q}" também contém "{b:Q}"',
        extra_types=TIPOS,
    )
)
def linha_da_saida_contem(estado: Estado, a: str, b: str) -> None:
    """Toda linha da última saída que contém a também contém b.

    Args:
        estado: Estado do cenário.
        a: Texto que identifica a linha.
        b: Texto exigido nessa linha.
    """
    saida = estado.resultado.fluxo("a saída")
    linhas = [linha for linha in saida.splitlines() if a in linha]
    assert linhas, f"nenhuma linha da saída contém {a!r}:\n{saida}"
    sem_b = [linha for linha in linhas if b not in linha]
    assert not sem_b, f"linha com {a!r} sem {b!r}: {sem_b}"


@then(parsers.parse('{fluxo:Fluxo} é "{texto:Q}"', extra_types=TIPOS))
def saida_igual(estado: Estado, fluxo: str, texto: str) -> None:
    """Confere o fluxo inteiro, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        fluxo: "a saída", "a saída padrão" ou "a saída de erro".
        texto: Texto esperado.
    """
    saida = estado.resultado.fluxo(fluxo).strip()
    assert saida == texto, f"{fluxo} é {saida!r}, esperado {texto!r}"


@then("o processo termina dentro do tempo limite")
def termina_no_tempo(estado: Estado) -> None:
    """Confere que o último comando não estourou o tempo limite.

    Args:
        estado: Estado do cenário.
    """
    resultado = estado.resultado
    if resultado.estourou:
        pytest.fail(f"'{resultado.comando}' estourou o tempo limite")


@then(
    parsers.parse(
        'o resultado da execução é "{resultado:Q}"', extra_types=TIPOS
    )
)
def resultado_da_execucao(estado: Estado, resultado: str) -> None:
    """Confere "sucesso" ou "erro citando A, B[; motivo: M]".

    Sucesso exige código 0, nenhum "Error:" e o OUTPUT_FILE do config
    gravado com conteúdo; erro exige código 1 e a mensagem da D01.

    Args:
        estado: Estado do cenário.
        resultado: "sucesso" ou "erro citando A, B[; motivo: M]".
    """
    execucao = estado.resultado
    if execucao.estourou:
        pytest.fail(f"'{execucao.comando}' estourou o tempo limite")
    if resultado == "sucesso":
        if execucao.codigo != 0 or "Error:" in execucao.saida_erro:
            pytest.fail(
                f"esperado sucesso, mas terminou com código "
                f"{execucao.codigo}:\n{execucao.saida_erro}"
            )
        saida = execucao.arquivo_saida
        if saida is None:
            pytest.fail("o comando não passa um config com OUTPUT_FILE")
        if not saida.is_file() or saida.stat().st_size == 0:
            pytest.fail(f"o arquivo de saída {saida.name} não foi gravado")
        return
    prefixo = "erro citando "
    if not resultado.startswith(prefixo):
        pytest.fail(
            f'resultado "{resultado}" não é "sucesso" nem começa com '
            f'"{prefixo}"'
        )
    citados, _, motivo = resultado[len(prefixo):].partition("; motivo: ")
    if execucao.codigo != 1:
        pytest.fail(
            f"esperado erro com código 1, mas terminou com código "
            f"{execucao.codigo}:\n{execucao.saida_padrao}"
            f"{execucao.saida_erro}"
        )
    mensagem = conferir_mensagem_de_erro(execucao, citados.split(", "))
    if motivo:
        conferir_motivo(mensagem, motivo)
