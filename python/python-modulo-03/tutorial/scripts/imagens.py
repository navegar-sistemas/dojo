"""Gera as imagens SVG do tutorial em static/img/.

Uso: python3 scripts/imagens.py

Só usa a biblioteca padrão. Rodar de novo gera arquivos idênticos. Os dados
vêm dos exemplos do enunciado; cada figura confere, com assert, que as contas
desenhadas batem com a saída que o enunciado mostra.
"""

from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = 'font-family="ui-sans-serif, system-ui, sans-serif"'
MONO = 'font-family="ui-monospace, SFMono-Regular, Menlo, monospace"'

COLORS = {
    "background": "#ffffff",
    "line": "#1f2937",
    "text": "#111827",
    "muted": "#6b7280",
    "faint": "#e5e7eb",
    "box": "#f3f4f6",
    "blue": "#2563eb",
    "blue_fill": "#dbeafe",
    "green": "#16a34a",
    "green_fill": "#bbf7d0",
    "red": "#dc2626",
    "red_fill": "#fee2e2",
    "orange": "#ea580c",
    "orange_fill": "#fed7aa",
    "purple": "#7c3aed",
    "purple_fill": "#ede9fe",
}

Point = tuple[float, float]


def text(x: float, y: float, value: str, *, size: int = 14,
         fill: str = "text", anchor: str = "middle",
         weight: str = "normal", mono: bool = False) -> str:
    """Escreve um texto SVG.

    Args:
        x: Posição horizontal.
        y: Posição vertical da linha de base.
        value: O texto.
        size: Tamanho da fonte.
        fill: Nome da cor na paleta.
        anchor: Alinhamento horizontal (start, middle ou end).
        weight: Peso da fonte.
        mono: Usa fonte de largura fixa, para código.

    Returns:
        O elemento <text>.
    """
    family = MONO if mono else FONT
    return (
        f'<text x="{x:g}" y="{y:g}" {family} font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS[fill]}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, *,
         fill: str = "box", stroke: str = "line", radius: float = 6,
         stroke_width: float = 1.5, dashed: bool = False) -> str:
    """Desenha um retângulo de cantos arredondados.

    Args:
        x: Canto esquerdo.
        y: Canto de cima.
        width: Largura.
        height: Altura.
        fill: Nome da cor de dentro.
        stroke: Nome da cor da borda.
        radius: Raio dos cantos.
        stroke_width: Espessura da borda.
        dashed: Borda tracejada.

    Returns:
        O elemento <rect>.
    """
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="{radius:g}" fill="{COLORS[fill]}" stroke="{COLORS[stroke]}" '
        f'stroke-width="{stroke_width:g}"{dash}/>'
    )


def line(start: Point, end: Point, *, stroke: str = "line",
         width: float = 1.5, dashed: bool = False,
         arrow: bool = False) -> str:
    """Desenha um segmento, com ponta de seta opcional.

    Args:
        start: Ponto de partida.
        end: Ponto de chegada.
        stroke: Nome da cor.
        width: Espessura.
        dashed: Traço tracejado.
        arrow: Põe uma ponta de seta em end.

    Returns:
        O elemento <line>.
    """
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    head = f' marker-end="url(#arrow-{stroke})"' if arrow else ""
    return (
        f'<line x1="{start[0]:g}" y1="{start[1]:g}" x2="{end[0]:g}" '
        f'y2="{end[1]:g}" stroke="{COLORS[stroke]}" '
        f'stroke-width="{width:g}"{dash}{head}/>'
    )


def circle(center: Point, radius: float, *, fill: str = "box",
           stroke: str = "line", width: float = 1.5) -> str:
    """Desenha um círculo.

    Args:
        center: Centro.
        radius: Raio.
        fill: Nome da cor de dentro, ou "none".
        stroke: Nome da cor da borda.
        width: Espessura da borda.

    Returns:
        O elemento <circle>.
    """
    paint = "none" if fill == "none" else COLORS[fill]
    return (
        f'<circle cx="{center[0]:g}" cy="{center[1]:g}" r="{radius:g}" '
        f'fill="{paint}" stroke="{COLORS[stroke]}" '
        f'stroke-width="{width:g}"/>'
    )


