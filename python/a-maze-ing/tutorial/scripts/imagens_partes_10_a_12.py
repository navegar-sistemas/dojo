"""Gera as imagens das partes 10 (utilitários), 11 (configuração) e 12.

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
CONFIG = IMG / "configuracao"
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


def sequence_svg() -> str:
    """Decompõe a sequência "\\x1b[41m" nas suas quatro peças.

    Returns:
        O documento SVG.
    """
    pieces = (
        ("ESC", "\\x1b", "avisa: vem um", "comando"),
        ("[", "", "abre o", "comando"),
        ("41", "", "o número:", "fundo vermelho"),
        ("m", "", "fecha: é um", "comando de cor"),
    )
    widths = (110, 70, 110, 70)
    gap, left, top, height = 16, 30, 60, 64
    body = [_text(left, 26, 'Python: "\\x1b[41m"', size=15, weight="bold",
                  anchor="start")]
    x = float(left)
    for (label, code, first, second), width in zip(pieces, widths):
        body.append(
            f'<rect x="{x:g}" y="{top}" width="{width}" height="{height}" '
            f'rx="8" fill="{COLORS["highlight"]}" stroke="{COLORS["wall"]}" '
            f'stroke-width="2"/>'
        )
        shift = 10 if code else 0
        body.append(_text(x + width / 2, top + height / 2 - shift, label,
                          size=22, weight="bold"))
        if code:
            body.append(_text(x + width / 2, top + height / 2 + 16, code,
                              size=12, fill="muted"))
        body.append(_text(x + width / 2, top + height + 22, first, size=13))
        body.append(_text(x + width / 2, top + height + 40, second, size=13))
        x += width + gap
    sample = x + 20
    body.append(swatch(sample, top + 7, 50, "red"))
    body.append(_text(sample + 25, top + height + 22, "o que vier", size=13))
    body.append(_text(sample + 25, top + height + 40, "depois", size=13))
    return _svg(sample + 90, top + height + 64, body)


def spaces_svg() -> str:
    """Compara posições de 1 e de 2 caracteres de largura no terminal.

    Um caractere de terminal tem mais ou menos o dobro de altura que de
    largura, então 2 caracteres lado a lado formam um quadrado.

    Returns:
        O documento SVG.
    """
    char_w, char_h, top, columns, rows, panel = 13, 26, 46, 5, 3, 220
    body: list[str] = []
    panels = ((1, "1 espaço por posição"), (2, "2 espaços por posição"))
    for index, (chars, title) in enumerate(panels):
        width = chars * char_w
        middle = 20 + index * panel + panel / 2
        left = middle - columns * width / 2
        body.append(_text(middle, 22, title, size=14, weight="bold"))
        for row in range(rows):
            for column in range(columns):
                name = ("white_wall" if (row + column) % 2 == 0
                        else "corridor")
                body.append(
                    f'<rect x="{left + column * width:g}" '
                    f'y="{top + row * char_h}" width="{width}" '
                    f'height="{char_h}" fill="{COLORS[name]}" '
                    f'stroke="#9ca3af" stroke-width="0.5"/>'
                )
        caption = "retângulos altos" if chars == 1 else "quadrados"
        body.append(_text(middle, top + rows * char_h + 20, caption,
                          size=13, fill="muted"))
    return _svg(40 + len(panels) * panel, top + rows * char_h + 42, body)


def config_grid_svg(pattern: set[tuple[int, int]]) -> str:
    """Grade 20x15 com o "42" e a entrada 6,5 em cima de uma célula dele.

    Args:
        pattern: Células (x, y) do "42" numa grade 20x15.

    Returns:
        O documento SVG.
    """
    grid = [[15] * 20 for _ in range(15)]
    fills = {cell: "pattern" for cell in pattern}
    return maze_svg(grid, cell=26, wall=1.5, coords=True, fills=fills,
                    labels={(6, 5): "E"},
                    caption="20 x 15 · cinza: células do \"42\" · E: a "
                            "entrada ENTRY=6,5, em cima de uma delas")


def main() -> None:
    """Gera todas as imagens destas partes."""
    sys.path.insert(0, sys.argv[1])
    from mazegen import MazeGenerator

    save(palette_svg(), UTILS / "paleta-ansi.svg")
    save(line_svg(), UTILS / "linha-sgr.svg")
    save(sequence_svg(), UTILS / "sequencia-sgr.svg")
    save(spaces_svg(), UTILS / "um-ou-dois-espacos.svg")
    save(config_grid_svg(MazeGenerator(20, 15).pattern),
         CONFIG / "entrada-no-42.svg")

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
                  caption="11 x 9, seed 3: o dígito de cada célula · magenta: "
                          "entrada · vermelho: saída · cinza: \"42\""),
         OUTPUT / "arquivo-11x9.svg")

    small = grid_from_hex(["913", "c46"])
    path = walk((0, 0), "EES")
    save(maze_svg(small, cell=72, path=path, show_open=True,
                  fills={(0, 0): "entry", (2, 1): "exit"},
                  labels={cell: str(index)
                          for index, cell in enumerate(path)},
                  caption="tracejado: parede aberta · número: posição "
                          "na lista path()"),
         OUTPUT / "caminho-3x2.svg")


if __name__ == "__main__":
    main()
