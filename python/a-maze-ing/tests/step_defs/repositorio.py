"""Passos que preparam e conferem o repositório de entrega (project/)."""

import random
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from suporte.config import CONFIG_BASE, Config
from suporte.estado import PROJECT_DIR, TIMEOUT, Estado, Execucao
from suporte.tipos import TIPOS

# O clone e as consultas ao git não podem herdar a configuração de quem roda
# a suíte: o ignore global mascararia um .gitignore incompleto, e hooks ou
# assinatura obrigatória quebrariam o commit da cópia.
GIT = [
    "git",
    "-c", "core.excludesFile=/dev/null",
    "-c", "core.hooksPath=/dev/null",
    "-c", "commit.gpgsign=false",
    "-c", "user.name=suite",
    "-c", "user.email=suite@localhost",
]


@dataclass
class Instalacao:
    """Resultado do ``make install``, feito uma vez por sessão de testes."""

    execucao: Execucao | None = None

    def garantir(self) -> Execucao:
        """Roda ``make install`` na primeira chamada e reaproveita depois.

        Returns:
            A execução do ``make install``.
        """
        if self.execucao is None:
            self.execucao = Estado().executar("make install")
        return self.execucao


@pytest.fixture(scope="session")
def instalacao() -> Instalacao:
    """Instalação compartilhada por todos os cenários da sessão.

    Returns:
        A instalação, ainda sem o ``make install`` executado.
    """
    return Instalacao()


def git(
    argumentos: list[str], pasta: Path
) -> subprocess.CompletedProcess[str]:
    """Roda o git com a configuração isolada da suíte.

    Args:
        argumentos: Subcomando e argumentos, sem o "git".
        pasta: Pasta onde o comando roda.

    Returns:
        O processo terminado, com stdout e stderr capturados.
    """
    return subprocess.run(
        [*GIT, *argumentos],
        cwd=pasta,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def git_ou_falha(argumentos: list[str], pasta: Path) -> str:
    """Roda o git e falha o teste se ele terminar com erro.

    Args:
        argumentos: Subcomando e argumentos, sem o "git".
        pasta: Pasta onde o comando roda.

    Returns:
        A saída padrão do comando.
    """
    processo = git(argumentos, pasta)
    if processo.returncode != 0:
        pytest.fail(
            f"'git {' '.join(argumentos)}' terminou com código "
            f"{processo.returncode}\n{processo.stdout}{processo.stderr}"
        )
    return processo.stdout


def clonar_limpo(destino: Path) -> None:
    """Recria em destino o repositório de entrega só com o que está no git.

    A raiz do git é o monorepo dojo; a cópia dos arquivos que
    ``git ls-files`` lista em project/ reproduz o clone do repositório da
    instituição, com um git próprio.

    Args:
        destino: Pasta vazia que recebe a cópia.
    """
    listagem = git_ou_falha(["ls-files", "-z"], PROJECT_DIR)
    for nome in filter(None, listagem.split("\0")):
        origem = PROJECT_DIR / nome
        if origem.is_file():
            alvo = destino / nome
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem, alvo)
    git_ou_falha(["init", "-q"], destino)
    git_ou_falha(["add", "-A"], destino)
    git_ou_falha(
        ["commit", "-q", "--allow-empty", "-m", "clone limpo"], destino
    )


def casar(estado: Estado, padrao: str) -> list[Path]:
    """Caminhos do repositório que casam com o padrão (aceita glob).

    Args:
        estado: Estado do cenário; o padrão é relativo a ``estado.cwd``.
        padrao: Caminho ou glob, com ou sem "/" no fim.

    Returns:
        Os caminhos existentes que casam.
    """
    return sorted(estado.cwd.glob(padrao.rstrip("/")))