def markers() -> str:
    """Define uma ponta de seta para cada cor da paleta.

    Returns:
        O elemento <defs> com os marcadores.
    """
    parts = []
    for name, value in COLORS.items():
        parts.append(
            f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" '
            f'refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{value}"/></marker>'
        )
    return "<defs>" + "".join(parts) + "</defs>"


def svg(width: int, height: int, title: str, body: list[str]) -> str:
    """Monta o documento SVG.

    Args:
        width: Largura em pixels.
        height: Altura em pixels.
        title: Título acessível da imagem.
        body: Os elementos do desenho.

    Returns:
        O texto do arquivo SVG.
    """
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f"<title>{escape(title)}</title>",
        markers(),
        f'<rect width="{width}" height="{height}" '
        f'fill="{COLORS["background"]}"/>',
        *body,
        "</svg>",
        "",
    ])


def save(relative: str, content: str) -> None:
    """Grava a imagem em static/img/.

    Args:
        relative: Caminho dentro de static/img/.
        content: O texto SVG.
    """
    path = ROOT / "static" / "img" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def search_list_vs_set() -> str:
    """Compara a busca em lista, um por um, com a busca em set, pelo hash.

    Returns:
        O SVG.
    """
    names = ["Crafting Genius", "World Savior", "Master Explorer",
             "Collector Supreme", "Boss Slayer", "Strategist",
             "Speed Runner", "Untouchable"]
    target = "Untouchable"
    drawers = {1: "Boss Slayer", 2: "Untouchable", 3: "World Savior",
               5: "Strategist", 6: "Crafting Genius", 8: "Speed Runner",
               9: "Master Explorer", 11: "Collector Supreme"}
    assert sorted(drawers.values()) == sorted(names)
    body = [
        text(210, 34, "lista: compara um por um", size=17, weight="bold"),
        text(650, 34, "set: o hash aponta a gaveta", size=17,
             weight="bold"),
        text(210, 58, f'"{target}" in achievements', size=13,
             fill="muted", mono=True),
        text(650, 58, f'"{target}" in achievements', size=13,
             fill="muted", mono=True),
    ]
    top = 76
    for index, name in enumerate(names):
        y = top + index * 34
        found = name == target
        body.append(text(92, y + 20, f"[{index}]", size=12, fill="muted",
                         anchor="end", mono=True))
        body.append(rect(100, y, 200, 28,
                         fill="green_fill" if found else "box",
                         stroke="green" if found else "line"))
        body.append(text(200, y + 19, name, size=13))
        body.append(circle((326, y + 14), 11,
                           fill="green" if found else "faint",
                           stroke="green" if found else "muted"))
        body.append(text(326, y + 18, str(index + 1), size=11,
                         fill="background" if found else "text",
                         weight="bold"))
    body.append(text(210, top + 8 * 34 + 26, "8 comparações", size=14,
                     fill="red", weight="bold"))

    slot_top = 76
    slot_height = 21
    body.append(rect(470, 140, 120, 46, fill="purple_fill",
                     stroke="purple"))
    body.append(text(530, 160, "hash(", size=13, mono=True))
    body.append(text(530, 178, f'"{target}")', size=12, mono=True))
    for slot in range(12):
        y = slot_top + slot * slot_height
        name = drawers.get(slot, "")
        found = name == target
        body.append(rect(640, y, 170, slot_height - 3, radius=3,
                         fill="green_fill" if found else
                         ("box" if name else "background"),
                         stroke="green" if found else "faint"))
        body.append(text(648, y + 14, str(slot), size=10, fill="muted",
                         anchor="start", mono=True))
        if name:
            body.append(text(732, y + 14, name, size=11))
    target_y = slot_top + 2 * slot_height + 9
    body.append(line((590, 163), (638, target_y), stroke="purple",
                     width=2, arrow=True))
    body.append(circle((836, target_y), 11, fill="green", stroke="green"))
    body.append(text(836, target_y + 4, "1", size=11, fill="background",
                     weight="bold"))
    body.append(text(650, top + 8 * 34 + 26, "1 comparação", size=14,
                     fill="green", weight="bold"))
    return svg(880, top + 8 * 34 + 46, "Busca em lista e em set", body)


