"""Programa falso que faz o papel do a_maze_ing.py nos autotestes da sessão.

Ele imprime a primeira saída, depois uma saída a cada linha lida do stdin;
quando acabam as saídas, termina com o código dado ou segue lendo até o
EOF. EOF e Ctrl+C terminam com código 0, como a D17 pede ao programa.
"""

import json
import shlex
import sys
from pathlib import Path

ROTEIRO = """\
import json
import sys

with open(sys.argv[1], encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
try:
    sys.stderr.write(dados["erro"])
    sys.stderr.flush()
    sys.stdout.write(dados["saidas"][0])
    sys.stdout.flush()
    for saida in dados["saidas"][1:]:
        if not sys.stdin.readline():
            sys.exit(0)
        sys.stdout.write(saida)
        sys.stdout.flush()
    if dados["codigo"] is not None:
        sys.exit(dados["codigo"])
    while sys.stdin.readline():
        pass
except KeyboardInterrupt:
    sys.exit(0)
"""


def programa_falso(
    pasta: Path,
    saidas: list[str],
    codigo: int | None = None,
    erro: str = "",
) -> str:
    """Grava o programa falso na pasta e devolve o comando que o roda.

    Args:
        pasta: Pasta onde o comando vai rodar.
        saidas: Texto inicial e o texto impresso depois de cada linha lida.
        codigo: Código de saída depois da última saída; None segue lendo
            o stdin até o EOF.
        erro: Texto escrito no stderr ao abrir.

    Returns:
        A linha de comando, relativa à pasta.
    """
    (pasta / "falso.py").write_text(ROTEIRO, encoding="utf-8")
    (pasta / "falso.json").write_text(
        json.dumps({"saidas": saidas, "codigo": codigo, "erro": erro}),
        encoding="utf-8",
    )
    return f"{shlex.quote(sys.executable)} falso.py falso.json"
