"""Desenha células, grades e labirintos em SVG para as imagens do tutorial.

Só usa a biblioteca padrão. As grades seguem o formato do projeto: grid[y][x]
guarda as paredes fechadas da célula (x, y) nos bits N=1, E=2, S=4, W=8.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from html import escape
from pathlib import Path

N, E, S, W = 1, 2, 4, 8

COLORS = {
    "background": "#ffffff",
    "wall": "#1f2937",
    "open": "#cbd5e1",
    "pattern": "#9ca3af",
    "entry": "#d946ef",
    "exit": "#ef4444",
    "path": "#22d3ee",
    "highlight": "#fde68a",
    "visited": "#bbf7d0",
    "current": "#fb923c",
    "stack": "#93c5fd",
    "text": "#111827",
    "muted": "#6b7280",
    "yellow": "#facc15",
    "green": "#22c55e",
    "blue": "#3b82f6",
    "red": "#ef4444",
}

FONT = "font-family=\"ui-sans-serif, system-ui, sans-serif\""

Cell = tuple[int, int]


def color(name: str) -> str:
    """Devolve a cor da paleta, ou o próprio texto se já for uma cor.

    Args:
        name: Nome da paleta ou cor CSS.

    Returns:
        A cor CSS.
    """
    return COLORS.get(name, name)


def grid_from_hex(lines: Iterable[str]) -> list[list[int]]:
    """Converte linhas de dígitos hexadecimais numa grade.

    Args:
        lines: Uma linha do arquivo de saída por linha da grade.

    Returns:
        A grade, grid[y][x].
    """
    return [[int(digit, 16) for digit in line.strip()] for line in lines]


def _caption_overflow(drawing_width: float, caption: str | None) -> float:
    """Quanto a legenda passa da largura do desenho.

    Args:
        drawing_width: Largura ocupada pelo desenho, com margens.
        caption: Legenda, ou None.

    Returns:
        Os pixels que faltam para a legenda caber; 0 se ela cabe.
    """
    if not caption:
        return 0
    return max(0.0, len(caption) * 7.4 + 40 - drawing_width)


def _svg(width: float, height: float, body: list[str]) -> str:
    """Envolve o corpo num documento SVG com fundo branco.

    Args:
        width: Largura em pixels.
        height: Altura em pixels.
        body: Elementos SVG.

    Returns:
        O documento SVG.
    """
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" '
        f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">'
    )
    background = (
        f'<rect width="{width:g}" height="{height:g}" '
        f'fill="{COLORS["background"]}" rx="8"/>'
    )
    return "\n".join([head, background, *body, "</svg>"]) + "\n"


def _text(x: float, y: float, value: str, size: float = 14,
          fill: str = "text", weight: str = "normal",
          anchor: str = "middle") -> str:
    """Cria um texto centrado verticalmente.

    Args:
        x: Posição horizontal.
        y: Posição vertical do centro.
        value: Texto.
        size: Tamanho da fonte.
        fill: Cor.
        weight: Peso da fonte.
        anchor: Âncora horizontal.

    Returns:
        O elemento SVG.
    """
    return (
        f'<text x="{x:g}" y="{y:g}" {FONT} font-size="{size:g}" '
        f'font-weight="{weight}" fill="{color(fill)}" '
        f'text-anchor="{anchor}" dominant-baseline="central">'
        f"{escape(value)}</text>"
    )


def _line(x1: float, y1: float, x2: float, y2: float, stroke: str,
          width: float, dash: str | None = None) -> str:
    """Cria uma linha com pontas arredondadas.

    Args:
        x1: Início, horizontal.
        y1: Início, vertical.
        x2: Fim, horizontal.
        y2: Fim, vertical.
        stroke: Cor.
        width: Espessura.
        dash: Padrão de tracejado, ou None para linha cheia.

    Returns:
        O elemento SVG.
    """
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{color(stroke)}" stroke-width="{width:g}" '
        f'stroke-linecap="round"{extra}/>'
    )


def maze_svg(
    grid: Sequence[Sequence[int]],
    *,
    cell: int = 36,
    wall: float = 4,
    fills: dict[Cell, str] | None = None,
    labels: dict[Cell, str] | None = None,
    path: Sequence[Cell] | None = None,
    coords: bool = False,
    show_open: bool = False,
    caption: str | None = None,
) -> str:
    """Desenha um labirinto a partir da grade de bits.

    Args:
        grid: grid[y][x] com as paredes fechadas da célula (x, y).
        cell: Lado de uma célula, em pixels.
        wall: Espessura das paredes.
        fills: Cor de fundo de algumas células.
        labels: Texto no centro de algumas células.
        path: Células ligadas por uma linha, na ordem.
        coords: Escreve o número das colunas em cima e das linhas à
            esquerda.
        show_open: Desenha as paredes abertas como linhas tracejadas.
        caption: Legenda abaixo do desenho.

    Returns:
        O documento SVG.
    """
    height = len(grid)
    width = len(grid[0])
    base_left = 58 if coords else 16
    left: float = base_left
    top = 54 if coords else 16
    bottom = 34 if caption else 16
    left += _caption_overflow(left + width * cell + 16, caption) / 2
    body: list[str] = []
    for (x, y), name in (fills or {}).items():
        body.append(
            f'<rect x="{left + x * cell:g}" y="{top + y * cell:g}" '
            f'width="{cell}" height="{cell}" fill="{color(name)}"/>'
        )
    if path:
        points = " ".join(
            f"{left + x * cell + cell / 2:g},{top + y * cell + cell / 2:g}"
            for x, y in path
        )
        body.append(
            f'<polyline points="{points}" fill="none" '
            f'stroke="{COLORS["path"]}" stroke-width="{cell * 0.28:g}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    for y, row in enumerate(grid):
        for x, bits in enumerate(row):
            x0, y0 = left + x * cell, top + y * cell
            x1, y1 = x0 + cell, y0 + cell
            sides = (
                (N, x0, y0, x1, y0),
                (E, x1, y0, x1, y1),
                (S, x0, y1, x1, y1),
                (W, x0, y0, x0, y1),
            )
            for bit, ax, ay, bx, by in sides:
                if bits & bit:
                    body.append(_line(ax, ay, bx, by, "wall", wall))
                elif show_open:
                    body.append(_line(ax, ay, bx, by, "open", 1.5, "4 4"))
    for (x, y), value in (labels or {}).items():
        body.append(_text(left + x * cell + cell / 2,
                          top + y * cell + cell / 2, value,
                          size=cell * 0.42, weight="bold"))
    if coords:
        for x in range(width):
            body.append(_text(left + x * cell + cell / 2, top - 14, str(x),
                              size=12, fill="muted"))
        for y in range(height):
            body.append(_text(left - 16, top + y * cell + cell / 2, str(y),
                              size=12, fill="muted"))
        body.append(_text(left + width * cell / 2, top - 38,
                          "x: horizontal →", size=13, fill="text",
                          weight="bold"))
        middle = top + height * cell / 2
        body.append(
            f'<g transform="rotate(90 {left - 40:g} {middle:g})">'
            + _text(left - 40, middle, "y: vertical →", size=13, fill="text",
                    weight="bold")
            + "</g>"
        )
    total_w = left * 2 - base_left + width * cell + 16
    total_h = top + height * cell + bottom
    if caption:
        body.append(_text(total_w / 2, total_h - 17, caption, size=13,
                          fill="muted"))
    return _svg(total_w, total_h, body)


def cell_bits_svg(bits: int, *, caption: str | None = None) -> str:
    """Desenha uma célula grande com o nome e o valor de cada parede.

    As paredes fechadas saem cheias; as abertas, tracejadas.

    Args:
        bits: Paredes fechadas, de 0 a 15.
        caption: Legenda abaixo do desenho.

    Returns:
        O documento SVG.
    """
    size, left, top = 150, 110, 50
    x0, y0, x1, y1 = left, top, left + size, top + size
    body: list[str] = []
    sides = (
        (N, x0, y0, x1, y0, "Norte = 1", (x0 + x1) / 2, y0 - 22),
        (E, x1, y0, x1, y1, "Leste = 2", x1 + 52, (y0 + y1) / 2),
        (S, x0, y1, x1, y1, "Sul = 4", (x0 + x1) / 2, y1 + 22),
        (W, x0, y0, x0, y1, "Oeste = 8", x0 - 52, (y0 + y1) / 2),
    )
    for bit, ax, ay, bx, by, label, tx, ty in sides:
        closed = bool(bits & bit)
        body.append(_line(ax, ay, bx, by, "wall" if closed else "open",
                          8 if closed else 3, None if closed else "8 8"))
        body.append(_text(tx, ty, label, size=15,
                          fill="text" if closed else "muted",
                          weight="bold" if closed else "normal"))
    body.append(_text((x0 + x1) / 2, (y0 + y1) / 2 - 12, f"{bits}",
                      size=34, weight="bold"))
    body.append(_text((x0 + x1) / 2, (y0 + y1) / 2 + 22,
                      f'"{bits:x}"  0b{bits:04b}', size=14, fill="muted"))
    total_w, total_h = x1 + 110, y1 + (70 if caption else 46)
    if caption:
        body.append(_text(total_w / 2, total_h - 20, caption, size=13,
                          fill="muted"))
    return _svg(total_w, total_h, body)


def sides_svg() -> str:
    """Desenha uma célula com o nome de cada um dos quatro lados.

    Returns:
        O documento SVG.
    """
    size, left, top = 150, 150, 64
    x0, y0, x1, y1 = left, top, left + size, top + size
    body = [
        f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" '
        f'fill="{COLORS["highlight"]}"/>',
        _line(x0, y0, x1, y0, "wall", 8),
        _line(x1, y0, x1, y1, "wall", 8),
        _line(x0, y1, x1, y1, "wall", 8),
        _line(x0, y0, x0, y1, "wall", 8),
        _text((x0 + x1) / 2, (y0 + y1) / 2, "célula", size=18,
              weight="bold"),
        _text((x0 + x1) / 2, y0 - 32, "Norte", size=17, weight="bold"),
        _text((x0 + x1) / 2, y0 - 13, "o lado de cima", size=13,
              fill="muted"),
        _text((x0 + x1) / 2, y1 + 18, "Sul", size=17, weight="bold"),
        _text((x0 + x1) / 2, y1 + 37, "o lado de baixo", size=13,
              fill="muted"),
        _text(x1 + 70, (y0 + y1) / 2 - 10, "Leste", size=17,
              weight="bold"),
        _text(x1 + 70, (y0 + y1) / 2 + 10, "o lado direito", size=13,
              fill="muted"),
        _text(x0 - 70, (y0 + y1) / 2 - 10, "Oeste", size=17,
              weight="bold"),
        _text(x0 - 70, (y0 + y1) / 2 + 10, "o lado esquerdo", size=13,
              fill="muted"),
    ]
    return _svg(x1 + left, y1 + 58, body)


def bits_svg(bits: int) -> str:
    """Desenha os 4 bits de uma célula na ordem em que se escreve o binário.

    O bit 3 (Oeste) fica à esquerda e o bit 0 (Norte) à direita, como as
    casas de um número: a da direita é a de menor valor.

    Args:
        bits: Paredes fechadas, de 0 a 15.

    Returns:
        O documento SVG.
    """
    box, gap, left, top = 92, 14, 40, 78
    names = ("Oeste", "Sul", "Leste", "Norte")
    body: list[str] = []
    terms: list[str] = []
    for index, name in enumerate(names):
        position = 3 - index
        value = 1 << position
        on = bool(bits & value)
        x = left + index * (box + gap)
        middle = x + box / 2
        body.append(_text(middle, top - 46, name, size=16, weight="bold"))
        body.append(_text(middle, top - 22, f"vale {value}", size=14,
                          fill="muted"))
        body.append(
            f'<rect x="{x:g}" y="{top}" width="{box}" height="{box}" rx="10" '
            f'fill="{COLORS["wall"] if on else COLORS["background"]}" '
            f'stroke="{COLORS["wall"]}" stroke-width="3"/>'
        )
        body.append(_text(middle, top + box / 2, "1" if on else "0",
                          size=40, weight="bold",
                          fill="#ffffff" if on else "muted"))
        body.append(_text(middle, top + box + 22, f"bit {position}",
                          size=14, fill="muted"))
        body.append(_text(middle, top + box + 44,
                          "fechada" if on else "aberta", size=14,
                          fill="text" if on else "muted",
                          weight="bold" if on else "normal"))
        terms.append(str(value) if on else "0")
    width = left * 2 + 4 * box + 3 * gap
    arrow_y = top + box + 78
    body.append(
        f'<line x1="{width - left:g}" y1="{arrow_y}" x2="{left + 10:g}" '
        f'y2="{arrow_y}" stroke="{COLORS["muted"]}" stroke-width="2" '
        f'marker-end="url(#seta)"/>'
    )
    body.insert(0, (
        '<defs><marker id="seta" markerWidth="10" markerHeight="10" '
        'refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" '
        f'fill="{COLORS["muted"]}"/></marker></defs>'
    ))
    body.append(_text(width / 2, arrow_y + 20,
                      "o bit 0 é o da direita; o valor dobra a cada casa "
                      "para a esquerda", size=13, fill="muted"))
    body.append(_text(width / 2, arrow_y + 54,
                      f"0b{bits:04b} = {' + '.join(terms)} = {bits} "
                      f"= \"{bits:x}\"", size=18, weight="bold"))
    return _svg(width, arrow_y + 80, body)


def save(svg: str, path: Path) -> None:
    """Grava o SVG, criando a pasta se preciso.

    Args:
        svg: Documento SVG.
        path: Destino.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
