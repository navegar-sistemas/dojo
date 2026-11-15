"""Gera as imagens das partes 10 (utilitários), 11 (configuração) e 12.

Uso, na pasta tutorial/:

    python3 scripts/imagens_partes_10_a_12.py <raiz da implementação>

A implementação pronta fornece o pacote mazegen, que gera os labirintos
reais.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path
from typing import Any

from svg import COLORS, _svg, _text, grid_from_hex, maze_svg, save
from terminal import SGR, arms_table, chars_body, decode, hex_colour

IMG = Path(__file__).resolve().parent.parent / "static" / "img"
UTILS = IMG / "utilitarios"
CONFIG = IMG / "configuracao"
OUTPUT = IMG / "geracao"
STEP = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

# Nome da constante de Ansi e o que ela pinta no desenho.
PALETTE = (
    ("WHITE", "fundo de tudo"),
    ("CHARCOAL", "parede (1ª cor)"),
    ("ORANGE", "parede (2ª cor)"),
    ("GREEN", "parede (3ª cor)"),
    ("BLUE", "parede (4ª cor)"),
    ("GREY", "fundo do \"42\""),
    ("MAGENTA", "fundo da entrada"),
    ("RED", "fundo da saída"),
    ("CYAN", "linha do caminho"),
)
NAMES = {1: "N", 2: "L", 4: "S", 8: "O"}
MONO = 'font-family="ui-monospace, Menlo, Consolas, monospace"'


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


def swatch(x: float, y: float, size: float, fill: str) -> str:
    """Cria um quadrado da cor indicada, com contorno.

    Args:
        x: Canto esquerdo.
        y: Topo.
        size: Lado.
        fill: Cor CSS.

    Returns:
        O elemento SVG.
    """
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{size:g}" height="{size:g}" '
        f'rx="4" fill="{fill}" stroke="#9ca3af" stroke-width="1"/>'
    )


def mono(x: float, y: float, value: str, size: float = 13,
         anchor: str = "start", fill: str = "text") -> str:
    """Cria um texto em fonte de largura fixa, com os espaços preservados.

    Args:
        x: Posição horizontal.
        y: Posição vertical do centro.
        value: Texto.
        size: Tamanho da fonte.
        anchor: Âncora horizontal.
        fill: Cor.

    Returns:
        O elemento SVG.
    """
    return (f'<text x="{x:g}" y="{y:g}" {MONO} font-size="{size:g}" '
            f'fill="{COLORS.get(fill, fill)}" text-anchor="{anchor}" '
            f'dominant-baseline="central" xml:space="preserve">'
            f"{escape(value)}</text>")


def palette_svg(ansi: Any) -> str:
    """Desenha as cores de Ansi: nome, valores RGB e uso.

    Args:
        ansi: A classe Ansi da implementação.

    Returns:
        O documento SVG.
    """
    column, size, left, top, per_row, row_height = 128, 44, 20, 20, 5, 130
    body: list[str] = []
    for index, (name, role) in enumerate(PALETTE):
        rgb = getattr(ansi, name)
        cx = left + index % per_row * column + column / 2
        cy = top + index // per_row * row_height
        body.append(swatch(cx - size / 2, cy, size, hex_colour(rgb)))
        body.append(_text(cx, cy + size + 18, name, size=13,
                          weight="bold"))
        body.append(_text(cx, cy + size + 36, "{}, {}, {}".format(*rgb),
                          size=12, fill="muted"))
        body.append(_text(cx, cy + size + 54, role, size=12,
                          fill="muted"))
    rows = (len(PALETTE) + per_row - 1) // per_row
    width = left * 2 + per_row * column
    return _svg(width, top + (rows - 1) * row_height + size + 76, body)


def line_svg(line: str, arms: dict[str, int]) -> str:
    """Separa uma linha real do desenho nos trechos de cada sequência SGR.

    Em cima, a linha desenhada, com o número de cada trecho; embaixo, o
    texto que o programa imprime para cada trecho.

    Args:
        line: Uma linha devolvida por RenderService.render.
        arms: Saída de arms_table.

    Returns:
        O documento SVG.
    """
    rows = decode([line])
    matches = list(SGR.finditer(line))
    ends = [match.start() for match in matches[1:]] + [len(line)]
    segments = [(f"\\x1b[{match.group(1)}m", line[match.end():end])
                for match, end in zip(matches, ends)]
    cw, ch, left, top = 22.0, 44.0, 70.0, 44.0
    body = chars_body(rows, arms, left, top, cw, ch)
    body.append(f'<rect x="{left:g}" y="{top:g}" '
                f'width="{len(rows[0]) * cw:g}" height="{ch:g}" fill="none" '
                f'stroke="#9ca3af" stroke-width="1"/>')
    start = 0
    for number, (_, text) in enumerate(segments[:-1], start=1):
        x0, x1 = left + start * cw, left + (start + len(text)) * cw
        body.append(f'<line x1="{x0 + 2:g}" y1="{top - 8:g}" '
                    f'x2="{x1 - 2:g}" y2="{top - 8:g}" stroke="#6b7280" '
                    f'stroke-width="2"/>')
        body.append(_text((x0 + x1) / 2, top - 22, str(number), size=13,
                          weight="bold"))
        start += len(text)
    y = top + ch + 34
    for number, (sequence, text) in enumerate(segments, start=1):
        label = str(number) if text else "fim"
        body.append(_text(left - 30, y, label, size=13, weight="bold"))
        shown = f'"{sequence}"' + (f' + "{text}"' if text else "")
        body.append(mono(left, y, shown))
        y += 26
    caption = ("cada trecho: a sequência das cores e os caracteres que ela "
               "pinta; o reset fecha a linha")
    width = max(left + max(len(rows[0]) * cw, 7.9 * max(
        len(f'"{seq}" + "{text}"') for seq, text in segments)) + 30,
        len(caption) * 7.4 + 40)
    body.append(_text(width / 2, y + 10, caption, size=13, fill="muted"))
    return _svg(width, y + 32, body)


def sequence_svg(ansi: Any) -> str:
    """Decompõe a sequência de texto grafite e fundo branco nas suas peças.

    À direita, o texto "Ab" decodificado da mesma sequência.

    Args:
        ansi: A classe Ansi da implementação.

    Returns:
        O documento SVG.
    """
    sequence = ansi.colours(ansi.CHARCOAL, ansi.WHITE)
    inner = sequence[2:-1]
    text_part, back_part = inner[:inner.index(";48")], inner[
        inner.index(";48") + 1:]
    pieces = (
        ("ESC", "\\x1b", "avisa: vem um", "comando"),
        ("[", "", "abre o", "comando"),
        (text_part, "", "38;2: cor do texto", "R;G;B: grafite"),
        (";", "", "separa os", "números"),
        (back_part, "", "48;2: cor do fundo", "R;G;B: branco"),
        ("m", "", "fecha: é um", "comando de cor"),
    )
    gap, left, top, height = 12, 30, 60, 64
    body = [mono(left, 26, f'Python: "\\x1b[{inner}m"', size=14)]
    x = float(left)
    for label, code, first, second in pieces:
        width = max(104.0, len(label) * 10.5 + 24)
        body.append(
            f'<rect x="{x:g}" y="{top}" width="{width:g}" height="{height}" '
            f'rx="8" fill="{COLORS["highlight"]}" stroke="{COLORS["wall"]}" '
            f'stroke-width="2"/>'
        )
        shift = 10 if code else 0
        body.append(mono(x + width / 2, top + height / 2 - shift, label,
                         size=17, anchor="middle"))
        if code:
            body.append(_text(x + width / 2, top + height / 2 + 16, code,
                              size=12, fill="muted"))
        body.append(_text(x + width / 2, top + height + 22, first, size=13))
        body.append(_text(x + width / 2, top + height + 40, second, size=13))
        x += width + gap
    sample = x + 24
    for index, (char, text, back) in enumerate(
            decode([sequence + "Ab" + ansi.RESET])[0]):
        cx = sample + index * 28
        body.append(f'<rect x="{cx:g}" y="{top + 4}" width="28" height="56" '
                    f'fill="{hex_colour(back)}" stroke="#d1d5db" '
                    f'stroke-width="1"/>')
        body.append(mono(cx + 14, top + 32, char, size=40, anchor="middle",
                         fill=hex_colour(text)))
    body.append(_text(sample + 28, top + height + 22, "o que vier", size=13))
    body.append(_text(sample + 28, top + height + 40, "depois", size=13))
    return _svg(sample + 90, top + height + 64, body)


def arms_svg(glyph: Any) -> str:
    """Desenha os 16 caracteres de Box.glyph com os braços de cada um.

    Args:
        glyph: A função Box.glyph da implementação.

    Returns:
        O documento SVG.
    """
    cw, ch, column, per_row, left, top = 34, 68, 78, 8, 24, 20
    arms = arms_table(glyph)
    white, charcoal = (255, 255, 255), (31, 41, 55)
    body: list[str] = []
    for value in range(16):
        x = left + value % per_row * column + (column - cw) / 2
        y = top + value // per_row * (ch + 70)
        rows = decode(["\x1b[38;2;{};{};{};48;2;{};{};{}m".format(
            *charcoal, *white) + glyph(value) + "\x1b[0m"])
        body.append(f'<rect x="{x:g}" y="{y:g}" width="{cw}" height="{ch}" '
                    f'fill="#f9fafb" stroke="#9ca3af" stroke-width="1" '
                    f'stroke-dasharray="3 3"/>')
        body.extend(chars_body(rows, arms, x, y, cw, ch)[1:])
        names = "+".join(name for bit, name in NAMES.items() if value & bit)
        body.append(_text(x + cw / 2, y + ch + 18, str(value), size=15,
                          weight="bold"))
        body.append(_text(x + cw / 2, y + ch + 38, names or "nenhum",
                          size=12, fill="muted"))
    width = left * 2 + per_row * column
    height = top + 2 * (ch + 70) + 20
    caption = ("N = Norte (1) · L = Leste (2) · S = Sul (4) · O = Oeste (8); "
               "o número é a soma dos braços")
    body.append(_text(width / 2, height - 18, caption, size=13,
                      fill="muted"))
    return _svg(width, height, body)


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
    from amazeing.domain.entities.view_state import ViewState
    from amazeing.domain.value_objects.generated_maze import GeneratedMaze
    from amazeing.services.render_service import RenderService
    from amazeing.utils.ansi import Ansi
    from amazeing.utils.box import Box
    from mazegen import MazeGenerator

    arms = arms_table(Box.glyph)
    example = GeneratedMaze(((13, 5, 3), (13, 5, 6)), (0, 0), (0, 1),
                            "EESWW", frozenset())
    second = RenderService().render(example, ViewState())[1]
    save(palette_svg(Ansi), UTILS / "paleta-ansi.svg")
    save(line_svg(second, arms), UTILS / "linha-sgr.svg")
    save(sequence_svg(Ansi), UTILS / "sequencia-sgr.svg")
    save(arms_svg(Box.glyph), UTILS / "caixa-bracos.svg")
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
