"""Testes da conferência do python3 que os cenários usam."""

import pytest

from suporte.ambiente import problema_da_versao, problema_do_python3


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
