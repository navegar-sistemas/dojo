"""Tipos de parâmetro usados nas frases dos passos."""

import re
from collections.abc import Callable

import parse

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
    """Separa uma lista de itens entre aspas ("a", "b" e "c").

    Args:
        string: Lista como aparece no .feature.

    Returns:
        Os itens, sem as aspas e com os escapes desfeitos.
    """
    return [desescapar(item) for item in re.findall(f'"({_TEXTO})"', string)]


def _enum(*valores: str) -> Callable[[str], str]:
    """Cria um tipo de parâmetro que aceita só os valores dados.

    Args:
        *valores: Alternativas aceitas.

    Returns:
        Conversor cujo padrão tenta primeiro a alternativa mais longa, para
        "a saída" não engolir "a saída de erro".
    """
    alternativas = sorted(valores, key=len, reverse=True)
    padrao = "|".join(re.escape(valor) for valor in alternativas)

    def conversor(string: str) -> str:
        """Devolve o valor como veio do passo.

        Args:
            string: Texto casado pelo padrão.

        Returns:
            O mesmo texto.
        """
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
    "Origem": _enum("base", "do repositório"),
    "TemLinha": _enum("tem uma linha", "não tem nenhuma linha"),
}
