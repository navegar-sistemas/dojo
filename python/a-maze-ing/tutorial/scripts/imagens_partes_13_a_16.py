"""Gera as imagens das partes 13 (desenho), 14 (menu) e 16 (bônus).

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_13_a_16.py <raiz da implementação>

A implementação fornece o mazegen e o amazeing reais: os desenhos do
terminal saem do RenderService, lido de volta código ANSI por código ANSI.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Sequence
from html import escape
from pathlib import Path
from typing import Any

from svg import _svg, _text, bits_svg, color, maze_svg, save

IMG = Path(__file__).resolve().parent.parent / "static" / "img"
TELA = IMG / "tela"
MENU = IMG / "menu"
BONUS = IMG / "bonus"

# A darker grey than COLORS["grey"]: next to the light walls, the cells of
# the "42" must stand out, as code 100 does in a real terminal.
TERMINAL_GREY = "#6b7280"
SGR_COLOUR = {
    47: "white_wall",
    43: "yellow_wall",
    42: "green_wall",
    44: "blue_wall",
    100: TERMINAL_GREY,
    45: "magenta",
    41: "red",
    46: "cyan",
    49: "corridor",
}
SGR = re.compile(r"\x1b\[(\d+)m  ")


def ansi_rows(lines: Sequence[str]) -> list[list[str]]:
    """Lê as linhas do RenderService e devolve a cor de cada posição.

    Args:
        lines: Linhas devolvidas por RenderService.render.

    Returns:
        rows[py][px] com o nome da cor na paleta do svg.py.
    """
    return [[SGR_COLOUR[int(code)] for code in SGR.findall(line)]
            for line in lines]


def panels_svg(panels: Sequence[tuple[list[list[str]], str]], *,
               size: int, columns: int,
               outlines: Sequence[set[tuple[int, int]]] = ()) -> str:
    """Desenha vários desenhos de terminal lado a lado, cada um com legenda.

    Args:
        panels: Pares (rows, legenda).
        size: Lado de cada posição.
        columns: Quantos painéis por linha.
        outlines: Por painel, as posições (px, py) contornadas em laranja.

    Returns:
        O documento SVG.
    """
    pad, gap, label_h = 16, 24, 26
    pw = len(panels[0][0][0]) * size
    ph = len(panels[0][0]) * size
    rows_n = (len(panels) + columns - 1) // columns
    total_w = pad * 2 + columns * pw + (columns - 1) * gap
    total_h = pad * 2 + rows_n * (ph + label_h) + (rows_n - 1) * gap
    body: list[str] = []
    for index, (rows, label) in enumerate(panels):
        ox = pad + (index % columns) * (pw + gap)
        oy = pad + (index // columns) * (ph + label_h + gap)
        for py, row in enumerate(rows):
            for px, name in enumerate(row):
                body.append(
                    f'<rect x="{ox + px * size:g}" y="{oy + py * size:g}" '
                    f'width="{size}" height="{size}" fill="{color(name)}" '
                    f'stroke="#d1d5db" stroke-width="0.5"/>'
                )
        marked = outlines[index] if index < len(outlines) else set()
        for px, py in sorted(marked):
            body.append(
                f'<rect x="{ox + px * size + 1.5:g}" '
                f'y="{oy + py * size + 1.5:g}" width="{size - 3:g}" '
                f'height="{size - 3:g}" fill="none" '
                f'stroke="{color("current")}" stroke-width="3"/>'
            )
        body.append(
            f'<rect x="{ox - 1.5:g}" y="{oy - 1.5:g}" width="{pw + 3:g}" '
            f'height="{ph + 3:g}" fill="none" stroke="{color("muted")}" '
            f'stroke-width="1.5"/>'
        )
        body.append(_text(ox + pw / 2, oy + ph + label_h / 2 + 2, label,
                          size=13, fill="muted"))
    return _svg(total_w, total_h, body)


def labeled_blocks_svg(rows: Sequence[Sequence[str]],
                       labels: dict[tuple[int, int], str], *, size: int,
                       caption: str, gap: float = 4,
                       axes: bool = True) -> str:
    """Desenha a grade de posições com texto em algumas posições.

    Args:
        rows: rows[py][px] com o nome da cor de cada posição.
        labels: Texto por posição (px, py).
        size: Lado de cada quadrado.
        caption: Legenda abaixo do desenho.
        gap: Espaço entre quadrados.
        axes: Numera as colunas px em cima e as linhas py à esquerda, com
            o nome de cada eixo.

    Returns:
        O documento SVG.
    """
    margin = 64 if axes else 16
    top = 58 if axes else 16
    width = len(rows[0]) * size
    total_w = max(margin + width + 16, len(caption) * 7.4 + 40)
    left = margin + (total_w - (margin + width + 16)) / 2
    body: list[str] = []
    for py, row in enumerate(rows):
        for px, name in enumerate(row):
            body.append(
                f'<rect x="{left + px * size + gap / 2:g}" '
                f'y="{top + py * size + gap / 2:g}" '
                f'width="{size - gap:g}" height="{size - gap:g}" '
                f'fill="{color(name)}" stroke="#e5e7eb" stroke-width="1"/>'
            )
    for (px, py), value in labels.items():
        dark = rows[py][px] in ("wall", "corridor", "blue_wall")
        body.append(_text(left + px * size + size / 2,
                          top + py * size + size / 2, value,
                          size=size * 0.26, weight="bold",
                          fill="#ffffff" if dark else "text"))
    if axes:
        for px in range(len(rows[0])):
            body.append(_text(left + px * size + size / 2, top - 14, str(px),
                              size=12, fill="muted"))
        for py in range(len(rows)):
            body.append(_text(left - 18, top + py * size + size / 2,
                              str(py), size=12, fill="muted"))
        body.append(_text(left + width / 2, top - 38,
                          "px: coluna do desenho →", size=13,
                          weight="bold"))
        middle = top + len(rows) * size / 2
        body.append(
            f'<g transform="rotate(90 {left - 42:g} {middle:g})">'
            + _text(left - 42, middle, "py: linha do desenho →", size=13,
                    weight="bold")
            + "</g>"
        )
    total_h = top + len(rows) * size + 46
    body.append(_text(total_w / 2, total_h - 22, caption, size=13,
                      fill="muted"))
    return _svg(total_w, total_h, body)


def terminal_svg(before: Sequence[str], rows: Sequence[Sequence[str]],
                 after: Sequence[str], *, size: int) -> str:
    """Desenha uma tela de terminal: texto, o desenho colorido e mais texto.

    Args:
        before: Linhas de texto acima do desenho.
        rows: rows[py][px] com o nome da cor de cada posição.
        after: Linhas de texto abaixo do desenho.
        size: Lado de cada posição.

    Returns:
        O documento SVG.
    """
    pad, line_h = 18, 20
    text_w = max(len(line) for line in [*before, *after]) * 8.4
    total_w = pad * 2 + max(len(rows[0]) * size, text_w)
    total_h = (pad * 2 + (len(before) + len(after)) * line_h
               + len(rows) * size)
    body = [f'<rect width="{total_w:g}" height="{total_h:g}" '
            f'fill="{color("corridor")}" rx="8"/>']
    mono = 'font-family="ui-monospace, Menlo, Consolas, monospace"'

    def text(y: float, value: str) -> str:
        return (f'<text x="{pad}" y="{y:g}" {mono} font-size="14" '
                f'fill="#e5e7eb" dominant-baseline="central" '
                f'xml:space="preserve">{escape(value)}</text>')

    y = pad + line_h / 2
    for line in before:
        body.append(text(y, line))
        y += line_h
    top = y - line_h / 2
    for py, row in enumerate(rows):
        for px, name in enumerate(row):
            body.append(
                f'<rect x="{pad + px * size:g}" y="{top + py * size:g}" '
                f'width="{size}" height="{size}" fill="{color(name)}"/>'
            )
    y = top + len(rows) * size + line_h / 2
    for line in after:
        body.append(text(y, line))
        y += line_h
    return _svg(total_w, total_h, body)


def position_kinds(grid: Sequence[Sequence[int]]) -> list[list[str]]:
    """Classifica cada posição do desenho pelo tipo, não pela cor final.

    Args:
        grid: grid[y][x] com as paredes fechadas.

    Returns:
        rows[py][px]: "wall" para canto, "stack" para parede fechada,
        "visited" para passagem aberta e "highlight" para célula.
    """
    height, width = len(grid), len(grid[0])
    rows = [["stack"] * (2 * width + 1) for _ in range(2 * height + 1)]
    for py in range(0, 2 * height + 1, 2):
        for px in range(0, 2 * width + 1, 2):
            rows[py][px] = "wall"
    for y in range(height):
        for x in range(width):
            rows[2 * y + 1][2 * x + 1] = "highlight"
            if not grid[y][x] & 2:
                rows[2 * y + 1][2 * x + 2] = "visited"
            if not grid[y][x] & 4:
                rows[2 * y + 2][2 * x + 1] = "visited"
    return rows


def render_steps(maze: Any, wall: str) -> list[tuple[list[list[str]], str]]:
    """Refaz as quatro etapas do render, uma tela por etapa.

    Args:
        maze: GeneratedMaze.
        wall: Nome da cor das paredes.

    Returns:
        Quatro pares (rows, legenda), um por etapa do render.
    """
    grid = maze.grid
    height, width = len(grid), len(grid[0])
    canvas = [[wall] * (2 * width + 1) for _ in range(2 * height + 1)]
    steps = [([row[:] for row in canvas], "1. tudo na cor das paredes")]
    for y, row in enumerate(grid):
        for x, walls in enumerate(row):
            canvas[2 * y + 1][2 * x + 1] = (
                TERMINAL_GREY if (x, y) in maze.pattern else "corridor")
            if not walls & 2:
                canvas[2 * y + 1][2 * x + 2] = "corridor"
            if not walls & 4:
                canvas[2 * y + 2][2 * x + 1] = "corridor"
    steps.append(([row[:] for row in canvas], "2. células e paredes abertas"))
    path = maze.path()
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        canvas[y1 + y2 + 1][x1 + x2 + 1] = "cyan"
        canvas[2 * y2 + 1][2 * x2 + 1] = "cyan"
    steps.append(([row[:] for row in canvas], "3. caminho em ciano"))
    ex, ey = maze.entry
    sx, sy = maze.exit
    canvas[2 * ey + 1][2 * ex + 1] = "magenta"
    canvas[2 * sy + 1][2 * sx + 1] = "red"
    steps.append(([row[:] for row in canvas], "4. entrada e saída por cima"))
    return steps


def enclosed_and_real(grid: Sequence[Sequence[int]],
                      pattern: set[tuple[int, int]]
                      ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Separa os becos reais dos becos cercados pelo "42" e pela borda.

    Args:
        grid: grid[y][x] com as paredes fechadas.
        pattern: Células do "42".

    Returns:
        (reais, cercados).
    """
    height, width = len(grid), len(grid[0])
    steps = {1: (0, -1), 2: (1, 0), 4: (0, 1), 8: (-1, 0)}
    real: list[tuple[int, int]] = []
    enclosed: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if (x, y) in pattern:
                continue
            walls = grid[y][x]
            if sum(1 for bit in steps if not walls & bit) != 1:
                continue
            openable = any(
                walls & bit and 0 <= x + dx < width and 0 <= y + dy < height
                and (x + dx, y + dy) not in pattern
                for bit, (dx, dy) in steps.items())
            (real if openable else enclosed).append((x, y))
    return real, enclosed


