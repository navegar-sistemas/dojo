"""Gera as imagens das partes 6 a 9 (Carver, Solver, Braider e gerador).

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_6_a_9.py <raiz de uma implementação pronta>

A implementação fornece o pacote mazegen. Os passos do backtracker e do
braiding são capturados repetindo os laços com o mesmo random.Random, e o
script confere que o resultado final é igual ao das classes reais.
"""

from __future__ import annotations

import random
import re
import sys
from collections import deque
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

from svg import (
    COLORS,
    _caption_overflow,
    _line,
    _svg,
    maze_svg,
    save,
)

IMG = Path(__file__).resolve().parent.parent / "static" / "img"
STEP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
XY = tuple[int, int]


def walk(start: XY, letters: str) -> list[XY]:
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


def origin(grid: Sequence[Sequence[int]], cell: int,
           caption: str | None) -> tuple[float, float]:
    """Canto superior esquerdo da grade dentro do SVG de maze_svg.

    Args:
        grid: Grade desenhada.
        cell: Lado da célula.
        caption: Legenda passada a maze_svg.

    Returns:
        As coordenadas (left, top), sem números de linha e coluna.
    """
    width = len(grid[0])
    left = 16 + _caption_overflow(16 + width * cell + 16, caption) / 2
    return left, 16


def overlay(svg: str, elements: list[str]) -> str:
    """Acrescenta elementos no fim de um SVG, por cima do desenho.

    Args:
        svg: Documento SVG.
        elements: Elementos a acrescentar.

    Returns:
        O documento com os elementos.
    """
    return svg.replace("</svg>", "\n".join(elements) + "\n</svg>")


def wall_marks(grid: Sequence[Sequence[int]], cell: int,
               caption: str | None, walls: list[tuple[XY, str]],
               stroke: str, width: float) -> list[str]:
    """Linhas sobre paredes escolhidas (lado E ou S de uma célula).

    Args:
        grid: Grade desenhada.
        cell: Lado da célula.
        caption: Legenda passada a maze_svg.
        walls: Pares (célula, "E" ou "S").
        stroke: Cor da linha.
        width: Espessura da linha.

    Returns:
        Os elementos SVG.
    """
    left, top = origin(grid, cell, caption)
    lines = []
    for (x, y), side in walls:
        x1, y1 = left + (x + 1) * cell, top + (y + 1) * cell
        if side == "E":
            lines.append(_line(x1, y1 - cell, x1, y1, stroke, width))
        else:
            lines.append(_line(x1 - cell, y1, x1, y1, stroke, width))
    return lines


def compose(images: list[str], columns: int, gap: int = 12) -> str:
    """Junta vários SVGs numa grade de quadros.

    Args:
        images: Documentos SVG.
        columns: Quadros por linha.
        gap: Espaço entre quadros.

    Returns:
        Um documento SVG com todos os quadros.
    """
    sizes = []
    for image in images:
        match = re.search(r'width="([\d.]+)" height="([\d.]+)"', image)
        if match is None:
            raise ValueError("SVG sem width e height")
        sizes.append(tuple(float(v) for v in match.groups()))
    rows = [sizes[i:i + columns] for i in range(0, len(sizes), columns)]
    col_w = [max(row[c][0] for row in rows if c < len(row))
             for c in range(columns)]
    row_h = [max(h for _, h in row) for row in rows]
    body = []
    for index, image in enumerate(images):
        r, c = divmod(index, columns)
        x = sum(col_w[:c]) + gap * c
        y = sum(row_h[:r]) + gap * r
        body.append(image.replace(
            '<svg xmlns="http://www.w3.org/2000/svg" ',
            f'<svg x="{x:g}" y="{y:g}" ', 1))
    total_w = sum(col_w) + gap * (columns - 1)
    total_h = sum(row_h) + gap * (len(rows) - 1)
    return _svg(total_w, total_h, body)


