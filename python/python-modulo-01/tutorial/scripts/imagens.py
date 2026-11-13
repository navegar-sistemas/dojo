"""Gera as imagens SVG do tutorial em static/img/.

Uso: python3 scripts/imagens.py

Só usa a biblioteca padrão. Rodar de novo gera arquivos idênticos. As alturas
dos gráficos saem das mesmas contas que os programas dos exercícios fazem.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = 'font-family="ui-sans-serif, system-ui, sans-serif"'
MONO = 'font-family="ui-monospace, SFMono-Regular, Menlo, monospace"'
WIDTH = 760

COLORS = {
    "background": "#ffffff",
    "axis": "#1f2937",
    "text": "#111827",
    "muted": "#6b7280",
    "grid": "#e5e7eb",
    "class_fill": "#ecfdf5",
    "class_edge": "#059669",
    "object_fill": "#eff6ff",
    "object_edge": "#2563eb",
    "plant": "#16a34a",
    "ok": "#16a34a",
    "error": "#dc2626",
    "error_fill": "#fef2f2",
    "nutrition": "#d97706",
    "shade": "#94a3b8",
    "trunk": "#92400e",
}


def text(x: float, y: float, value: str, *, size: int = 14,
         fill: str = "text", anchor: str = "middle",
         weight: str = "normal", mono: bool = False) -> str:
    """Texto SVG; y é a linha de base e fill é um nome da paleta COLORS."""
    family = MONO if mono else FONT
    return (
        f'<text x="{x:g}" y="{y:g}" {family} font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS[fill]}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, *, fill: str,
         stroke: str, radius: int = 8) -> str:
    """Retângulo com borda de 2 px; fill e stroke são nomes de COLORS."""
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="{radius}" fill="{COLORS[fill]}" stroke="{COLORS[stroke]}" '
        f'stroke-width="2"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, *, color: str = "axis",
         width: int = 2, dashed: bool = False) -> str:
    """Segmento de reta; color é um nome da paleta COLORS."""
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{COLORS[color]}" stroke-width="{width}"{dash}/>'
    )


def arrow(x1: float, y1: float, x2: float, y2: float, *,
          color: str = "axis") -> list[str]:
    """Seta só horizontal ou vertical, com a ponta em (x2, y2)."""
    if x1 == x2:
        step = 9 if y2 > y1 else -9
        head = (f"M{x2:g} {y2:g} l-6 {-step:g} h12 z")
    else:
        step = 9 if x2 > x1 else -9
        head = (f"M{x2:g} {y2:g} l{-step:g} -6 v12 z")
    return [
        line(x1, y1, x2, y2, color=color),
        f'<path d="{head}" fill="{COLORS[color]}"/>',
    ]


def svg(height: int, body: list[str]) -> str:
    """Documento SVG de largura WIDTH, com fundo branco arredondado."""
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{height}" viewBox="0 0 {WIDTH} {height}">'
    )
    background = (
        f'<rect width="{WIDTH}" height="{height}" '
        f'fill="{COLORS["background"]}" rx="8"/>'
    )
    return "\n".join([head, background, *body, "</svg>"]) + "\n"


def decimal(value: float) -> str:
    """Uma casa decimal, com vírgula como no texto: 25.8 vira "25,8"."""
    return f"{value:.1f}".replace(".", ",")


def molde_e_instancias() -> str:
    """Ex1: a classe Plant como molde e três objetos feitos a partir dela."""
    body = [
        rect(30, 70, 220, 170, fill="class_fill", stroke="class_edge"),
        text(140, 100, "class Plant", size=17, fill="class_edge",
             weight="bold", mono=True),
        line(30, 114, 250, 114, color="class_edge"),
        text(48, 140, "name: str", anchor="start", mono=True),
        text(48, 164, "height: int", anchor="start", mono=True),
        text(48, 188, "age_days: int", anchor="start", mono=True),
        text(48, 222, "show()", anchor="start", mono=True),
        text(140, 50, "a classe: o molde", size=13, fill="muted"),
        text(590, 30, "os objetos: cada um com os seus valores", size=13,
             fill="muted"),
    ]
    objects = (("rose", "Rose", 25, 30), ("sunflower", "Sunflower", 80, 45),
               ("cactus", "Cactus", 15, 120))
    for index, (variable, name, height, age) in enumerate(objects):
        top = 46 + index * 90
        body.append(line(250, 155, 440, top + 38, color="class_edge"))
        body += [
            rect(440, top, 300, 76, fill="object_fill",
                 stroke="object_edge"),
            text(456, top + 22, variable, size=14, fill="object_edge",
                 anchor="start", weight="bold", mono=True),
            text(456, top + 44, f'name = "{name}"', size=13,
                 anchor="start", mono=True),
            text(456, top + 64, f"height = {height}", size=13,
                 anchor="start", mono=True),
            text(600, top + 64, f"age_days = {age}", size=13,
                 anchor="start", mono=True),
        ]
    body.append(text(140, 270, "cada Plant() cria um objeto novo",
                     size=13, fill="class_edge"))
    return svg(320, body)


def crescimento_da_semana() -> str:
    """Ex2: a altura da rosa do dia 0 ao dia 7, 0,8 cm por dia."""
    heights = [25.0]
    height = 25.0
    for _ in range(7):
        height += 0.8
        heights.append(height)
    left, right, top, bottom = 80, 600, 40, 300
    low, high = 24.0, 31.0

    def x_of(day: int) -> float:
        return left + day * (right - left) / 7

    def y_of(value: float) -> float:
        return bottom - (value - low) * (bottom - top) / (high - low)

    body = [
        line(left, bottom, right + 20, bottom),
        line(left, bottom, left, top - 10),
        text(left - 10, top - 18, "altura (cm)", size=12, fill="muted",
             anchor="start"),
        text((left + right) / 2, bottom + 46, "dia", size=12, fill="muted"),
    ]
    for tick in range(25, 32):
        y = y_of(tick)
        body.append(line(left, y, right, y, color="grid", width=1))
        body.append(text(left - 10, y + 4, str(tick), size=12,
                         fill="muted", anchor="end"))
    points = " ".join(
        f"{x_of(day):g},{y_of(value):g}" for day, value in enumerate(heights)
    )
    body.append(
        f'<polyline points="{points}" fill="none" '
        f'stroke="{COLORS["plant"]}" stroke-width="3"/>'
    )
    for day, value in enumerate(heights):
        x, y = x_of(day), y_of(value)
        body.append(text(x, bottom + 22, str(day), size=12))
        body.append(f'<circle cx="{x:g}" cy="{y:g}" r="5" '
                    f'fill="{COLORS["plant"]}"/>')
        body.append(text(x + 8 if day == 0 else x,
                         y + 22 if day == 0 else y - 12,
                         decimal(round(value, 1)), size=12, fill="plant",
                         weight="bold", anchor="start" if day == 0
                         else "middle"))
    first, last = y_of(heights[0]), y_of(heights[-1])
    body += [
        line(right + 40, first, right + 40, last, color="ok"),
        line(right + 32, first, right + 48, first, color="ok"),
        line(right + 32, last, right + 48, last, color="ok"),
        text(right + 56, (first + last) / 2,
             f"+{decimal(round(heights[-1] - heights[0], 1))} cm",
             size=15, fill="ok", anchor="start", weight="bold"),
        text(right + 56, (first + last) / 2 + 18, "na semana", size=12,
             fill="muted", anchor="start"),
    ]
    return svg(360, body)


def fabrica() -> str:
    """Ex3: as cinco plantas como barras, na mesma escala."""
    plants = (("Rose", 25.0, 30), ("Oak", 200.0, 365), ("Cactus", 5.0, 90),
              ("Sunflower", 80.0, 45), ("Fern", 15.0, 120))
    bottom, top = 290, 50
    scale = (bottom - top) / 200
    body = [line(40, bottom, WIDTH - 40, bottom)]
    for index, (name, height, age) in enumerate(plants):
        center = 110 + index * 135
        bar = height * scale
        body += [
            rect(center - 30, bottom - bar, 60, bar, fill="class_fill",
                 stroke="plant", radius=3),
            text(center, bottom - bar - 10, f"{decimal(height)} cm",
                 size=13, fill="plant", weight="bold"),
            text(center, bottom + 22, name, size=14, weight="bold"),
            text(center, bottom + 42, f"{age} dias", size=12, fill="muted"),
        ]
    return svg(350, body)


def setter() -> str:
    """Ex4: set_height aceitando 25.0 e recusando -5.0."""
    body: list[str] = []
    rows = (
        ("rose.set_height(25.0)", "25.0 < 0? não", "_height: 15.0 → 25.0",
         "devolve True", "ok", "object_fill", 40),
        ("rose.set_height(-5.0)", "-5.0 < 0? sim", "_height continua 25.0",
         "devolve False", "error", "error_fill", 160),
    )
    for call, check, result, answer, color, fill, top in rows:
        body += [
            text(30, top + 40, call, size=14, anchor="start", mono=True,
                 weight="bold"),
            rect(250, top + 14, 160, 40, fill=fill, stroke=color),
            text(330, top + 39, check, size=13, fill=color, mono=True),
            rect(470, top + 14, 260, 40, fill=fill, stroke=color),
            text(600, top + 39, result, size=13, fill=color, mono=True),
            text(600, top + 76, answer, size=13, fill=color,
                 weight="bold"),
        ]
        body += arrow(210, top + 34, 248, top + 34)
        body += arrow(410, top + 34, 468, top + 34, color=color)
    body.append(text(250, 270, 'e o setter imprime "Rose: Error, '
                     'height can\'t be negative"', size=12, fill="error",
                     anchor="start"))
    body.append(text(30, 30, "antes das duas chamadas, a rosa tem "
                     "_height = 15.0", size=12, fill="muted",
                     anchor="start"))
    return svg(300, body)


def sombra() -> str:
    """Ex5: a sombra do carvalho vista de cima, 200 cm por 5 cm."""
    length, diameter = 200.0, 5.0
    pixels = 3.0
    left, middle = 60, 110
    shade_width = diameter * pixels
    shade_length = length * pixels
    top = middle - shade_width / 2
    body = [
        f'<rect x="{left:g}" y="{top:g}" width="{shade_length:g}" '
        f'height="{shade_width:g}" fill="{COLORS["shade"]}"/>',
        f'<circle cx="{left:g}" cy="{middle:g}" r="{shade_width / 2:g}" '
        f'fill="{COLORS["trunk"]}"/>',
        text(left, top - 22, "tronco", size=12, fill="trunk"),
        line(left, middle + 28, left + shade_length, middle + 28,
             color="muted", width=1),
        line(left, middle + 20, left, middle + 36, color="muted", width=1),
        line(left + shade_length, middle + 20, left + shade_length,
             middle + 36, color="muted", width=1),
        text(left + shade_length / 2, middle + 52,
             f"{decimal(length)} cm: a altura da árvore", size=13),
        line(left + shade_length + 20, top, left + shade_length + 20,
             top + shade_width, color="muted", width=1),
        text(left + shade_length + 28, middle + 5,
             f"{decimal(diameter)} cm", size=13, anchor="start"),
        text(left + shade_length + 28, middle + 22, "o tronco", size=11,
             fill="muted", anchor="start"),
        text(WIDTH / 2, 36, "vista de cima, na mesma escala nas duas medidas",
             size=12, fill="muted"),
    ]
    return svg(190, body)


def tomate() -> str:
    """Ex5: altura e valor nutricional do tomate nos 20 dias."""
    heights = [5.0]
    values = [0.0]
    height, value = 5.0, 0.0
    for _ in range(20):
        height += 2.1
        value += 0.5
        value += 0.5
        heights.append(height)
        values.append(value)
    left, right = 70, 700

    def x_of(day: int) -> float:
        return left + day * (right - left) / 20

    body: list[str] = []
    panels = (
        ("altura (cm)", heights, 0.0, 50.0, 40, 180, "plant", 10.0),
        ("valor nutricional", values, 0.0, 20.0, 240, 360, "nutrition",
         5.0),
    )
    for label, series, low, high, top, bottom, color, step in panels:

        def y_of(number: float, low: float = low, high: float = high,
                 top: int = top, bottom: int = bottom) -> float:
            return bottom - (number - low) * (bottom - top) / (high - low)

        body.append(text(left, top - 14, label, size=12, fill=color,
                         anchor="start", weight="bold"))
        tick = low
        while tick <= high:
            body.append(line(left, y_of(tick), right, y_of(tick),
                             color="grid", width=1))
            body.append(text(left - 8, y_of(tick) + 4, f"{tick:g}", size=11,
                             fill="muted", anchor="end"))
            tick += step
        if color == "nutrition":
            path = [f"M{x_of(0):g} {y_of(series[0]):g}"]
            for day in range(1, len(series)):
                path.append(f"H{x_of(day):g} V{y_of(series[day]):g}")
            body.append(f'<path d="{" ".join(path)}" fill="none" '
                        f'stroke="{COLORS[color]}" stroke-width="3"/>')
        else:
            points = " ".join(f"{x_of(day):g},{y_of(number):g}"
                              for day, number in enumerate(series))
            body.append(f'<polyline points="{points}" fill="none" '
                        f'stroke="{COLORS[color]}" stroke-width="3"/>')
        first, last = series[0], series[-1]
        first_text = (decimal(first) if color == "plant"
                      else str(round(first)))
        last_text = (decimal(round(last, 1)) if color == "plant"
                     else str(round(last)))
        body.append(text(x_of(0) + 6, y_of(first) - 8, first_text, size=12,
                         fill=color, anchor="start", weight="bold"))
        body.append(text(x_of(20), y_of(last) - 10, last_text, size=12,
                         fill=color, anchor="end", weight="bold"))
    for day in range(0, 21, 5):
        body.append(text(x_of(day), 382, str(day), size=11, fill="muted"))
    body.append(text((left + right) / 2, 402, "dia", size=12, fill="muted"))
    return svg(420, body)


def estatisticas() -> str:
    """Ex6: cada planta e o seu objeto de estatísticas no fim do programa."""
    plants = (
        ("rose", "Flower", "Plant.Stats", (1, 0, 2), None),
        ("oak", "Tree", "Tree.Stats", (0, 0, 1), 1),
        ("sunflower", "Seed", "Plant.Stats", (1, 1, 2), None),
        ("unknown", "Plant", "Plant.Stats", (0, 0, 1), None),
    )
    body: list[str] = []
    for index, (variable, kind, stats, counts, shade) in enumerate(plants):
        left = 20 + index * 185
        body += [
            rect(left, 20, 170, 56, fill="object_fill",
                 stroke="object_edge"),
            text(left + 85, 44, variable, size=14, fill="object_edge",
                 weight="bold", mono=True),
            text(left + 85, 64, kind, size=12, fill="muted"),
            text(left + 92, 98, "_stats", size=11, fill="muted",
                 anchor="start", mono=True),
        ]
        body += arrow(left + 85, 76, left + 85, 112, color="class_edge")
        rows = [("_grow_calls", counts[0]), ("_age_calls", counts[1]),
                ("_show_calls", counts[2])]
        if shade is not None:
            rows.append(("_shade_calls", shade))
        height = 40 + 22 * len(rows)
        body += [
            rect(left, 114, 170, height, fill="class_fill",
                 stroke="class_edge"),
            text(left + 85, 136, stats, size=13, fill="class_edge",
                 weight="bold", mono=True),
        ]
        for row, (name, count) in enumerate(rows):
            y = 162 + row * 22
            body.append(text(left + 14, y, name, size=12, anchor="start",
                             mono=True))
            body.append(text(left + 156, y, str(count), size=13,
                             anchor="end", weight="bold"))
    return svg(260, body)


def main() -> None:
    """Grava as imagens em static/img/."""
    images = {
        "ex1/molde-e-instancias.svg": molde_e_instancias(),
        "ex2/crescimento-da-semana.svg": crescimento_da_semana(),
        "ex3/fabrica.svg": fabrica(),
        "ex4/setter.svg": setter(),
        "ex5/sombra.svg": sombra(),
        "ex5/tomate.svg": tomate(),
        "ex6/estatisticas.svg": estatisticas(),
    }
    for name, content in images.items():
        path = ROOT / "static" / "img" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
