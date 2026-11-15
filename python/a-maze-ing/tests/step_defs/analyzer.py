"""Passos que rodam o maze_analyzer.py e conferem o relatório dele."""

import shlex

import pytest
from pytest_bdd import parsers, then, when

from step_defs.geracao import gerar_pelo_programa
from step_defs.repositorio import config_atual
from suporte.analyzer import (
    analisar,
    analise_atual,
    arquivo_atual,
    primeiro_inteiro,
    valor_da_linha,
)
from suporte.config import chaves_das_linhas
from suporte.estado import Estado
from suporte.tipos import TIPOS

# Começo da linha "Verdict:" para cada valor de PERFECT (V85).
VEREDITOS = {"true": "PERFECT maze", "false": "Pac-Man-USABLE"}


@when("eu analiso o labirinto com o maze_analyzer")
def eu_analiso(estado: Estado) -> None:
    """Roda o maze_analyzer sobre o arquivo do labirinto atual.

    Args:
        estado: Estado do cenário.
    """
    analisar(estado, arquivo_atual(estado), [])


@when(
    parsers.parse(
        'eu analiso o labirinto com o maze_analyzer "{opcoes:Q}"',
        extra_types=TIPOS,
    )
)
def eu_analiso_com_opcoes(estado: Estado, opcoes: str) -> None:
    """Roda o maze_analyzer com as opções sobre o arquivo atual.

    Args:
        estado: Estado do cenário.
        opcoes: Opções como na linha de comando, ex.: "--max-dead-ends 0".
    """
    analisar(estado, arquivo_atual(estado), shlex.split(opcoes))


@when("eu gero o labirinto e o analiso com o maze_analyzer")
def eu_gero_e_analiso(estado: Estado) -> None:
    """Gera o labirinto pelo programa e o analisa com o maze_analyzer.

    Uma geração que não produz labirinto falha aqui: analisar o labirinto
    anterior do cenário conferiria o arquivo errado.

    Args:
        estado: Estado do cenário.
    """
    execucao = gerar_pelo_programa(estado)
    if execucao.labirinto is None:
        pytest.fail(
            f"'{execucao.comando}' não gerou um labirinto (código "
            f"{execucao.codigo}):\n{execucao.saida_padrao}"
            f"{execucao.saida_erro}"
        )
    eu_analiso(estado)


@then(
    parsers.parse(
        'a linha "{rotulo:Q}" do maze_analyzer {op:Op} {textos:L}',
        extra_types=TIPOS,
    )
)
def linha_do_analyzer(
    estado: Estado, rotulo: str, op: str, textos: list[str]
) -> None:
    """Confere o valor da linha do rótulo; roda o analyzer se ainda não rodou.

    "começa com" exige que o valor comece com cada texto; "contém" exige
    todos os textos no valor.

    Args:
        estado: Estado do cenário.
        rotulo: Começo da linha no relatório do analyzer.
        op: "começa com" ou "contém".
        textos: Textos procurados no valor.
    """
    valor = valor_da_linha(analise_atual(estado).saida_padrao, rotulo)
    if op == "começa com":
        faltam = [texto for texto in textos if not valor.startswith(texto)]
    elif op == "contém":
        faltam = [texto for texto in textos if texto not in valor]
    else:
        pytest.fail(f'"{op}" não existe; os válidos são: começa com, contém')
    if faltam:
        pytest.fail(
            f"a linha {rotulo!r} do maze_analyzer não {op} {faltam}: "
            f"{valor!r}"
        )


@then(
    parsers.parse(
        'o número na linha "{rotulo:Q}" do maze_analyzer é {cmp:Cmp} {n:d}',
        extra_types=TIPOS,
    )
)
def numero_do_analyzer(estado: Estado, rotulo: str, cmp: str, n: int) -> None:
    """Compara o primeiro inteiro da linha do rótulo com n.

    Args:
        estado: Estado do cenário.
        rotulo: Começo da linha no relatório do analyzer.
        cmp: "pelo menos" ou "no máximo".
        n: Limite.
    """
    valor = valor_da_linha(analise_atual(estado).saida_padrao, rotulo)
    numero = primeiro_inteiro(valor, rotulo)
    if cmp == "pelo menos":
        certo = numero >= n
    elif cmp == "no máximo":
        certo = numero <= n
    else:
        pytest.fail(
            f'"{cmp}" não existe; os válidos são: pelo menos, no máximo'
        )
    if not certo:
        pytest.fail(
            f"o número na linha {rotulo!r} do maze_analyzer é {numero}, "
            f"esperado {cmp} {n}: {valor!r}"
        )


@then("o veredito do maze_analyzer corresponde ao PERFECT do config")
def veredito_do_perfect(estado: Estado) -> None:
    """True pede "PERFECT maze" no Verdict:, False pede "Pac-Man-USABLE".

    Args:
        estado: Estado do cenário, com o config carregado.
    """
    perfeito = chaves_das_linhas(config_atual(estado).linhas).get("PERFECT")
    esperado = VEREDITOS.get((perfeito or "").lower())
    if esperado is None:
        pytest.fail(f"o config não tem PERFECT True ou False: {perfeito!r}")
    valor = valor_da_linha(analise_atual(estado).saida_padrao, "Verdict:")
    if not valor.startswith(esperado):
        pytest.fail(
            f"com PERFECT={perfeito}, o veredito deveria começar com "
            f"{esperado!r}: {valor!r}"
        )
