"""Lê as linhas coloridas do RenderService e as desenha em SVG.

Só usa a biblioteca padrão. Cada linha do desenho do terminal é decodificada
de volta em caracteres, cada um com a cor do texto e a do fundo que as
sequências SGR de 24 bits lhe deram; os caracteres de caixa viram retângulos
do centro do caractere até as bordas dos braços dele.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from html import escape

from svg import _svg, _text, color

Rgb = tuple[int, int, int]
Char = tuple[str, Rgb, Rgb]
Rows = list[list[Char]]
Spot = tuple[int, int]

N, E, S, W = 1, 2, 4, 8
SGR = re.compile(r"\x1b\[([0-9;]*)m")
TERMINAL = "#1f2328"
TERMINAL_TEXT = "#e5e7eb"
MONO = 'font-family="ui-monospace, Menlo, Consolas, monospace"'


def hex_colour(rgb: Rgb) -> str:
    """Escreve uma cor RGB no formato CSS.

    Args:
        rgb: Vermelho, verde e azul, de 0 a 255.

    Returns:
        A cor como #rrggbb.
    """
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def decode(lines: Sequence[str]) -> Rows:
    """Devolve cada caractere das linhas com a cor do texto e a do fundo.

    Args:
        lines: Linhas devolvidas por RenderService.render.

    Returns:
        rows[linha][coluna] = (caractere, cor do texto, cor do fundo).

    Raises:
        ValueError: A linha tem uma sequência que não é a de 24 bits nem o
            reset, um caractere sem cor ou não termina com o reset.
    """
    rows: Rows = []
    for line in lines:
        row: list[Char] = []
        colours: tuple[Rgb, Rgb] | None = None
        position = 0
        for match in SGR.finditer(line):
            for char in line[position:match.start()]:
                if colours is None:
                    raise ValueError(f"caractere sem cor: {line!r}")
                row.append((char, *colours))
            params = [int(part) for part in match.group(1).split(";")]
            if params == [0]:
                colours = None
            elif (len(params) == 10 and params[:2] == [38, 2]
                  and params[5:7] == [48, 2]):
                colours = ((params[2], params[3], params[4]),
                           (params[7], params[8], params[9]))
            else:
                raise ValueError(f"sequência inesperada: {match.group(0)!r}")
            position = match.end()
        if colours is not None or position != len(line):
            raise ValueError(f"linha sem o reset no fim: {line!r}")
        rows.append(row)
    return rows


def arms_table(glyph: object) -> dict[str, int]:
    """Monta, a partir de Box.glyph, os braços de cada caractere de caixa.

    Args:
        glyph: A função Box.glyph da implementação.

    Returns:
        Caractere -> soma dos bits dos braços (N=1, E=2, S=4, W=8).
    """
    if not callable(glyph):
        raise TypeError("Box.glyph precisa ser chamável")
    table: dict[str, int] = {}
    for arms in range(16):
        char = glyph(arms)
        if not isinstance(char, str):
            raise TypeError("Box.glyph precisa devolver str")
        table[char] = arms
    return table


def _rect(x: float, y: float, width: float, height: float, fill: str,
          extra: str = "") -> str:
    """Cria um retângulo sem contorno.

    Args:
        x: Canto esquerdo.
        y: Topo.
        width: Largura.
        height: Altura.
        fill: Cor CSS.
        extra: Atributos a mais.

    Returns:
        O elemento SVG.
    """
    return (f'<rect x="{x:g}" y="{y:g}" width="{width:g}" '
            f'height="{height:g}" fill="{fill}"{extra}/>')


def glyph_path(arms: int, x: float, y: float, cw: float, ch: float,
               weight: float) -> str:
    """Contorno das linhas de um caractere de caixa, para um <path>.

    Cada braço é um retângulo do centro do caractere até a borda; o
    quadrado do centro liga os braços.

    Args:
        arms: Soma dos bits dos braços.
        x: Canto esquerdo do caractere.
        y: Topo do caractere.
        cw: Largura do caractere.
        ch: Altura do caractere.
        weight: Espessura das linhas.

    Returns:
        Os comandos do path; vazio sem braços.
    """
    if not arms:
        return ""
    cx, cy, half = x + cw / 2, y + ch / 2, weight / 2
    boxes = [(cx - half, cy - half, weight, weight)]
    if arms & N:
        boxes.append((cx - half, y, weight, ch / 2))
    if arms & S:
        boxes.append((cx - half, cy, weight, ch / 2))
    if arms & E:
        boxes.append((cx, cy - half, cw / 2, weight))
    if arms & W:
        boxes.append((x, cy - half, cw / 2, weight))
    return "".join(f"M{bx:g} {by:g}h{bw:g}v{bh:g}h{-bw:g}z"
                   for bx, by, bw, bh in boxes)


def chars_body(rows: Rows, arms: Mapping[str, int], left: float, top: float,
               cw: float, ch: float,
               overlay: Mapping[Spot, str] | None = None) -> list[str]:
    """Desenha os caracteres decodificados: fundos, realces e linhas.

    Args:
        rows: Saída de decode.
        arms: Saída de arms_table.
        left: Canto esquerdo do desenho.
        top: Topo do desenho.
        cw: Largura de um caractere.
        ch: Altura de um caractere.
        overlay: Cor translúcida por (coluna, linha), por cima do fundo.

    Returns:
        Os elementos SVG.

    Raises:
        ValueError: Um caractere que não é espaço nem caractere de caixa.
    """
    body: list[str] = []
    crisp = ' shape-rendering="crispEdges"'
    for line, row in enumerate(rows):
        start = 0
        for column in range(1, len(row) + 1):
            if column == len(row) or row[column][2] != row[start][2]:
                body.append(_rect(left + start * cw, top + line * ch,
                                  (column - start) * cw, ch,
                                  hex_colour(row[start][2]), crisp))
                start = column
    for (column, line), name in (overlay or {}).items():
        body.append(_rect(left + column * cw, top + line * ch, cw, ch,
                          color(name), ' fill-opacity="0.75"'))
    paths: dict[Rgb, list[str]] = {}
    for line, row in enumerate(rows):
        for column, (char, text, _) in enumerate(row):
            if char not in arms:
                raise ValueError(f"caractere inesperado: {char!r}")
            piece = glyph_path(arms[char], left + column * cw,
                               top + line * ch, cw, ch, cw * 0.3)
            if piece:
                paths.setdefault(text, []).append(piece)
    for text, pieces in paths.items():
        body.append(f'<path d="{"".join(pieces)}" '
                    f'fill="{hex_colour(text)}"/>')
    return body


def grid_lines(columns: int, lines: int, left: float, top: float,
               cw: float, ch: float) -> list[str]:
    """Linhas finas que separam os caracteres, com os números dos eixos.

    Args:
        columns: Número de colunas.
        lines: Número de linhas.
        left: Canto esquerdo do desenho.
        top: Topo do desenho.
        cw: Largura de um caractere.
        ch: Altura de um caractere.

    Returns:
        Os elementos SVG.
    """
    body: list[str] = []
    stroke = 'stroke="#9ca3af" stroke-width="0.6" stroke-dasharray="2 2"'
    for column in range(columns + 1):
        x = left + column * cw
        body.append(f'<line x1="{x:g}" y1="{top:g}" x2="{x:g}" '
                    f'y2="{top + lines * ch:g}" {stroke}/>')
    for line in range(lines + 1):
        y = top + line * ch
        body.append(f'<line x1="{left:g}" y1="{y:g}" '
                    f'x2="{left + columns * cw:g}" y2="{y:g}" {stroke}/>')
    for column in range(columns):
        body.append(_text(left + column * cw + cw / 2, top - 12, str(column),
                          size=11, fill="muted"))
    for line in range(lines):
        body.append(_text(left - 14, top + line * ch + ch / 2, str(line),
                          size=11, fill="muted"))
    return body


def drawing_svg(rows: Rows, arms: Mapping[str, int], *, cw: float,
                ch: float, caption: str | None = None, axes: bool = False,
                overlay: Mapping[Spot, str] | None = None,
                outline: Mapping[Spot, str] | None = None) -> str:
    """Desenha um desenho do terminal, com moldura escura em volta.

    Args:
        rows: Saída de decode.
        arms: Saída de arms_table.
        cw: Largura de um caractere.
        ch: Altura de um caractere.
        caption: Legenda abaixo do desenho.
        axes: Separa os caracteres e numera colunas e linhas; sem moldura.
        overlay: Cor translúcida por (coluna, linha).
        outline: Cor do contorno por (coluna, linha), por cima de tudo.

    Returns:
        O documento SVG.
    """
    columns, lines = len(rows[0]), len(rows)
    frame = 0 if axes else 12
    margin = 40 if axes else 16
    inner_w, inner_h = columns * cw, lines * ch
    used = inner_w + 2 * (frame + margin)
    width = max(used, len(caption) * 7.4 + 40 if caption else 0)
    left = (width - inner_w) / 2
    top = margin + frame
    body: list[str] = []
    if frame:
        body.append(_rect(left - frame, top - frame, inner_w + 2 * frame,
                          inner_h + 2 * frame, TERMINAL, ' rx="6"'))
    body.extend(chars_body(rows, arms, left, top, cw, ch, overlay))
    if axes:
        body.extend(grid_lines(columns, lines, left, top, cw, ch))
    for (column, line), name in (outline or {}).items():
        body.append(f'<rect x="{left + column * cw + 2:g}" '
                    f'y="{top + line * ch + 2:g}" width="{cw - 4:g}" '
                    f'height="{ch - 4:g}" fill="none" stroke="{color(name)}" '
                    f'stroke-width="3"/>')
    height = top + inner_h + frame + (40 if caption else 16)
    if caption:
        body.append(_text(width / 2, height - 20, caption, size=13,
                          fill="muted"))
    return _svg(width, height, body)


def panels_svg(panels: Sequence[tuple[Rows, str]], arms: Mapping[str, int],
               *, cw: float, ch: float, columns: int,
               overlays: Sequence[Mapping[Spot, str]] = ()) -> str:
    """Desenha vários desenhos do terminal lado a lado, cada um com legenda.

    Args:
        panels: Pares (rows, legenda).
        arms: Saída de arms_table.
        cw: Largura de um caractere.
        ch: Altura de um caractere.
        columns: Quantos painéis por linha.
        overlays: Por painel, cores translúcidas por (coluna, linha).

    Returns:
        O documento SVG.
    """
    pad, gap, frame, label_h = 16, 28, 10, 28
    pw = len(panels[0][0][0]) * cw
    ph = len(panels[0][0]) * ch
    rows_n = (len(panels) + columns - 1) // columns
    cell_w, cell_h = pw + 2 * frame, ph + 2 * frame + label_h
    total_w = pad * 2 + columns * cell_w + (columns - 1) * gap
    total_h = pad * 2 + rows_n * cell_h + (rows_n - 1) * gap
    body: list[str] = []
    for index, (rows, label) in enumerate(panels):
        ox = pad + (index % columns) * (cell_w + gap)
        oy = pad + (index // columns) * (cell_h + gap)
        body.append(_rect(ox, oy, cell_w, ph + 2 * frame, TERMINAL,
                          ' rx="6"'))
        overlay = overlays[index] if index < len(overlays) else None
        body.extend(chars_body(rows, arms, ox + frame, oy + frame, cw, ch,
                               overlay))
        body.append(_text(ox + cell_w / 2, oy + ph + 2 * frame + label_h / 2,
                          label, size=13, fill="muted"))
    return _svg(total_w, total_h, body)


def session_svg(before: Sequence[str], rows: Rows, after: Sequence[str],
                arms: Mapping[str, int], *, cw: float, ch: float) -> str:
    """Desenha uma tela de terminal: texto, o desenho e mais texto.

    O texto usa a mesma grade de caracteres do desenho: cada linha de texto
    tem a altura de uma linha do desenho, e cada caractere a largura de um.

    Args:
        before: Linhas de texto acima do desenho.
        rows: Saída de decode.
        after: Linhas de texto abaixo do desenho.
        arms: Saída de arms_table.
        cw: Largura de um caractere.
        ch: Altura de um caractere.

    Returns:
        O documento SVG.
    """
    pad = 18
    widest = max([len(rows[0]), *(len(line) for line in [*before, *after])])
    total_w = pad * 2 + widest * cw
    total_h = pad * 2 + (len(before) + len(rows) + len(after)) * ch
    body = [_rect(0, 0, total_w, total_h, TERMINAL, ' rx="8"')]

    def text(line: int, value: str) -> str:
        return (f'<text x="{pad}" y="{pad + line * ch + ch / 2:g}" {MONO} '
                f'font-size="{cw / 0.6:g}" textLength="{len(value) * cw:g}" '
                f'fill="{TERMINAL_TEXT}" dominant-baseline="central" '
                f'xml:space="preserve">{escape(value)}</text>')

    for line, value in enumerate(before):
        if value:
            body.append(text(line, value))
    body.extend(chars_body(rows, arms, pad, pad + len(before) * ch, cw, ch))
    first = len(before) + len(rows)
    for line, value in enumerate(after):
        if value:
            body.append(text(first + line, value))
    return _svg(total_w, total_h, body)


def layout_svg(width: int, height: int, labels: Mapping[Spot, str], *,
               caption: str, cw: float, ch: float) -> str:
    """Esquema da grade de caracteres de um labirinto, pelo tipo de lugar.

    Os cantos ficam nas linhas pares e nas colunas múltiplas de 4; o resto
    das linhas pares e das colunas múltiplas de 4 são lugares de parede; o
    resto é o interior das células, com o centro na coluna 4x + 2.

    Args:
        width: Colunas de células.
        height: Linhas de células.
        labels: Texto por (coluna, linha) do desenho.
        caption: Legenda abaixo do desenho.
        cw: Largura de um caractere.
        ch: Altura de um caractere.

    Returns:
        O documento SVG.
    """
    columns, lines = 4 * width + 1, 2 * height + 1
    inner_w, inner_h = columns * cw, lines * ch
    width_px = max(inner_w + 2 * 56, len(caption) * 7.4 + 40)
    left, top, gap = (width_px - inner_w) / 2, 64, 2
    body: list[str] = []
    for line in range(lines):
        for column in range(columns):
            if line % 2 == 0 and column % 4 == 0:
                name = "wall"
            elif line % 2 == 0 or column % 4 == 0:
                name = "stack"
            elif column % 4 == 2:
                name = "#fcd34d"
            else:
                name = "highlight"
            body.append(_rect(left + column * cw + gap / 2,
                              top + line * ch + gap / 2, cw - gap, ch - gap,
                              color(name)))
            value = labels.get((column, line))
            if value:
                body.append(_text(left + column * cw + cw / 2,
                                  top + line * ch + ch / 2, value,
                                  size=min(cw * 0.5, 13), weight="bold",
                                  fill="#ffffff" if name == "wall"
                                  else "text"))
    for column in range(columns):
        body.append(_text(left + column * cw + cw / 2, top - 12, str(column),
                          size=11, fill="muted"))
    for line in range(lines):
        body.append(_text(left - 16, top + line * ch + ch / 2, str(line),
                          size=11, fill="muted"))
    body.append(_text(left + inner_w / 2, top - 36, "coluna do desenho →",
                      size=13, weight="bold"))
    middle = top + inner_h / 2
    body.append(f'<g transform="rotate(90 {left - 38:g} {middle:g})">'
                + _text(left - 38, middle, "linha do desenho →", size=13,
                        weight="bold")
                + "</g>")
    height_px = top + inner_h + 48
    body.append(_text(width_px / 2, height_px - 20, caption, size=13,
                      fill="muted"))
    return _svg(width_px, height_px, body)
