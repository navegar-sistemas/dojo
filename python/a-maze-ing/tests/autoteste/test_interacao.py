"""Testes dos passos da sessão interativa com o menu."""

import time

import pytest

from autoteste.desenho import TEXTO_DO_MENU, grade, saida
from autoteste.falso import programa_falso
from step_defs import interacao
from step_defs.interacao import (
    aguarda_no_prompt,
    continua_em_execucao,
    envio_ao_menu,
    evento_no_menu,
    programa_iniciado,
    programa_iniciado_com_caminho,
)
from suporte.config import Config
from suporte.estado import Estado
from suporte.sessao import PROMPT

OCULTO = saida(grade(caminho=False))
VISIVEL = saida(grade())
CURTO = 0.3


def iniciar(
    cenario: Estado, saidas: list[str], codigo: int | None = None
) -> str:
    """Grava o programa falso e devolve o comando, com o config de exemplo.

    Args:
        cenario: Estado numa pasta temporária.
        saidas: Texto inicial e o impresso depois de cada linha lida.
        codigo: Código de saída depois da última saída.

    Returns:
        O comando do programa falso.
    """
    cenario.config = Config(["WIDTH=3", "HEIGHT=2"])
    return programa_falso(cenario.cwd, saidas, codigo)


def test_programa_iniciado_espera_o_prompt(cenario: Estado) -> None:
    """O passo grava o config e só volta com o menu na tela.

    Args:
        cenario: Estado numa pasta temporária.
    """
    programa_iniciado(cenario, iniciar(cenario, [OCULTO]))
    assert cenario.sessao is not None
    assert cenario.sessao.saida_padrao.endswith(PROMPT)
    gravado = (cenario.cwd / "cfg.txt").read_text(encoding="utf-8")
    assert gravado == "WIDTH=3\nHEIGHT=2\n"


def test_programa_que_termina_antes_do_menu(cenario: Estado) -> None:
    """Terminar sem esperar no menu derruba o passo Dado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="código 2"):
        programa_iniciado(cenario, iniciar(cenario, ["erro\n"], codigo=2))


def test_programa_sem_prompt(
    cenario: Estado, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sem prompt dentro do prazo, o passo falha mostrando a saída.

    Args:
        cenario: Estado numa pasta temporária.
        monkeypatch: Encurta o prazo da espera.
    """
    monkeypatch.setattr(interacao, "ESPERA", CURTO)
    with pytest.raises(pytest.fail.Exception, match="não mostrou o prompt"):
        programa_iniciado(cenario, iniciar(cenario, ["sem menu\n"]))


@pytest.mark.parametrize(
    ("vis", "saidas"),
    [("oculto", [OCULTO]), ("visível", [OCULTO, VISIVEL])],
    ids=["oculto", "visível"],
)
def test_caminho_inicial(cenario: Estado, vis: str, saidas: list[str]) -> None:
    """Oculto confere a falta de ciano; visível envia 2 e vê o ciano.

    Args:
        cenario: Estado numa pasta temporária.
        vis: "oculto" ou "visível".
        saidas: Exibições do programa falso.
    """
    programa_iniciado_com_caminho(cenario, iniciar(cenario, saidas), vis)
    assert cenario.sessao is not None
    assert cenario.sessao.enviados == ([] if vis == "oculto" else ["2"])


@pytest.mark.parametrize(
    ("vis", "saidas", "mensagem"),
    [
        ("oculto", [VISIVEL], "começar oculto"),
        ("visível", [OCULTO, OCULTO], "nenhuma posição ciano"),
    ],
    ids=["oculto com ciano", "visível sem ciano"],
)
def test_caminho_inicial_errado(
    cenario: Estado, vis: str, saidas: list[str], mensagem: str
) -> None:
    """O estado do caminho que não bate com o pedido derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        vis: "oculto" ou "visível".
        saidas: Exibições do programa falso.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        programa_iniciado_com_caminho(cenario, iniciar(cenario, saidas), vis)


def test_envio_ao_menu(cenario: Estado) -> None:
    """Cada linha vai ao stdin e o passo espera o prompt seguinte.

    Args:
        cenario: Estado numa pasta temporária.
    """
    programa_iniciado(
        cenario, iniciar(cenario, [OCULTO, f"Invalid choice\n{PROMPT}", ""],
                         codigo=0)
    )
    envio_ao_menu(cenario, ["9", "4"])
    assert cenario.sessao is not None
    assert cenario.sessao.enviados == ["9", "4"]
    assert cenario.sessao.esperar_fim() == 0
    assert cenario.resultado.saida_padrao.endswith(
        f"{TEXTO_DO_MENU}Invalid choice\n{PROMPT}"
    )


def test_envio_a_programa_que_terminou(cenario: Estado) -> None:
    """Enviar depois do fim do programa derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    programa_iniciado(cenario, iniciar(cenario, [OCULTO, ""], codigo=0))
    with pytest.raises(pytest.fail.Exception, match="antes de receber '1'"):
        envio_ao_menu(cenario, ["4", "1"])


def test_envio_sem_sessao(cenario: Estado) -> None:
    """Sem sessão aberta não há a quem enviar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhum programa"):
        envio_ao_menu(cenario, ["1"])


@pytest.mark.parametrize("evento", ["EOF", "SIGINT"])
def test_eventos_que_encerram(cenario: Estado, evento: str) -> None:
    """EOF e SIGINT chegam ao programa, que termina.

    Args:
        cenario: Estado numa pasta temporária.
        evento: "EOF" ou "SIGINT".
    """
    programa_iniciado(cenario, iniciar(cenario, [OCULTO]))
    evento_no_menu(cenario, evento)
    assert cenario.sessao is not None
    assert cenario.sessao.esperar_fim() == 0
    with pytest.raises(pytest.fail.Exception, match="terminou com código 0"):
        continua_em_execucao(cenario)


def test_um_segundo_sem_entrada(cenario: Estado) -> None:
    """O evento espera 1 segundo e o programa segue no prompt.

    Args:
        cenario: Estado numa pasta temporária.
    """
    programa_iniciado(cenario, iniciar(cenario, [OCULTO]))
    inicio = time.monotonic()
    evento_no_menu(cenario, "1 segundo sem entrada")
    assert time.monotonic() - inicio >= 1
    continua_em_execucao(cenario)
    aguarda_no_prompt(cenario, PROMPT)


def test_evento_invalido(cenario: Estado) -> None:
    """Evento fora da lista fechada derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="os válidos são: EOF"):
        evento_no_menu(cenario, "Ctrl+D")


def test_prompt_invalido(cenario: Estado) -> None:
    """Prompt fora da lista fechada derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        aguarda_no_prompt(cenario, "> ")


def test_saida_depois_do_prompt(cenario: Estado) -> None:
    """Texto impresso depois do prompt mostra que ele não é o último.

    Args:
        cenario: Estado numa pasta temporária.
    """
    programa_iniciado(cenario, iniciar(cenario, [f"{OCULTO}depois"]))
    assert cenario.sessao is not None
    limite = time.monotonic() + 5
    while not cenario.sessao.saida_padrao.endswith("depois"):
        assert time.monotonic() < limite
        time.sleep(0.02)
    with pytest.raises(pytest.fail.Exception, match="não termina no prompt"):
        aguarda_no_prompt(cenario, PROMPT)
