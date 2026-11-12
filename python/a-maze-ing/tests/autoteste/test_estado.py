"""Testes do estado do cenário: comandos, proteção de caminhos e config."""

import os
import signal
import time
from pathlib import Path

import pytest

from suporte.config import Config
from suporte.estado import Estado, Execucao


def processo_morreu(pid: int) -> bool:
    """Espera até 5 segundos o processo deixar de existir.

    Args:
        pid: Identificador do processo.

    Returns:
        True se o processo sumiu dentro do prazo.
    """
    limite = time.monotonic() + 5
    while time.monotonic() < limite:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        time.sleep(0.05)
    return False


def test_executar_guarda_codigo_e_fluxos(cenario: Estado) -> None:
    """Código de saída, stdout e stderr ficam separados na execução.

    Args:
        cenario: Estado numa pasta temporária.
    """
    execucao = cenario.executar("printf fora; printf erro >&2; exit 3")
    assert execucao == Execucao(
        "printf fora; printf erro >&2; exit 3", 3, "fora", "erro"
    )
    assert execucao.fluxo("a saída padrão") == "fora"
    assert execucao.fluxo("a saída de erro") == "erro"
    assert execucao.fluxo("a saída") == "foraerro"
    assert cenario.resultado is execucao


def test_executar_envia_a_entrada_e_roda_na_pasta(cenario: Estado) -> None:
    """O stdin recebe a entrada e o comando roda no cwd do cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    (cenario.cwd / "aqui.txt").write_text("", encoding="utf-8")
    assert cenario.executar("cat", "linha\n").saida_padrao == "linha\n"
    assert cenario.executar("ls").saida_padrao == "aqui.txt\n"


def test_executar_poe_os_caminhos_extras_no_path(cenario: Estado) -> None:
    """Os caminhos extras vêm antes do PATH de quem roda a suíte.

    Args:
        cenario: Estado numa pasta temporária.
    """
    binarios = cenario.cwd / "bin"
    binarios.mkdir()
    programa = binarios / "ls"
    programa.write_text("#!/bin/sh\necho falso\n", encoding="utf-8")
    programa.chmod(0o755)
    cenario.caminhos_extras = [binarios]
    assert cenario.executar("ls").saida_padrao == "falso\n"


def test_tempo_limite_mata_o_grupo_do_comando(
    cenario: Estado, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No estouro, o processo iniciado pelo shell também morre.

    Args:
        cenario: Estado numa pasta temporária.
        monkeypatch: Troca o tempo limite por meio segundo.
    """
    monkeypatch.setattr("suporte.estado.TIMEOUT", 0.5)
    execucao = cenario.executar("sleep 30 & echo $!; wait")
    assert execucao.estourou
    assert processo_morreu(int(execucao.saida_padrao))


