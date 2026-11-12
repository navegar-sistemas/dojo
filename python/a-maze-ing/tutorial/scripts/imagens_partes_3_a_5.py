"""Gera as imagens das partes 4 (value objects) e 5 (a entidade Maze).

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_3_a_5.py <raiz de uma implementação pronta>

A implementação fornece o pacote mazegen: Direction, Cell, Pattern42 e Maze
reais calculam o que cada imagem mostra.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Sequence
from pathlib import Path

from svg import COLORS, _caption_overflow, _svg, _text, color, maze_svg, save

ROOT = Path(__file__).resolve().parent.parent / "static" / "img"
OUT_VO = ROOT / "value-objects"
OUT_MAZE = ROOT / "maze"

Pos = tuple[int, int]


def board_svg(
    width: int,
    height: int,
    *,
    cell: int = 60,
    fills: dict[Pos, str] | None = None,
    labels: dict[Pos, Sequence[str]] | None = None,
    ghosts: Sequence[Pos] = (),
    arrows: Sequence[tuple[Pos, Pos]] = (),
    blocks: Sequence[tuple[int, int, int, int]] = (),
    coords: bool = True,
    caption: str | None = None,
) -> str:
    """Desenha uma grade de posições, sem paredes de labirinto.

    Args:
        width: Colunas da grade.
        height: Linhas da grade.
        cell: Lado de uma célula, em pixels.
        fills: Cor de fundo de algumas células.
        labels: Linhas de texto no centro de algumas células.
        ghosts: Posições fora da grade, desenhadas tracejadas.
        arrows: Setas entre centros de células.
        blocks: Retângulos tracejados (x, y, largura, altura), em células.
        coords: Escreve o número das colunas e das linhas.
        caption: Legenda abaixo do desenho.

    Returns:
        O documento SVG.
    """
    every = [(x, y) for y in range(height) for x in range(width)]
    every += list(ghosts)
    min_x = min(x for x, _ in every)
    min_y = min(y for _, y in every)
    max_x = max(x for x, _ in every)
    max_y = max(y for _, y in every)
    pad = 34 if coords else 16
    drawing_w = pad + (max_x - min_x + 1) * cell + 16
    left = pad + _caption_overflow(drawing_w, caption) / 2
    top = pad
    total_w = left + (max_x - min_x + 1) * cell + 16 + (left - pad)
    total_h = top + (max_y - min_y + 1) * cell + (40 if caption else 16)

    def corner(x: int, y: int) -> tuple[float, float]:
        return left + (x - min_x) * cell, top + (y - min_y) * cell

    def centre(x: int, y: int) -> tuple[float, float]:
        cx, cy = corner(x, y)
        return cx + cell / 2, cy + cell / 2

    body: list[str] = [
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["wall"]}"/>'
        "</marker></defs>"
    ]
    fills = fills or {}
    for x, y in every:
        cx, cy = corner(x, y)
        ghost = not (0 <= x < width and 0 <= y < height)
        fill = color(fills.get((x, y), "background"))
        dash = ' stroke-dasharray="6 5"' if ghost else ""
        body.append(
            f'<rect x="{cx:g}" y="{cy:g}" width="{cell}" height="{cell}" '
            f'fill="{fill}" stroke="{COLORS["muted"] if ghost else "#d1d5db"}"'
            f' stroke-width="{2 if ghost else 1.5}"{dash}/>'
        )
    gx, gy = corner(0, 0)
    body.append(
        f'<rect x="{gx:g}" y="{gy:g}" width="{width * cell}" '
        f'height="{height * cell}" fill="none" stroke="{COLORS["wall"]}" '
        f'stroke-width="3"/>'
    )
    for bx, by, bw, bh in blocks:
        cx, cy = corner(bx, by)
        body.append(
            f'<rect x="{cx:g}" y="{cy:g}" width="{bw * cell}" '
            f'height="{bh * cell}" fill="none" stroke="{COLORS["exit"]}" '
            f'stroke-width="2.5" stroke-dasharray="7 5"/>'
        )
    for start, end in arrows:
        x1, y1 = centre(*start)
        x2, y2 = centre(*end)
        shrink = cell * 0.22
        dx = (x2 - x1) / max(abs(x2 - x1) + abs(y2 - y1), 1)
        dy = (y2 - y1) / max(abs(x2 - x1) + abs(y2 - y1), 1)
        body.append(
            f'<line x1="{x1 + dx * shrink:g}" y1="{y1 + dy * shrink:g}" '
            f'x2="{x2 - dx * shrink * 1.6:g}" y2="{y2 - dy * shrink * 1.6:g}" '
            f'stroke="{COLORS["wall"]}" stroke-width="2.5" '
            f'marker-end="url(#arrow)"/>'
        )
    for (x, y), lines in (labels or {}).items():
        cx, cy = centre(x, y)
        size = cell * (0.2 if len(lines) > 1 else 0.26)
        first = cy - (len(lines) - 1) * size * 0.65
        for index, value in enumerate(lines):
            body.append(_text(cx, first + index * size * 1.3, value,
                              size=size, weight="bold" if index == 0
                              else "normal"))
    if coords:
        for x in range(width):
            cx, _ = centre(x, 0)
            body.append(_text(cx, top - 14, str(x),
                              size=12, fill="muted"))
        for y in range(height):
            _, cy = centre(0, y)
            body.append(_text(left - 16, cy, str(y), size=12, fill="muted"))
    if caption:
        body.append(_text(total_w / 2, total_h - 20, caption, size=13,
                          fill="muted"))
    return _svg(total_w, total_h, body)


def border_only(width: int, height: int) -> list[list[int]]:
    """Grade sem paredes internas, só com a borda fechada.

    Args:
        width: Colunas.
        height: Linhas.

    Returns:
        A grade de bits.
    """
    grid = [[0] * width for _ in range(height)]
    for x in range(width):
        grid[0][x] |= 1
        grid[height - 1][x] |= 4
    for y in range(height):
        grid[y][0] |= 8
        grid[y][width - 1] |= 2
    return grid


def direction_images() -> None:
    """Imagens de Direction e Cell."""
    from mazegen.value_objects.cell import Cell
    from mazegen.value_objects.direction import Direction

    centre = (1, 1)
    labels: dict[Pos, Sequence[str]] = {centre: ["célula", "atual"]}
    arrows: list[tuple[Pos, Pos]] = []
    fills: dict[Pos, str] = {centre: "current"}
    for side in Direction:
        target = (1 + side.dx, 1 + side.dy)
        labels[target] = [side.name, f"dx {side.dx:+d}, dy {side.dy:+d}"
                          .replace("+0", "0")]
        fills[target] = "visited"
        arrows.append((centre, target))
    save(board_svg(3, 3, cell=120, fills=fills, labels=labels,
                   arrows=arrows, coords=False,
                   caption="um passo para cada lado: x soma dx, y soma dy"),
         OUT_VO / "direction-deltas.svg")

    start = Cell(3, 4)
    labels = {start.as_tuple(): ["3,4"]}
    fills = {start.as_tuple(): "current"}
    arrows = []
    for side in Direction:
        other = start.step(side)
        labels[other.as_tuple()] = [f"{other.x},{other.y}", side.letter]
        fills[other.as_tuple()] = "visited"
        arrows.append((start.as_tuple(), other.as_tuple()))
    save(board_svg(6, 6, cell=64, fills=fills, labels=labels, arrows=arrows,
                   caption="Cell(3, 4).step(d) para cada Direction"),
         OUT_VO / "cell-step.svg")

    corner = Cell(0, 0)
    labels = {(0, 0): ["0,0"]}
    fills = {(0, 0): "current"}
    arrows = []
    ghosts: list[Pos] = []
    for side in Direction:
        other = corner.step(side)
        labels[other.as_tuple()] = [f"{other.x},{other.y}", side.letter]
        arrows.append(((0, 0), other.as_tuple()))
        if 0 <= other.x < 4 and 0 <= other.y < 3:
            fills[other.as_tuple()] = "visited"
        else:
            ghosts.append(other.as_tuple())
    save(board_svg(4, 3, cell=64, fills=fills, labels=labels, arrows=arrows,
                   ghosts=ghosts, coords=False,
                   caption="step não confere limites: (0,-1) e (-1,0) "
                           "ficam fora da grade"),
         OUT_VO / "cell-step-canto.svg")


def pattern_images() -> None:
    """Imagens do Pattern42 em três tamanhos de grade."""
    from mazegen.value_objects.pattern42 import (
        GLYPHS,
        PATTERN_HEIGHT,
        PATTERN_WIDTH,
        Pattern42,
    )

    for width, height, size in ((9, 7, 44), (20, 15, 30)):
        pattern = Pattern42.for_size(width, height)
        x0 = (width - PATTERN_WIDTH) // 2
        y0 = (height - PATTERN_HEIGHT) // 2
        fills: dict[Pos, str] = {
            c.as_tuple(): "pattern" for c in pattern.cells
        }
        save(board_svg(width, height, cell=size, fills=fills,
                       labels={(x0, y0): [f"{x0},{y0}"]},
                       blocks=[(x0, y0, PATTERN_WIDTH, PATTERN_HEIGHT)],
                       caption=f"{width} x {height}: x0 = {x0}, y0 = {y0}, "
                               f"{len(pattern.cells)} células"),
             OUT_VO / f"pattern42-{width}x{height}.svg")

    width, height = 8, 7
    x0 = (width - PATTERN_WIDTH) // 2
    y0 = (height - PATTERN_HEIGHT) // 2
    fills = {(x0 + dx, y0 + dy): "highlight"
             for dy, row in enumerate(GLYPHS)
             for dx, char in enumerate(row) if char == "X"}
    assert not Pattern42.for_size(width, height)
    save(board_svg(width, height, cell=44, fills=fills,
                   blocks=[(x0, y0, PATTERN_WIDTH, PATTERN_HEIGHT)],
                   caption="8 x 7: o bloco encostaria na borda esquerda; "
                           "o padrão fica vazio"),
         OUT_VO / "pattern42-8x7.svg")


def maze_images() -> None:
    """Imagens da entidade Maze."""
    from mazegen.entities.maze import Maze
    from mazegen.services.carver import Carver
    from mazegen.value_objects.cell import Cell
    from mazegen.value_objects.direction import Direction as D
    from mazegen.value_objects.pattern42 import Pattern42

    def new(width: int, height: int) -> Maze:
        return Maze(width, height, Pattern42.for_size(width, height))

    def values(maze: Maze) -> dict[Pos, str]:
        return {(x, y): str(bits) for y, row in enumerate(maze.rows())
                for x, bits in enumerate(row)}

    m = new(3, 2)
    save(maze_svg(m.rows(), cell=72, coords=True, show_open=True,
                  labels=values(m), caption="Maze(3, 2, ...): tudo vale 15"),
         OUT_MAZE / "abrir-antes.svg")
    m.open_wall(Cell(0, 0), D.EAST)
    save(maze_svg(m.rows(), cell=72, coords=True, show_open=True,
                  labels=values(m),
                  fills={(0, 0): "highlight", (1, 0): "highlight"},
                  caption="open_wall(Cell(0, 0), EAST): 15 - 2 = 13 "
                          "e 15 - 8 = 7"),
         OUT_MAZE / "abrir-depois.svg")

    m9 = new(9, 7)
    fills: dict[Pos, str] = {c.as_tuple(): "pattern"
                             for c in m9.pattern.cells}
    fills[(0, 1)] = "current"
    labels: dict[Pos, str] = {}
    for side in D:
        other = m9.neighbour(Cell(0, 1), side)
        if other is not None:
            fills[other.as_tuple()] = "visited"
            labels[other.as_tuple()] = side.letter
    labels[(1, 1)] = "E"
    save(maze_svg(m9.rows(), cell=44, coords=True, fills=fills,
                  labels=labels,
                  caption="vizinhos de (0,1): N e S existem; E (42) e "
                          "W (fora) dão None"),
         OUT_MAZE / "vizinhos-9x7.svg")

    found = None
    for seed in range(200):
        maze = new(9, 7)
        Carver().carve(maze, Cell(0, 0), random.Random(seed))
        real = maze.dead_ends()
        enclosed = [c for c in maze.cells()
                    if len(maze.passages(c)) == 1 and not maze.closed_sides(c)]
        if len(real) <= 6 and len(enclosed) == 2:
            found = maze, real, enclosed
            break
    assert found is not None
    maze, real, enclosed = found
    fills = {c.as_tuple(): "pattern" for c in maze.pattern.cells}
    fills.update({c.as_tuple(): "current" for c in real})
    fills.update({c.as_tuple(): "highlight" for c in enclosed})
    save(maze_svg(maze.rows(), cell=44, coords=True, fills=fills,
                  caption=f"laranja: {len(real)} becos reais · amarelo: "
                          f"{len(enclosed)} becos cercados pelo 42"),
         OUT_MAZE / "becos-9x7.svg")

    snake = new(3, 2)
    for cell, side in [(Cell(0, 0), D.EAST), (Cell(1, 0), D.EAST),
                       (Cell(2, 0), D.SOUTH), (Cell(2, 1), D.WEST),
                       (Cell(1, 1), D.WEST)]:
        snake.open_wall(cell, side)
    save(maze_svg(snake.rows(), cell=72, coords=True, show_open=True,
                  fills={(0, 0): "current", (0, 1): "current"},
                  caption=f"6 células, 5 passagens: "
                          f"{snake.loop_count()} ciclos, 2 becos reais"),
         OUT_MAZE / "ciclos-serpentina.svg")
    snake.open_wall(Cell(0, 0), D.SOUTH)
    snake.open_wall(Cell(1, 0), D.SOUTH)
    save(maze_svg(snake.rows(), cell=72, coords=True, show_open=True,
                  caption=f"6 células, 7 passagens: 7 - 6 + 1 = "
                          f"{snake.loop_count()} ciclos"),
         OUT_MAZE / "ciclos-dois.svg")

    m3 = new(3, 3)
    for y in range(3):
        for x in range(3):
            if x < 2:
                m3.open_wall(Cell(x, y), D.EAST)
            if y < 2:
                m3.open_wall(Cell(x, y), D.SOUTH)
    assert m3.has_open_3x3()
    save(maze_svg(m3.rows(), cell=64, coords=True, show_open=True,
                  fills={(x, y): "highlight" for x in range(3)
                         for y in range(3)},
                  caption="as 12 paredes internas abertas: proibido"),
         OUT_MAZE / "janela-3x3-aberta.svg")
    m3.close_wall(Cell(1, 1), D.EAST)
    assert not m3.has_open_3x3()
    save(maze_svg(m3.rows(), cell=64, coords=True, show_open=True,
                  fills={(1, 1): "visited", (2, 1): "visited"},
                  caption="uma parede interna fechada já basta"),
         OUT_MAZE / "janela-3x3-fechada.svg")

    window = border_only(5, 4)
    save(maze_svg(window, cell=56, coords=True, show_open=True, wall=4,
                  fills={(x, y): "highlight" for x in range(1, 4)
                         for y in range(0, 3)},
                  caption="5 x 4 tem 3 x 2 = 6 janelas; esta começa "
                          "em (1, 0)"),
         OUT_MAZE / "janelas-5x4.svg")


def main() -> None:
    """Gera todas as imagens das partes 4 e 5."""
    sys.path.insert(0, sys.argv[1])
    direction_images()
    pattern_images()
    maze_images()


if __name__ == "__main__":
    main()
