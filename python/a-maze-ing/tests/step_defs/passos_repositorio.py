"""Passos que preparam e conferem o repositório de entrega (project/)."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then

from conftest import PROJECT_DIR, TIMEOUT, TIPOS, Estado, Execucao

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
    """Instalação compartilhada por todos os cenários da sessão."""
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
    """V02: prepara o repositório no estado pedido.

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
    pytest.fail(f'estado "{nome}" ainda não implementado (V02 no README)')


@given(
    parsers.parse(
        'o arquivo "{arquivo:Q}" na raiz do repositório', extra_types=TIPOS
    )
)
def arquivo_na_raiz(estado: Estado, arquivo: str) -> None:
    """V01: confere que o arquivo existe no repositório.

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
def caminho_preparado(
    estado: Estado, tmp_path: Path, caminho: str, tipo: str
) -> None:
    """V16: prepara o caminho; a fixture estado desfaz tudo no fim.

    Um original que exista no caminho vai para a reserva em tmp_path e
    volta no fim do teste.

    Args:
        estado: Estado do cenário.
        tmp_path: Pasta temporária do cenário, onde fica a reserva.
        caminho: Caminho relativo ao repositório.
        tipo: "inexistente", "vazio" ou "diretório"; os demais tipos ainda
            não existem.
    """
    alvo = estado.cwd / caminho
    if tipo == "diretório":
        criado = alvo
        while not criado.parent.exists():
            criado = criado.parent
        if not alvo.exists():
            estado.preparados.append((criado, None))
        alvo.mkdir(parents=True, exist_ok=True)
        return
    if tipo not in ("inexistente", "vazio"):
        pytest.fail(f'tipo "{tipo}" ainda não implementado (V16 no README)')
    reserva = None
    if alvo.exists() or alvo.is_symlink():
        reserva = tmp_path / "reserva" / str(len(estado.preparados))
        reserva.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(alvo, reserva)
    estado.preparados.append((alvo, reserva))
    if tipo == "vazio":
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(b"")


@then(
    parsers.parse(
        'o caminho "{caminho:Q}" {situacao:EstadoCaminho}', extra_types=TIPOS
    )
)
def caminho_na_situacao(estado: Estado, caminho: str, situacao: str) -> None:
    """V60: confere a existência, o conteúdo ou a situação no git.

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
