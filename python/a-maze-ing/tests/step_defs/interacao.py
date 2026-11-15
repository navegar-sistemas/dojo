"""Passos da sessão interativa com o menu do programa."""

import time

import pytest
from pytest_bdd import given, parsers, then, when

from step_defs.renderizacao import tem_ciano
from suporte.estado import Estado
from suporte.sessao import ESPERA, PROMPT, Sessao
from suporte.tipos import TIPOS

EVENTOS = ("EOF", "SIGINT", "1 segundo sem entrada")
PROMPTS = (PROMPT,)
MOSTRAR_CAMINHO = "2"
SEM_ENTRADA = 1.0


def sessao_aberta(estado: Estado) -> Sessao:
    """Sessão que é a ação mais recente do cenário.

    Args:
        estado: Estado do cenário.

    Returns:
        A sessão aberta.
    """
    sessao = estado.em_sessao()
    if sessao is None:
        pytest.fail("nenhum programa foi aberto numa sessão antes deste passo")
    return sessao


def esperar(sessao: Sessao, depois_de: str) -> None:
    """Espera o prompt ou o fim; o prazo esgotado derruba o passo.

    Args:
        sessao: Sessão aberta.
        depois_de: Ação que precedeu a espera, para a mensagem.
    """
    if not sessao.esperar_prompt_ou_fim(ESPERA):
        pytest.fail(
            f"'{sessao.comando}' não mostrou o prompt {PROMPT!r} nem terminou "
            f"depois de {depois_de}; saída até aqui:\n{sessao.saida_padrao}"
            f"{sessao.saida_erro}"
        )


def enviar_linhas(sessao: Sessao, linhas: list[str]) -> None:
    """Envia cada linha ao menu e espera o prompt ou o fim.

    Args:
        sessao: Sessão aberta.
        linhas: Linhas enviadas, na ordem.
    """
    for linha in linhas:
        if not sessao.enviar(linha):
            pytest.fail(
                f"'{sessao.comando}' terminou com código "
                f"{sessao.processo.poll()} antes de receber {linha!r}:\n"
                f"{sessao.saida_erro}"
            )
        esperar(sessao, f"receber {linha!r}")


@given(
    parsers.parse('o programa iniciado com "{comando:Q}"', extra_types=TIPOS)
)
def programa_iniciado(estado: Estado, comando: str) -> None:
    """Grava o config, abre o programa e espera o primeiro prompt (I03).

    Args:
        estado: Estado do cenário.
        comando: Linha de comando.
    """
    estado.gravar_config()
    sessao = estado.abrir_sessao(comando)
    esperar(sessao, "abrir")
    if not sessao.viva():
        pytest.fail(
            f"'{comando}' terminou com código {sessao.processo.poll()} sem "
            f"esperar no menu:\n{sessao.saida_padrao}{sessao.saida_erro}"
        )


@given(
    parsers.parse(
        'o programa iniciado com "{comando:Q}", com o caminho {vis:Visib}',
        extra_types=TIPOS,
    )
)
def programa_iniciado_com_caminho(
    estado: Estado, comando: str, vis: str
) -> None:
    """Abre o programa e deixa o caminho visível ou confere que está oculto.

    ``visível`` envia a opção 2 e confere que o ciano apareceu; ``oculto``
    confere que a renderização não tem ciano.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando.
        vis: "visível" ou "oculto".
    """
    programa_iniciado(estado, comando)
    if vis == "visível":
        enviar_linhas(sessao_aberta(estado), [MOSTRAR_CAMINHO])
        if not tem_ciano(estado):
            pytest.fail(
                f"depois da opção {MOSTRAR_CAMINHO}, a última renderização "
                f"não tem nenhuma posição ciano"
            )
    elif tem_ciano(estado):
        pytest.fail("o caminho deveria começar oculto, mas há ciano (I03)")


@when(parsers.parse("eu envio ao menu {linhas:L}", extra_types=TIPOS))
def envio_ao_menu(estado: Estado, linhas: list[str]) -> None:
    """Escreve cada linha no stdin e espera o prompt ou o fim.

    Args:
        estado: Estado do cenário.
        linhas: Linhas enviadas ao menu, na ordem.
    """
    enviar_linhas(sessao_aberta(estado), linhas)


@when(
    parsers.parse(
        'o evento "{evento:Q}" acontece no menu', extra_types=TIPOS
    )
)
def evento_no_menu(estado: Estado, evento: str) -> None:
    """Fecha o stdin, envia SIGINT ao grupo ou espera 1 segundo.

    Depois do EOF e do SIGINT, espera o prompt ou o fim, como um envio.

    Args:
        estado: Estado do cenário.
        evento: "EOF", "SIGINT" ou "1 segundo sem entrada".
    """
    if evento not in EVENTOS:
        pytest.fail(
            f'"{evento}" não existe; os válidos são: {", ".join(EVENTOS)}'
        )
    sessao = sessao_aberta(estado)
    if evento == "EOF":
        sessao.fechar_entrada()
    elif evento == "SIGINT":
        sessao.interromper()
    else:
        time.sleep(SEM_ENTRADA)
        return
    esperar(sessao, evento)


@then("o programa continua em execução")
def continua_em_execucao(estado: Estado) -> None:
    """O processo da sessão ainda roda.

    Args:
        estado: Estado do cenário.
    """
    sessao = sessao_aberta(estado)
    codigo = sessao.processo.poll()
    if codigo is not None:
        pytest.fail(
            f"'{sessao.comando}' terminou com código {codigo}:\n"
            f"{sessao.saida_erro}"
        )


@then(
    parsers.parse(
        'o programa aguarda no prompt "{prompt:Q}"', extra_types=TIPOS
    )
)
def aguarda_no_prompt(estado: Estado, prompt: str) -> None:
    """O processo roda e o prompt é a última coisa impressa em stdout.

    Args:
        estado: Estado do cenário.
        prompt: Prompt do menu (I03).
    """
    if prompt not in PROMPTS:
        pytest.fail(
            f'"{prompt}" não existe; os válidos são: {", ".join(PROMPTS)}'
        )
    continua_em_execucao(estado)
    saida = sessao_aberta(estado).saida_padrao
    if not saida.endswith(prompt):
        pytest.fail(
            f"a saída padrão não termina no prompt {prompt!r}: "
            f"{saida[-80:]!r}"
        )
