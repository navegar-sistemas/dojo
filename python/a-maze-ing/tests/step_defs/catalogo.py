"""Passos do catálogo de casos de erro: carregar, executar e conferir."""

import builtins
import os
import re

import pytest
from pytest_bdd import given, then, when

from step_defs.execucao import conferir_mensagem_de_erro
from step_defs.repositorio import (
    DEPENDEM_DE_PERMISSAO,
    SITUACOES,
    aplicar_pares,
    config_de,
    config_atual,
    preparar,
)
from suporte.catalogo import CATALOGO, Caso
from suporte.estado import Estado, Execucao

# Nomes de exceção que vazam quando o programa imprime str() ou repr() de
# uma exceção: as embutidas e qualquer nome CamelCase terminado em Error ou
# Exception (como uma exceção própria do projeto). "Error:" sozinho, o
# prefixo da D01, não casa.
EXCECOES_EMBUTIDAS = sorted(
    nome for nome, valor in vars(builtins).items()
    if isinstance(valor, type) and issubclass(valor, BaseException)
)
NOME_DE_EXCECAO = re.compile(
    r"\b(?:" + "|".join(EXCECOES_EMBUTIDAS) + r"|[A-Z]\w*(?:Error|Exception))"
    r"\b"
)


def depende_de_permissao(caso: Caso) -> bool:
    """Diz se o caso só dá erro quando o chmod barra o acesso.

    Args:
        caso: Caso do catálogo.

    Returns:
        True quando o caso prepara um caminho sem permissão.
    """
    tipo = caso.preparado[1] if caso.preparado is not None else None
    return (
        tipo in DEPENDEM_DE_PERMISSAO
        or caso.situacao == "arquivo de configuração sem permissão de leitura"
    )


def montar(estado: Estado, caso: Caso) -> None:
    """Prepara no estado o config e os caminhos do caso.

    Args:
        estado: Estado próprio do caso.
        caso: Caso do catálogo.
    """
    if caso.config is not None:
        config_de(estado, caso.config)
        config = config_atual(estado)
        aplicar_pares(config, list(caso.pares))
        try:
            if caso.sem is not None:
                config.sem(caso.sem)
            if caso.linha is not None:
                config.trocar_linha(*caso.linha)
            if caso.linha_da_chave is not None:
                config.trocar_linha_da_chave(*caso.linha_da_chave)
        except ValueError as erro:
            pytest.fail(f"{caso.nome}: {erro}")
        if caso.situacao is not None:
            SITUACOES[caso.situacao](estado, config)
    if caso.preparado is not None:
        caminho, tipo = caso.preparado
        preparar(estado, estado.cwd / caminho, tipo)


def executar_caso(estado: Estado, caso: Caso, indice: int) -> Execucao:
    """Roda um caso num estado próprio e desfaz tudo o que ele criou.

    Cada caso tem seu estado: o que um caso prepara (config gravado,
    caminho trancado, gravação desligada) não vaza para o seguinte.

    Args:
        estado: Estado do cenário; dá a pasta, o PATH e a reserva.
        caso: Caso do catálogo.
        indice: Posição do caso, para a pasta de reserva própria.

    Returns:
        A execução do comando do caso.
    """
    if estado.reserva is None:
        pytest.fail("este estado não tem pasta de reserva")
    reserva = estado.reserva / f"caso-{indice}"
    reserva.mkdir()
    proprio = Estado(
        cwd=estado.cwd,
        caminhos_extras=list(estado.caminhos_extras),
        reserva=reserva,
    )
    try:
        montar(proprio, caso)
        proprio.gravar_config()
        return proprio.executar(caso.comando)
    finally:
        proprio.restaurar()


def casos_executados(estado: Estado) -> list[tuple[Caso, Execucao]]:
    """Pares (caso, execução) do catálogo já executado.

    Args:
        estado: Estado do cenário.

    Returns:
        Cada caso com a sua execução, na ordem do catálogo.
    """
    if not estado.catalogo:
        pytest.fail("o catálogo de casos de erro não foi carregado")
    if len(estado.execucoes) != len(estado.catalogo):
        pytest.fail(
            f"o catálogo tem {len(estado.catalogo)} casos e "
            f"{len(estado.execucoes)} execuções; os casos não foram "
            "executados"
        )
    return list(zip(estado.catalogo, estado.execucoes))


def relatar(problemas: list[str], propriedade: str) -> None:
    """Falha listando os casos que não cumprem a propriedade.

    Args:
        problemas: Uma descrição por caso com defeito.
        propriedade: Nome da propriedade, para a mensagem.
    """
    if problemas:
        pytest.fail(
            f'{len(problemas)} caso(s) sem "{propriedade}":\n'
            + "\n".join(problemas)
        )


