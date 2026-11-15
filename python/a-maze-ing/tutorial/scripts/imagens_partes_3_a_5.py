"""Gera as imagens das partes 2 a 5: arquitetura, ambiente, VOs e Maze.

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_3_a_5.py <raiz de uma implementação pronta>

A implementação fornece o pacote mazegen: Direction, Cell, Pattern42 e Maze
reais calculam o que cada imagem mostra.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Sequence
from html import escape
from pathlib import Path

from svg import (
    COLORS,
    _caption_overflow,
    _line,
    _svg,
    _text,
    color,
    maze_svg,
    save,
)

ROOT = Path(__file__).resolve().parent.parent / "static" / "img"
OUT_ARCH = ROOT / "arquitetura"
OUT_ENV = ROOT / "ambiente"
OUT_VO = ROOT / "value-objects"
OUT_MAZE = ROOT / "maze"

MONO = 'font-family="ui-monospace, SFMono-Regular, Menlo, monospace"'

Pos = tuple[int, int]


def _mono(x: float, y: float, value: str, size: float = 18,
          fill: str = "text", weight: str = "normal") -> str:
    """Cria um texto em fonte monoespaçada, alinhado à esquerda.

    Args:
        x: Posição horizontal do começo do texto.
        y: Posição vertical do centro.
        value: Texto.
        size: Tamanho da fonte.
        fill: Cor.
        weight: Peso da fonte.

    Returns:
        O elemento SVG.
    """
    return (
        f'<text x="{x:g}" y="{y:g}" {MONO} font-size="{size:g}" '
        f'font-weight="{weight}" fill="{color(fill)}" text-anchor="start" '
        f'dominant-baseline="central" xml:space="preserve">'
        f"{escape(value)}</text>"
    )


def layers_svg() -> str:
    """Desenha as camadas do projeto como anéis, do centro para a borda.

    Cada camada importa a si mesma e anéis mais para dentro, e camadas
    diferentes do mesmo anel não se importam: é o limite máximo dos
    imports, e a tabela de imports da parte 2 é mais restrita.

    Returns:
        O documento SVG.
    """
    rings = (
        ("a_maze_ing.py",
         "cria e liga as peças; imprime a mensagem de erro final",
         "#f3f4f6"),
        ("ui",
         "o menu: o único que lê o teclado; imprime o labirinto e o menu",
         "#e0e7ff"),
        ("services · repositories",
         "o desenho colorido · a leitura e a gravação de arquivos",
         "#bfdbfe"),
        ("use_cases", "a operação gerar e gravar, e a sua porta", "#bbf7d0"),
        ("domain", "os dados: config lido, labirinto pronto, tela",
         "#d9f99d"),
        ("utils · errors", "funções de apoio · tipos de erro", "#fde68a"),
        ("mazegen", "o gerador: Cell, Maze, Carver, Solver...", "#fb923c"),
    )
    center_note = "subpastas: entities/, value_objects/, services/"
    width, step, rings_h = 760, 34, 500
    body: list[str] = []
    for index, (name, role, fill) in enumerate(rings):
        inset = index * step
        x, y = 16 + inset, 16 + inset
        w, h = width - 32 - 2 * inset, rings_h - 2 * inset
        body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" '
            f'fill="{fill}" stroke="{COLORS["wall"]}" stroke-width="1.5"/>'
        )
        if index < len(rings) - 1:
            body.append(_text(width / 2, y + step / 2, f"{name}: {role}",
                              size=13.5, weight="bold"))
        else:
            body.append(_text(width / 2, y + h / 2 - 22, name, size=20,
                              weight="bold"))
            body.append(_text(width / 2, y + h / 2 + 2, role, size=14))
            body.append(_text(width / 2, y + h / 2 + 24, center_note,
                              size=13))
    legend_y = rings_h + 16 + 24
    body.append(_text(width / 2, legend_y,
                      "cada camada importa a si mesma e anéis mais para "
                      "dentro",
                      size=14, fill="muted"))
    body.append(_text(width / 2, legend_y + 22,
                      "as camadas de um mesmo anel (separadas por ·) não se "
                      "importam", size=14, fill="muted"))
    return _svg(width, legend_y + 44, body)


def makefile_rule_svg() -> str:
    """Anota as partes de uma regra do Makefile.

    Returns:
        O documento SVG.
    """
    size, char = 19.0, 11.45
    left, line1, line2, line3 = 40.0, 70.0, 140.0, 182.0
    tab_w = 4 * char
    body = [
        _mono(left, line1, "lint:", size=size, weight="bold"),
        f'<rect x="{left + 4 * char - 2:g}" y="{line1 - 15:g}" '
        f'width="{char + 4:g}" height="30" rx="5" fill="none" '
        f'stroke="{COLORS["exit"]}" stroke-width="2"/>',
        f'<rect x="{left - 4:g}" y="{line1 - 15:g}" width="{4 * char:g}" '
        f'height="30" rx="5" fill="none" stroke="{COLORS["blue"]}" '
        f'stroke-width="2"/>',
        _text(left - 4, line1 - 34, "alvo: o nome da regra",
              size=14, fill="blue", weight="bold", anchor="start"),
        _text(left + 4.5 * char + 150, line1, "← dois-pontos: fecha o nome",
              size=14, fill="exit", weight="bold"),
    ]
    for y, command in ((line2, "$(PY) -m flake8 ."),
                       (line3, "$(PY) -m mypy . $(MYPY_FLAGS)")):
        body.append(
            f'<rect x="{left:g}" y="{y - 15:g}" width="{tab_w - 6:g}" '
            f'height="30" rx="5" fill="{COLORS["highlight"]}" '
            f'stroke="{COLORS["yellow"]}" stroke-width="2"/>'
        )
        body.append(_text(left + (tab_w - 6) / 2, y, "TAB", size=13,
                          weight="bold"))
        body.append(_mono(left + tab_w, y, command, size=size))
    body.append(_text(left, line3 + 38,
                      "↑ um caractere TAB no começo, nunca espaços",
                      size=14, fill="text", weight="bold", anchor="start"))
    brace_x = left + tab_w + 30 * char + 18
    body.append(_line(brace_x, line2 - 14, brace_x, line3 + 14, "visited",
                      4))
    body.append(_text(brace_x + 14, (line2 + line3) / 2 - 10,
                      "comandos, executados", size=14, anchor="start",
                      weight="bold"))
    body.append(_text(brace_x + 14, (line2 + line3) / 2 + 10,
                      "em ordem, um por linha", size=14, anchor="start",
                      weight="bold"))
    body.append(_text(360, 266,
                      "make lint executa os dois comandos; se um falha, "
                      "o make para ali", size=14, fill="muted"))
    return _svg(720, 292, body)


def bit_ops_svg() -> str:
    """Mostra &, ~ e | sobre os 4 bits de paredes de uma célula.

    Returns:
        O documento SVG.
    """
    rows = (
        ("walls", 15, "= 15", "as quatro paredes fechadas"),
        ("Direction.EAST", 2, "= 2", "só o bit do Leste"),
        ("walls & Direction.EAST", 2, "= 2", "≠ 0: o Leste está fechado"),
        ("~Direction.EAST", 13, "= -3",
         "todos os bits ligados, menos o do Leste"),
        ("walls & ~Direction.EAST", 13, "= 13",
         "o Leste aberto, o resto igual"),
        ("13 | Direction.EAST", 15, "= 15", "o Leste fechado de novo"),
    )
    names = ("Oeste", "Sul", "Leste", "Norte")
    box, gap, label_w, top, row_h = 40, 6, 250, 76, 52
    grid_x = 20 + label_w
    body: list[str] = []
    for index, name in enumerate(names):
        value = 8 >> index
        cx = grid_x + index * (box + gap) + box / 2
        body.append(_text(cx, top - 44, name, size=13, weight="bold",
                          fill="blue" if value == 2 else "text"))
        body.append(_text(cx, top - 26, str(value), size=13, fill="muted"))
    leste_x = grid_x + 2 * (box + gap) - 3
    body.append(
        f'<rect x="{leste_x}" y="{top - 58}" width="{box + 6}" '
        f'height="{len(rows) * row_h + 50}" rx="8" fill="none" '
        f'stroke="{COLORS["blue"]}" stroke-width="2" '
        f'stroke-dasharray="6 4"/>'
    )
    for row, (expr, bits, shown, note) in enumerate(rows):
        y = top + row * row_h
        body.append(_mono(20, y + box / 2, expr, size=15))
        for index in range(4):
            on = bool(bits & (8 >> index))
            x = grid_x + index * (box + gap)
            body.append(
                f'<rect x="{x}" y="{y}" width="{box}" height="{box}" rx="6" '
                f'fill="{COLORS["wall"] if on else COLORS["background"]}" '
                f'stroke="{COLORS["wall"]}" stroke-width="2"/>'
            )
            body.append(_text(x + box / 2, y + box / 2, "1" if on else "0",
                              size=20, weight="bold",
                              fill="#ffffff" if on else "muted"))
        after = grid_x + 4 * (box + gap) + 10
        body.append(_text(after, y + box / 2, shown, size=15,
                          weight="bold", anchor="start"))
        body.append(_text(after + 52, y + box / 2, note, size=14,
                          fill="muted", anchor="start"))
    width = grid_x + 4 * (box + gap) + 360
    return _svg(width, top + len(rows) * row_h + 14, body)


def coherence_svg() -> str:
    """Duas células vizinhas, cada uma com as suas paredes, lado a lado.

    O par da esquerda concorda sobre a parede do meio; o da direita não.

    Returns:
        O documento SVG.
    """
    size, gap, top = 110, 16, 60
    pairs = (
        (40, 13, 7, "coerente: as duas dizem «aberta»", "green"),
        (380, 13, 15, "incoerente: uma diz «aberta», a outra «fechada»",
         "exit"),
    )
    notes = (
        "as células aparecem afastadas só para mostrar a anotação de cada "
        "uma;",
        "na grade, as duas linhas dentro do tracejado colorido são uma "
        "parede só",
        "linha preta cheia: parede fechada · linha cinza tracejada: "
        "parede aberta",
    )
    body: list[str] = []
    for left, a, b, caption, tone in pairs:
        for offset, bits, name in ((0, a, "0,0"), (size + gap, b, "1,0")):
            x0 = left + offset
            x1, y1 = x0 + size, top + size
            sides = ((1, x0, top, x1, top), (2, x1, top, x1, y1),
                     (4, x0, y1, x1, y1), (8, x0, top, x0, y1))
            for bit, ax, ay, bx, by in sides:
                closed = bool(bits & bit)
                body.append(_line(ax, ay, bx, by,
                                  "wall" if closed else "open",
                                  7 if closed else 2.5,
                                  None if closed else "7 6"))
            body.append(_text(x0 + size / 2, top + size / 2 - 12, name,
                              size=14, fill="muted"))
            body.append(_text(x0 + size / 2, top + size / 2 + 14,
                              str(bits), size=26, weight="bold"))
        middle = left + size + gap / 2
        body.append(
            f'<rect x="{middle - gap / 2 - 10:g}" y="{top - 14}" '
            f'width="{gap + 20}" height="{size + 28}" rx="8" fill="none" '
            f'stroke="{color(tone)}" stroke-width="2.5" '
            f'stroke-dasharray="6 4"/>'
        )
        body.append(_text(left + size + gap / 2, top - 32,
                          "Leste de 0,0 · Oeste de 1,0", size=13,
                          fill="muted"))
        body.append(_text(left + size + gap / 2, top + size + 36, caption,
                          size=14, weight="bold"))
    for index, note in enumerate(notes):
        body.append(_text(350, top + size + 70 + index * 20, note, size=12.5,
                          fill="muted"))
    return _svg(700, top + size + 70 + len(notes) * 20 + 8, body)


def window_walls_svg() -> str:
    """As 12 paredes internas de uma janela 3x3 e quem confere cada uma.

    Returns:
        O documento SVG.
    """
    cell, left, top = 96, 60, 56
    body: list[str] = []
    for y in range(3):
        for x in range(3):
            checks = []
            if x < 2:
                checks.append("E")
            if y < 2:
                checks.append("S")
            body.append(_text(left + x * cell + cell / 2,
                              top + y * cell + cell / 2 - 12,
                              f"x0+{x}, y0+{y}".replace("+0", ""),
                              size=12, fill="muted"))
            body.append(_text(left + x * cell + cell / 2,
                              top + y * cell + cell / 2 + 12,
                              " ".join(checks) or "nada", size=18,
                              weight="bold",
                              fill="text" if checks else "muted"))
    for y in range(3):
        for x in range(2):
            gx = left + (x + 1) * cell
            body.append(_line(gx, top + y * cell + 6, gx,
                              top + (y + 1) * cell - 6, "blue", 6))
    for y in range(2):
        for x in range(3):
            gy = top + (y + 1) * cell
            body.append(_line(left + x * cell + 6, gy,
                              left + (x + 1) * cell - 6, gy, "green",
                              6))
    body.append(
        f'<rect x="{left}" y="{top}" width="{3 * cell}" height="{3 * cell}" '
        f'fill="none" stroke="{COLORS["wall"]}" stroke-width="4"/>'
    )
    legend_x = left + 3 * cell + 36
    body.append(_line(legend_x, top + 40, legend_x + 36, top + 40,
                      "blue", 6))
    body.append(_text(legend_x + 48, top + 32, "6 paredes verticais:",
                      size=14, anchor="start", weight="bold"))
    body.append(_text(legend_x + 48, top + 52,
                      "o Leste (E) das colunas x0 e x0+1", size=14,
                      anchor="start"))
    body.append(_line(legend_x, top + 120, legend_x + 36, top + 120,
                      "green", 6))
    body.append(_text(legend_x + 48, top + 112, "6 paredes horizontais:",
                      size=14, anchor="start", weight="bold"))
    body.append(_text(legend_x + 48, top + 132,
                      "o Sul (S) das linhas y0 e y0+1", size=14,
                      anchor="start"))
    body.append(_text(legend_x + 48, top + 200,
                      "a borda da janela (preta) não conta:", size=14,
                      anchor="start", fill="muted"))
    body.append(_text(legend_x + 48, top + 220,
                      "ela separa a janela do resto da grade", size=14,
                      anchor="start", fill="muted"))
    return _svg(legend_x + 330, top + 3 * cell + 30, body)


def cells_order_svg() -> str:
    """A ordem em que Maze.cells() visita uma grade 9x7, pulando o "42".

    Returns:
        O documento SVG.
    """
    from mazegen.entities.maze import Maze
    from mazegen.value_objects.pattern42 import Pattern42

    maze = Maze(9, 7, Pattern42.for_size(9, 7))
    fills: dict[Pos, str] = {c.as_tuple(): "pattern"
                             for c in maze.pattern.cells}
    labels: dict[Pos, Sequence[str]] = {}
    for index, cell in enumerate(maze.cells(), start=1):
        labels[cell.as_tuple()] = [str(index)]
    return board_svg(9, 7, cell=50, fills=fills, labels=labels,
                     caption=[f"número: a ordem em que cells() entrega a "
                              f"célula (1 a {len(labels)})",
                              "cinza: célula do 42, que cells() pula"])


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
    caption: str | Sequence[str] | None = None,
    arrow_start: float = 0.22,
    arrow_end: float = 0.352,
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
        caption: Legenda abaixo do desenho, uma string por linha.
        arrow_start: Distância entre o centro da célula de origem e o
            começo da seta, em frações do lado da célula.
        arrow_end: Distância entre a ponta da seta e o centro da célula de
            destino, em frações do lado da célula.

    Returns:
        O documento SVG.
    """
    caption_lines = ([caption] if isinstance(caption, str)
                     else list(caption or []))
    longest = max(caption_lines, key=len) if caption_lines else None
    every = [(x, y) for y in range(height) for x in range(width)]
    every += list(ghosts)
    min_x = min(x for x, _ in every)
    min_y = min(y for _, y in every)
    max_x = max(x for x, _ in every)
    max_y = max(y for _, y in every)
    pad = 34 if coords else 16
    drawing_w = pad + (max_x - min_x + 1) * cell + 16
    left = pad + _caption_overflow(drawing_w, longest) / 2
    top = pad
    total_w = left + (max_x - min_x + 1) * cell + 16 + (left - pad)
    total_h = (top + (max_y - min_y + 1) * cell
               + (20 + 20 * len(caption_lines) if caption_lines else 16))

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
        dx = (x2 - x1) / max(abs(x2 - x1) + abs(y2 - y1), 1)
        dy = (y2 - y1) / max(abs(x2 - x1) + abs(y2 - y1), 1)
        head, tail = cell * arrow_start, cell * arrow_end
        body.append(
            f'<line x1="{x1 + dx * head:g}" y1="{y1 + dy * head:g}" '
            f'x2="{x2 - dx * tail:g}" y2="{y2 - dy * tail:g}" '
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
    first_line = top + (max_y - min_y + 1) * cell + 22
    for index, line in enumerate(caption_lines):
        body.append(_text(total_w / 2, first_line + index * 20, line,
                          size=13, fill="muted"))
    return _svg(total_w, total_h, body)


def deltas_svg() -> str:
    """Os quatro passos a partir de uma célula, com dx e dy de cada lado.

    Os rótulos ficam no lado de fora de cada vizinha e as setas saem da
    borda da célula atual, para não cobrir nenhum texto.

    Returns:
        O documento SVG.
    """
    from mazegen.value_objects.direction import Direction

    cell, pad = 130, 24
    left = top = pad
    body: list[str] = [
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["wall"]}"/>'
        "</marker></defs>"
    ]

    def square(x: int, y: int, fill: str) -> str:
        return (
            f'<rect x="{left + x * cell}" y="{top + y * cell}" '
            f'width="{cell}" height="{cell}" fill="{color(fill)}" '
            f'stroke="#d1d5db" stroke-width="1.5"/>'
        )

    for y in range(3):
        for x in range(3):
            body.append(square(x, y, "background"))
    body.append(square(1, 1, "current"))
    cx, cy = left + 1.5 * cell, top + 1.5 * cell
    body.append(_text(cx, cy - 11, "célula", size=17, weight="bold"))
    body.append(_text(cx, cy + 11, "atual", size=17, weight="bold"))
    for side in Direction:
        body.append(square(1 + side.dx, 1 + side.dy, "visited"))
        tx = cx + side.dx * cell * 1.05
        ty = cy + side.dy * cell * 1.05
        body.append(_text(tx, ty - 11, side.name, size=16, weight="bold"))
        delta = f"dx {side.dx:+d}, dy {side.dy:+d}".replace("+0", "0")
        body.append(_text(tx, ty + 11, delta, size=14))
        x1, y1 = cx + side.dx * cell * 0.5, cy + side.dy * cell * 0.5
        x2, y2 = cx + side.dx * cell * 0.76, cy + side.dy * cell * 0.76
        if side.dx == 0:
            x1 = x2 = cx + 34
        else:
            y1 = y2 = cy + 30
        body.append(
            f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
            f'stroke="{COLORS["wall"]}" stroke-width="2.5" '
            f'marker-end="url(#arrow)"/>'
        )
    width = 2 * pad + 3 * cell
    captions = ("um passo para cada lado: x soma dx, y soma dy",
                "laranja: a célula atual · verde: as quatro vizinhas")
    for index, line in enumerate(captions):
        body.append(_text(width / 2, top + 3 * cell + 22 + index * 20, line,
                          size=13, fill="muted"))
    return _svg(width, top + 3 * cell + 22 + len(captions) * 20, body)