def stuck_dead_end(root: str) -> list[list[int]]:
    """Monta, com o Maze real, um beco que o braiding não consegue abrir.

    Grade 5x3 com todas as paredes internas abertas, menos o Leste e o
    Oeste da célula (2, 2): ela fica com uma passagem só, para o Norte.

    Args:
        root: Raiz da implementação (só para a mensagem de erro).

    Returns:
        A grade de bits.

    Raises:
        SystemExit: O Maze real não confirma o que o texto afirma.
    """
    from mazegen.entities.maze import Maze
    from mazegen.value_objects.cell import Cell
    from mazegen.value_objects.direction import Direction
    from mazegen.value_objects.pattern42 import Pattern42

    maze = Maze(5, 3, Pattern42.for_size(5, 3))
    for cell in list(maze.cells()):
        for side in (Direction.EAST, Direction.SOUTH):
            if maze.neighbour(cell, side) is not None:
                maze.open_wall(cell, side)
    stuck = Cell(2, 2)
    maze.close_wall(stuck, Direction.EAST)
    maze.close_wall(stuck, Direction.WEST)
    blocked = []
    for side in maze.closed_sides(stuck):
        maze.open_wall(stuck, side)
        blocked.append(maze.has_open_3x3())
        maze.close_wall(stuck, side)
    if (maze.dead_ends() != [stuck] or maze.has_open_3x3()
            or blocked != [True, True]):
        raise SystemExit(f"{root}: o beco preso não se confirmou")
    return maze.rows()


