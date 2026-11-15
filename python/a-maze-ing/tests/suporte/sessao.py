"""Sessão interativa com o programa: envio ao menu e espera do prompt."""

import contextlib
import os
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import IO

PROMPT = "Choice? (1-4): "
ESPERA = 30.0
INTERVALO = 0.02
FECHAMENTO = 2.0


class Sessao:
    """Programa aberto com stdin, stdout e stderr ligados à suíte.

    Duas threads leem stdout e stderr para os pipes nunca encherem; o
    passo espera o prompt do menu (I03) ou o fim do processo. ``enviados``
    guarda as linhas que chegaram ao stdin, na ordem.
    """

    def __init__(
        self, comando: str, cwd: Path, ambiente: dict[str, str]
    ) -> None:
        """Abre o processo numa sessão própria.

        Args:
            comando: Linha de comando, como escrita no .feature.
            cwd: Pasta onde o comando roda.
            ambiente: Variáveis de ambiente do processo.
        """
        self.comando = comando
        self.enviados: list[str] = []
        self._trava = threading.Lock()
        self._saida_padrao: list[str] = []
        self._saida_erro: list[str] = []
        self._prompts_vistos = 0
        self.processo = subprocess.Popen(
            comando,
            shell=True,
            cwd=cwd,
            env=ambiente,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        )
        self._leitores = [
            threading.Thread(
                target=self._ler, args=(fluxo, destino), daemon=True
            )
            for fluxo, destino in (
                (self.processo.stdout, self._saida_padrao),
                (self.processo.stderr, self._saida_erro),
            )
        ]
        for leitor in self._leitores:
            leitor.start()

    def _ler(self, fluxo: IO[str] | None, destino: list[str]) -> None:
        """Copia o fluxo para o buffer, caractere a caractere.

        O prompt não termina em quebra de linha; ler por caractere deixa
        ele visível assim que é impresso.

        Args:
            fluxo: stdout ou stderr do processo.
            destino: Buffer que recebe o texto.
        """
        if fluxo is None:
            return
        while True:
            # O pipe fechado por ``encerrar`` enquanto a thread ainda lê é
            # o fim do fluxo, não um erro: a thread só termina.
            try:
                caractere = fluxo.read(1)
            except (ValueError, OSError):
                return
            if not caractere:
                return
            with self._trava:
                destino.append(caractere)

    @property
    def saida_padrao(self) -> str:
        """Tudo o que o programa imprimiu em stdout até agora.

        Returns:
            O texto lido.
        """
        with self._trava:
            return "".join(self._saida_padrao)

    @property
    def saida_erro(self) -> str:
        """Tudo o que o programa imprimiu em stderr até agora.

        Returns:
            O texto lido.
        """
        with self._trava:
            return "".join(self._saida_erro)

    def viva(self) -> bool:
        """Diz se o processo ainda roda.

        Returns:
            True enquanto ``poll()`` devolve None.
        """
        return self.processo.poll() is None

    def esperar_prompt_ou_fim(self, espera: float = ESPERA) -> bool:
        """Espera um prompt novo do menu ou o fim do processo.

        Args:
            espera: Segundos até desistir.

        Returns:
            True quando um prompt novo apareceu ou o processo terminou;
            False quando o prazo acabou antes.
        """
        limite = time.monotonic() + espera
        while time.monotonic() < limite:
            vistos = self.saida_padrao.count(PROMPT)
            if vistos > self._prompts_vistos:
                self._prompts_vistos = vistos
                return True
            if not self.viva():
                self._juntar_leitores()
                self._prompts_vistos = self.saida_padrao.count(PROMPT)
                return True
            time.sleep(INTERVALO)
        return False

    def enviar(self, linha: str) -> bool:
        """Escreve a linha no stdin, terminada em quebra de linha.

        Args:
            linha: Texto enviado ao menu.

        Returns:
            True quando a linha chegou ao pipe; False quando o processo
            já terminou ou o stdin está fechado.
        """
        entrada = self.processo.stdin
        if entrada is None or entrada.closed or not self.viva():
            return False
        try:
            entrada.write(f"{linha}\n")
            entrada.flush()
        except BrokenPipeError:
            return False
        self.enviados.append(linha)
        return True

    def fechar_entrada(self) -> None:
        """Fecha o stdin: o programa recebe EOF no próximo input()."""
        entrada = self.processo.stdin
        if entrada is not None and not entrada.closed:
            # Com o processo já morto, o flush do close dá BrokenPipeError;
            # o pipe fica fechado do mesmo jeito.
            with contextlib.suppress(BrokenPipeError):
                entrada.close()

    def interromper(self) -> None:
        """Envia SIGINT ao grupo de processos, como o Ctrl+C do terminal."""
        if self.viva():
            os.killpg(self.processo.pid, signal.SIGINT)

    def esperar_fim(self, espera: float = ESPERA) -> int | None:
        """Espera o processo terminar.

        Args:
            espera: Segundos até desistir.

        Returns:
            O código de saída, ou None se o prazo acabou.
        """
        try:
            codigo = self.processo.wait(timeout=espera)
        except subprocess.TimeoutExpired:
            return None
        self._juntar_leitores()
        return codigo

    def _juntar_leitores(self) -> None:
        """Espera as threads lerem o que sobrou nos pipes."""
        for leitor in self._leitores:
            leitor.join(timeout=FECHAMENTO)

    def encerrar(self) -> None:
        """Mata o grupo de processos, se ainda roda, e fecha os pipes."""
        if self.viva():
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(self.processo.pid, signal.SIGKILL)
            self.processo.kill()
        self.fechar_entrada()
        self.processo.wait()
        self._juntar_leitores()
        for fluxo in (self.processo.stdout, self.processo.stderr):
            if fluxo is not None:
                fluxo.close()
