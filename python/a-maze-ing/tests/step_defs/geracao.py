"""Passos que geram labirintos pelo programa ou pelo módulo mazegen."""

import shlex
from typing import Any

import pytest
from pytest_bdd import given, parsers, when

from step_defs.repositorio import aplicar_pares, config_atual
from suporte.config import CONFIG_BASE, Config, chaves_das_linhas
from suporte.estado import Estado, Execucao
from suporte.modulo import (
    classe_geradora,
    labirinto_do_gerador,
    parametros_do_config,
)
from suporte.tipos import TIPOS

SAIR = "4\n"


def gerar_pelo_programa(estado: Estado) -> Execucao:
    """Grava o config e roda o programa com a opção de sair no stdin.

    Args:
        estado: Estado do cenário, com o config carregado.

    Returns:
        A execução; com código 0, o labirinto entra em ``labirintos``.
    """
    config = config_atual(estado)
    estado.gravar_config()
    comando = f"python3 a_maze_ing.py {shlex.quote(config.destino)}"
    return estado.executar(comando, SAIR)


def gerar_pelo_modulo(estado: Estado) -> Execucao:
    """Gera com MazeGenerator usando os valores do config atual.

    Args:
        estado: Estado do cenário, com o config carregado.

    Returns:
        Uma execução sem processo, com o labirinto da classe.
    """
    chaves = chaves_das_linhas(config_atual(estado).linhas)
    try:
        parametros = parametros_do_config(chaves)
    except (KeyError, ValueError) as erro:
        pytest.fail(f"o config não serve à classe geradora: {erro!r}")
    gerador: Any = classe_geradora()(**parametros)
    gerador.generate()
    estado.gerador = gerador
    entrada = parametros["entry"]
    saida = parametros["exit"]
    assert isinstance(entrada, tuple) and isinstance(saida, tuple)
    labirinto = labirinto_do_gerador(gerador, entrada, saida)
    execucao = Execucao(
        f"MazeGenerator(**{parametros!r})", 0, "", "", labirinto=labirinto
    )
    estado.labirintos.append(labirinto)
    return execucao


def gerar_com_sucesso(estado: Estado, gerador: str) -> None:
    """Gera pelo programa ou pelo módulo e exige um labirinto.

    Args:
        estado: Estado do cenário, com o config carregado.
        gerador: "programa" ou "módulo mazegen".
    """
    if gerador == "módulo mazegen":
        gerar_pelo_modulo(estado)
        return
    execucao = gerar_pelo_programa(estado)
    if execucao.codigo != 0 or execucao.labirinto is None:
        pytest.fail(
            f"'{execucao.comando}' não gerou um labirinto (código "
            f"{execucao.codigo}):\n{execucao.saida_erro}"
        )


def repetir(estado: Estado, configs: list[Config]) -> None:
    """Gera uma vez por config e troca a lista de execuções.

    O config do cenário volta a ser o original no fim.

    Args:
        estado: Estado do cenário.
        configs: Um config por geração.
    """
    original = config_atual(estado)
    execucoes: list[Execucao] = []
    try:
        for config in configs:
            estado.config = config
            execucoes.append(gerar_pelo_programa(estado))
    finally:
        estado.config = original
    estado.execucoes = execucoes


def copia(config: Config) -> Config:
    """Cópia independente do config, com o mesmo destino e variação.

    Args:
        config: Config de origem.

    Returns:
        A cópia.
    """
    return Config(list(config.linhas), config.destino, config.variacao)


@given(
    parsers.parse(
        "um labirinto gerado pelo {gerador:Gerador} com o config base",
        extra_types=TIPOS,
    )
)
def labirinto_gerado(estado: Estado, gerador: str) -> None:
    """Carrega o config base e gera um labirinto.

    Args:
        estado: Estado do cenário.
        gerador: "programa" ou "módulo mazegen".
    """
    estado.config = Config(list(CONFIG_BASE))
    gerar_com_sucesso(estado, gerador)


@given(
    parsers.parse(
        "um labirinto gerado pelo {gerador:Gerador} com o config base mais "
        "{pares:L}",
        extra_types=TIPOS,
    )
)
def labirinto_gerado_com(
    estado: Estado, gerador: str, pares: list[str]
) -> None:
    """Carrega o config base com os pares e gera um labirinto.

    Args:
        estado: Estado do cenário.
        gerador: "programa" ou "módulo mazegen".
        pares: Itens CHAVE=valor.
    """
    estado.config = Config(list(CONFIG_BASE))
    aplicar_pares(estado.config, pares)
    gerar_com_sucesso(estado, gerador)


@when("eu gero o labirinto")
def eu_gero(estado: Estado) -> None:
    """Roda o programa com o config atual e a opção de sair.

    Args:
        estado: Estado do cenário.
    """
    gerar_pelo_programa(estado)


@when(parsers.parse("eu gero o labirinto {n:d} vezes"))
def eu_gero_vezes(estado: Estado, n: int) -> None:
    """Roda o programa n vezes com o mesmo config.

    Args:
        estado: Estado do cenário.
        n: Número de gerações.
    """
    config = config_atual(estado)
    repetir(estado, [copia(config) for _ in range(n)])


@when(
    parsers.parse(
        "eu gero o labirinto com cada um de {pares:L}", extra_types=TIPOS
    )
)
def eu_gero_com_cada(estado: Estado, pares: list[str]) -> None:
    """Uma geração por par, cada uma sobre uma cópia do config.

    Args:
        estado: Estado do cenário.
        pares: Itens CHAVE=valor.
    """
    configs: list[Config] = []
    for par in pares:
        config = copia(config_atual(estado))
        aplicar_pares(config, [par])
        configs.append(config)
    repetir(estado, configs)


@when(
    parsers.parse("eu gero o labirinto com cada seed de {inicio:d} a {fim:d}")
)
def eu_gero_com_cada_seed(estado: Estado, inicio: int, fim: int) -> None:
    """Uma geração por seed, de inicio a fim.

    Args:
        estado: Estado do cenário.
        inicio: Primeira seed.
        fim: Última seed, inclusive.
    """
    configs: list[Config] = []
    for seed in range(inicio, fim + 1):
        config = copia(config_atual(estado))
        config.definir("SEED", str(seed))
        configs.append(config)
    repetir(estado, configs)
