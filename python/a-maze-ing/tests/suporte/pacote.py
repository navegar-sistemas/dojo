"""Pacotes mazegen-* (wheel e sdist), virtualenvs e textos do repositório."""

import re
import shlex
import tarfile
import zipfile
from dataclasses import dataclass
from email.message import Message
from email.parser import Parser
from pathlib import Path

from suporte.estado import Estado, Execucao

WHEEL = ".whl"
SDIST = ".tar.gz"
NOME_DO_WHEEL = re.compile(
    r"(?P<nome>[^-]+)-(?P<versao>[^-]+)(?:-\d[^-]*)?-[^-]+-[^-]+-[^-]+\.whl"
)
NOME_DO_SDIST = re.compile(r"(?P<nome>[^-]+)-(?P<versao>[^-]+)\.tar\.gz")
METADATA_DO_WHEEL = re.compile(r"[^/]+\.dist-info/METADATA")
PKG_INFO_DO_SDIST = re.compile(r"[^/]+/PKG-INFO")
LICENCAS_DO_WHEEL = re.compile(r"[^/]+\.dist-info/licenses/(?P<caminho>.+)")
# Arquivos que o setuptools cria no sdist; não vêm do repositório.
GERADOS_NO_SDIST = {"PKG-INFO", "setup.cfg"}
TITULO = re.compile(
    r" {0,3}(?P<nivel>#{1,6})[ \t]+(?P<texto>.*?)(?:[ \t]+#+)?"
)
CERCA = re.compile(r" {0,3}(?:```|~~~)")
VERSAO = re.compile(r'version\s*=\s*"(?P<versao>[^"]*)"\s*(?:#.*)?')


@dataclass
class Pacote:
    """Conteúdo de um wheel ou de um sdist, lido inteiro para a memória.

    ``arquivos`` mapeia o caminho de cada arquivo dentro do pacote para os
    bytes; ``info`` é o caminho do METADATA (wheel) ou do PKG-INFO da raiz
    (sdist).
    """

    caminho: Path
    arquivos: dict[str, bytes]
    info: str

    @property
    def wheel(self) -> bool:
        """Diz se o pacote é um wheel.

        Returns:
            True para .whl, False para .tar.gz.
        """
        return self.caminho.name.endswith(WHEEL)

    @property
    def raiz(self) -> str:
        """Prefixo dos caminhos do projeto dentro do pacote.

        Returns:
            "" no wheel; a pasta de topo com a barra no sdist.
        """
        return "" if self.wheel else self.info.split("/")[0] + "/"

    def metadados(self) -> Message:
        """Metadados do pacote lidos com ``email.parser``.

        Returns:
            A mensagem com os campos e, no corpo, a descrição longa.
        """
        texto = self.arquivos[self.info].decode("utf-8")
        return Parser().parsestr(texto)

    def fontes(self) -> dict[str, str]:
        """Arquivos do pacote que vêm do repositório.

        No wheel, os arquivos fora do ``.dist-info`` e as licenças de
        ``.dist-info/licenses/``; no sdist, tudo abaixo da pasta de topo
        menos o que o setuptools gera (PKG-INFO, setup.cfg, *.egg-info).

        Returns:
            Caminho dentro do pacote para o caminho no repositório.
        """
        achadas: dict[str, str] = {}
        for nome in self.arquivos:
            if self.wheel:
                licenca = LICENCAS_DO_WHEEL.fullmatch(nome)
                if licenca:
                    achadas[nome] = licenca["caminho"]
                elif ".dist-info/" not in nome:
                    achadas[nome] = nome
                continue
            relativo = nome[len(self.raiz):]
            partes = relativo.split("/")
            if relativo in GERADOS_NO_SDIST or partes[0].endswith(
                ".egg-info"
            ):
                continue
            achadas[nome] = relativo
        return achadas


def _ler_wheel(caminho: Path) -> dict[str, bytes]:
    """Arquivos de um wheel.

    Args:
        caminho: Arquivo .whl.

    Returns:
        Caminho de cada arquivo para os bytes.
    """
    with zipfile.ZipFile(caminho) as arquivo:
        return {
            membro.filename: arquivo.read(membro)
            for membro in arquivo.infolist()
            if not membro.is_dir()
        }


def _ler_sdist(caminho: Path) -> dict[str, bytes]:
    """Arquivos de um sdist.

    Args:
        caminho: Arquivo .tar.gz.

    Returns:
        Caminho de cada arquivo regular para os bytes.
    """
    arquivos: dict[str, bytes] = {}
    with tarfile.open(caminho, "r:gz") as arquivo:
        for membro in arquivo.getmembers():
            conteudo = arquivo.extractfile(membro) if membro.isfile() else None
            if conteudo is not None:
                with conteudo:
                    arquivos[membro.name] = conteudo.read()
    return arquivos