def test_tempo_limite_com_neto_segurando_a_saida(
    cenario: Estado, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Neto noutra sessão com o stdout aberto não prende a execução.

    O grupo do shell já acabou quando o tempo estoura; a execução termina
    perto de TIMEOUT + FECHAMENTO, com a saída lida até ali.

    Args:
        cenario: Estado numa pasta temporária.
        monkeypatch: Troca os dois prazos por meio segundo.
    """
    monkeypatch.setattr("suporte.estado.TIMEOUT", 0.5)
    monkeypatch.setattr("suporte.estado.FECHAMENTO", 0.5)
    comando = (
        "python3 -c 'import subprocess; print(subprocess.Popen("
        "[\"sleep\", \"30\"], start_new_session=True).pid)'"
    )
    inicio = time.monotonic()
    execucao = cenario.executar(comando)
    duracao = time.monotonic() - inicio
    os.kill(int(execucao.saida_padrao), signal.SIGKILL)
    assert execucao.estourou
    assert duracao < 3


def test_resultado_sem_execucao_falha(cenario: Estado) -> None:
    """Pedir o último resultado antes de rodar um comando é erro do cenário.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhum comando"):
        cenario.resultado


def test_resultado_de_reaproveita_ou_roda(cenario: Estado) -> None:
    """O comando já executado não roda de novo; o inédito roda na hora.

    Args:
        cenario: Estado numa pasta temporária.
    """
    primeira = cenario.executar("echo a")
    cenario.executar("echo b")
    assert cenario.resultado_de("echo a") is primeira
    assert cenario.resultado_de("echo c").saida_padrao == "c\n"
    assert len(cenario.resultados) == 3


def test_proteger_devolve_o_original(cenario: Estado) -> None:
    """O arquivo que existia volta com o conteúdo de antes.

    Args:
        cenario: Estado numa pasta temporária.
    """
    alvo = cenario.cwd / "maze.txt"
    alvo.write_text("original", encoding="utf-8")
    cenario.proteger(alvo)
    assert not alvo.exists()
    alvo.write_text("do teste", encoding="utf-8")
    cenario.restaurar()
    assert alvo.read_text(encoding="utf-8") == "original"


def test_proteger_apaga_o_que_o_teste_criou(cenario: Estado) -> None:
    """Arquivo, pasta e arquivo sem permissão criados pelo teste somem.

    Args:
        cenario: Estado numa pasta temporária.
    """
    arquivo = cenario.cwd / "novo.txt"
    pasta = cenario.cwd / "pasta"
    trancado = cenario.cwd / "trancado.txt"
    for caminho in (arquivo, pasta, trancado):
        cenario.proteger(caminho)
    arquivo.write_text("x", encoding="utf-8")
    (pasta / "dentro").mkdir(parents=True)
    trancado.write_text("x", encoding="utf-8")
    trancado.chmod(0)
    cenario.restaurar()
    assert list(cenario.cwd.iterdir()) == []


def test_restaurar_duas_vezes_nao_apaga_o_original(cenario: Estado) -> None:
    """A segunda chamada não tem mais nada a desfazer.

    Args:
        cenario: Estado numa pasta temporária.
    """
    alvo = cenario.cwd / "maze.txt"
    alvo.write_text("original", encoding="utf-8")
    cenario.proteger(alvo)
    cenario.restaurar()
    cenario.restaurar()
    assert alvo.read_text(encoding="utf-8") == "original"


def test_reservado_e_criar_pastas(cenario: Estado) -> None:
    """Só a pasta mais alta criada é registrada, e ela some no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    fundo = cenario.cwd / "a" / "b" / "c"
    cenario.criar_pastas(fundo)
    assert fundo.is_dir()
    assert cenario.preparados == [(cenario.cwd / "a", None)]
    assert cenario.reservado(cenario.cwd / "a")
    assert not cenario.reservado(fundo)
    cenario.criar_pastas(fundo)
    assert len(cenario.preparados) == 1
    cenario.restaurar()
    assert list(cenario.cwd.iterdir()) == []


def test_proteger_sem_reserva_falha(tmp_path: Path) -> None:
    """Estado criado sem pasta de reserva não pode proteger caminhos.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    with pytest.raises(pytest.fail.Exception, match="reserva"):
        Estado(cwd=tmp_path).proteger(tmp_path / "x")


def test_gravar_config_escreve_as_linhas(cenario: Estado) -> None:
    """O config vai para o destino, uma linha por par, e some no fim.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.config = Config(["WIDTH=20", "HEIGHT=15"], "sub/cfg.txt")
    cenario.gravar_config()
    destino = cenario.cwd / "sub" / "cfg.txt"
    assert destino.read_text(encoding="utf-8") == "WIDTH=20\nHEIGHT=15\n"
    cenario.restaurar()
    assert list(cenario.cwd.iterdir()) == []


def test_gravar_config_respeita_destino_preparado(cenario: Estado) -> None:
    """Sem config, ou com o destino preparado à mão, nada é gravado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cenario.gravar_config()
    cenario.config = Config(["WIDTH=20"])
    cenario.sem_gravacao.add(cenario.cwd / "cfg.txt")
    cenario.gravar_config()
    assert list(cenario.cwd.iterdir()) == []


def test_executar_protege_o_arquivo_de_saida(cenario: Estado) -> None:
    """O OUTPUT_FILE do config sai do caminho antes do programa rodar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    saida = cenario.cwd / "maze.txt"
    saida.write_text("antigo", encoding="utf-8")
    (cenario.cwd / "cfg.txt").write_text(
        "OUTPUT_FILE=maze.txt\n", encoding="utf-8"
    )
    (cenario.cwd / "a_maze_ing.py").write_text(
        'import os\nprint(os.path.exists("maze.txt"))\n', encoding="utf-8"
    )
    execucao = cenario.executar("python3 a_maze_ing.py cfg.txt")
    assert execucao.saida_padrao == "False\n"
    assert execucao.arquivo_saida == saida
    cenario.restaurar()
    assert saida.read_text(encoding="utf-8") == "antigo"
