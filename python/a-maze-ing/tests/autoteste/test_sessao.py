"""Testes da sessão interativa com o programa."""

import os
import shlex
import sys
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from autoteste.falso import programa_falso
from suporte.sessao import PROMPT, Sessao

CURTO = 0.3
Abrir = Callable[[str], Sessao]


@pytest.fixture
def abrir(tmp_path: Path) -> Iterator[Abrir]:
    """Abre sessões na pasta temporária e encerra todas no fim.

    Args:
        tmp_path: Pasta temporária do teste.

    Yields:
        A função que abre uma sessão com o comando dado.
    """
    abertas: list[Sessao] = []

    def nova(comando: str) -> Sessao:
        """Abre e registra uma sessão.

        Args:
            comando: Linha de comando.

        Returns:
            A sessão aberta.
        """
        sessao = Sessao(comando, tmp_path, dict(os.environ))
        abertas.append(sessao)
        return sessao

    yield nova
    for sessao in abertas:
        sessao.encerrar()


def test_espera_cada_prompt_novo(tmp_path: Path, abrir: Abrir) -> None:
    """Cada prompt conta uma vez; sem prompt novo o prazo acaba.

    Args:
        tmp_path: Pasta temporária do teste.
        abrir: Abre uma sessão.
    """
    sessao = abrir(programa_falso(tmp_path, [PROMPT, f"ok\n{PROMPT}"]))
    assert sessao.esperar_prompt_ou_fim()
    assert not sessao.esperar_prompt_ou_fim(CURTO)
    assert sessao.enviar("1")
    assert sessao.esperar_prompt_ou_fim()
    assert sessao.saida_padrao == f"{PROMPT}ok\n{PROMPT}"
    assert sessao.enviados == ["1"]
    assert sessao.viva()


def test_o_fim_do_processo_encerra_a_espera(
    tmp_path: Path, abrir: Abrir
) -> None:
    """Um processo que termina sem prompt não prende a espera.

    Args:
        tmp_path: Pasta temporária do teste.
        abrir: Abre uma sessão.
    """
    sessao = abrir(programa_falso(tmp_path, ["fim\n"], codigo=3, erro="e\n"))
    assert sessao.esperar_prompt_ou_fim()
    assert sessao.esperar_fim() == 3
    assert (sessao.saida_padrao, sessao.saida_erro) == ("fim\n", "e\n")
    assert not sessao.viva()
    assert not sessao.enviar("1")
    assert sessao.enviados == []


@pytest.mark.parametrize(
    "acao",
    [Sessao.fechar_entrada, Sessao.interromper],
    ids=["EOF", "SIGINT"],
)
def test_eof_e_sigint_terminam_o_programa(
    tmp_path: Path, abrir: Abrir, acao: Callable[[Sessao], None]
) -> None:
    """O EOF no stdin e o SIGINT no grupo chegam ao programa.

    Args:
        tmp_path: Pasta temporária do teste.
        abrir: Abre uma sessão.
        acao: Método que fecha o stdin ou envia o sinal.
    """
    sessao = abrir(programa_falso(tmp_path, [PROMPT]))
    assert sessao.esperar_prompt_ou_fim()
    acao(sessao)
    assert sessao.esperar_fim() == 0
    sessao.fechar_entrada()
    assert not sessao.enviar("1")


def test_esperar_fim_com_prazo(tmp_path: Path, abrir: Abrir) -> None:
    """Um processo que segue rodando estoura o prazo da espera do fim.

    Args:
        tmp_path: Pasta temporária do teste.
        abrir: Abre uma sessão.
    """
    sessao = abrir(programa_falso(tmp_path, [PROMPT]))
    assert sessao.esperar_fim(CURTO) is None
    assert sessao.viva()


def test_encerrar_mata_o_grupo_e_fecha_os_pipes(abrir: Abrir) -> None:
    """Encerrar mata o shell e o filho e pode ser chamado de novo.

    Args:
        abrir: Abre uma sessão.
    """
    filho = f"{shlex.quote(sys.executable)} -c 'import time; time.sleep(60)'"
    sessao = abrir(f"{filho} & {filho}; wait")
    sessao.encerrar()
    assert not sessao.viva()
    assert sessao.processo.stdout is not None
    assert sessao.processo.stdout.closed
    sessao.encerrar()
