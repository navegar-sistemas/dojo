"""Estado de um cenário: pasta, config, comandos executados e limpeza."""

import ast
import contextlib
import os
import shutil
import signal
import stat
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from suporte.config import Config, arquivo_de_saida

TESTS_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = TESTS_DIR.parent / "project"
TIMEOUT = 30
FECHAMENTO = 2


def remover(caminho: Path) -> None:
    """Apaga um arquivo ou uma pasta, se existir.

    Args:
        caminho: Caminho a apagar.
    """
    if caminho.is_dir() and not caminho.is_symlink():
        shutil.rmtree(caminho)
    else:
        caminho.unlink(missing_ok=True)


def texto_de(dados: bytes | None) -> str:
    """Decodifica a saída parcial que um TimeoutExpired carrega.

    Args:
        dados: Bytes lidos do pipe até o estouro, ou None.

    Returns:
        O texto, decodificado como o Popen faz no modo texto.
    """
    if dados is None:
        return ""
    texto = dados.decode("utf-8", errors="replace")
    return texto.replace("\r\n", "\n").replace("\r", "\n")


def encerrar_grupo(processo: subprocess.Popen[str]) -> None:
    """Mata o grupo de processos do comando e o próprio shell.

    O grupo pode já ter acabado (só sobrou um neto noutra sessão) ou ter
    um membro de outro usuário; nos dois casos o shell ainda é morto.

    Args:
        processo: Shell iniciado com sessão própria.
    """
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(processo.pid, signal.SIGKILL)
    processo.kill()


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
        """Guarda o original do caminho até a chamada de ``restaurar``.

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

    def reservado(self, caminho: Path) -> bool:
        """Diz se o caminho já foi preparado ou protegido no cenário.

        Args:
            caminho: Caminho absoluto.

        Returns:
            True se ``restaurar`` já vai desfazer o caminho.
        """
        return any(preparado == caminho for preparado, _ in self.preparados)

    def criar_pastas(self, pasta: Path) -> None:
        """Cria a pasta e os pais que faltam; ``restaurar`` apaga os criados.

        Só a pasta mais alta que não existia é registrada: apagá-la leva as
        de baixo junto.

        Args:
            pasta: Pasta que precisa existir.
        """
        criada = None
        atual = pasta
        while not atual.exists():
            criada = atual
            atual = atual.parent
        if criada is None:
            return
        pasta.mkdir(parents=True)
        self.preparados.append((criada, None))

    def restaurar(self) -> None:
        """Desfaz os caminhos preparados, do último para o primeiro.

        Cada caminho recebe permissão de volta e é apagado; se havia um
        original guardado na reserva, ele volta para o lugar. As pastas pai
        criadas pelo cenário saem por último.
        """
        for caminho, guardado in reversed(self.preparados):
            if caminho.exists() and not caminho.is_symlink():
                caminho.chmod(stat.S_IRWXU)
            remover(caminho)
            if guardado is not None:
                shutil.move(guardado, caminho)
        self.preparados.clear()

    def gravar_config(self) -> None:
        """Grava o config no destino.

        Não grava quando não há config ou quando um passo preparou o
        destino à mão. As pastas pai que faltam são criadas e somem no fim.
        """
        if self.config is None:
            return
        destino = self.cwd / self.config.destino
        if destino in self.sem_gravacao:
            return
        self.criar_pastas(destino.parent)
        self.proteger(destino)
        destino.write_text(
            "\n".join(self.config.linhas) + "\n", encoding="utf-8"
        )

    @property
    def resultado(self) -> Execucao:
        """Última execução do cenário.

        Returns:
            A execução mais recente.
        """
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

        O OUTPUT_FILE do config vai para a reserva antes, salvo quando um
        passo já preparou esse caminho: aí ele fica como o passo deixou.

        Args:
            comando: Linha de comando, como escrita no .feature.
            entrada: Texto enviado ao stdin.

        Returns:
            A execução, também guardada em ``resultados``.
        """
        saida = arquivo_de_saida(comando, self.cwd)
        if saida is not None and not self.reservado(saida):
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
                estourou = True
                encerrar_grupo(processo)
                # Um neto noutra sessão sobrevive ao killpg e segura os
                # pipes; o prazo curto evita esperar por ele.
                try:
                    saida_padrao, saida_erro = processo.communicate(
                        timeout=FECHAMENTO
                    )
                except subprocess.TimeoutExpired as parcial:
                    saida_padrao = texto_de(parcial.output)
                    saida_erro = texto_de(parcial.stderr)
                    for pipe in (processo.stdout, processo.stderr):
                        if pipe is not None:
                            pipe.close()
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
