"""Gera as imagens da introdução e da parte 1 (entendendo o problema).

Uso, na pasta tutorial/:

    python3 scripts/imagens_introducao.py <raiz de uma implementação pronta>

A implementação fornece o pacote mazegen, que gera os labirintos reais.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Sequence
from pathlib import Path

from svg import (
    COLORS,
    _svg,
    _text,
    bits_svg,
    cell_bits_svg,
    color,
    grid_from_hex,
    maze_svg,
    save,
    sides_svg,
)

OUT = Path(__file__).resolve().parent.parent / "static" / "img" / "problema"
STEP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
GLYPHS = ("X...XXX", "X.....X", "XXX.XXX", "..X.X..", "..X.XXX")
XY = tuple[int, int]
SIZE_RE = re.compile(r'<svg [^>]*?width="([\d.]+)" height="([\d.]+)"[^>]*>')


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


def render_rows(grid: list[list[int]], entry: XY, exit_: XY,
                path: list[XY], visible: bool) -> list[list[str]]:
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


def passages(grid: list[list[int]]) -> dict[XY, list[XY]]:
    """Lista, para cada célula, as vizinhas ligadas por passagem.

    Args:
        grid: Grade de bits.

    Returns:
        O grafo das passagens.
    """
    height, width = len(grid), len(grid[0])
    sides = ((1, 0, -1), (2, 1, 0), (4, 0, 1), (8, -1, 0))
    graph: dict[XY, list[XY]] = {}
    for y in range(height):
        for x in range(width):
            graph[(x, y)] = [(x + dx, y + dy) for bit, dx, dy in sides
                             if not grid[y][x] & bit
                             and 0 <= x + dx < width and 0 <= y + dy < height]
    return graph


def dead_ends(grid: list[list[int]]) -> list[XY]:
    """Células com uma única passagem.

    Args:
        grid: Grade de bits.

    Returns:
        Os becos, em ordem de linha.
    """
    graph = passages(grid)
    return sorted((cell for cell, near in graph.items() if len(near) == 1),
                  key=lambda cell: (cell[1], cell[0]))


def route(grid: list[list[int]], start: XY, end: XY) -> list[XY]:
    """O caminho entre duas células, andando só pelas passagens.

    Args:
        grid: Grade de bits de um labirinto perfeito.
        start: Primeira célula.
        end: Última célula.

    Returns:
        As células de start a end.
    """
    graph = passages(grid)
    parents = {start: start}
    queue = [start]
    for cell in queue:
        for nxt in graph[cell]:
            if nxt not in parents:
                parents[nxt] = cell
                queue.append(nxt)
    cells = [end]
    while cells[-1] != start:
        cells.append(parents[cells[-1]])
    return cells[::-1]


def opened_walls(before: list[list[int]],
                 after: list[list[int]]) -> list[tuple[XY, XY]]:
    """As paredes abertas entre duas versões da mesma grade.

    Args:
        before: Grade antes.
        after: Grade depois; só tem paredes a menos.

    Returns:
        Cada parede aberta como o par de células que ela separava.
    """
    walls: list[tuple[XY, XY]] = []
    for y, row in enumerate(before):
        for x, bits in enumerate(row):
            gone = bits & ~after[y][x]
            if gone & 2:
                walls.append(((x, y), (x + 1, y)))
            if gone & 4:
                walls.append(((x, y), (x, y + 1)))
    return walls


def nested(svg: str, x: float, y: float) -> tuple[str, float, float]:
    """Põe um documento SVG dentro de outro, na posição x, y.

    Args:
        svg: Documento SVG gerado pela biblioteca.
        x: Posição horizontal no documento de fora.
        y: Posição vertical no documento de fora.

    Returns:
        O elemento aninhado, a largura e a altura dele.
    """
    match = SIZE_RE.match(svg)
    if match is None:
        raise ValueError("documento SVG sem largura e altura")
    width, height = float(match.group(1)), float(match.group(2))
    head = (f'<svg x="{x:g}" y="{y:g}" width="{width:g}" '
            f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">')
    return head + svg[match.end():].rstrip(), width, height


def side_by_side(panels: Sequence[tuple[str, str]], caption: str) -> str:
    """Desenha vários SVGs lado a lado, cada um com um título em cima.

    Args:
        panels: Pares (documento SVG, título).
        caption: Legenda abaixo de todos.

    Returns:
        O documento SVG.
    """
    gap, top = 20, 34
    sizes = [nested(svg, 0, 0)[1:] for svg, _ in panels]
    used = sum(width for width, _ in sizes) + gap * (len(panels) - 1)
    total_w = max(used, len(caption) * 7.4 + 40)
    total_h = top + max(height for _, height in sizes) + 30
    body: list[str] = []
    x = (total_w - used) / 2
    for svg, title in panels:
        element, width, _ = nested(svg, x, top)
        body.append(element)
        body.append(_text(x + width / 2, top - 14, title, size=14,
                          weight="bold"))
        x += width + gap
    body.append(_text(total_w / 2, total_h - 18, caption, size=13,
                      fill="muted"))
    return _svg(total_w, total_h, body)


def terminal_svg(rows: Sequence[Sequence[str]], size: int,
                 caption: str) -> str:
    """Desenha as posições como o terminal, com a moldura escura do fundo.

    Args:
        rows: rows[py][px] com o nome da cor de cada posição.
        size: Lado de cada quadrado.
        caption: Legenda abaixo do desenho.

    Returns:
        O documento SVG.
    """
    pad, frame = 16, 14
    inner_w, inner_h = len(rows[0]) * size, len(rows) * size
    width = max(inner_w + 2 * (pad + frame), len(caption) * 7.4 + 40)
    left, top = (width - inner_w) / 2, pad + frame
    body = [
        f'<rect x="{left - frame:g}" y="{pad}" '
        f'width="{inner_w + 2 * frame:g}" height="{inner_h + 2 * frame:g}" '
        f'rx="6" fill="{COLORS["corridor"]}"/>'
    ]
    for py, row in enumerate(rows):
        for px, name in enumerate(row):
            body.append(
                f'<rect x="{left + px * size:g}" y="{top + py * size:g}" '
                f'width="{size}" height="{size}" fill="{color(name)}"/>'
            )
    total_h = top + inner_h + frame + 40
    body.append(_text(width / 2, total_h - 20, caption, size=13,
                      fill="muted"))
    return _svg(width, total_h, body)


def positions_svg() -> str:
    """Desenha as 7 x 5 posições de uma grade 3x2, numeradas.

    A célula 1,0 e as posições das paredes Norte e Oeste dela levam
    rótulos.

    Returns:
        O documento SVG.
    """
    size, gap, top = 48, 4, 70
    caption = ("amarelo: célula · azul: posição de parede (fechada ou "
               "aberta) · escuro: canto")
    width = max(7 * size + 130, len(caption) * 7.4 + 40)
    left = (width - 7 * size) / 2 + 20
    labels = {(3, 1): "1,0", (3, 0): "N", (2, 1): "O"}
    body: list[str] = []
    for py in range(5):
        for px in range(7):
            if px % 2 == 0 and py % 2 == 0:
                name = "wall"
            elif px % 2 == 1 and py % 2 == 1:
                name = "highlight"
            else:
                name = "stack"
            x, y = left + px * size, top + py * size
            body.append(
                f'<rect x="{x + gap / 2:g}" y="{y + gap / 2:g}" '
                f'width="{size - gap}" height="{size - gap}" '
                f'fill="{color(name)}"/>'
            )
            if (px, py) in labels:
                body.append(_text(x + size / 2, y + size / 2,
                                  labels[(px, py)], size=15, weight="bold"))
    for px in range(7):
        body.append(_text(left + px * size + size / 2, top - 14, str(px),
                          size=13, fill="muted"))
    for py in range(5):
        body.append(_text(left - 16, top + py * size + size / 2, str(py),
                          size=13, fill="muted"))
    body.append(_text(left + 7 * size / 2, top - 42, "coluna do quadro →",
                      size=13, weight="bold"))
    middle = top + 5 * size / 2
    body.append(
        f'<g transform="rotate(90 {left - 44:g} {middle:g})">'
        + _text(left - 44, middle, "linha do quadro →", size=13,
                weight="bold")
        + "</g>"
    )
    height = top + 5 * size + 44
    body.append(_text(width / 2, height - 20, caption, size=13,
                      fill="muted"))
    return _svg(width, height, body)


def glyph_svg(extra: dict[XY, str], caption: str) -> str:
    """Desenha o bloco 7 x 5 do "42", com as posições numeradas.

    Args:
        extra: Cores de células comuns a destacar.
        caption: Legenda abaixo do desenho.

    Returns:
        O documento SVG.
    """
    glyph = [[0] * 7 for _ in range(5)]
    fills = {(dx, dy): "pattern" for dy, row in enumerate(GLYPHS)
             for dx, char in enumerate(row) if char == "X"}
    fills.update(extra)
    return maze_svg(glyph, cell=40, show_open=True, coords=True, wall=0,
                    fills=fills, caption=caption)


def main() -> None:
    """Gera todas as imagens desta parte."""
    sys.path.insert(0, sys.argv[1])
    from mazegen import MazeGenerator

    closed = [[15] * 6 for _ in range(4)]
    save(maze_svg(closed, coords=True, cell=44, labels={
        (0, 0): "0,0", (5, 0): "5,0", (2, 1): "2,1", (0, 3): "0,3",
        (5, 3): "5,3"},
        caption="a célula 5,3: coluna 5, linha 3, contando de 0"),
        OUT / "coordenadas.svg")

    save(sides_svg(), OUT / "lados-da-celula.svg")
    save(maze_svg(grid_from_hex(["d53", "d56"]), cell=70,
                  labels={(0, 0): "A", (1, 0): "B", (0, 1): "C"},
                  fills={(0, 0): "highlight", (1, 0): "visited",
                         (0, 1): "stack"},
                  caption="entre A e B não há parede: passagem; "
                          "entre A e C há parede"),
         OUT / "parede-e-passagem.svg")
    save(bits_svg(9), OUT / "bits-9.svg")
    save(bits_svg(10), OUT / "bits-a.svg")
    save(cell_bits_svg(9, caption="Norte e Oeste fechados: 1 + 8 = 9"),
         OUT / "celula-9.svg")
    save(cell_bits_svg(10, caption="Leste e Oeste fechados: 2 + 8 = 10"),
         OUT / "celula-a.svg")
    save(cell_bits_svg(15, caption="tudo fechado: 1 + 2 + 4 + 8 = 15"),
         OUT / "celula-15.svg")

    save(maze_svg([[15, 15]], cell=90, labels={(0, 0): "A", (1, 0): "B"},
                  fills={(0, 0): "highlight", (1, 0): "visited"},
                  caption="a parede do meio é o Leste de A e o Oeste de B"),
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
                  caption="em ciano, o caminho EESWW"),
         OUT / "exemplo-3x2-caminho.svg")

    ring = walk((0, 0), "EESWWN")
    save(maze_svg(grid_from_hex(["953", "c56"]), cell=64, path=ring,
                  caption="em ciano, um ciclo: a volta em torno da "
                          "parede do meio"),
         OUT / "ciclo-3x2.svg")
    open_3x2 = grid_from_hex(["913", "c46"])
    save(side_by_side(
        [(maze_svg(open_3x2, cell=64, path=walk((0, 0), "ESWN")),
          "ciclo 1"),
         (maze_svg(open_3x2, cell=64, path=walk((1, 0), "ESWN")),
          "ciclo 2")],
        "a grade 3 x 2 sem nenhuma parede por dentro: "
        "dois ciclos independentes, em ciano"),
        OUT / "ciclos-3x2-dois.svg")
    save(side_by_side(
        [(maze_svg(grid_from_hex(["913", "802", "c46"]), cell=48,
                   show_open=True), "3x3 aberto: proibido"),
         (maze_svg(grid_from_hex(["913", "842", "c56"]), cell=48,
                   show_open=True), "3x3 com uma parede: permitido"),
         (maze_svg(open_3x2, cell=48, show_open=True),
          "3x2 aberto: permitido")],
        "linha cheia: parede · tracejado: passagem (parede aberta)"),
        OUT / "saloes-3x3.svg")

    grids: dict[bool, list[list[int]]] = {}
    for perfect, name in ((True, "perfeito-6x4"), (False, "pacman-6x4")):
        gen = MazeGenerator(width=6, height=4, perfect=perfect, seed=7)
        gen.generate()
        grids[perfect] = gen.grid
        save(maze_svg(gen.grid, cell=48,
                      fills={(0, 0): "entry", (5, 3): "exit"},
                      caption="entrada em magenta, saída em vermelho"),
             OUT / f"{name}.svg")
    ends = {cell: "current" for cell in dead_ends(grids[True])}
    save(maze_svg(grids[True], cell=48, fills=ends,
                  caption="em laranja, os becos sem saída: "
                          "uma única abertura"),
         OUT / "perfeito-6x4-becos.svg")
    panels: list[tuple[str, str]] = []
    for number, (start, end) in enumerate(
            opened_walls(grids[True], grids[False]), start=1):
        cycle = route(grids[True], start, end) + [start]
        panels.append((
            maze_svg(grids[False], cell=40, path=cycle),
            f"ciclo {number}: parede aberta entre "
            f"{start[0]},{start[1]} e {end[0]},{end[1]}"))
    save(side_by_side(panels, "cada parede aberta num beco criou um "
                              "ciclo, em ciano"),
         OUT / "pacman-6x4-ciclos.svg")

    save(glyph_svg({}, "cinza: as 18 células do 42 · branco: células "
                       "comuns · tracejado: limite entre células"),
         OUT / "glifo-42.svg")
    save(glyph_svg({(5, 1): "highlight", (5, 3): "highlight"},
                   "cinza: o 42 · amarelo: os dois becos cercados · "
                   "branco: células comuns · tracejado: limite entre "
                   "células"),
         OUT / "glifo-42-cercados.svg")

    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate()
    fills = {cell: "pattern" for cell in gen.pattern}
    fills[(0, 0)] = "entry"
    fills[(19, 14)] = "exit"
    save(maze_svg(gen.grid, cell=28, wall=3, fills=fills,
                  caption="20 x 15, modo Pac-Man, semente 42"),
         OUT / "labirinto-20x15.svg")
    save(maze_svg(gen.grid, cell=28, wall=3, fills=fills,
                  path=walk((0, 0), gen.solution),
                  caption="20 x 15, modo Pac-Man, semente 42, com o "
                          "caminho mais curto"),
         OUT / "labirinto-20x15-caminho.svg")

    for visible, name in ((False, "desenho-3x2"),
                          (True, "desenho-3x2-caminho")):
        rows = render_rows(small, (0, 0), (0, 1), small_path, visible)
        caption = ("cores do terminal: branco = parede, escuro = corredor, "
                   "magenta = entrada, vermelho = saída")
        if visible:
            caption += ", ciano = caminho"
        save(terminal_svg(rows, 34, caption), OUT / f"{name}.svg")

    save(positions_svg(), OUT / "posicoes.svg")


if __name__ == "__main__":
    main()