def argv_boxes() -> str:
    """Mostra sys.argv do comando com hello world 42.

    Returns:
        O SVG.
    """
    argv = ["ft_command_quest.py", "hello", "world", "42"]
    widths = [210, 110, 110, 110]
    body = [text(380, 30, "python3 ft_command_quest.py hello world 42",
                 size=14, mono=True, fill="muted")]
    x = 40.0
    centers: list[float] = []
    for index, (value, width) in enumerate(zip(argv, widths)):
        is_name = index == 0
        body.append(text(x + width / 2, 66, f"sys.argv[{index}]", size=12,
                         fill="muted", mono=True))
        body.append(rect(x, 76, width, 44,
                         fill="box" if is_name else "blue_fill",
                         stroke="line" if is_name else "blue"))
        body.append(text(x + width / 2, 104, f"'{value}'", size=14,
                         mono=True))
        centers.append(x + width / 2)
        x += width + 12
    first_arg = 40 + widths[0] + 12
    last_end = x - 12
    body.append(line((first_arg, 136), (last_end, 136), stroke="blue",
                     width=2))
    body.append(text((first_arg + last_end) / 2, 158,
                     "sys.argv[1:]: os argumentos, len = 3", size=14,
                     fill="blue", weight="bold"))
    body.append(line((40, 180), (last_end, 180), stroke="line", width=2))
    body.append(text((40 + last_end) / 2, 202,
                     "sys.argv inteira: o total, len = 4", size=14,
                     weight="bold"))
    body.append(text(centers[0], 158, "o nome do programa", size=13,
                     fill="muted"))
    return svg(int(last_end + 40), 224, "A lista sys.argv", body)


def score_filter() -> str:
    """Mostra o filtro dos argumentos e as estatísticas das pontuações.

    Returns:
        O SVG.
    """
    arguments = ["1500", "ab", "2300", "1800"]
    scores = [int(a) for a in arguments if a.isdigit()]
    assert scores == [1500, 2300, 1800]
    average = sum(scores) / len(scores)
    high, low = max(scores), min(scores)
    row = 46
    body = [text(110, 28, "argumentos", size=15, weight="bold"),
            text(565, 28, "scores", size=15, weight="bold", mono=True)]
    valid_y: list[float] = []
    for index, argument in enumerate(arguments):
        y = 44 + index * row
        middle = y + 17
        ok = argument.isdigit()
        body.append(rect(60, y, 100, 34, fill="box" if ok else "red_fill",
                         stroke="line" if ok else "red"))
        body.append(text(110, y + 22, f"'{argument}'", size=14, mono=True))
        if ok:
            target = 61 + len(valid_y) * row
            body.append(line((162, middle), (496, target), arrow=True,
                             stroke="green", width=1.8))
            valid_y.append(target)
        else:
            body.append(line((162, middle), (218, middle), arrow=True,
                             stroke="red", width=1.8))
            body.append(text(226, middle + 5,
                             f"Invalid parameter: '{argument}'", size=12,
                             fill="red", anchor="start", mono=True))
    for index, score in enumerate(scores):
        body.append(rect(500, valid_y[index] - 17, 130, 34,
                         fill="green_fill", stroke="green"))
        body.append(text(565, valid_y[index] + 5, str(score), size=14,
                         mono=True))
        body.append(text(640, valid_y[index] + 5, f"[{index}]", size=11,
                         fill="muted", anchor="start", mono=True))

    base = 520
    scale = 0.08
    chart_left = 120
    body.append(text(440, 290, "as estatísticas da lista", size=15,
                     weight="bold"))
    body.append(line((chart_left - 20, base), (590, base)))
    for index, score in enumerate(scores):
        x = chart_left + index * 140
        height = score * scale
        body.append(rect(x, base - height, 80, height, radius=2,
                         fill="blue_fill", stroke="blue"))
        body.append(text(x + 40, base + 20, str(score), size=13, mono=True))
    # O programa imprime a média sem arredondar (1866.6666666666667); o
    # rótulo corta esse texto, para não sugerir um arredondamento.
    printed = str(average)
    shown = printed if len(printed) <= 8 else f"{printed[:8]}…"
    levels: list[tuple[float, str, str]] = [
        (high, f"maior: {high}", "red"),
        (low, f"menor: {low}", "blue"),
        (average, f"média: {shown}", "green"),
    ]
    for value, label, color in levels:
        level_y = base - value * scale
        body.append(line((chart_left - 20, level_y), (590, level_y),
                         stroke=color, dashed=True))
        body.append(text(600, level_y + 5, label, size=13, fill=color,
                         anchor="start", weight="bold"))
    top, bottom = base - high * scale, base - low * scale
    body.append(line((770, top), (770, bottom), stroke="orange", width=2,
                     arrow=True))
    body.append(line((770, bottom), (770, top), stroke="orange", width=2,
                     arrow=True))
    body.append(text(780, (top + bottom) / 2 + 5,
                     f"amplitude: {high - low}", size=13, fill="orange",
                     anchor="start", weight="bold"))
    body.append(text(440, base + 46,
                     f"quantidade {len(scores)}, total {sum(scores)}",
                     size=13, fill="muted"))
    return svg(900, base + 64, "Filtro e estatísticas das pontuações", body)