@given(parsers.parse('o repositório no estado "{nome:Q}"', extra_types=TIPOS))
def repositorio_no_estado(
    estado: Estado, instalacao: Instalacao, tmp_path: Path, nome: str
) -> None:
    """Prepara o repositório no estado pedido.

    Args:
        estado: Estado do cenário.
        instalacao: Instalação da sessão.
        tmp_path: Pasta temporária do cenário.
        nome: "atual", "instalado" ou "clone limpo"; "clone do remoto"
            ainda não existe.
    """
    estado.cwd = PROJECT_DIR
    if nome == "atual":
        return
    if nome == "instalado":
        execucao = instalacao.garantir()
        if execucao.codigo != 0:
            pytest.fail(
                f"'{execucao.comando}' terminou com código {execucao.codigo}"
                f"\n{execucao.saida_padrao}{execucao.saida_erro}"
            )
        estado.caminhos_extras = [PROJECT_DIR / ".venv" / "bin"]
        return
    if nome == "clone limpo":
        clone = tmp_path / "clone"
        clone.mkdir()
        clonar_limpo(clone)
        estado.cwd = clone
        estado.caminhos_extras = [clone / ".venv" / "bin"]
        return
    pytest.fail(f'estado "{nome}" ainda não implementado')


@given(
    parsers.parse(
        'o arquivo "{arquivo:Q}" na raiz do repositório', extra_types=TIPOS
    )
)
def arquivo_na_raiz(estado: Estado, arquivo: str) -> None:
    """Confere que o arquivo existe no repositório.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório; aceita glob.
    """
    if not casar(estado, arquivo):
        pytest.fail(f'"{arquivo}" não existe em {estado.cwd}')


@given(
    parsers.parse(
        'o caminho "{caminho:Q}" preparado como "{tipo:Q}"', extra_types=TIPOS
    )
)
def caminho_preparado(estado: Estado, caminho: str, tipo: str) -> None:
    """Prepara o caminho; a fixture estado desfaz tudo no fim.

    Args:
        estado: Estado do cenário.
        caminho: Caminho relativo ao repositório.
        tipo: "inexistente", "diretório" ou uma chave de CONTEUDOS.
    """
    preparar(estado, estado.cwd / caminho, tipo)


def _texto(linhas: list[str]) -> bytes:
    """Linhas de config como bytes UTF-8, uma por linha.

    Args:
        linhas: Linhas do config, sem a quebra de linha.

    Returns:
        O conteúdo do arquivo.
    """
    return ("\n".join(linhas) + "\n").encode("utf-8")


# Conteúdo de cada tipo de arquivo preparado. O primeiro byte 0xFF nunca
# aparece em UTF-8, então os bytes aleatórios são sempre inválidos.
CONTEUDOS: dict[str, Callable[[], bytes]] = {
    "vazio": lambda: b"",
    "bytes binários aleatórios": (
        lambda: b"\xff" + random.Random(0).randbytes(255)
    ),
    "só espaços e tabulações": lambda: b"  \t \n\t\t  \n \n",
    "BOM UTF-8 + config base": lambda: b"\xef\xbb\xbf" + _texto(CONFIG_BASE),
    "config base com WIDTH de 100000 dígitos": lambda: _texto(
        ["WIDTH=" + "9" * 100000, *CONFIG_BASE[1:]]
    ),
    "só WÍDTH=20 e HEÍGHT=15, com acento": (
        lambda: _texto(["WÍDTH=20", "HEÍGHT=15"])
    ),
    "sem permissão de leitura": lambda: _texto(CONFIG_BASE),
}


def preparar(estado: Estado, alvo: Path, tipo: str) -> None:
    """Prepara o alvo conforme o tipo.

    O original vai para a reserva e o destino deixa de receber o config
    automático do cenário.

    Args:
        estado: Estado do cenário.
        alvo: Caminho absoluto.
        tipo: "inexistente", "diretório" ou uma chave de CONTEUDOS.
    """
    if tipo == "diretório":
        criado = alvo
        while not criado.parent.exists():
            criado = criado.parent
        if not alvo.exists():
            estado.preparados.append((criado, None))
        alvo.mkdir(parents=True, exist_ok=True)
        return
    if tipo != "inexistente" and tipo not in CONTEUDOS:
        pytest.fail(f'tipo "{tipo}" ainda não implementado')
    estado.proteger(alvo)
    estado.sem_gravacao.add(alvo)
    if tipo == "inexistente":
        return
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_bytes(CONTEUDOS[tipo]())
    if tipo == "sem permissão de leitura":
        alvo.chmod(0)