def descrever(caso: Caso, execucao: Execucao) -> str:
    """Caso, comando e saídas, para a mensagem de falha.

    Args:
        caso: Caso do catálogo.
        execucao: Execução do caso.

    Returns:
        O texto que identifica o caso e mostra o que ele imprimiu.
    """
    return (
        f"- {caso.nome}: '{execucao.comando}' terminou com código "
        f"{execucao.codigo}\n  stdout: {execucao.saida_padrao!r}\n"
        f"  stderr: {execucao.saida_erro!r}"
    )


def sem_falha(caso: Caso, execucao: Execucao, cita: list[str]) -> str | None:
    """Confere a mensagem da D01 do caso, sem interromper o passo.

    Args:
        caso: Caso do catálogo.
        execucao: Execução do caso.
        cita: Itens que a mensagem cita, na ordem.

    Returns:
        A descrição do defeito, ou None quando a mensagem está certa.
    """
    try:
        conferir_mensagem_de_erro(execucao, cita)
    except pytest.fail.Exception as falha:
        return f"{descrever(caso, execucao)}\n  {falha}"
    return None


@given("os casos de erro do catálogo da suíte")
def casos_do_catalogo(estado: Estado) -> None:
    """Carrega o catálogo de casos de erro de suporte/catalogo.py.

    Como root, o chmod não barra a leitura nem a escrita: os casos que
    dependem dele ficam de fora, como os cenários de origem são pulados.

    Args:
        estado: Estado do cenário.
    """
    root = os.geteuid() == 0
    estado.catalogo = [
        caso for caso in CATALOGO
        if not (root and depende_de_permissao(caso))
    ]


@when("cada caso do catálogo é executado com tempo limite")
def cada_caso_executado(estado: Estado) -> None:
    """Roda cada caso do catálogo e troca a lista de execuções.

    Args:
        estado: Estado do cenário, com o catálogo carregado.
    """
    if not estado.catalogo:
        pytest.fail("o catálogo de casos de erro não foi carregado")
    estado.execucoes = [
        executar_caso(estado, caso, indice)
        for indice, caso in enumerate(estado.catalogo)
    ]


@then('o catálogo de casos de erro confirma "nenhum caso termina com '
      'Traceback"')
def nenhum_traceback(estado: Estado) -> None:
    """Nenhuma execução mostra Traceback em stdout ou stderr.

    Args:
        estado: Estado do cenário, com o catálogo executado.
    """
    relatar(
        [
            descrever(caso, execucao)
            for caso, execucao in casos_executados(estado)
            if "Traceback" in execucao.fluxo("a saída")
        ],
        "nenhum caso termina com Traceback",
    )


@then('o catálogo de casos de erro confirma "nenhum caso estoura o tempo '
      'limite"')
def nenhum_estouro(estado: Estado) -> None:
    """Nenhuma execução passa do tempo limite.

    Args:
        estado: Estado do cenário, com o catálogo executado.
    """
    relatar(
        [
            descrever(caso, execucao)
            for caso, execucao in casos_executados(estado)
            if execucao.estourou
        ],
        "nenhum caso estoura o tempo limite",
    )


@then('o catálogo de casos de erro confirma "mensagem começa com Error:"')
def mensagem_comeca_com_error(estado: Estado) -> None:
    """A saída de erro é uma única linha que começa com "Error: " (D01).

    O uso errado da linha de comando (I12) fica de fora.

    Args:
        estado: Estado do cenário, com o catálogo executado.
    """
    problemas = [
        sem_falha(caso, execucao, [])
        for caso, execucao in casos_executados(estado)
        if not caso.uso
    ]
    relatar(
        [problema for problema in problemas if problema is not None],
        "mensagem começa com Error:",
    )


@then('o catálogo de casos de erro confirma "mensagem cita o arquivo, a '
      'linha ou a chave"')
def mensagem_cita_a_causa(estado: Estado) -> None:
    """A mensagem cita, na ordem, o que o cenário de origem do caso pede.

    O uso errado da linha de comando (I12) fica de fora.

    Args:
        estado: Estado do cenário, com o catálogo executado.
    """
    problemas = [
        sem_falha(caso, execucao, list(caso.cita))
        for caso, execucao in casos_executados(estado)
        if not caso.uso
    ]
    relatar(
        [problema for problema in problemas if problema is not None],
        "mensagem cita o arquivo, a linha ou a chave",
    )


@then('o catálogo de casos de erro confirma "mensagem sem nome de exceção '
      'do Python"')
def mensagem_sem_excecao(estado: Estado) -> None:
    """A saída de erro não mostra nome de exceção do Python.

    O uso errado da linha de comando (I12) fica de fora.

    Args:
        estado: Estado do cenário, com o catálogo executado.
    """
    problemas: list[str] = []
    for caso, execucao in casos_executados(estado):
        achado = NOME_DE_EXCECAO.search(execucao.saida_erro)
        if not caso.uso and achado is not None:
            problemas.append(
                f"{descrever(caso, execucao)}\n  cita {achado.group(0)!r}"
            )
    relatar(problemas, "mensagem sem nome de exceção do Python")