def abrir_pacote(caminho: Path) -> Pacote:
    """Lê um wheel ou um sdist.

    Args:
        caminho: Arquivo .whl ou .tar.gz.

    Returns:
        O pacote.

    Raises:
        ValueError: O arquivo não é .whl nem .tar.gz, não abre, ou não tem
            um único METADATA (wheel) ou PKG-INFO na raiz (sdist).
    """
    nome = caminho.name
    try:
        if nome.endswith(WHEEL):
            arquivos = _ler_wheel(caminho)
            info = METADATA_DO_WHEEL
        elif nome.endswith(SDIST):
            arquivos = _ler_sdist(caminho)
            info = PKG_INFO_DO_SDIST
        else:
            raise ValueError(f"{nome} não é {WHEEL} nem {SDIST}")
    except (zipfile.BadZipFile, tarfile.TarError, OSError) as erro:
        raise ValueError(f"{nome} não abre: {erro}") from erro
    achados = [membro for membro in arquivos if info.fullmatch(membro)]
    if len(achados) != 1:
        raise ValueError(
            f"{nome} deveria ter um arquivo de metadados ({info.pattern}), "
            f"mas tem {achados}"
        )
    return Pacote(caminho, arquivos, achados[0])


def nome_e_versao(nome: str) -> tuple[str, str] | None:
    """Nome e versão que o nome do arquivo do pacote declara.

    Args:
        nome: Nome do arquivo, como ``mazegen-1.0.0-py3-none-any.whl``.

    Returns:
        O nome da distribuição e a versão, ou None fora dos formatos de
        nome do wheel e do sdist.
    """
    for formato in (NOME_DO_WHEEL, NOME_DO_SDIST):
        casado = formato.fullmatch(nome)
        if casado:
            return casado["nome"], casado["versao"]
    return None


def versao_do_pyproject(texto: str) -> str | None:
    """Versão declarada na tabela ``[project]`` do pyproject.toml.

    O tomllib só existe a partir do Python 3.11 e a suíte roda no 3.10;
    por isso a leitura procura só a linha ``version = "..."`` dentro de
    ``[project]``, a forma da I13.

    Args:
        texto: Conteúdo do pyproject.toml.

    Returns:
        A versão, ou None quando a tabela não declara uma.
    """
    tabela = ""
    for linha in texto.splitlines():
        limpa = linha.strip()
        if limpa.startswith("["):
            tabela = limpa
            continue
        casado = VERSAO.fullmatch(limpa)
        if tabela == "[project]" and casado:
            return casado["versao"]
    return None


def secao_markdown(texto: str, titulo: str) -> str | None:
    """Corpo de uma seção de Markdown, sem o título.

    Vai da linha ``#… titulo`` até o próximo título de nível igual ou
    mais alto; linhas dentro de blocos de código cercados não são título.

    Args:
        texto: Documento Markdown.
        titulo: Texto do título, sem os ``#``.

    Returns:
        O corpo, ou None se não há título com esse texto.
    """
    nivel: int | None = None
    corpo: list[str] = []
    em_cerca = False
    for linha in texto.splitlines(keepends=True):
        casado = None
        if CERCA.match(linha):
            em_cerca = not em_cerca
        elif not em_cerca:
            casado = TITULO.fullmatch(linha.rstrip("\r\n"))
        if nivel is None:
            if casado and casado["texto"] == titulo:
                nivel = len(casado["nivel"])
            continue
        if casado and len(casado["nivel"]) <= nivel:
            break
        corpo.append(linha)
    return None if nivel is None else "".join(corpo)


def criar_virtualenv(destino: Path, caminhos: list[Path]) -> Execucao:
    """Cria um virtualenv com o python3 do PATH do cenário.

    Args:
        destino: Pasta do virtualenv, que ainda não existe.
        caminhos: Pastas que o cenário põe na frente do PATH.

    Returns:
        A execução de ``python3 -m venv``.
    """
    criador = Estado(cwd=destino.parent, caminhos_extras=list(caminhos))
    return criador.executar(f"python3 -m venv {shlex.quote(str(destino))}")


def rodar_no_virtualenv(venv: Path, pasta: Path, comando: str) -> Execucao:
    """Roda um comando com o bin do virtualenv na frente do PATH.

    Args:
        venv: Pasta do virtualenv.
        pasta: Pasta onde o comando roda.
        comando: Linha de comando.

    Returns:
        A execução, fora da lista de resultados do cenário.
    """
    return Estado(cwd=pasta, caminhos_extras=[bin_do(venv)]).executar(comando)


def bin_do(venv: Path) -> Path:
    """Pasta dos executáveis de um virtualenv.

    Args:
        venv: Pasta do virtualenv.

    Returns:
        ``venv/bin``.
    """
    return venv / "bin"