def blend(start: str, end: str, t: float) -> str:
    """Cor entre duas cores hexadecimais.

    Args:
        start: Cor de t = 0.
        end: Cor de t = 1.
        t: Posição, de 0 a 1.

    Returns:
        A cor intermediária.
    """
    a = [int(start[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(end[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02x}"
                         for p, q in zip(a, b))


def carve_frames(maze: Any, start: Any, rng: random.Random,
                 direction: Any) -> Iterator[tuple[set[Any], list[Any],
                                                   str]]:
    """Repete o laço do Carver e entrega o estado depois de cada volta.

    Args:
        maze: Maze novo.
        start: Célula de partida.
        rng: Fonte aleatória, a mesma que o Carver usaria.
        direction: A classe Direction.

    Yields:
        (visitadas, pilha, ação) depois de cada volta do laço.
    """
    visited = {start}
    stack = [start]
    yield set(visited), list(stack), "início"
    while stack:
        current = stack[-1]
        options = []
        for side in direction:
            nxt = maze.neighbour(current, side)
            if nxt is not None and nxt not in visited:
                options.append(side)
        if not options:
            stack.pop()
            yield set(visited), list(stack), "recua"
            continue
        side = rng.choice(options)
        maze.open_wall(current, side)
        nxt = current.step(side)
        visited.add(nxt)
        stack.append(nxt)
        yield set(visited), list(stack), "avança " + side.letter


def bfs(maze: Any, start: Any) -> dict[Any, int]:
    """Distância de cada célula até a partida.

    Args:
        maze: Maze escavado.
        start: Célula de partida.

    Returns:
        A distância, em passos, de cada célula alcançável.
    """
    seen = {start: 0}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for side in maze.passages(cell):
            nxt = cell.step(side)
            if nxt not in seen:
                seen[nxt] = seen[cell] + 1
                queue.append(nxt)
    return seen


def dead_end_fills(maze: Any) -> dict[XY, str]:
    """Cores do "42", dos becos reais e dos becos cercados.

    Args:
        maze: Maze escavado.

    Returns:
        Cinza no "42", amarelo nos becos reais, laranja nos cercados.
    """
    fills = {cell.as_tuple(): "pattern" for cell in maze.pattern.cells}
    for cell in maze.cells():
        if len(maze.passages(cell)) == 1:
            fills[cell.as_tuple()] = ("highlight" if maze.closed_sides(cell)
                                      else "current")
    return fills


def opened_walls(before: Sequence[Sequence[int]],
                 after: Sequence[Sequence[int]]) -> list[tuple[XY, str]]:
    """Paredes internas fechadas antes e abertas depois.

    Args:
        before: Grade anterior.
        after: Grade posterior.

    Returns:
        Pares (célula, "E" ou "S") de cada parede aberta.
    """
    return [((x, y), side)
            for y, row in enumerate(after) for x, bits in enumerate(row)
            for side, bit in (("E", 2), ("S", 4))
            if before[y][x] & bit and not bits & bit]


def carver_images(out: Path, mz: dict[str, Any]) -> None:
    """Árvore geradora, passos do backtracker e a seed.

    Args:
        out: Pasta de destino.
        mz: Classes do mazegen.
    """
    maze_cls, cell_cls, pattern_cls = mz["Maze"], mz["Cell"], mz["Pattern42"]
    direction = mz["Direction"]

    maze = maze_cls(6, 4, pattern_cls.for_size(6, 4))
    mz["Carver"]().carve(maze, cell_cls(0, 0), random.Random(7))
    grid = maze.rows()
    size = 56
    caption = "24 células, 23 passagens: cada ponto é uma célula"
    left, top = origin(grid, size, caption)
    marks = []
    for cell in maze.cells():
        cx = left + cell.x * size + size / 2
        cy = top + cell.y * size + size / 2
        for side in (direction.EAST, direction.SOUTH):
            if maze.is_open(cell, side):
                marks.append(_line(cx, cy, cx + side.dx * size,
                                   cy + side.dy * size, "current", 5))
    for cell in maze.cells():
        cx = left + cell.x * size + size / 2
        cy = top + cell.y * size + size / 2
        marks.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="7" '
                     f'fill="{COLORS["wall"]}"/>')
    save(overlay(maze_svg(grid, cell=size, caption=caption), marks),
         out / "arvore-6x4.svg")

    seed, width, height = 3, 5, 4
    maze = maze_cls(width, height, pattern_cls.for_size(width, height))
    frames = []
    for visited, stack, action in carve_frames(
            maze, cell_cls(0, 0), random.Random(seed), direction):
        frames.append((maze.rows(), visited, stack, action))
    real = maze_cls(width, height, pattern_cls.for_size(width, height))
    mz["Carver"]().carve(real, cell_cls(0, 0), random.Random(seed))
    assert real.rows() == frames[-1][0], "o laço copiado diverge do Carver"
    first_back = next(i for i, f in enumerate(frames) if f[3] == "recua")
    resume = next(i for i in range(first_back, len(frames))
                  if frames[i][3].startswith("avança"))
    second_back = next(i for i in range(resume, len(frames))
                       if frames[i][3] == "recua")
    chosen = [0, 1, first_back - 1, first_back, resume, second_back - 1,
              len(frames) - 2, len(frames) - 1]
    pictures = []
    for index in chosen:
        rows, visited, stack, action = frames[index]
        fills = {cell.as_tuple(): "visited" for cell in visited}
        fills.update({cell.as_tuple(): "stack" for cell in stack})
        if stack:
            fills[stack[-1].as_tuple()] = "current"
        labels = {cell.as_tuple(): str(n + 1)
                  for n, cell in enumerate(stack)}
        pictures.append(maze_svg(
            rows, cell=40, fills=fills, labels=labels,
            caption=f"passo {index}: {action}, pilha com {len(stack)}"))
    save(compose(pictures, 4), out / "backtracker-passos.svg")

    pictures = []
    for seed in (1, 2, 1):
        maze = maze_cls(8, 5, pattern_cls.for_size(8, 5))
        mz["Carver"]().carve(maze, cell_cls(0, 0), random.Random(seed))
        pictures.append(maze_svg(maze.rows(), cell=30, wall=3,
                                 fills={(0, 0): "entry"},
                                 caption=f"Random({seed})"))
    save(compose(pictures, 3), out / "seeds.svg")


def solver_images(out: Path, mz: dict[str, Any]) -> None:
    """Camadas da busca em largura, os pais e o desempate.

    Args:
        out: Pasta de destino.
        mz: Classes do mazegen.
    """
    gen = mz["MazeGenerator"](9, 7, seed=4)
    gen.generate()
    maze = mz["Maze"](9, 7, mz["Pattern42"].for_size(9, 7))
    for y, row in enumerate(gen.grid):
        for x, bits in enumerate(row):
            for side in mz["Direction"]:
                cell = mz["Cell"](x, y)
                if not bits & side and maze.walls(cell) & side:
                    maze.open_wall(cell, side)
    assert maze.rows() == gen.grid
    distance = bfs(maze, mz["Cell"](0, 0))
    far = max(distance.values())
    fills = {cell.as_tuple(): blend("#eff6ff", "#60a5fa", d / far)
             for cell, d in distance.items()}
    fills.update({cell: "pattern" for cell in gen.pattern})
    labels = {cell.as_tuple(): str(d) for cell, d in distance.items()}
    save(maze_svg(gen.grid, cell=48, fills=fills, labels=labels,
                  caption="distância de cada célula até a entrada (0,0)"),
         out / "camadas.svg")
    path_fills = {cell: "pattern" for cell in gen.pattern}
    path_fills[(0, 0)] = "entry"
    path_fills[(8, 6)] = "exit"
    save(maze_svg(gen.grid, cell=48, fills=path_fills, labels=labels,
                  path=walk((0, 0), gen.solution),
                  caption=f"saída a {distance[mz['Cell'](8, 6)]} passos: "
                          f"{gen.solution}"),
         out / "caminho.svg")

    maze = mz["Maze"](6, 4, mz["Pattern42"].for_size(6, 4))
    mz["Carver"]().carve(maze, mz["Cell"](0, 0), random.Random(7))
    letters = mz["Solver"]().shortest_path(maze, mz["Cell"](0, 0),
                                           mz["Cell"](5, 3))
    parents: dict[Any, str] = {}
    queue = deque([mz["Cell"](0, 0)])
    seen = {mz["Cell"](0, 0)}
    while queue:
        cell = queue.popleft()
        for side in maze.passages(cell):
            nxt = cell.step(side)
            if nxt not in seen:
                seen.add(nxt)
                parents[nxt.as_tuple()] = side.letter
                queue.append(nxt)
    save(maze_svg(maze.rows(), cell=56, labels=parents,
                  fills={(0, 0): "entry", (5, 3): "exit"},
                  path=walk((0, 0), letters),
                  caption=f"lendo da saída até a entrada e invertendo: "
                          f"{letters}"),
         out / "pais.svg")

    open_grid = [[9, 1, 3], [12, 4, 6]]
    pictures = []
    for route, note in (("EES", "o escolhido"), ("ESE", "mesmo tamanho"),
                        ("SEE", "mesmo tamanho")):
        pictures.append(maze_svg(open_grid, cell=56, path=walk((0, 0), route),
                                 fills={(0, 0): "entry", (2, 1): "exit"},
                                 caption=f"{route}: {note}"))
    save(compose(pictures, 3), out / "empate-3x2.svg")


def braider_images(out: Path, mz: dict[str, Any]) -> None:
    """Becos, antes e depois do braiding e a regra do 3x3.

    Args:
        out: Pasta de destino.
        mz: Classes do mazegen.
    """
    maze_cls, cell_cls, pattern_cls = mz["Maze"], mz["Cell"], mz["Pattern42"]
    direction = mz["Direction"]

    maze = maze_cls(9, 7, pattern_cls.for_size(9, 7))
    mz["Carver"]().carve(maze, cell_cls(0, 0), random.Random(1))
    save(maze_svg(maze.rows(), cell=48, fills=dead_end_fills(maze),
                  caption="amarelo: beco real · laranja: beco cercado "
                          "pela borda e pelo 42"),
         out / "becos-9x7.svg")

    maze = maze_cls(20, 15, pattern_cls.for_size(20, 15))
    rng = random.Random(42)
    mz["Carver"]().carve(maze, cell_cls(0, 0), rng)
    before = maze.rows()
    dead = maze.dead_ends()
    fills = dead_end_fills(maze)
    left_svg = maze_svg(before, cell=22, wall=3, fills=fills,
                        caption=f"perfeito: {len(dead)} becos reais")
    mz["Braider"]().braid(maze, rng)
    gen = mz["MazeGenerator"](20, 15, seed=42)
    gen.generate()
    assert maze.rows() == gen.grid
    after = maze.rows()
    opened = opened_walls(before, after)
    caption = (f"Pac-Man: {len(opened)} paredes abertas, "
               f"{maze.loop_count()} ciclos")
    right_svg = overlay(
        maze_svg(after, cell=22, wall=3, fills=fills, caption=caption),
        wall_marks(after, 22, caption, opened, "green_wall", 6))
    save(compose([left_svg, right_svg], 2), out / "antes-depois.svg")

    seed, width, height = 32, 4, 3
    maze = maze_cls(width, height, pattern_cls.for_size(width, height))
    rng = random.Random(seed)
    mz["Carver"]().carve(maze, cell_cls(0, 0), rng)
    braider = mz["Braider"]()
    stages = [(maze.rows(), "perfeito")]
    braider._remove_dead_ends(maze, rng)
    stages.append((maze.rows(), "passo (a)"))
    braider._add_loops(maze, rng)
    stages.append((maze.rows(), "passo (b)"))
    real = maze_cls(width, height, pattern_cls.for_size(width, height))
    rng = random.Random(seed)
    mz["Carver"]().carve(real, cell_cls(0, 0), rng)
    braider.braid(real, rng)
    assert real.rows() == stages[-1][0]
    pictures = []
    previous = stages[0][0]
    for rows, name in stages:
        probe = maze_cls(width, height, pattern_cls.for_size(width, height))
        for cell in probe.cells():
            for side in probe.closed_sides(cell):
                if not rows[cell.y][cell.x] & side:
                    probe.open_wall(cell, side)
        loops = probe.loop_count()
        fills = {cell.as_tuple(): "highlight" for cell in probe.dead_ends()}
        caption = (f"{name}: {loops} {'ciclo' if loops == 1 else 'ciclos'}, "
                   f"{len(fills)} becos")
        pictures.append(overlay(
            maze_svg(rows, cell=56, fills=fills, caption=caption),
            wall_marks(rows, 56, caption, opened_walls(previous, rows),
                       "green_wall", 7)))
        previous = rows
    save(compose(pictures, 3), out / "passos-4x3.svg")

    def opened_block(width: int, height: int) -> list[list[int]]:
        block = maze_cls(width, height, pattern_cls.for_size(width, height))
        for cell in block.cells():
            for side in block.closed_sides(cell):
                block.open_wall(cell, side)
        opened: list[list[int]] = block.rows()
        return opened

    pictures = [
        maze_svg(opened_block(3, 3), cell=48, show_open=True,
                 fills={(x, y): "#fecaca" for x in range(3) for y in range(3)},
                 caption="3x3 aberto: proibido"),
        maze_svg(opened_block(2, 3), cell=48, show_open=True,
                 fills={(x, y): "visited" for x in range(2) for y in range(3)},
                 caption="2x3 aberto: permitido"),
        maze_svg(opened_block(3, 2), cell=48, show_open=True,
                 fills={(x, y): "visited" for x in range(3) for y in range(2)},
                 caption="3x2 aberto: permitido"),
    ]
    save(compose(pictures, 3), out / "area-3x3.svg")

    block = maze_cls(3, 3, pattern_cls.for_size(3, 3))
    for cell in block.cells():
        for side in block.closed_sides(cell):
            if (cell.as_tuple(), side) != ((1, 1), direction.EAST):
                block.open_wall(cell, side)
    almost = block.rows()
    caption = "11 abertas; a vermelha é a candidata"
    first = overlay(
        maze_svg(almost, cell=48, show_open=True, caption=caption),
        wall_marks(almost, 48, caption, [((1, 1), "E")], "red", 6))
    block.open_wall(cell_cls(1, 1), direction.EAST)
    assert block.has_open_3x3()
    second = maze_svg(block.rows(), cell=48, show_open=True,
                      fills={(x, y): "#fecaca" for x in range(3)
                             for y in range(3)},
                      caption="abriu: has_open_3x3() é True")
    block.close_wall(cell_cls(1, 1), direction.EAST)
    third = maze_svg(block.rows(), cell=48, show_open=True,
                     caption="close_wall desfaz")
    save(compose([first, second, third], 3), out / "desfazer.svg")


def generator_images(out: Path, mz: dict[str, Any]) -> None:
    """As três etapas de uma chamada a generate().

    Args:
        out: Pasta de destino.
        mz: Classes do mazegen.
    """
    maze = mz["Maze"](20, 15, mz["Pattern42"].for_size(20, 15))
    rng = random.Random(42)
    mz["Carver"]().carve(maze, mz["Cell"](0, 0), rng)
    carved = maze.rows()
    mz["Braider"]().braid(maze, rng)
    gen = mz["MazeGenerator"](20, 15, seed=42)
    gen.generate()
    assert maze.rows() == gen.grid
    fills = {cell: "pattern" for cell in gen.pattern}
    fills[(0, 0)] = "entry"
    fills[(19, 14)] = "exit"
    pictures = [
        maze_svg(carved, cell=16, wall=2.5, fills=fills,
                 caption="1. Carver: perfeito"),
        maze_svg(gen.grid, cell=16, wall=2.5, fills=fills,
                 caption="2. Braider: Pac-Man"),
        maze_svg(gen.grid, cell=16, wall=2.5, fills=fills,
                 path=walk((0, 0), gen.solution),
                 caption="3. Solver: solution"),
    ]
    save(compose(pictures, 3), out / "etapas.svg")


def main() -> None:
    """Gera todas as imagens das partes 6 a 9."""
    sys.path.insert(0, sys.argv[1])
    from mazegen import MazeGenerator
    from mazegen.entities.maze import Maze
    from mazegen.services.braider import Braider
    from mazegen.services.carver import Carver
    from mazegen.services.solver import Solver
    from mazegen.value_objects.cell import Cell
    from mazegen.value_objects.direction import Direction
    from mazegen.value_objects.pattern42 import Pattern42

    mz: dict[str, Any] = {
        "MazeGenerator": MazeGenerator, "Maze": Maze, "Braider": Braider,
        "Carver": Carver, "Solver": Solver, "Cell": Cell,
        "Direction": Direction, "Pattern42": Pattern42,
    }
    carver_images(IMG / "carver", mz)
    solver_images(IMG / "solver", mz)
    braider_images(IMG / "braider", mz)
    generator_images(IMG / "gerador", mz)


if __name__ == "__main__":
    main()
