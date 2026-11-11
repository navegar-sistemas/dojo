"""Passos que executam comandos e conferem a saída."""

from pytest_bdd import parsers, then, when

from conftest import TIPOS, Estado


@when(parsers.parse("eu executo {comandos:L}", extra_types=TIPOS))
def eu_executo(estado: Estado, comandos: list[str]) -> None:
    """V29: roda cada comando, com stdin vazio, e guarda os resultados.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
    """
    for comando in comandos:
        estado.executar(comando)


@then(
    parsers.parse(
        "{fluxo:Fluxo} {verbo:Contem} {textos:L}", extra_types=TIPOS
    )
)
def saida_contem(
    estado: Estado, fluxo: str, verbo: str, textos: list[str]
) -> None:
    """V52: confere se o fluxo contém (ou não) cada texto.

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
    """V48: confere o código de saída do último comando.

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
    """V50: roda o comando agora e confere o código de saída.

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
    """V55: roda o comando agora e compara a saída, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando.
        texto: Saída esperada (stdout e stderr juntos).
    """
    saida = estado.executar(comando).fluxo("a saída").strip()
    assert saida == texto, f"'{comando}' mostrou {saida!r}, esperado {texto!r}"


@then(parsers.parse('{fluxo:Fluxo} é "{texto:Q}"', extra_types=TIPOS))
def saida_igual(estado: Estado, fluxo: str, texto: str) -> None:
    """V53: confere o fluxo inteiro, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        fluxo: "a saída", "a saída padrão" ou "a saída de erro".
        texto: Texto esperado.
    """
    saida = estado.resultado.fluxo(fluxo).strip()
    assert saida == texto, f"{fluxo} é {saida!r}, esperado {texto!r}"
