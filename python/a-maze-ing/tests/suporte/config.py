"""Arquivo de configuração que os cenários montam e gravam."""

import shlex
from dataclasses import dataclass
from pathlib import Path

CONFIG_BASE = [
    "WIDTH=20",
    "HEIGHT=15",
    "ENTRY=0,0",
    "EXIT=19,14",
    "OUTPUT_FILE=maze.txt",
    "PERFECT=True",
    "SEED=42",
]


def ler_chaves(arquivo: Path) -> dict[str, str]:
    """Lê um config como a D04, sem validar os valores.

    Args:
        arquivo: Arquivo de configuração.

    Returns:
        Chave em maiúsculas para valor; vazio se o arquivo não pode ser
        lido como UTF-8.
    """
    try:
        with arquivo.open(encoding="utf-8-sig") as entrada:
            linhas = entrada.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    chaves: dict[str, str] = {}
    for linha in linhas:
        texto = linha.strip()
        if not texto or texto.startswith("#") or "=" not in texto:
            continue
        chave, valor = texto.split("=", 1)
        chaves[chave.strip().upper()] = valor.strip()
    return chaves


def arquivo_de_saida(comando: str, cwd: Path) -> Path | None:
    """OUTPUT_FILE do config que o comando passa ao a_maze_ing.py.

    Args:
        comando: Linha de comando.
        cwd: Pasta onde o comando roda.

    Returns:
        O caminho do arquivo de saída, ou None se o comando não roda o
        programa com um config legível.
    """
    try:
        partes = shlex.split(comando)
    except ValueError:
        return None
    for indice, parte in enumerate(partes[:-1]):
        if Path(parte).name == "a_maze_ing.py":
            saida = ler_chaves(cwd / partes[indice + 1]).get("OUTPUT_FILE")
            return cwd / saida if saida else None
    return None


@dataclass
class Config:
    """Config do cenário; só vai para o disco num passo Quando."""

    linhas: list[str]
    destino: str = "cfg.txt"

    def _indices(self, chave: str) -> list[int]:
        """Posições das linhas da chave, sem diferenciar maiúsculas.

        Args:
            chave: Nome da chave.

        Returns:
            Os índices em ``linhas``, na ordem do arquivo.
        """
        return [
            indice for indice, linha in enumerate(self.linhas)
            if linha.split("=", 1)[0].strip().upper() == chave.upper()
        ]

    def definir(self, chave: str, valor: str) -> None:
        """Troca a linha da chave ou acrescenta no fim.

        Args:
            chave: Nome da chave.
            valor: Novo valor.
        """
        indices = self._indices(chave)
        if indices:
            self.linhas[indices[0]] = f"{chave}={valor}"
        else:
            self.linhas.append(f"{chave}={valor}")

    def sem(self, chave: str) -> None:
        """Remove todas as linhas da chave.

        Args:
            chave: Nome da chave.
        """
        removidas = set(self._indices(chave))
        self.linhas = [
            linha for indice, linha in enumerate(self.linhas)
            if indice not in removidas
        ]
