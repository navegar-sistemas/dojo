"""Os .feature não repetem cenários e citam as decisões que usam."""

import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field

import pytest

from suporte.estado import TESTS_DIR

FEATURES = TESTS_DIR / "features"
PASSO = re.compile(r"(?:Dad[oa]s?|Quando|Então|E|Mas) (.*)")
CENARIO = ("Cenário:", "Esquema do Cenário:")

# Passos cujo resultado depende do valor que a decisão fixa: o menu e o
# prompt da I03, as coordenadas x,y do rodapé da D13.
DECISOES_DOS_PASSOS = {
    "decisao-I03": re.compile(
        r"^(o programa iniciado com|eu envio ao menu|o evento \"|"
        r"o programa aguarda no prompt)|com a entrada (.*, )?\"[123]\""
    ),
    "decisao-D13": re.compile(
        r"linha (1|2|<\w+>) do rodapé|coordenadas do rodapé|"
        r"iguais às do rodapé|rodapé com ENTRY"
    ),
}


@dataclass
class Cenario:
    """Cenário automatizado lido de um .feature."""

    local: str
    tags: list[str]
    passos: list[str] = field(default_factory=list)
    exemplos: list[str] = field(default_factory=list)


def cenarios_automatizados() -> list[Cenario]:
    """Lê os cenários @automatizado, com os passos do Contexto na frente.

    Returns:
        Os cenários de todos os .feature, na ordem dos arquivos.
    """
    achados: list[Cenario] = []
    for arquivo in sorted(FEATURES.glob("*.feature")):
        contexto: list[str] = []
        tags: list[str] = []
        atual: Cenario | None = None
        no_contexto = False
        with arquivo.open(encoding="utf-8") as feature:
            linhas = feature.read().splitlines()
        for numero, linha in enumerate(linhas, start=1):
            texto = linha.strip()
            passo = PASSO.fullmatch(texto)
            if texto.startswith("@"):
                tags = [tag.lstrip("@") for tag in texto.split()]
            elif texto.startswith("Contexto:"):
                no_contexto = True
            elif texto.startswith(CENARIO):
                no_contexto = False
                atual = Cenario(f"{arquivo.name}:{numero}", tags, [*contexto])
                if "automatizado" in tags:
                    achados.append(atual)
            elif passo and no_contexto:
                contexto.append(passo.group(1))
            elif passo and atual is not None:
                atual.passos.append(passo.group(1))
            elif texto.startswith("|") and atual is not None:
                atual.exemplos.append(re.sub(r"\s+", " ", texto))
    return achados


def test_ha_cenarios_automatizados() -> None:
    """A leitura dos .feature encontra os cenários."""
    assert len(cenarios_automatizados()) > 100


def test_nenhum_cenario_automatizado_repete_outro() -> None:
    """Dois cenários com os mesmos passos e exemplos conferem a mesma coisa."""
    grupos: dict[tuple[tuple[str, ...], tuple[str, ...]], list[str]] = (
        defaultdict(list)
    )
    for cenario in cenarios_automatizados():
        chave = (tuple(cenario.passos), tuple(cenario.exemplos))
        grupos[chave].append(cenario.local)
    repetidos = [locais for locais in grupos.values() if len(locais) > 1]
    assert repetidos == []


@pytest.mark.parametrize("decisao", sorted(DECISOES_DOS_PASSOS))
def test_cenario_cita_a_decisao_que_usa(decisao: str) -> None:
    """Cenário com passo que depende de uma decisão tem a tag dela.

    Args:
        decisao: Tag da decisão, sem o "@".
    """
    padrao = DECISOES_DOS_PASSOS[decisao]
    sem_tag = [
        cenario.local for cenario in cenarios_automatizados()
        if decisao not in cenario.tags
        and any(padrao.search(passo) for passo in cenario.passos)
    ]
    assert sem_tag == []


def test_nenhuma_frase_falta() -> None:
    """make faltantes não acha frase sem função nem cenário sem test_*.py."""
    processo = subprocess.run(
        ["make", "faltantes"],
        cwd=TESTS_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    assert processo.returncode == 0, processo.stdout + processo.stderr
