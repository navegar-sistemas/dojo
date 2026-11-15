"""Execução do maze_analyzer.py do subject e leitura do relatório dele."""

import re
import shlex
import tempfile
from pathlib import Path

import pytest

from suporte.ambiente import caminho_do_analyzer
from suporte.estado import Estado, Execucao

# Rótulos das linhas do relatório que os cenários leem (V83, V84). Cada
# linha é "rótulo", espaços opcionais, ":" opcional, espaços e o valor;
# no "Verdict:" os dois-pontos já fazem parte do rótulo.
ROTULOS = (
    "Verdict:",
    "Reachable region",
    "Independent loops",
    "Dead-ends",
    "Corners + centre",
    "Wall coherence",
    "Entry",
)
INTEIRO = re.compile(r"-?\d+")


def arquivo_atual(estado: Estado) -> Path:
    """Arquivo de saída do labirinto atual, que o analyzer vai ler.

    O labirinto atual é o último de ``estado.labirintos``. Vale o
    OUTPUT_FILE da execução que o produziu, se o disco ainda tem esse
    conteúdo; senão (labirinto de teste, ou arquivo regravado depois), o
    texto do labirinto vai para um arquivo temporário, apagado no fim do
    cenário. Labirinto sem texto (da classe geradora) não tem arquivo.

    Args:
        estado: Estado do cenário.

    Returns:
        O caminho do arquivo a analisar.
    """
    if not estado.labirintos:
        pytest.fail("nenhum labirinto foi produzido antes deste passo")
    atual = estado.labirintos[-1]
    if atual.texto is None:
        pytest.fail(
            "o labirinto atual veio da classe geradora e não tem arquivo de "
            "saída para o maze_analyzer"
        )
    for execucao in reversed([*estado.resultados, *estado.execucoes]):
        saida = execucao.arquivo_saida
        if (
            execucao.labirinto is atual
            and saida is not None
            and Estado.ler_saida_de(saida) == atual.texto
        ):
            return saida
    pasta = Path(tempfile.mkdtemp(prefix="analyzer-"))
    estado.preparados.append((pasta, None))
    arquivo = pasta / "labirinto.txt"
    arquivo.write_text(atual.texto, encoding="utf-8", newline="")
    return arquivo


def analisar(estado: Estado, arquivo: Path, opcoes: list[str]) -> Execucao:
    """Roda ``python3 maze_analyzer.py <arquivo> <opções>``.

    O comando roda na pasta e com o PATH do cenário, como os demais.

    Args:
        estado: Estado do cenário.
        arquivo: Arquivo de saída a analisar.
        opcoes: Opções do analyzer, como "--max-dead-ends", "0".

    Returns:
        A execução, guardada também em ``resultados`` e em ``analise``.
    """
    comando = shlex.join(
        ["python3", str(caminho_do_analyzer()), str(arquivo), *opcoes]
    )
    estado.analise = estado.executar(comando)
    return estado.analise


def analise_atual(estado: Estado) -> Execucao:
    """Análise do cenário; roda o analyzer sobre o arquivo atual se faltar.

    Args:
        estado: Estado do cenário.

    Returns:
        A execução do analyzer.
    """
    if estado.analise is None:
        return analisar(estado, arquivo_atual(estado), [])
    return estado.analise


def valor_da_linha(saida: str, rotulo: str) -> str:
    """Valor da única linha do relatório que começa com o rótulo.

    O valor é o que vem depois do rótulo, dos espaços e dos dois-pontos:
    em "Dead-ends        : 2 real + 0 enclosed", o valor de "Dead-ends" é
    "2 real + 0 enclosed".

    Args:
        saida: Saída padrão do analyzer.
        rotulo: Um dos ROTULOS.

    Returns:
        O valor da linha.
    """
    if rotulo not in ROTULOS:
        pytest.fail(
            f'rótulo "{rotulo}" não existe; os válidos são: '
            f"{', '.join(ROTULOS)}"
        )
    linhas = [
        linha for linha in saida.splitlines() if linha.startswith(rotulo)
    ]
    if len(linhas) != 1:
        pytest.fail(
            f"esperada uma linha do maze_analyzer começando com {rotulo!r}, "
            f"vieram {len(linhas)}:\n{saida}"
        )
    valor = linhas[0][len(rotulo):].lstrip()
    if valor.startswith(":"):
        valor = valor[1:].lstrip()
    return valor


def primeiro_inteiro(valor: str, rotulo: str) -> int:
    """Primeiro número inteiro do valor de uma linha do relatório.

    Args:
        valor: Valor devolvido por ``valor_da_linha``.
        rotulo: Rótulo da linha, para a mensagem.

    Returns:
        O inteiro.
    """
    achado = INTEIRO.search(valor)
    if achado is None:
        pytest.fail(f"a linha {rotulo!r} não tem número: {valor!r}")
    return int(achado.group(0))
