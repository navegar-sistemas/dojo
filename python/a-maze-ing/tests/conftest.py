"""Configuração da suíte: hook de tags, tipos de parâmetro e estado."""

import os
import re
import subprocess
from collections.abc import Callable
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
}


@dataclass
class Execucao:
    """Resultado de um comando executado por um passo."""

    comando: str
    codigo: int
    saida_padrao: str
    saida_erro: str

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

    @property
    def resultado(self) -> Execucao:
        """Última execução do cenário."""
        if not self.resultados:
            pytest.fail("nenhum comando foi executado antes deste passo")
        return self.resultados[-1]

    def executar(self, comando: str, entrada: str = "") -> Execucao:
        """Roda um comando no shell, na pasta e com o PATH do cenário.

        Args:
            comando: Linha de comando, como escrita no .feature.
            entrada: Texto enviado ao stdin.

        Returns:
            A execução, também guardada em ``resultados``.
        """
        ambiente = dict(os.environ)
        extras = [str(caminho) for caminho in self.caminhos_extras]
        ambiente["PATH"] = os.pathsep.join([*extras, os.environ["PATH"]])
        processo = subprocess.run(
            comando,
            shell=True,
            cwd=self.cwd,
            env=ambiente,
            input=entrada,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        execucao = Execucao(
            comando,
            processo.returncode,
            processo.stdout,
            processo.stderr,
        )
        self.resultados.append(execucao)
        return execucao


@pytest.fixture
def estado() -> Estado:
    """Estado novo para cada cenário."""
    return Estado()