def distance_box() -> str:
    """Desenha a caixa entre dois pontos 3D e as duas diagonais.

    Returns:
        O SVG.
    """
    first = (1.0, 2.5, 3.0)
    second = (4.0, 5.0, 6.0)
    dx, dy, dz = (b - a for a, b in zip(first, second))
    total = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    assert round(total, 4) == 4.9244

    def project(x: float, y: float, z: float) -> Point:
        return (150 + 90 * x + 52 * y, 380 - 80 * z - 34 * y)

    a = project(0, 0, 0)
    b = project(dx, 0, 0)
    c = project(dx, dy, 0)
    d = project(0, dy, 0)
    a2 = project(0, 0, dz)
    b2 = project(dx, 0, dz)
    c2 = project(dx, dy, dz)
    d2 = project(0, dy, dz)
    body = []
    for start, end in ((a, d), (d, c), (d, d2)):
        body.append(line(start, end, stroke="muted", dashed=True, width=1))
    for start, end in ((b, b2), (a, a2), (a2, b2), (b2, c2), (c2, d2),
                       (d2, a2)):
        body.append(line(start, end, stroke="muted", width=1))
    body.append(line(a, b, stroke="red", width=3))
    body.append(line(b, c, stroke="green", width=3))
    body.append(line(c, c2, stroke="blue", width=3))
    body.append(line(a, c, stroke="orange", width=2, dashed=True))
    body.append(line(a, c2, stroke="purple", width=3.5))
    body.append(circle(a, 6, fill="line", stroke="line"))
    body.append(circle(c2, 6, fill="line", stroke="line"))
    body.append(text(a[0] - 10, a[1] + 26, "(1.0, 2.5, 3.0)", size=14,
                     mono=True, weight="bold"))
    body.append(text(c2[0] + 12, c2[1] - 12, "(4.0, 5.0, 6.0)", size=14,
                     mono=True, weight="bold", anchor="start"))
    body.append(text((a[0] + b[0]) / 2, a[1] + 26, f"Δx = {dx:g}", size=15,
                     fill="red", weight="bold"))
    body.append(text((b[0] + c[0]) / 2 + 30, (b[1] + c[1]) / 2 + 14,
                     f"Δy = {dy:g}", size=15, fill="green", weight="bold",
                     anchor="start"))
    body.append(text(c[0] + 12, (c[1] + c2[1]) / 2, f"Δz = {dz:g}",
                     size=15, fill="blue", weight="bold", anchor="start"))
    body.append(text((a[0] + c[0]) / 2 + 40, (a[1] + c[1]) / 2 + 22,
                     "√(3² + 2.5²)", size=14, fill="orange",
                     weight="bold"))
    body.append(text(30, 40, "distância = √(3² + 2.5² + 3²) = √24.25 "
                     f"≈ {round(total, 4)}", size=16, fill="purple",
                     weight="bold", anchor="start"))
    return svg(760, 420, "Distância entre dois pontos 3D", body)


