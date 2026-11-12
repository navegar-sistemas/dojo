"""Testes da conferência do python3 e do maze_analyzer."""

import re
from pathlib import Path

import pytest

from suporte.ambiente import (
    ANALYZER,
    caminho_do_analyzer,
    problema_da_versao,
    problema_do_python3,
)
from suporte.estado import TESTS_DIR


@pytest.mark.parametrize("versao", ["3.10", "3.14", "4.0"])
def test_versao_aceita(versao: str) -> None:
    """A partir do 3.10 não há problema a relatar.

    Args:
        versao: Versão no formato "maior.menor".
    """
    assert problema_da_versao("/usr/bin/python3", versao) is None


@pytest.mark.parametrize("versao", ["3.9", "2.7"])
def test_versao_recusada(versao: str) -> None:
    """Abaixo do 3.10 a mensagem cita a versão e o caminho encontrados.

    Args:
        versao: Versão no formato "maior.menor".
    """
    problema = problema_da_versao("/usr/bin/python3", versao)
    assert problema is not None
    assert f"{versao} (/usr/bin/python3)" in problema


def test_python3_ausente(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sem python3 no PATH a mensagem diz que ele falta.

    Args:
        monkeypatch: Esvazia o PATH durante o teste.
    """
    monkeypatch.setenv("PATH", "")
    problema = problema_do_python3()
    assert problema is not None
    assert "não há python3 no PATH" in problema


def test_python3_desta_rodada_serve() -> None:
    """A rodada só chega aqui com um python3 aceito pela guarda."""
    assert problema_do_python3() is None


def test_analyzer_fica_em_private() -> None:
    """O analyzer é procurado em a-maze-ing/private/, ao lado de tests/."""
    assert ANALYZER == TESTS_DIR.parent / "private" / "maze_analyzer.py"


def test_analyzer_ausente_diz_o_caminho(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sem o arquivo, o passo falha citando o caminho que falta.

    Args:
        tmp_path: Pasta temporária do teste.
        monkeypatch: Aponta o analyzer para um caminho vazio.
    """
    falta = tmp_path / "private" / "maze_analyzer.py"
    monkeypatch.setattr("suporte.ambiente.ANALYZER", falta)
    with pytest.raises(pytest.fail.Exception, match=re.escape(str(falta))):
        caminho_do_analyzer()


def test_analyzer_presente(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Com o arquivo no lugar, o caminho é devolvido.

    Args:
        tmp_path: Pasta temporária do teste.
        monkeypatch: Aponta o analyzer para o arquivo criado.
    """
    arquivo = tmp_path / "maze_analyzer.py"
    arquivo.write_text("", encoding="utf-8")
    monkeypatch.setattr("suporte.ambiente.ANALYZER", arquivo)
    assert caminho_do_analyzer() == arquivo
