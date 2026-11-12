"""Gera as imagens da introdução e da parte 1 (entendendo o problema).

Uso, na pasta tutorial/:

    python3 scripts/imagens_introducao.py <raiz de uma implementação pronta>

A implementação fornece o pacote mazegen, que gera os labirintos reais.
"""

from __future__ import annotations

import sys
from pathlib import Path

from svg import (
    blocks_svg,
    cell_bits_svg,
    grid_from_hex,
    maze_svg,
    save,
)

OUT = Path(__file__).resolve().parent.parent / "static" / "img" / "problema"
STEP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
GLYPHS = ("X...XXX", "X.....X", "XXX.XXX", "..X.X..", "..X.XXX")


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


def render_rows(grid: list[list[int]], entry: tuple[int, int],
                exit_: tuple[int, int], path: list[tuple[int, int]],
                visible: bool) -> list[list[str]]:
    """Reproduz as cores do desenho do terminal, posição por posição.

    Args:
        grid: Grade de bits.
        entry: Entrada.
        exit_: Saída.
        path: Células do caminho.
        visible: Caminho visível.

    Returns:
        A matriz de cores, (2H+1) x (2W+1).
    """
    height, width = len(grid), len(grid[0])
    on_path = set(path) if visible else set()
    steps = set(zip(path, path[1:])) if visible else set()
    rows: list[list[str]] = []
    for py in range(2 * height + 1):
        row: list[str] = []
        for px in range(2 * width + 1):
            x, y = px // 2, py // 2
            if px % 2 == 0 and py % 2 == 0:
                name = "white_wall"
            elif px % 2 == 1 and py % 2 == 1:
                if (x, y) == entry:
                    name = "magenta"
                elif (x, y) == exit_:
                    name = "red"
                elif (x, y) in on_path:
                    name = "cyan"
                else:
                    name = "corridor"
            elif py % 2 == 0:
                closed = y == height or grid[y][x] & 1
                pair = ((x, y - 1), (x, y))
                if closed:
                    name = "white_wall"
                elif pair in steps or pair[::-1] in steps:
                    name = "cyan"
                else:
                    name = "corridor"
            else:
                closed = x == width or grid[y][x] & 8
                pair = ((x - 1, y), (x, y))
                if closed:
                    name = "white_wall"
                elif pair in steps or pair[::-1] in steps:
                    name = "cyan"
                else:
                    name = "corridor"
            row.append(name)
        rows.append(row)
    return rows


def main() -> None:
    """Gera todas as imagens desta parte."""
    sys.path.insert(0, sys.argv[1])
    from mazegen import MazeGenerator

    closed = [[15] * 6 for _ in range(4)]
    save(maze_svg(closed, coords=True, cell=44, labels={
        (0, 0): "0,0", (5, 0): "5,0", (2, 1): "2,1", (0, 3): "0,3",
        (5, 3): "5,3"}, caption="x é a coluna, y é a linha"),
        OUT / "coordenadas.svg")

    save(cell_bits_svg(9, caption="Norte e Oeste fechados: 1 + 8 = 9"),
         OUT / "celula-9.svg")
    save(cell_bits_svg(15, caption="tudo fechado: 1 + 2 + 4 + 8 = 15"),
         OUT / "celula-15.svg")

    save(maze_svg([[15, 15]], cell=90, labels={(0, 0): "3,4", (1, 0): "4,4"},
                  fills={(0, 0): "highlight", (1, 0): "visited"},
                  caption="a parede do meio é o Leste de (3,4) "
                          "e o Oeste de (4,4)"),
         OUT / "parede-compartilhada.svg")

    small = grid_from_hex(["d53", "d56"])
    small_path = walk((0, 0), "EESWW")
    save(maze_svg(small, cell=64, coords=True,
                  fills={(0, 0): "entry", (0, 1): "exit"},
                  labels={(0, 0): "d", (1, 0): "5", (2, 0): "3",
                          (0, 1): "d", (1, 1): "5", (2, 1): "6"},
                  caption="d53 / d56: entrada em magenta, saída em vermelho"),
         OUT / "exemplo-3x2.svg")
    save(maze_svg(small, cell=64, path=small_path,
                  fills={(0, 0): "entry", (0, 1): "exit"},
                  caption="o caminho EESWW"),
         OUT / "exemplo-3x2-caminho.svg")

    for perfect, name in ((True, "perfeito-6x4"), (False, "pacman-6x4")):
        gen = MazeGenerator(width=6, height=4, perfect=perfect, seed=7)
        gen.generate()
        save(maze_svg(gen.grid, cell=48, fills={(0, 0): "entry",
                                                (5, 3): "exit"}),
             OUT / f"{name}.svg")

    glyph = [[0] * 7 for _ in range(5)]
    fills = {(dx, dy): "pattern" for dy, row in enumerate(GLYPHS)
             for dx, char in enumerate(row) if char == "X"}
    save(maze_svg(glyph, cell=40, show_open=True, coords=True, wall=0,
                  fills=fills, caption="18 células num bloco de 7 x 5"),
         OUT / "glifo-42.svg")

    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate()
    fills = {cell: "pattern" for cell in gen.pattern}
    fills[(0, 0)] = "entry"
    fills[(19, 14)] = "exit"
    save(maze_svg(gen.grid, cell=28, wall=3, fills=fills,
                  caption="20 x 15, modo Pac-Man, seed 42"),
         OUT / "labirinto-20x15.svg")
    save(maze_svg(gen.grid, cell=28, wall=3, fills=fills,
                  path=walk((0, 0), gen.solution),
                  caption="o mesmo labirinto com o caminho mais curto"),
         OUT / "labirinto-20x15-caminho.svg")

    for visible, name in ((False, "desenho-3x2"),
                          (True, "desenho-3x2-caminho")):
        rows = render_rows(small, (0, 0), (0, 1), small_path, visible)
        save(blocks_svg(rows, size=34,
                        caption="caminho visível" if visible
                        else "caminho oculto"),
             OUT / f"{name}.svg")

    kinds = [["wall" if px % 2 == 0 and py % 2 == 0 else
              "highlight" if px % 2 == 1 and py % 2 == 1 else "stack"
              for px in range(7)] for py in range(5)]
    save(blocks_svg(kinds, size=40, gap=4,
                    caption="amarelo: célula · azul: parede · "
                            "escuro: canto"),
         OUT / "posicoes.svg")


if __name__ == "__main__":
    main()
