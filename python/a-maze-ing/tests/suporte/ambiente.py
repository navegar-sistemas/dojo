"""Conferência do que os cenários usam fora do projeto: python3 e analyzer."""

import shutil
import subprocess
from pathlib import Path

import pytest

MINIMO = (3, 10)
IMPRIMIR_VERSAO = "import sys; print('%d.%d' % sys.version_info[:2])"
ANALYZER = (
    Path(__file__).resolve().parents[2] / "private" / "maze_analyzer.py"
)


def problema_da_versao(caminho: str, versao: str) -> str | None:
    """Diz o que há de errado com a versão de um python3.

    Args:
        caminho: Caminho do executável.
        versao: Versão no formato "maior.menor".

    Returns:
        A mensagem para quem roda a suíte, ou None se a versão serve.
    """
    numeros = tuple(int(parte) for parte in versao.split("."))
    if numeros >= MINIMO:
        return None
    return (
        f"o python3 do PATH é {versao} ({caminho}); os cenários rodam "
        "'python3 a_maze_ing.py' e o subject exige Python 3.10 ou "
        "posterior. Ponha um python3 mais novo antes no PATH."
    )


def problema_do_python3() -> str | None:
    """Diz o que há de errado com o python3 do PATH.

    Returns:
        A mensagem para quem roda a suíte, ou None se o python3 serve.
    """
    caminho = shutil.which("python3")
    if caminho is None:
        return (
            "não há python3 no PATH; os cenários rodam "
            "'python3 a_maze_ing.py'."
        )
    processo = subprocess.run(
        [caminho, "-c", IMPRIMIR_VERSAO],
        capture_output=True,
        text=True,
        check=True,
    )
    return problema_da_versao(caminho, processo.stdout.strip())


def caminho_do_analyzer() -> Path:
    """Caminho do maze_analyzer.py que acompanha o subject.

    O arquivo fica em private/, fora do git: num checkout novo ele falta e
    o passo que o usa falha dizendo onde colocá-lo.

    Returns:
        O caminho do analyzer.
    """
    if not ANALYZER.is_file():
        pytest.fail(
            f"{ANALYZER} não existe: o maze_analyzer.py vem com o subject e "
            "não é versionado; copie-o para esse caminho"
        )
    return ANALYZER