def two_loops_svg(maze_rows: list[list[int]]) -> str:
    """A grade 3x2 toda aberta, com os dois ciclos independentes marcados.

    Args:
        maze_rows: A grade de paredes, rows()[y][x].

    Returns:
        O documento SVG.
    """
    cell = 72
    caption = ("6 células, 7 passagens: 7 - 6 + 1 = 2 ciclos "
               "(laranja e azul)")
    drawing = maze_svg(maze_rows, cell=cell, coords=True, show_open=True,
                       caption=caption)
    left = 58 + _caption_overflow(58 + 3 * cell + 16, caption) / 2
    top = 54
    loops = (("current", 0, -5), ("blue", 1, 5))
    extra: list[str] = []
    for tone, column, shift in loops:
        x1 = left + column * cell + cell / 2 + shift
        y1 = top + cell / 2 + shift
        extra.append(
            f'<rect x="{x1:g}" y="{y1:g}" width="{cell}" height="{cell}" '
            f'rx="10" fill="none" stroke="{color(tone)}" stroke-width="4" '
            f'stroke-dasharray="10 6"/>'
        )
    return drawing.replace("</svg>", "\n".join(extra) + "\n</svg>")


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

    save(deltas_svg(), OUT_VO / "direction-deltas.svg")

    start = Cell(3, 4)
    labels: dict[Pos, Sequence[str]] = {start.as_tuple(): ["3,4"]}
    fills: dict[Pos, str] = {start.as_tuple(): "current"}
    arrows: list[tuple[Pos, Pos]] = []
    for side in Direction:
        other = start.step(side)
        labels[other.as_tuple()] = [f"{other.x},{other.y}", side.letter]
        fills[other.as_tuple()] = "visited"
        arrows.append((start.as_tuple(), other.as_tuple()))
    save(board_svg(6, 6, cell=80, fills=fills, labels=labels, arrows=arrows,
                   arrow_start=0.34, arrow_end=0.36,
                   caption=["Cell(3, 4).step(d) para cada Direction",
                            "laranja: a célula de partida · verde: o "
                            "resultado de cada passo"]),
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
    save(board_svg(4, 3, cell=80, fills=fills, labels=labels, arrows=arrows,
                   ghosts=ghosts, coords=False, arrow_start=0.34,
                   arrow_end=0.36,
                   caption=["step não confere limites: 0,-1 e -1,0 "
                            "ficam fora da grade",
                            "laranja: partida · verde: dentro da grade · "
                            "tracejado: fora da grade"]),
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
                       caption=[f"{width} x {height}: x0 = {x0}, "
                                f"y0 = {y0}, {len(pattern.cells)} células",
                                "cinza: célula do 42 · tracejado: o "
                                "bloco 7x5"]),
             OUT_VO / f"pattern42-{width}x{height}.svg")

    width, height = 8, 7
    x0 = (width - PATTERN_WIDTH) // 2
    y0 = (height - PATTERN_HEIGHT) // 2
    fills = {(x0 + dx, y0 + dy): "highlight"
             for dy, row in enumerate(GLYPHS)
             for dx, char in enumerate(row) if char == "X"}
    assert not Pattern42.for_size(width, height).cells
    save(board_svg(width, height, cell=44, fills=fills,
                   blocks=[(x0, y0, PATTERN_WIDTH, PATTERN_HEIGHT)],
                   caption=["8 x 7: o bloco encostaria na borda esquerda; "
                            "o padrão fica vazio",
                            "amarelo: onde o 42 ficaria · tracejado: o "
                            "bloco 7x5"]),
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
                  labels=values(m),
                  caption="Maze(3, 2, ...): toda célula vale 15"),
         OUT_MAZE / "abrir-antes.svg")
    m.open_wall(Cell(0, 0), D.EAST)
    save(maze_svg(m.rows(), cell=72, coords=True, show_open=True,
                  labels=values(m),
                  fills={(0, 0): "highlight", (1, 0): "highlight"},
                  caption="open_wall(Cell(0, 0), EAST): 0,0 desliga o "
                          "bit 2 e 1,0 desliga o bit 8"),
         OUT_MAZE / "abrir-depois.svg")

    m9 = new(9, 7)
    fills: dict[Pos, str] = {c.as_tuple(): "pattern"
                             for c in m9.pattern.cells}
    fills[(0, 1)] = "current"
    near: dict[Pos, Sequence[str]] = {(0, 1): ["0,1"]}
    for side in D:
        other = m9.neighbour(Cell(0, 1), side)
        if other is not None:
            fills[other.as_tuple()] = "visited"
            near[other.as_tuple()] = [side.letter, "vizinha"]
    near[(1, 1)] = ["E", "None"]
    near[(-1, 1)] = ["W", "None"]
    save(board_svg(9, 7, cell=48, fills=fills, labels=near,
                   ghosts=[(-1, 1)],
                   caption=["vizinhos de 0,1: N e S existem; E (célula do "
                            "42) e W (fora da grade) dão None",
                            "laranja: 0,1 · verde: vizinha · cinza: 42 · "
                            "tracejado: fora da grade"]),
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
                          f"{len(enclosed)} becos cercados · cinza: 42"),
         OUT_MAZE / "becos-9x7.svg")

    snake = new(3, 2)
    for cell, side in [(Cell(0, 0), D.EAST), (Cell(1, 0), D.EAST),
                       (Cell(2, 0), D.SOUTH), (Cell(2, 1), D.WEST),
                       (Cell(1, 1), D.WEST)]:
        snake.open_wall(cell, side)
    save(maze_svg(snake.rows(), cell=72, coords=True, show_open=True,
                  fills={(0, 0): "current", (0, 1): "current"},
                  caption=f"6 células, 5 passagens: "
                          f"{snake.loop_count()} ciclos · laranja: os 2 "
                          f"becos reais"),
         OUT_MAZE / "ciclos-serpentina.svg")
    snake.open_wall(Cell(0, 0), D.SOUTH)
    snake.open_wall(Cell(1, 0), D.SOUTH)
    assert snake.loop_count() == 2
    save(two_loops_svg(snake.rows()), OUT_MAZE / "ciclos-dois.svg")

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
                  caption="as 12 paredes internas abertas: proibido · "
                          "amarelo: o bloco 3x3"),
         OUT_MAZE / "janela-3x3-aberta.svg")
    m3.close_wall(Cell(1, 1), D.EAST)
    assert not m3.has_open_3x3()
    save(maze_svg(m3.rows(), cell=64, coords=True, show_open=True,
                  fills={(1, 1): "visited", (2, 1): "visited"},
                  caption="uma parede interna fechada já basta · verde: as "
                          "duas células dessa parede"),
         OUT_MAZE / "janela-3x3-fechada.svg")

    window = border_only(5, 4)
    save(maze_svg(window, cell=56, coords=True, show_open=True, wall=4,
                  fills={(x, y): "highlight" for x in range(1, 4)
                         for y in range(0, 3)},
                  caption="5 x 4 tem 3 x 2 = 6 janelas · amarelo: a "
                          "janela que começa em 1,0"),
         OUT_MAZE / "janelas-5x4.svg")


def concept_images() -> None:
    """Imagens de conceito das partes 2 a 5, desenhadas sem labirinto."""
    save(layers_svg(), OUT_ARCH / "camadas.svg")
    save(makefile_rule_svg(), OUT_ENV / "regra-makefile.svg")
    save(bit_ops_svg(), OUT_VO / "bits-operacoes.svg")
    save(coherence_svg(), OUT_MAZE / "coerencia.svg")
    save(window_walls_svg(), OUT_MAZE / "janela-paredes-conferidas.svg")
    save(cells_order_svg(), OUT_MAZE / "cells-ordem-9x7.svg")


def main() -> None:
    """Gera todas as imagens das partes 2 a 5."""
    sys.path.insert(0, sys.argv[1])
    direction_images()
    pattern_images()
    maze_images()
    concept_images()


if __name__ == "__main__":
    main()
