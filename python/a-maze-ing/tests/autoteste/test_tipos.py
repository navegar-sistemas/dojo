"""Testes dos tipos de parâmetro das frases."""

import pytest
from pytest_bdd import parsers

from suporte.tipos import TIPOS, desescapar


def casar(frase: str, texto: str) -> dict[str, object] | None:
    """Casa um texto com uma frase, como o pytest-bdd faz com um passo.

    Args:
        frase: Frase do passo, com os tipos da suíte.
        texto: Texto do passo.

    Returns:
        Os parâmetros convertidos, ou None se o texto não casa.
    """
    passo = parsers.parse(frase, extra_types=TIPOS)
    return passo.parse_arguments(texto) if passo.is_matching(texto) else None


@pytest.mark.parametrize(
    ("escrito", "esperado"),
    [
        ("", ""),
        ("texto simples", "texto simples"),
        (r"diz \"oi\"", 'diz "oi"'),
        (r"a\nb", "a\nb"),
        (r"a\rb", "a\rb"),
        (r"a\tb", "a\tb"),
        (r"\x1b[0m", "\x1b[0m"),
        (r"^\d+,\d+$", r"^\d+,\d+$"),
    ],
)
def test_desescapar(escrito: str, esperado: str) -> None:
    """Só os cinco escapes aceitos são desfeitos; o resto fica como está.

    Args:
        escrito: Valor como aparece no .feature.
        esperado: Valor entregue à função do passo.
    """
    assert desescapar(escrito) == esperado


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ('o arquivo ""', ""),
        ('o arquivo "cfg.txt"', "cfg.txt"),
        (r'o arquivo "a \"b\" c"', 'a "b" c'),
    ],
)
def test_q_aceita_vazio_e_aspas_escapadas(texto: str, esperado: str) -> None:
    """O tipo Q lê o texto entre aspas, inclusive vazio e com aspas dentro.

    Args:
        texto: Texto do passo.
        esperado: Valor convertido.
    """
    assert casar('o arquivo "{nome:Q}"', texto) == {"nome": esperado}


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ('eu executo "make run"', ["make run"]),
        ('eu executo "a" e "b"', ["a", "b"]),
        ('eu executo "a", "b" e "c"', ["a", "b", "c"]),
        ('eu executo "a, b" e "c e d"', ["a, b", "c e d"]),
        (r'eu executo "echo \"x\"" e ""', ['echo "x"', ""]),
    ],
)
def test_l_separa_os_itens(texto: str, esperado: list[str]) -> None:
    """O tipo L separa por vírgula e por "e" só fora das aspas.

    Args:
        texto: Texto do passo.
        esperado: Itens convertidos.
    """
    assert casar("eu executo {comandos:L}", texto) == {"comandos": esperado}


@pytest.mark.parametrize(
    "texto",
    ["eu executo make run", 'eu executo "a" ou "b"', 'eu executo "a",  "b"'],
)
def test_l_recusa_lista_mal_formada(texto: str) -> None:
    """Item sem aspas ou separador diferente não casa com o tipo L.

    Args:
        texto: Texto do passo.
    """
    assert casar("eu executo {comandos:L}", texto) is None


@pytest.mark.parametrize(
    "fluxo", ["a saída", "a saída padrão", "a saída de erro"]
)
def test_enum_casa_a_alternativa_inteira(fluxo: str) -> None:
    """A alternativa mais longa ganha: "a saída" não engole as outras.

    Args:
        fluxo: Valor do tipo Fluxo.
    """
    assert casar('{fluxo:Fluxo} é "{texto:Q}"', f'{fluxo} é "x"') == {
        "fluxo": fluxo,
        "texto": "x",
    }


def test_enum_recusa_valor_fora_da_lista() -> None:
    """Valor que não está na lista fechada não casa."""
    assert casar('{fluxo:Fluxo} é "{texto:Q}"', 'o log é "x"') is None
