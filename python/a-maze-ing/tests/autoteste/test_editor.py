"""As frases dos passos e a configuração da extensão Cucumber batem."""

import ast
import json
import re

from suporte.estado import TESTS_DIR
from suporte.tipos import TIPOS

CONFIGURACAO = TESTS_DIR.parents[2] / ".vscode" / "settings.json"
DECORADORES = {"given", "when", "then"}
INTEIRO = r"-?\d+"

# A extensão trata como expressão regular a frase que tem um destes
# caracteres, e deixa de casar os parâmetros {nome:Tipo}.
LIDOS_COMO_REGEX = set("().*\\|")


def texto_de(no: ast.expr) -> str:
    """Texto de uma frase escrita como string ou como soma de strings.

    Args:
        no: Argumento do decorador do passo.

    Returns:
        A frase inteira.
    """
    if isinstance(no, ast.BinOp):
        return texto_de(no.left) + texto_de(no.right)
    if isinstance(no, ast.Call):
        return texto_de(no.args[0])
    assert isinstance(no, ast.Constant) and isinstance(no.value, str)
    return no.value


def frases() -> list[str]:
    """Frases de todos os passos de step_defs/.

    Returns:
        O texto de cada decorador given, when ou then.
    """
    achadas: list[str] = []
    for arquivo in sorted((TESTS_DIR / "step_defs").glob("*.py")):
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if (
                isinstance(no, ast.Call)
                and isinstance(no.func, ast.Name)
                and no.func.id in DECORADORES
            ):
                achadas.append(texto_de(no.args[0]))
    return achadas


def regex_do_editor(tipo: str) -> str:
    """Expressão que o settings.json deve ter para um tipo de parâmetro.

    Args:
        tipo: Nome do tipo, como aparece depois dos dois-pontos na frase.

    Returns:
        O padrão do tipo, sem a barra que re.escape põe antes dos espaços.
    """
    if tipo == "d":
        return INTEIRO
    padrao: str = getattr(TIPOS[tipo], "pattern")
    return padrao.replace("\\ ", " ")


def test_ha_frases_para_conferir() -> None:
    """A leitura de step_defs/ encontra os passos."""
    assert len(frases()) > 20


def test_frases_sem_caractere_lido_como_regex() -> None:
    """O texto fixo das frases não usa . ( ) * barra invertida nem barra."""
    com_defeito = [
        frase for frase in frases()
        if LIDOS_COMO_REGEX & set(re.sub(r"\{[^}]*\}", "", frase))
    ]
    assert com_defeito == []


def test_tipos_de_parametro_registrados_no_editor() -> None:
    """Todo par {nome:Tipo} das frases tem a mesma regex no settings.json."""
    with CONFIGURACAO.open(encoding="utf-8") as arquivo:
        registrados = {
            entrada["name"]: entrada["regexp"]
            for entrada in json.load(arquivo)["cucumber.parameterTypes"]
        }
    usados = {
        f"{nome}:{tipo}": regex_do_editor(tipo)
        for frase in frases()
        for nome, tipo in re.findall(r"\{(\w+):(\w+)\}", frase)
    }
    assert registrados == usados
