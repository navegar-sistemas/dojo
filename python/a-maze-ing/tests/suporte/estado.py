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

from suporte.catalogo import Caso
from suporte.config import Config, arquivo_de_saida
from suporte.labirinto import Labirinto, ler_saida
from suporte.sessao import Sessao

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
    conteudo_saida: str | None = None
    labirinto: Labirinto | None = None

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
    lido: list[Path] = field(default_factory=list)
    labirintos: list[Labirinto] = field(default_factory=list)
    execucoes: list[Execucao] = field(default_factory=list)
    celula: int | None = None
    gerador: object | None = None
    expressao: str | None = None
    excecao: Exception | None = None
    sessao: Sessao | None = None
    sessao_desde: int = 0
    analise: Execucao | None = None
    venvs: dict[str, Path] = field(default_factory=dict)
    catalogo: list[Caso] = field(default_factory=list)

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
        criadas pelo cenário saem por último. Uma sessão aberta é encerrada
        antes, para o processo não segurar arquivos do cenário.
        """
        if self.sessao is not None:
            self.sessao.encerrar()
            self.sessao = None
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
        destino.write_bytes(self.config.conteudo())

    def em_sessao(self) -> Sessao | None:
        """Sessão aberta depois da última execução, se houver.

        Returns:
            A sessão, quando ela é a ação mais recente do cenário.
        """
        if self.sessao is not None and self.sessao_desde == len(
            self.resultados
        ):
            return self.sessao
        return None

    @property
    def resultado(self) -> Execucao:
        """Última execução do cenário, ou o retrato da sessão aberta.

        Numa sessão, o código é o do processo já terminado, ou -1 enquanto
        ele ainda roda; quem precisa do código final espera o fim antes.

        Returns:
            A execução mais recente.
        """
        sessao = self.em_sessao()
        if sessao is not None:
            codigo = sessao.processo.poll()
            saida = self.saida_da_sessao()
            return Execucao(
                sessao.comando,
                -1 if codigo is None else codigo,
                sessao.saida_padrao,
                sessao.saida_erro,
                False,
                saida,
                self.ler_saida_de(saida),
            )
        if not self.resultados:
            pytest.fail("nenhum comando foi executado antes deste passo")
        return self.resultados[-1]

    def saida_da_sessao(self) -> Path | None:
        """OUTPUT_FILE do config usado pela sessão.

        Returns:
            O caminho, ou None se não há sessão ou o config não o define.
        """
        if self.sessao is None:
            return None
        return arquivo_de_saida(self.sessao.comando, self.cwd)

    @staticmethod
    def ler_saida_de(caminho: Path | None) -> str | None:
        """Lê o arquivo de saída, se existir.

        Args:
            caminho: OUTPUT_FILE de uma execução.

        Returns:
            O conteúdo sem converter quebras de linha (``newline=""``),
            para "\\r" ser detectável, ou None quando não há arquivo
            legível.
        """
        if caminho is None or not caminho.is_file():
            return None
        try:
            with caminho.open(
                encoding="utf-8", errors="replace", newline=""
            ) as arquivo:
                return arquivo.read()
        except OSError:
            return None

    def registrar_labirinto(self, execucao: Execucao) -> None:
        """Guarda o labirinto do OUTPUT_FILE de uma execução com código 0.

        Um arquivo que não se lê como labirinto não entra: os passos sobre
        labirinto falham depois dizendo que nenhum foi produzido.

        Args:
            execucao: Execução com ``conteudo_saida`` já lido.
        """
        if execucao.codigo != 0 or execucao.conteudo_saida is None:
            return
        try:
            execucao.labirinto = ler_saida(execucao.conteudo_saida)
        except ValueError:
            return
        self.labirintos.append(execucao.labirinto)

    def ambiente(self) -> dict[str, str]:
        """Variáveis de ambiente dos comandos do cenário.

        Returns:
            Cópia de os.environ com os caminhos extras na frente do PATH.
        """
        ambiente = dict(os.environ)
        extras = [str(caminho) for caminho in self.caminhos_extras]
        ambiente["PATH"] = os.pathsep.join([*extras, os.environ["PATH"]])
        return ambiente

    def abrir_sessao(self, comando: str) -> Sessao:
        """Abre o programa numa sessão interativa.

        O OUTPUT_FILE do config vai para a reserva como em ``executar``.

        Args:
            comando: Linha de comando, como escrita no .feature.

        Returns:
            A sessão, também guardada em ``sessao``.
        """
        if self.sessao is not None:
            self.sessao.encerrar()
        saida = arquivo_de_saida(comando, self.cwd)
        if saida is not None and not self.reservado(saida):
            self.proteger(saida)
        self.sessao = Sessao(comando, self.cwd, self.ambiente())
        self.sessao_desde = len(self.resultados)
        return self.sessao

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
            A execução, também guardada em ``resultados``; com código 0, o
            labirinto do OUTPUT_FILE entra em ``labirintos``.
        """
        saida = arquivo_de_saida(comando, self.cwd)
        if saida is not None and not self.reservado(saida):
            self.proteger(saida)
        ambiente = self.ambiente()
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
            self.ler_saida_de(saida),
        )
        self.registrar_labirinto(execucao)
        self.resultados.append(execucao)
        return execucao
