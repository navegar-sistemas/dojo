"""Configuração da suíte: hook de tags, tipos de parâmetro e estado."""

import ast
import os
import re
import shlex
import shutil
import signal
import stat
import subprocess
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

import parse
import pytest

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TESTS_DIR.parent / "project"
ANALYZER = TESTS_DIR / "maze_analyzer.py"
TIMEOUT = 30

pytest_plugins = [
    "step_defs.passos_repositorio",
    "step_defs.passos_execucao",
    "step_defs.passos_analise",
    "step_defs.passos_propriedades",
    "step_defs.passos_renderizacao",
]

REFERENCIAS = ("pdf-", "md-", "regua-", "decisao-")


def pytest_bdd_apply_tag(tag: str, function: Callable[..., object]) -> object:
    """Converte as tags dos .feature em marcadores do pytest.

    Args:
        tag: Tag do cenário, sem o "@".
        function: Função de teste gerada pelo pytest-bdd.

    Returns:
        True quando a tag foi tratada aqui; None para o pytest-bdd criar o
        marcador registrado no pytest.ini.
    """
    if tag == "manual":
        pytest.mark.manual(function)
        pytest.mark.skip(reason="verificação manual")(function)
        return True
    if tag == "decisao-I19":
        pytest.mark.skip(reason="fora da primeira versão (I19)")(function)
        return True
    if tag.startswith(REFERENCIAS):
        return True
    return None


_TEXTO = r'(?:[^"\\]|\\.)*'
_ITEM = f'"{_TEXTO}"'
_ESCAPES = (
    ('\\"', '"'),
    ("\\n", "\n"),
    ("\\r", "\r"),
    ("\\t", "\t"),
    ("\\x1b", "\x1b"),
)


# Os conversores recebem o parâmetro "string": o stub do pacote parse define
# o tipo de conversor como um Protocol com __call__(self, string: str).


def desescapar(string: str) -> str:
    """Desfaz os escapes aceitos dentro das aspas de um passo.

    Args:
        string: Valor como aparece no .feature, sem as aspas externas.

    Returns:
        O valor com aspas, quebras de linha, tabulações e ESC reais.
    """
    for escape, caractere in _ESCAPES:
        string = string.replace(escape, caractere)
    return string


def _lista(string: str) -> list[str]:
    """Separa uma lista de itens entre aspas ("a", "b" e "c")."""
    return [desescapar(item) for item in re.findall(f'"({_TEXTO})"', string)]


def _enum(*valores: str) -> Callable[[str], str]:
    """Cria um tipo de parâmetro que aceita só os valores dados."""
    alternativas = sorted(valores, key=len, reverse=True)
    padrao = "|".join(re.escape(valor) for valor in alternativas)

    def conversor(string: str) -> str:
        return string

    return parse.with_pattern(padrao)(conversor)


TIPOS: dict[str, Callable[[str], object]] = {
    "Q": parse.with_pattern(_TEXTO)(desescapar),
    "L": parse.with_pattern(rf"{_ITEM}(?:(?:, | e ){_ITEM})*")(_lista),
    "Fluxo": _enum("a saída", "a saída padrão", "a saída de erro"),
    "Contem": _enum("contém", "não contém"),
    "EstadoCaminho": _enum(
        "existe",
        "não existe",
        "é ignorado pelo git",
        "não é ignorado pelo git",
        "está versionado no git",
        "não está vazio",
    ),
    "Sujeito": _enum(
        "o validador da suíte",
        "a renderização",
        "a análise estática",
        "o módulo mazegen",
        "o catálogo de casos de erro",
    ),
    "Origem": _enum("base", "do repositório"),
}

CONFIG_BASE = [
    "WIDTH=20",
    "HEIGHT=15",
    "ENTRY=0,0",
    "EXIT=19,14",
    "OUTPUT_FILE=maze.txt",
    "PERFECT=True",
    "SEED=42",
]

MOTIVOS = {
    "arquivo não encontrado": "not found",
    "arquivo não é UTF-8": "UTF-8",
    "chave obrigatória ausente": "missing",
    "entrada igual à saída": "differ",
    "tamanho sem tabuleiro Pac-Man": "Pac-Man",
    "coordenada no padrão 42": '"42"',
}


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
        """Posições das linhas da chave, sem diferenciar maiúsculas."""
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


@dataclass
class Execucao:
    """Resultado de um comando executado por um passo."""

    comando: str
    codigo: int
    saida_padrao: str
    saida_erro: str
    estourou: bool = False
    arquivo_saida: Path | None = None

    def fluxo(self, nome: str) -> str:
        """Devolve o texto do fluxo pedido pelo passo.

        Args:
            nome: "a saída", "a saída padrão" ou "a saída de erro".

        Returns:
            stdout, stderr ou os dois juntos.
        """
        if nome == "a saída padrão":
            return self.saida_padrao
        if nome == "a saída de erro":
            return self.saida_erro
        return self.saida_padrao + self.saida_erro


