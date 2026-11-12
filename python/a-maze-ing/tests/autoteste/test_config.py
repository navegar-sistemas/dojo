"""Testes do config dos cenários e da leitura de arquivos de config."""

from pathlib import Path

import pytest

from suporte.config import CONFIG_BASE, Config, arquivo_de_saida, ler_chaves


def test_definir_troca_a_linha_da_chave() -> None:
    """A chave existente é trocada no lugar, sem diferenciar maiúsculas."""
    config = Config(list(CONFIG_BASE))
    config.definir("width", "9")
    assert config.linhas[0] == "width=9"
    assert len(config.linhas) == len(CONFIG_BASE)


def test_definir_acrescenta_chave_nova_no_fim() -> None:
    """Chave que não existe vira a última linha."""
    config = Config(list(CONFIG_BASE))
    config.definir("ALGORITHM", "prim")
    assert config.linhas == [*CONFIG_BASE, "ALGORITHM=prim"]


def test_definir_troca_so_a_primeira_ocorrencia() -> None:
    """Com a chave repetida, só a primeira linha muda."""
    config = Config(["WIDTH=1", "HEIGHT=2", "WIDTH=3"])
    config.definir("WIDTH", "9")
    assert config.linhas == ["WIDTH=9", "HEIGHT=2", "WIDTH=3"]


def test_sem_remove_todas_as_linhas_da_chave() -> None:
    """Todas as ocorrências saem, com ou sem espaços e em qualquer caixa."""
    config = Config(["WIDTH=1", "HEIGHT=2", " width = 3"])
    config.sem("WIDTH")
    assert config.linhas == ["HEIGHT=2"]


def test_sem_chave_ausente_nao_muda_nada() -> None:
    """Remover uma chave que não existe deixa o config igual."""
    config = Config(list(CONFIG_BASE))
    config.sem("ALGORITHM")
    assert config.linhas == CONFIG_BASE


def test_ler_chaves_segue_o_formato_do_config(tmp_path: Path) -> None:
    """BOM, comentários, linhas sem "=" e espaços são tratados.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = tmp_path / "cfg.txt"
    arquivo.write_bytes(
        b"\xef\xbb\xbf# comentario\n\nwidth = 20 \nsem igual\n"
        b"ENTRY=0,0\nOUTPUT_FILE=a=b.txt\n"
    )
    assert ler_chaves(arquivo) == {
        "WIDTH": "20",
        "ENTRY": "0,0",
        "OUTPUT_FILE": "a=b.txt",
    }


def test_ler_chaves_repetida_vale_a_ultima(tmp_path: Path) -> None:
    """Com a chave repetida, fica o valor da última linha.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    arquivo = tmp_path / "cfg.txt"
    arquivo.write_text("WIDTH=1\nWIDTH=2\n", encoding="utf-8")
    assert ler_chaves(arquivo) == {"WIDTH": "2"}


def test_ler_chaves_de_arquivo_ilegivel_e_vazio(tmp_path: Path) -> None:
    """Arquivo inexistente ou que não é UTF-8 não tem chaves.

    Args:
        tmp_path: Pasta temporária do teste.
    """
    binario = tmp_path / "binario.txt"
    binario.write_bytes(b"\xff\xfeWIDTH=20\n")
    assert ler_chaves(tmp_path / "inexistente.txt") == {}
    assert ler_chaves(binario) == {}


@pytest.mark.parametrize(
    "comando",
    [
        "python3 a_maze_ing.py cfg.txt",
        "python3 -X dev ./a_maze_ing.py cfg.txt",
        ".venv/bin/python a_maze_ing.py cfg.txt < /dev/null",
    ],
)
def test_arquivo_de_saida_do_comando(tmp_path: Path, comando: str) -> None:
    """O OUTPUT_FILE vem do config que segue o a_maze_ing.py no comando.

    Args:
        tmp_path: Pasta temporária do teste.
        comando: Linha de comando que roda o programa.
    """
    (tmp_path / "cfg.txt").write_text(
        "OUTPUT_FILE=saida/maze.txt\n", encoding="utf-8"
    )
    assert arquivo_de_saida(comando, tmp_path) == (
        tmp_path / "saida" / "maze.txt"
    )


@pytest.mark.parametrize(
    "comando",
    [
        "make run",
        "python3 a_maze_ing.py",
        "python3 a_maze_ing.py inexistente.txt",
        "python3 a_maze_ing.py sem_saida.txt",
        "python3 a_maze_ing.py 'aspas abertas",
    ],
)
def test_comando_sem_arquivo_de_saida(tmp_path: Path, comando: str) -> None:
    """Sem programa, sem config legível ou sem OUTPUT_FILE não há saída.

    Args:
        tmp_path: Pasta temporária do teste.
        comando: Linha de comando.
    """
    (tmp_path / "sem_saida.txt").write_text("WIDTH=20\n", encoding="utf-8")
    assert arquivo_de_saida(comando, tmp_path) is None