def set_operations() -> str:
    """Desenha união, interseção e diferença de dois sets.

    Returns:
        O SVG.
    """
    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    results = [("a.union(b)", a.union(b)),
               ("a.intersection(b)", a.intersection(b)),
               ("a.difference(b)", a.difference(b))]
    body = ['<defs>']
    for panel in range(3):
        cx = 140 + panel * 260
        body.append(f'<clipPath id="clip-a-{panel}">'
                    f'<circle cx="{cx - 35}" cy="120" r="70"/></clipPath>')
    body.append('</defs>')
    for panel, (label, result) in enumerate(results):
        cx = 140 + panel * 260
        left, right = (cx - 35, 120.0), (cx + 35, 120.0)
        fill = COLORS["blue_fill"]
        if panel == 0:
            body.append(circle(left, 70, fill="blue_fill", stroke="blue"))
            body.append(circle(right, 70, fill="blue_fill", stroke="blue"))
        elif panel == 1:
            body.append(f'<circle cx="{right[0]:g}" cy="120" r="70" '
                        f'fill="{fill}" clip-path="url(#clip-a-{panel})"/>')
        else:
            body.append(circle(left, 70, fill="blue_fill", stroke="blue"))
            body.append(circle(right, 70, fill="background",
                               stroke="background"))
        body.append(circle(left, 70, fill="none", stroke="line"))
        body.append(circle(right, 70, fill="none", stroke="line"))
        body.append(text(left[0] - 70, 50, "a", size=16, weight="bold"))
        body.append(text(right[0] + 70, 50, "b", size=16, weight="bold"))
        body.append(text(left[0] - 30, 125, "1  2", size=15, mono=True))
        body.append(text(cx, 125, "3 4", size=15, mono=True))
        body.append(text(right[0] + 32, 125, "5", size=15, mono=True))
        shown = "{" + ", ".join(str(n) for n in sorted(result)) + "}"
        body.append(text(cx, 222, label, size=14, mono=True,
                         weight="bold"))
        body.append(text(cx, 246, shown, size=14, mono=True, fill="blue"))
    body.append(text(320, 278, "a = {1, 2, 3, 4}", size=13, fill="muted",
                     mono=True))
    body.append(text(480, 278, "b = {3, 4, 5}", size=13, fill="muted",
                     mono=True))
    return svg(800, 296, "União, interseção e diferença", body)


def achievement_grid() -> str:
    """Tabela das conquistas do exemplo do enunciado por jogador.

    Returns:
        O SVG.
    """
    achievements = [
        "Crafting Genius", "Strategist", "World Savior", "Speed Runner",
        "Survivor", "Master Explorer", "Treasure Hunter", "Unstoppable",
        "First Steps", "Collector Supreme", "Untouchable", "Sharp Mind",
        "Boss Slayer", "Hidden Path Finder",
    ]
    players = {
        "Alice": {"Crafting Genius", "World Savior", "Master Explorer",
                  "Collector Supreme", "Untouchable", "Boss Slayer"},
        "Bob": {"Crafting Genius", "Strategist", "World Savior",
                "Master Explorer", "Unstoppable", "Collector Supreme",
                "Untouchable"},
        "Charlie": {"Strategist", "Speed Runner", "Survivor",
                    "Master Explorer", "Treasure Hunter", "First Steps",
                    "Collector Supreme", "Untouchable", "Sharp Mind"},
        "Dylan": {"Strategist", "Speed Runner", "Unstoppable",
                  "Untouchable", "Boss Slayer"},
    }
    common = set(achievements).intersection(*players.values())
    assert common == {"Untouchable"}
    exclusive: dict[str, set[str]] = {}
    for name, owned in players.items():
        others = set().union(*(o for n, o in players.items() if n != name))
        exclusive[name] = owned.difference(others)
    assert exclusive["Charlie"] == {"Survivor", "Treasure Hunter",
                                    "First Steps", "Sharp Mind"}
    assert not exclusive["Alice"] and not exclusive["Bob"]
    assert not exclusive["Dylan"]
    nobody = set(achievements).difference(*players.values())
    assert nobody == {"Hidden Path Finder"}

    left, top, row, col = 30, 70, 28, 96
    width = left + 190 + col * len(players) + 30
    body = []
    for index, name in enumerate(players):
        body.append(text(left + 190 + col * index + col / 2, top - 14, name,
                         size=14, weight="bold"))
    for r, achievement in enumerate(achievements):
        y = top + r * row
        if achievement in common:
            body.append(rect(left - 6, y, width - left - 18, row - 2,
                             radius=4, fill="green_fill", stroke="green"))
        elif achievement in nobody:
            body.append(rect(left - 6, y, width - left - 18, row - 2,
                             radius=4, fill="box", stroke="muted",
                             dashed=True))
        body.append(text(left, y + 18, achievement, size=13,
                         anchor="start"))
        for c, (name, owned) in enumerate(players.items()):
            cx = left + 190 + col * c + col / 2
            if achievement in exclusive[name]:
                body.append(rect(cx - 30, y + 2, 60, row - 6, radius=4,
                                 fill="orange_fill", stroke="orange"))
            if achievement in owned:
                body.append(circle((cx, y + row / 2 - 1), 6, fill="line",
                                   stroke="line"))
    legend_y = top + len(achievements) * row + 26
    body.append(rect(left, legend_y - 14, 18, 18, radius=3,
                     fill="green_fill", stroke="green"))
    body.append(text(left + 26, legend_y, "comum: todos têm", size=13,
                     anchor="start"))
    body.append(rect(left + 180, legend_y - 14, 18, 18, radius=3,
                     fill="orange_fill", stroke="orange"))
    body.append(text(left + 206, legend_y, "só um jogador tem", size=13,
                     anchor="start"))
    body.append(rect(left + 360, legend_y - 14, 18, 18, radius=3,
                     fill="box", stroke="muted", dashed=True))
    body.append(text(left + 386, legend_y, "ninguém tem", size=13,
                     anchor="start"))
    body.append(text(width / 2, 30, "As conquistas do exemplo do enunciado",
                     size=16, weight="bold"))
    return svg(int(width), legend_y + 22, "Conquistas por jogador", body)


