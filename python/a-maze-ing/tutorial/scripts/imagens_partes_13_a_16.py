"""Gera as imagens das partes 13 (desenho), 14 (menu) e 16 (bônus).

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_13_a_16.py <raiz da implementação>

A implementação fornece o mazegen e o amazeing reais: os desenhos do
terminal saem do RenderService, decodificados caractere por caractere.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from svg import bits_svg, maze_svg, save
from terminal import (
    Rows,
    Spot,
    arms_table,
    decode,
    drawing_svg,
    layout_svg,
    panels_svg,
    session_svg,
)

IMG = Path(__file__).resolve().parent.parent / "static" / "img"
TELA = IMG / "tela"
MENU = IMG / "menu"
BONUS = IMG / "bonus"


def layers(renderer: Any, maze: Any, wall: Any,
           white: Any) -> tuple[list[str], list[str]]:
    """Roda as duas primeiras camadas do render, cada uma até o texto.

    Usa os métodos do próprio RenderService: _draw_walls, _fill_pattern e
    _join, nas tabelas que o render cria.

    Args:
        renderer: RenderService.
        maze: GeneratedMaze.
        wall: Cor das paredes.
        white: Cor do fundo.

    Returns:
        As linhas só com as paredes e as linhas com as paredes e o "42".
    """
    lines = 2 * len(maze.grid) + 1
    columns = 4 * len(maze.grid[0]) + 1
    chars = [[" "] * columns for _ in range(lines)]
    texts = [[wall] * columns for _ in range(lines)]
    backs = [[white] * columns for _ in range(lines)]

    def joined() -> list[str]:
        return [renderer._join(row, text_row, back_row)
                for row, text_row, back_row in zip(chars, texts, backs)]

    renderer._draw_walls(maze.grid, chars)
    walls = joined()
    renderer._fill_pattern(maze.pattern, backs)
    return walls, joined()


def interior(column: int, line: int) -> bool:
    """Diz se o caractere fica no interior de uma célula.

    Args:
        column: Coluna do desenho.
        line: Linha do desenho.

    Returns:
        True nas linhas ímpares fora das colunas múltiplas de 4.
    """
    return line % 2 == 1 and column % 4 != 0


def same_except(first: Rows, second: Rows, index: int,
                allowed: set[Spot]) -> bool:
    """Compara dois desenhos num dos campos, fora de alguns lugares.

    Args:
        first: Saída de decode.
        second: Saída de decode.
        index: 0 compara os caracteres, 1 o texto, 2 o fundo.
        allowed: Lugares (coluna, linha) que podem diferir.

    Returns:
        True se o campo é igual em todo o resto.
    """
    return all(
        a[index] == b[index] or (column, line) in allowed
        for line, (row_a, row_b) in enumerate(zip(first, second))
        for column, (a, b) in enumerate(zip(row_a, row_b)))


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
    from amazeing.ui.menu import MENU as MENU_LINES
    from amazeing.ui.menu import PROMPT
    from amazeing.utils.ansi import Ansi
    from amazeing.utils.box import Box
    from mazegen import MazeGenerator

    arms = arms_table(Box.glyph)
    renderer = RenderService()

    def build(width: int, height: int, perfect: bool,
              seed: int) -> GeneratedMaze:
        gen = MazeGenerator(width, height, perfect=perfect, seed=seed)
        gen.generate()
        return GeneratedMaze.from_generator(gen, (0, 0),
                                            (width - 1, height - 1))

    def drawn(maze: GeneratedMaze, path: bool, colour: int = 0) -> Rows:
        state = ViewState()
        if path:
            state.toggle_path()
        for _ in range(colour):
            state.next_colour()
        return decode(renderer.render(maze, state))

    small = build(4, 3, True, 1)
    save(maze_svg([list(r) for r in small.grid], cell=60, coords=True,
                  fills={small.entry: "entry", small.exit: "exit"},
                  caption="labirinto perfeito 4 x 3"),
         TELA / "labirinto-4x3.svg")
    save(drawing_svg(drawn(small, False), arms, cw=16, ch=32,
                     caption="o mesmo labirinto, como o terminal mostra"),
         TELA / "desenho-4x3.svg")
    labels = {(4 * x + 2, 2 * y + 1): f"{x},{y}"
              for y in range(3) for x in range(4)}
    save(layout_svg(4, 3, labels, cw=26, ch=44,
                    caption="escuro: canto · azul: lugar de parede · "
                            "amarelo: interior da célula, com o centro "
                            "mais forte"),
         TELA / "grade-4x3.svg")

    first = small.grid[0][0]
    save(bits_svg(first), TELA / f"bits-{first}.svg")
    small_walls, _ = layers(renderer, small, ViewState().wall_colour,
                            Ansi.WHITE)
    walls_rows = decode(small_walls)
    crop = [row[:5] for row in walls_rows[:3]]
    save(drawing_svg(crop, arms, cw=40, ch=80, axes=True,
                     overlay={(c, 1): "highlight" for c in (1, 2, 3)},
                     caption=f"célula 0,0 = {first}: Norte, Sul e Oeste "
                             f"fechados, Leste aberto"),
         TELA / "paredes-0-0.svg")
    corners = {(c, line): "highlight"
               for line in range(0, len(walls_rows), 2)
               for c in range(0, len(walls_rows[0]), 4)}
    save(drawing_svg(walls_rows, arms, cw=26, ch=52, axes=True,
                     overlay=corners,
                     caption=f"em amarelo, os {len(corners)} cantos: "
                             f"linhas pares, colunas múltiplas de 4"),
         TELA / "cantos-4x3.svg")

    path = small.path()
    save(maze_svg([list(r) for r in small.grid], cell=60, coords=True,
                  fills={small.entry: "entry", small.exit: "exit"},
                  path=path,
                  labels={cell: str(i) for i, cell in enumerate(path)},
                  caption=f"solution = {small.solution}: "
                          f"{len(path)} células"),
         TELA / "caminho-4x3.svg")
    centres = {(4 * x + 2, 2 * y + 1): "current" for x, y in path}
    save(drawing_svg(drawn(small, True), arms, cw=26, ch=52, axes=True,
                     outline=centres,
                     caption="contornado em laranja, o centro de cada "
                             "célula do caminho, na coluna 4x + 2"),
         TELA / "caminho-linha-4x3.svg")

    board = build(9, 7, False, 4)
    hidden, shown = drawn(board, False), drawn(board, True)
    walls_only, with_pattern = layers(renderer, board,
                                      ViewState().wall_colour, Ansi.WHITE)
    walls_rows = decode(walls_only)
    pattern_rows = decode(with_pattern)
    ends = {(c, 2 * y + 1) for x, y in (board.entry, board.exit)
            for c in range(4 * x + 1, 4 * x + 4)}
    if not (same_except(walls_rows, hidden, 0, set())
            and same_except(pattern_rows, hidden, 2, ends)
            and same_except(hidden, shown, 2, set())):
        raise SystemExit(f"{root}: as camadas não batem com o render")
    save(panels_svg([
        (walls_rows, "1. paredes e cantos"),
        (pattern_rows, "2. o \"42\" em cinza"),
        (hidden, "3. entrada e saída"),
        (shown, "4. o caminho em ciano"),
    ], arms, cw=7, ch=14, columns=2), TELA / "etapas-9x7.svg")
    save(panels_svg([(hidden, "caminho oculto"),
                     (shown, "caminho visível")], arms, cw=8, ch=16,
                    columns=2), TELA / "desenho-9x7.svg")
    grey_walls = {(column, line): "current"
                  for line, row in enumerate(hidden)
                  for column, (_, _, back) in enumerate(row)
                  if back == Ansi.GREY and not interior(column, line)}
    save(panels_svg([(hidden, "como o terminal mostra"),
                     (hidden, "em laranja, as paredes com fundo cinza")],
                    arms, cw=10, ch=20, columns=2,
                    overlays=[{}, grey_walls]),
         TELA / "quarenta-e-dois-9x7.svg")

    menu_lines = list(MENU_LINES)
    save(session_svg(
        ["$ .venv/bin/python a_maze_ing.py nove.txt", ""], hidden,
        [*menu_lines, f"{PROMPT}9", "Invalid choice", f"{PROMPT}2", ""],
        arms, cw=8, ch=16), MENU / "sessao-9x7.svg")
    save(session_svg([], shown, [*menu_lines, PROMPT], arms, cw=8, ch=16),
         MENU / "sessao-9x7-caminho.svg")

    names = ("grafite", "laranja", "verde", "azul")
    save(panels_svg([(drawn(board, True, index),
                      f"colour_index = {index}: {name}")
                     for index, name in enumerate(names)],
                    arms, cw=6, ch=12, columns=2),
         TELA / "paleta-9x7.svg")

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