@dataclass
class Estado:
    """Estado compartilhado pelos passos de um cenário."""

    cwd: Path = PROJECT_DIR
    caminhos_extras: list[Path] = field(default_factory=list)
    resultados: list[Execucao] = field(default_factory=list)
    fontes: list[Path] = field(default_factory=list)
    arvores: dict[Path, ast.Module] = field(default_factory=dict)
    preparados: list[tuple[Path, Path | None]] = field(default_factory=list)
    reserva: Path | None = None
    config: Config | None = None
    sem_gravacao: set[Path] = field(default_factory=set)

    def proteger(self, caminho: Path) -> None:
        """Guarda o original do caminho; a fixture estado o devolve no fim.

        Args:
            caminho: Caminho que o teste vai criar, trocar ou apagar.
        """
        if self.reserva is None:
            pytest.fail("este estado não tem pasta de reserva")
        guardado = None
        if caminho.exists() or caminho.is_symlink():
            guardado = self.reserva / str(len(self.preparados))
            shutil.move(caminho, guardado)
        self.preparados.append((caminho, guardado))

    def gravar_config(self) -> None:
        """Grava o config no destino.

        Não grava quando não há config ou quando V16 ou V18 prepararam o
        destino à mão.
        """
        if self.config is None:
            return
        destino = self.cwd / self.config.destino
        if destino in self.sem_gravacao:
            return
        self.proteger(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            "\n".join(self.config.linhas) + "\n", encoding="utf-8"
        )

    @property
    def resultado(self) -> Execucao:
        """Última execução do cenário."""
        if not self.resultados:
            pytest.fail("nenhum comando foi executado antes deste passo")
        return self.resultados[-1]

    def resultado_de(self, comando: str) -> Execucao:
        """Última execução do comando no cenário; se não houver, roda agora.

        Args:
            comando: Linha de comando, como escrita no .feature.

        Returns:
            A execução encontrada ou a nova.
        """
        for execucao in reversed(self.resultados):
            if execucao.comando == comando:
                return execucao
        return self.executar(comando)

    def executar(self, comando: str, entrada: str = "") -> Execucao:
        """Roda um comando no shell, na pasta e com o PATH do cenário.

        Args:
            comando: Linha de comando, como escrita no .feature.
            entrada: Texto enviado ao stdin.

        Returns:
            A execução, também guardada em ``resultados``.
        """
        saida = arquivo_de_saida(comando, self.cwd)
        if saida is not None:
            self.proteger(saida)
        ambiente = dict(os.environ)
        extras = [str(caminho) for caminho in self.caminhos_extras]
        ambiente["PATH"] = os.pathsep.join([*extras, os.environ["PATH"]])
        # Sessão própria: no tempo limite o grupo inteiro morre, inclusive o
        # programa que o shell ou o make iniciou.
        with subprocess.Popen(
            comando,
            shell=True,
            cwd=self.cwd,
            env=ambiente,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        ) as processo:
            try:
                saida_padrao, saida_erro = processo.communicate(
                    entrada, timeout=TIMEOUT
                )
                estourou = False
            except subprocess.TimeoutExpired:
                os.killpg(processo.pid, signal.SIGKILL)
                saida_padrao, saida_erro = processo.communicate()
                estourou = True
        execucao = Execucao(
            comando,
            processo.returncode,
            saida_padrao,
            saida_erro,
            estourou,
            saida,
        )
        self.resultados.append(execucao)
        return execucao


def remover(caminho: Path) -> None:
    """Apaga um arquivo ou uma pasta, se existir.

    Args:
        caminho: Caminho a apagar.
    """
    if caminho.is_dir() and not caminho.is_symlink():
        shutil.rmtree(caminho)
    else:
        caminho.unlink(missing_ok=True)


@pytest.fixture
def estado(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Estado]:
    """Estado novo para cada cenário; desfaz os caminhos preparados no fim.

    Cada caminho preparado recebe permissão de volta e é apagado; se havia
    um original guardado na reserva, ele volta para o lugar.
    """
    novo = Estado(reserva=tmp_path_factory.mktemp("reserva"))
    yield novo
    for caminho, guardado in reversed(novo.preparados):
        if caminho.exists() and not caminho.is_symlink():
            caminho.chmod(stat.S_IRWXU)
        remover(caminho)
        if guardado is not None:
            shutil.move(guardado, caminho)


Verificacao = Callable[[Estado], None]

PROPRIEDADES: dict[tuple[str, str], Verificacao] = {}


def propriedade(
    sujeito: str, nome: str
) -> Callable[[Verificacao], Verificacao]:
    """Registra a verificação de uma propriedade da V72.

    Args:
        sujeito: Valor do tipo Sujeito, como escrito no passo.
        nome: Propriedade da lista fechada do sujeito.

    Returns:
        Decorador que guarda a função em PROPRIEDADES e a devolve.
    """

    def registrar(funcao: Verificacao) -> Verificacao:
        PROPRIEDADES[(sujeito, nome)] = funcao
        return funcao

    return registrar