def inventory_bars() -> str:
    """Mostra o dicionário do inventário e a porcentagem de cada item.

    Returns:
        O SVG.
    """
    inventory = {"sword": 1, "potion": 5, "shield": 2, "armor": 3,
                 "helmet": 1}
    total = sum(inventory.values())
    shares = {name: round(q / total * 100, 1)
              for name, q in inventory.items()}
    assert list(shares.values()) == [8.3, 41.7, 16.7, 25.0, 8.3]
    body = [text(150, 30, "chave", size=14, weight="bold"),
            text(270, 30, "valor", size=14, weight="bold"),
            text(560, 30, f"parte do total ({total})", size=14,
                 weight="bold")]
    for index, (name, quantity) in enumerate(inventory.items()):
        y = 44 + index * 44
        body.append(rect(90, y, 120, 34, fill="blue_fill", stroke="blue"))
        body.append(text(150, y + 22, f"'{name}'", size=14, mono=True))
        body.append(line((212, y + 17), (236, y + 17), arrow=True))
        body.append(rect(240, y, 60, 34, fill="box"))
        body.append(text(270, y + 22, str(quantity), size=14, mono=True))
        width = shares[name] * 5
        color = ("green" if name == "potion" else
                 "orange" if name == "sword" else "blue")
        body.append(rect(360, y + 4, width, 26, radius=3,
                         fill=f"{color}_fill", stroke=color))
        body.append(text(368 + width, y + 22, f"{shares[name]}%", size=13,
                         anchor="start", mono=True))
    body.append(text(30, 286, "mais abundante: potion (5)", size=13,
                     fill="green", anchor="start", weight="bold"))
    body.append(text(300, 286, "menos abundante: sword (1), o primeiro "
                     "do empate com helmet", size=13, fill="orange",
                     anchor="start", weight="bold"))
    return svg(760, 306, "Inventário e porcentagens", body)


