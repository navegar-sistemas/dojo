"""Gera as imagens das partes 10 (utilitários) e 12 (geração e saída).

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_10_a_12.py <raiz da implementação>

A implementação pronta fornece o pacote mazegen, que gera os labirintos
reais.
"""

from __future__ import annotations

import sys
from pathlib import Path

from svg import COLORS, _svg, _text, grid_from_hex, maze_svg, save

IMG = Path(__file__).resolve().parent.parent / "static" / "img"
UTILS = IMG / "utilitarios"
OUTPUT = IMG / "geracao"
STEP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

PALETTE = (
    ("DEFAULT", 49, "corridor", "corredor"),
    ("WHITE", 47, "white_wall", "parede"),
    ("YELLOW", 43, "yellow_wall", "parede"),
    ("GREEN", 42, "green_wall", "parede"),
    ("BLUE", 44, "blue_wall", "parede"),
    ("GREY", 100, "grey", "\"42\""),
    ("MAGENTA", 45, "magenta", "entrada"),
    ("RED", 41, "red", "saída"),
    ("CYAN", 46, "cyan", "caminho"),
)


def walk(start: tuple[int, int], letters: str) -> list[tuple[int, int]]:
    """Converte o caminho em letras na lista de células.

    Args:
        start: Célula de entrada.
        letters: Letras N, E, S e W.

    Returns:
        As células visitadas, da entrada à saída.
    """
    cells = [start]
    for letter in letters:
        dx, dy = STEP[letter]
        x, y = cells[-1]
        cells.append((x + dx, y + dy))
    return cells


def swatch(x: float, y: float, size: float, name: str) -> str:
    """Cria um quadrado da cor indicada, com contorno.

    Args:
        x: Canto esquerdo.
        y: Topo.
        size: Lado.
        name: Nome da cor em COLORS.

    Returns:
        O elemento SVG.
    """
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" '
        f'rx="4" fill="{COLORS[name]}" stroke="#9ca3af" stroke-width="1"/>'
    )


def palette_svg() -> str:
    """Desenha as constantes de Ansi: nome, código SGR e cor.

    Returns:
        O documento SVG.
    """
    column, size, left, top, per_row, row_height = 92, 44, 20, 20, 5, 130
    body: list[str] = []
    for index, (name, code, colour, role) in enumerate(PALETTE):
        cx = left + index % per_row * column + column / 2
        cy = top + index // per_row * row_height
        body.append(swatch(cx - size / 2, cy, size, colour))
        body.append(_text(cx, cy + size + 18, name, size=13,
                          weight="bold"))
        body.append(_text(cx, cy + size + 36, f"\\x1b[{code}m", size=12,
                          fill="muted"))
        body.append(_text(cx, cy + size + 54, role, size=12,
                          fill="muted"))
    rows = (len(PALETTE) + per_row - 1) // per_row
    width = left * 2 + per_row * column
    return _svg(width, top + (rows - 1) * row_height + size + 76, body)


def line_svg() -> str:
    """Mostra que cada posição do desenho é uma sequência SGR e 2 espaços.

    A linha é a segunda do desenho do labirinto 3x2 com o caminho oculto.

    Returns:
        O documento SVG.
    """
    codes = (47, 45, 49, 49, 49, 49, 47)
    colours = {47: "white_wall", 45: "magenta", 49: "corridor"}
    column, size, left, top = 86, 50, 20, 20
    body: list[str] = []
    for index, code in enumerate(codes):
        cx = left + index * column + column / 2
        body.append(swatch(cx - size / 2, top, size, colours[code]))
        body.append(_text(cx, top + size + 18, f'"\\x1b[{code}m  "',
                          size=12, fill="text").replace(
            "<text ", '<text xml:space="preserve" style="white-space:pre" ',
            1))
    reset_x = left + len(codes) * column + 50
    body.append(_text(reset_x, top + size / 2, "fim da linha", size=12,
                      fill="muted"))
    body.append(_text(reset_x, top + size + 18, '"\\x1b[0m"', size=12,
                      fill="text"))
    width = reset_x + 70
    caption = ("cada posição: a sequência da cor e dois espaços; "
               "o reset fecha a linha")
    body.append(_text(width / 2, top + size + 50, caption, size=13,
                      fill="muted"))
    return _svg(width, top + size + 72, body)


def main() -> None:
    """Gera todas as imagens destas partes."""
    sys.path.insert(0, sys.argv[1])
    from mazegen import MazeGenerator

    save(palette_svg(), UTILS / "paleta-ansi.svg")
    save(line_svg(), UTILS / "linha-sgr.svg")

    gen = MazeGenerator(width=11, height=9, seed=3)
    gen.generate()
    rows = ["".join(format(cell, "x") for cell in row) for row in gen.grid]
    fills = {cell: "pattern" for cell in gen.pattern}
    fills[(0, 0)] = "entry"
    fills[(10, 8)] = "exit"
    labels = {(x, y): digit for y, row in enumerate(rows)
              for x, digit in enumerate(row)}
    save(maze_svg(gen.grid, cell=40, coords=True, fills=fills,
                  labels=labels,
                  caption="11 x 9, seed 3: o dígito de cada célula"),
         OUTPUT / "arquivo-11x9.svg")

    small = grid_from_hex(["913", "c46"])
    path = walk((0, 0), "EES")
    save(maze_svg(small, cell=72, path=path,
                  fills={(0, 0): "entry", (2, 1): "exit"},
                  labels={cell: str(index)
                          for index, cell in enumerate(path)},
                  caption="EES vira 4 células: path()[0] a path()[3]"),
         OUTPUT / "caminho-3x2.svg")


if __name__ == "__main__":
    main()