def main() -> None:
    """Gera todas as imagens das partes 13 a 16."""
    root = sys.argv[1]
    sys.path.insert(0, root)
    from amazeing.domain.entities.view_state import ViewState
    from amazeing.domain.value_objects.generated_maze import GeneratedMaze
    from amazeing.services.render_service import RenderService
    from mazegen import MazeGenerator

    def build(width: int, height: int, perfect: bool,
              seed: int) -> GeneratedMaze:
        gen = MazeGenerator(width, height, perfect=perfect, seed=seed)
        gen.generate()
        return GeneratedMaze.from_generator(gen, (0, 0),
                                            (width - 1, height - 1))

    small = build(4, 3, True, 1)
    save(maze_svg([list(r) for r in small.grid], cell=60, coords=True,
                  fills={small.entry: "entry", small.exit: "exit"},
                  caption="labirinto perfeito 4 x 3"),
         TELA / "labirinto-4x3.svg")
    kinds = position_kinds(small.grid)
    labels = {(2 * x + 1, 2 * y + 1): f"{x},{y}"
              for y in range(3) for x in range(4)}
    save(labeled_blocks_svg(
        kinds, labels, size=46,
        caption="amarelo: célula · escuro: canto · azul: parede fechada · "
                "verde: parede aberta"),
         TELA / "posicoes-4x3.svg")

    save(panels_svg(render_steps(small, "white_wall"), size=22, columns=2),
         TELA / "etapas-4x3.svg")

    first = small.grid[0][0]
    save(bits_svg(first), TELA / f"bits-{first}.svg")
    around = [["wall", "stack", "wall"],
              ["stack", "highlight", "stack"],
              ["wall", "stack", "wall"]]
    if not first & 2:
        around[1][2] = "visited"
    if not first & 4:
        around[2][1] = "visited"
    save(labeled_blocks_svg(
        around, {(1, 1): "0,0", (1, 0): "N", (2, 1): "E", (1, 2): "S",
                 (0, 1): "W"}, size=70,
        caption=f"célula 0,0 = {first}: Leste aberto (verde), "
                f"Sul fechado (azul)"),
         TELA / "leitura-0-0.svg")

    path = small.path()
    save(maze_svg([list(r) for r in small.grid], cell=60, coords=True,
                  fills={small.entry: "entry", small.exit: "exit"},
                  path=path,
                  labels={cell: str(i) for i, cell in enumerate(path)},
                  caption=f"solution = {small.solution}: "
                          f"{len(path)} células"),
         TELA / "caminho-4x3.svg")

    save(labeled_blocks_svg(
        kinds, {(3, 1): "1,0", (5, 1): "2,0", (4, 1): "?"}, size=46,
        caption="células 1,0 e 2,0: a passagem fica em "
                "px = 1 + 2 + 1 = 4, py = 0 + 0 + 1 = 1"),
         TELA / "passagem.svg")

    board = build(9, 7, False, 4)
    hidden = ViewState()
    shown = ViewState()
    shown.toggle_path()
    renderer = RenderService()
    save(panels_svg([
        (ansi_rows(renderer.render(board, hidden)), "caminho oculto"),
        (ansi_rows(renderer.render(board, shown)), "caminho visível"),
    ], size=18, columns=2), TELA / "desenho-9x7.svg")
    glyph = {(2 * x + 1, 2 * y + 1) for x, y in board.pattern}
    plain = ansi_rows(renderer.render(board, hidden))
    save(panels_svg([(plain, "como o terminal mostra"),
                     (plain, "as 18 células do 42 contornadas")],
                    size=22, columns=2, outlines=[set(), glyph]),
         TELA / "quarenta-e-dois-9x7.svg")

    menu_lines = ["=== A-Maze-ing ===", "1. Re-generate a new maze",
                  "2. Show / Hide the shortest path",
                  "3. Rotate the wall colours", "4. Quit"]
    save(terminal_svg(
        ["$ .venv/bin/python a_maze_ing.py nove.txt", ""],
        ansi_rows(renderer.render(board, hidden)),
        [*menu_lines, "Choice? (1-4): 9", "Invalid choice",
         "Choice? (1-4): 2", ""],
        size=16), MENU / "sessao-9x7.svg")
    save(terminal_svg(
        [], ansi_rows(renderer.render(board, shown)),
        [*menu_lines, "Choice? (1-4): "], size=16),
         MENU / "sessao-9x7-caminho.svg")

    panels = []
    state = ViewState()
    state.toggle_path()
    for name in ("branco", "amarelo", "verde", "azul"):
        panels.append((ansi_rows(renderer.render(board, state)),
                       f"colour_index = {state.colour_index}: {name}"))
        state.next_colour()
    save(panels_svg(panels, size=12, columns=2), TELA / "paleta-9x7.svg")

    for perfect, name, caption in (
            (True, "perfeito-20x15", "PERFECT=True, seed 42"),
            (False, "pacman-20x15", "PERFECT=False, seed 42")):
        gen = MazeGenerator(20, 15, perfect=perfect, seed=42)
        gen.generate()
        real, enclosed = enclosed_and_real(gen.grid, gen.pattern)
        fills = {cell: "pattern" for cell in gen.pattern}
        fills.update({cell: "current" for cell in real})
        fills.update({cell: "highlight" for cell in enclosed})
        fills[(0, 0)] = "entry"
        fills[(19, 14)] = "exit"
        save(maze_svg(gen.grid, cell=26, wall=3, fills=fills,
                      caption=f"{caption}: {len(real)} becos reais "
                              f"(laranja), {len(enclosed)} cercados "
                              f"pelo 42 (amarelo)"),
             BONUS / f"{name}.svg")

    stuck = stuck_dead_end(root)
    save(maze_svg(stuck, cell=60, coords=True, fills={(2, 2): "current"},
                  show_open=True,
                  caption="a célula 2,2 é beco: só a passagem Norte"),
         BONUS / "beco-preso.svg")
    for side, bit, x0, name in (("Oeste", 8, 0, "oeste"),
                                ("Leste", 2, 2, "leste")):
        opened = [row[:] for row in stuck]
        opened[2][2] &= ~bit
        nx = 1 if bit == 8 else 3
        opened[2][nx] &= ~(2 if bit == 8 else 8)
        fills = {(x, y): "highlight" for y in range(3)
                 for x in range(x0, x0 + 3)}
        fills[(2, 2)] = "current"
        save(maze_svg(opened, cell=60, coords=True, fills=fills,
                      show_open=True,
                      caption=f"abrir o {side} deixa este 3x3 todo aberto"),
             BONUS / f"beco-preso-{name}.svg")


if __name__ == "__main__":
    main()