def shrinking_list() -> str:
    """Mostra a lista do enunciado encolhendo a cada evento consumido.

    Returns:
        O SVG.
    """
    built = [("charlie", "move"), ("dylan", "grab"), ("alice", "use"),
             ("alice", "use"), ("charlie", "swim"), ("bob", "run"),
             ("charlie", "move"), ("dylan", "climb"), ("alice", "use"),
             ("bob", "release")]
    got = [("charlie", "swim"), ("alice", "use"), ("charlie", "move"),
           ("charlie", "move")]
    remains = [
        [("charlie", "move"), ("dylan", "grab"), ("alice", "use"),
         ("alice", "use"), ("bob", "run"), ("charlie", "move"),
         ("dylan", "climb"), ("alice", "use"), ("bob", "release")],
        [("charlie", "move"), ("dylan", "grab"), ("alice", "use"),
         ("bob", "run"), ("charlie", "move"), ("dylan", "climb"),
         ("alice", "use"), ("bob", "release")],
        [("dylan", "grab"), ("alice", "use"), ("bob", "run"),
         ("charlie", "move"), ("dylan", "climb"), ("alice", "use"),
         ("bob", "release")],
        [("dylan", "grab"), ("alice", "use"), ("bob", "run"),
         ("dylan", "climb"), ("alice", "use"), ("bob", "release")],
    ]
    states = [built]
    picks: list[int] = []
    for event, after in zip(got, remains):
        before = states[-1]
        index = next(i for i in range(len(before))
                     if before[i] == event
                     and before[:i] + before[i + 1:] == after)
        picks.append(index)
        states.append(after)

    left, box, gap, row = 150, 66, 6, 70
    body = [text(400, 26, "events: a mesma lista no main e em "
                 "consume_event", size=15, weight="bold")]
    for step, state in enumerate(states):
        y = 44 + step * row
        label = "Built list" if step == 0 else f"depois do {step}º"
        body.append(text(left - 14, y + 30, label, size=13, anchor="end",
                         fill="muted"))
        for index, (name, action) in enumerate(state):
            x = left + index * (box + gap)
            picked = step < len(picks) and picks[step] == index
            body.append(rect(x, y, box, 46, radius=5,
                             fill="orange_fill" if picked else "box",
                             stroke="orange" if picked else "line",
                             stroke_width=2.5 if picked else 1.2))
            body.append(text(x + box / 2, y + 19, name, size=11, mono=True))
            body.append(text(x + box / 2, y + 36, action, size=11,
                             mono=True, fill="muted"))
        if step < len(picks):
            name, action = got[step]
            body.append(text(left + len(state) * (box + gap) + 4, y + 30,
                             f"→ yield ('{name}', '{action}')", size=12,
                             anchor="start", fill="orange", mono=True))
    width = left + 10 * (box + gap) + 210
    return svg(width, 44 + len(states) * row + 10,
               "A lista encolhendo em consume_event", body)


def comprehension_rows() -> str:
    """Mostra as duas list comprehensions sobre os nomes do enunciado.

    Returns:
        O SVG.
    """
    players = ["Alice", "bob", "Charlie", "dylan", "Emma", "Gregory",
               "john", "kevin", "Liam"]
    capitalized = [name.capitalize() for name in players]
    already = [name for name in players if name == name.capitalize()]
    assert already == ["Alice", "Charlie", "Emma", "Gregory", "Liam"]
    left, box, gap = 30, 84, 8
    rows = [
        ("PLAYERS", 30),
        ("[name.capitalize() for name in PLAYERS]", 130),
        ("[name for name in PLAYERS if name == name.capitalize()]", 230),
    ]
    body = []
    for label, y in rows:
        body.append(text(left, y, label, size=13, anchor="start",
                         mono=True, weight="bold"))
    for index, name in enumerate(players):
        x = left + index * (box + gap)
        center = x + box / 2
        body.append(rect(x, 40, box, 34))
        body.append(text(center, 62, name, size=13, mono=True))
        changed = capitalized[index] != name
        body.append(rect(x, 140, box, 34,
                         fill="purple_fill" if changed else "box",
                         stroke="purple" if changed else "line"))
        body.append(text(center, 162, capitalized[index], size=13,
                         mono=True, weight="bold" if changed else "normal"))
        kept = name in already
        body.append(rect(x, 240, box, 34,
                         fill="green_fill" if kept else "background",
                         stroke="green" if kept else "faint",
                         dashed=not kept))
        body.append(text(center, 262, name if kept else "fora", size=13,
                         mono=True, fill="text" if kept else "muted"))
    width = left + len(players) * (box + gap) + 22
    body.append(text(left, 302, "roxo: capitalize() mudou o nome; verde: "
                     "o nome já era igual a name.capitalize()", size=12,
                     anchor="start", fill="muted"))
    return svg(width, 320, "Duas list comprehensions", body)


def main() -> None:
    """Gera todas as imagens."""
    save("colecoes/busca-lista-vs-set.svg", search_list_vs_set())
    save("ex0/argv.svg", argv_boxes())
    save("ex1/filtro.svg", score_filter())
    save("ex2/distancia.svg", distance_box())
    save("ex3/operacoes.svg", set_operations())
    save("ex3/conquistas.svg", achievement_grid())
    save("ex4/inventario.svg", inventory_bars())
    save("ex5/lista-encolhendo.svg", shrinking_list())
    save("ex6/comprehensions.svg", comprehension_rows())


if __name__ == "__main__":
    main()
