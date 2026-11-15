"""Arquivo de configuração que os cenários montam e gravam."""

import re
import shlex
from collections.abc import Callable
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
    return chaves_das_linhas(linhas)


def chaves_das_linhas(linhas: list[str]) -> dict[str, str]:
    """Chaves e valores de linhas KEY=VALUE, como a D04 lê.

    Args:
        linhas: Linhas do config.

    Returns:
        Chave em maiúsculas para valor; vale a última chave repetida.
    """
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


def _chave_de(linha: str) -> str:
    """Chave de uma linha KEY=VALUE, como o programa a lê (D04).

    Args:
        linha: Linha do config.

    Returns:
        A chave sem espaços e em maiúsculas; vazio sem "=".
    """
    if "=" not in linha:
        return ""
    return linha.split("=", 1)[0].strip().upper()


def _por_par(linhas: list[str]) -> list[str]:
    """Põe uma linha vazia entre cada par de linhas.

    Args:
        linhas: Linhas do config.

    Returns:
        As linhas intercaladas com linhas vazias.
    """
    intercaladas: list[str] = []
    for indice, linha in enumerate(linhas):
        if indice:
            intercaladas.append("")
        intercaladas.append(linha)
    return intercaladas


def _em_volta_do_igual(linhas: list[str]) -> list[str]:
    """Põe um espaço de cada lado do primeiro "=".

    Args:
        linhas: Linhas do config.

    Returns:
        As linhas com " = " no lugar do primeiro "=".
    """
    return [linha.replace("=", " = ", 1) for linha in linhas]


def _minuscula(chave: str | None) -> Callable[[list[str]], list[str]]:
    """Cria a variação que escreve a chave (ou todas) em minúsculas.

    Args:
        chave: Chave a trocar; None troca todas.

    Returns:
        A função que transforma as linhas.
    """

    def trocar(linhas: list[str]) -> list[str]:
        """Escreve em minúsculas a parte antes do "=".

        Args:
            linhas: Linhas do config.

        Returns:
            As linhas com a chave trocada.
        """
        trocadas: list[str] = []
        for linha in linhas:
            atual = _chave_de(linha)
            if atual and chave in (None, atual):
                nome, valor = linha.split("=", 1)
                linha = f"{nome.lower()}={valor}"
            trocadas.append(linha)
        return trocadas

    return trocar


def _capitalizada(linhas: list[str]) -> list[str]:
    """Escreve a chave HEIGHT como "Height".

    Args:
        linhas: Linhas do config.

    Returns:
        As linhas com a chave trocada.
    """
    return [
        re.sub(r"^HEIGHT=", "Height=", linha) for linha in linhas
    ]


def _perfect_minusculo(linhas: list[str]) -> list[str]:
    """Escreve a linha PERFECT inteira em minúsculas.

    Args:
        linhas: Linhas do config.

    Returns:
        As linhas com "perfect=true" ou "perfect=false".
    """
    return [
        linha.lower() if _chave_de(linha) == "PERFECT" else linha
        for linha in linhas
    ]


# Variações da V15: as que mexem nas linhas, e as de final de linha.
VARIACOES_DE_LINHA: dict[str, Callable[[list[str]], list[str]]] = {
    "uma linha vazia entre cada par": _por_par,
    "espaços em volta do igual": _em_volta_do_igual,
    "espaços no fim de cada linha": lambda linhas: [
        f"{linha}   " for linha in linhas
    ],
    "chave WIDTH minúscula": _minuscula("WIDTH"),
    "todas as chaves minúsculas": _minuscula(None),
    "chave HEIGHT capitalizada": _capitalizada,
    "perfect=true minúsculo": _perfect_minusculo,
}
VARIACOES_DE_FIM = ("finais de linha CRLF", "sem quebra de linha depois da"
                    " última linha")
VARIACOES = (*VARIACOES_DE_LINHA, *VARIACOES_DE_FIM)


@dataclass
class Config:
    """Config do cenário; só vai para o disco num passo Quando."""

    linhas: list[str]
    destino: str = "cfg.txt"
    variacao: str | None = None

    def _indices(self, chave: str) -> list[int]:
        """Posições das linhas da chave, sem diferenciar maiúsculas.

        Args:
            chave: Nome da chave.

        Returns:
            Os índices em ``linhas``, na ordem do arquivo.
        """
        return [
            indice for indice, linha in enumerate(self.linhas)
            if _chave_de(linha) == chave.upper()
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

    def trocar_linha(self, numero: int, linha: str) -> None:
        """Troca a linha pelo número, contado a partir de 1.

        Args:
            numero: Número da linha.
            linha: Linha nova.

        Raises:
            ValueError: Quando o config não tem essa linha.
        """
        if not 1 <= numero <= len(self.linhas):
            raise ValueError(
                f"o config tem {len(self.linhas)} linhas, não tem a {numero}"
            )
        self.linhas[numero - 1] = linha

    def trocar_linha_da_chave(self, chave: str, linha: str) -> None:
        """Troca a primeira linha da chave; texto vazio remove a linha.

        Args:
            chave: Nome da chave.
            linha: Linha nova, ou "" para remover.

        Raises:
            ValueError: Quando o config não tem a chave.
        """
        indices = self._indices(chave)
        if not indices:
            raise ValueError(f"o config não tem a chave {chave}")
        if linha:
            self.linhas[indices[0]] = linha
        else:
            del self.linhas[indices[0]]

    def inserir(self, linha: str, no_inicio: bool) -> None:
        """Insere a linha no início ou acrescenta no fim.

        Args:
            linha: Linha nova.
            no_inicio: True para a primeira posição.
        """
        if no_inicio:
            self.linhas.insert(0, linha)
        else:
            self.linhas.append(linha)

    def conteudo(self) -> bytes:
        """Bytes gravados no destino, com a variação aplicada (V15).

        Returns:
            As linhas em UTF-8, cada uma terminada em "\\n", salvo pelas
            variações de final de linha.

        Raises:
            ValueError: Quando a variação não existe.
        """
        linhas = list(self.linhas)
        if self.variacao is not None and self.variacao not in VARIACOES:
            raise ValueError(
                f'variação "{self.variacao}" não existe; as válidas são: '
                f"{', '.join(VARIACOES)}"
            )
        transformar = VARIACOES_DE_LINHA.get(self.variacao or "")
        if transformar is not None:
            linhas = transformar(linhas)
        if self.variacao == VARIACOES_DE_FIM[0]:
            texto = "".join(f"{linha}\r\n" for linha in linhas)
        elif self.variacao == VARIACOES_DE_FIM[1]:
            texto = "\n".join(linhas)
        else:
            texto = "".join(f"{linha}\n" for linha in linhas)
        return texto.encode("utf-8")