@given(parsers.parse("o config {origem:Origem}", extra_types=TIPOS))
def config_de(estado: Estado, origem: str) -> None:
    """Carrega o config base ou o config.txt do repositório.

    Args:
        estado: Estado do cenário.
        origem: "base" ou "do repositório".
    """
    if origem == "base":
        estado.config = Config(list(CONFIG_BASE))
        return
    repositorio = estado.cwd / "config.txt"
    if not repositorio.is_file():
        pytest.fail(f"config.txt não existe em {estado.cwd}")
    estado.config = Config(
        repositorio.read_text(encoding="utf-8").splitlines()
    )


# O que cada situação de erro faz com o config e com o seu destino.
SITUACOES: dict[str, Callable[[Estado, Config], None]] = {
    "arquivo de configuração inexistente": lambda estado, config: preparar(
        estado, estado.cwd / config.destino, "inexistente"
    ),
    "arquivo de configuração sem permissão de leitura": (
        lambda estado, config: preparar(
            estado, estado.cwd / config.destino, "sem permissão de leitura"
        )
    ),
    "chave obrigatória ausente": lambda estado, config: config.sem("WIDTH"),
    "valor inválido": lambda estado, config: config.definir("WIDTH", "abc"),
    "parâmetros impossíveis": (
        lambda estado, config: config.definir("EXIT", "0,0")
    ),
    "OUTPUT_FILE num diretório inexistente": (
        lambda estado, config: config.definir(
            "OUTPUT_FILE", "diretorio_inexistente/maze.txt"
        )
    ),
}


@given(parsers.parse('a situação de erro "{situacao:Q}"', extra_types=TIPOS))
@when(parsers.parse('a situação de erro "{situacao:Q}"', extra_types=TIPOS))
def situacao_de_erro(estado: Estado, situacao: str) -> None:
    """Aplica a situação de erro ao config atual e ao seu destino.

    Args:
        estado: Estado do cenário.
        situacao: Uma das chaves de SITUACOES.
    """
    if estado.config is None:
        pytest.fail("a situação de erro precisa de um config antes")
    aplicar = SITUACOES.get(situacao)
    if aplicar is None:
        pytest.fail(
            f'situação "{situacao}" não existe; as válidas são: '
            f"{', '.join(SITUACOES)}"
        )
    aplicar(estado, estado.config)


@then(
    parsers.parse(
        'o caminho "{caminho:Q}" {situacao:EstadoCaminho}', extra_types=TIPOS
    )
)
def caminho_na_situacao(estado: Estado, caminho: str, situacao: str) -> None:
    """Confere a existência, o conteúdo ou a situação no git.

    Args:
        estado: Estado do cenário.
        caminho: Caminho relativo ao repositório; aceita glob nas
            situações de existência e conteúdo.
        situacao: Valor do tipo EstadoCaminho.
    """
    if situacao == "existe":
        if not casar(estado, caminho):
            pytest.fail(f'"{caminho}" não existe')
    elif situacao == "não existe":
        if casar(estado, caminho):
            pytest.fail(f'"{caminho}" existe')
    elif situacao == "não está vazio":
        if not any(
            (item.is_file() and item.stat().st_size > 0)
            or (item.is_dir() and any(item.iterdir()))
            for item in casar(estado, caminho)
        ):
            pytest.fail(f'"{caminho}" não existe ou está vazio')
    elif situacao == "está versionado no git":
        processo = git(["ls-files", "--error-unmatch", caminho], estado.cwd)
        if processo.returncode != 0:
            pytest.fail(f'"{caminho}" não está versionado no git')
    else:
        processo = git(["check-ignore", "-q", caminho], estado.cwd)
        if processo.returncode not in (0, 1):
            pytest.fail(f"git check-ignore falhou:\n{processo.stderr}")
        ignorado = processo.returncode == 0
        if ignorado != (situacao == "é ignorado pelo git"):
            pytest.fail(
                f'"{caminho}" {"é" if ignorado else "não é"} ignorado pelo '
                f"git em {estado.cwd}"
            )
