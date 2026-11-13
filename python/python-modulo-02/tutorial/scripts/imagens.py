"""Gera as imagens SVG do tutorial em static/img/.

Uso: python3 scripts/imagens.py

Só usa a biblioteca padrão. Rodar de novo gera arquivos idênticos.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = 'font-family="ui-sans-serif, system-ui, sans-serif"'

COLORS = {
    "background": "#ffffff",
    "axis": "#1f2937",
    "text": "#111827",
    "muted": "#6b7280",
    "zone": "#bbf7d0",
    "zone_edge": "#16a34a",
    "ok": "#16a34a",
    "hot": "#dc2626",
    "cold": "#2563eb",
    "invalid": "#f3f4f6",
}

WIDTH = 760
LEFT = 60
RIGHT = WIDTH - 40
AXIS_Y = 120
LOW = -60
HIGH = 110


@dataclass(frozen=True)
class Marker:
    """Um valor de teste marcado sobre a linha das temperaturas."""

    value: int
    label: str
    note: str
    color: str


def scale(value: float) -> float:
    """Converte uma temperatura na posição horizontal do desenho.

    Args:
        value: Temperatura em graus Celsius.

    Returns:
        A coordenada x, em pixels.
    """
    return LEFT + (value - LOW) * (RIGHT - LEFT) / (HIGH - LOW)


def text(x: float, y: float, value: str, *, size: int = 14,
         fill: str = "text", anchor: str = "middle",
         weight: str = "normal") -> str:
    """Escreve um texto SVG.

    Args:
        x: Posição horizontal.
        y: Posição vertical da linha de base.
        value: O texto.
        size: Tamanho da fonte.
        fill: Nome da cor na paleta.
        anchor: Alinhamento horizontal (start, middle ou end).
        weight: Peso da fonte.

    Returns:
        O elemento <text>.
    """
    return (
        f'<text x="{x:g}" y="{y:g}" {FONT} font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS[fill]}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def svg(height: int, body: list[str]) -> str:
    """Monta o documento SVG com fundo branco.

    Args:
        height: Altura do desenho.
        body: Os elementos do desenho.

    Returns:
        O SVG completo.
    """
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{height}" viewBox="0 0 {WIDTH} {height}">'
    )
    background = (
        f'<rect width="{WIDTH}" height="{height}" '
        f'fill="{COLORS["background"]}" rx="8"/>'
    )
    return "\n".join([head, background, *body, "</svg>"]) + "\n"


def axis(ticks: tuple[int, ...]) -> list[str]:
    """Desenha a linha das temperaturas com as marcas pedidas.

    Args:
        ticks: Temperaturas que ganham marca e número.

    Returns:
        Os elementos da linha.
    """
    parts = [
        f'<line x1="{LEFT}" y1="{AXIS_Y}" x2="{RIGHT}" y2="{AXIS_Y}" '
        f'stroke="{COLORS["axis"]}" stroke-width="2"/>',
        f'<path d="M{RIGHT} {AXIS_Y} l-10 -6 v12 z" '
        f'fill="{COLORS["axis"]}"/>',
        text(RIGHT, AXIS_Y + 50, "temperatura (°C) →", size=13,
             fill="muted", anchor="end"),
    ]
    for tick in ticks:
        x = scale(tick)
        parts.append(
            f'<line x1="{x:g}" y1="{AXIS_Y - 6}" x2="{x:g}" '
            f'y2="{AXIS_Y + 6}" stroke="{COLORS["axis"]}" stroke-width="2"/>'
        )
        parts.append(text(x, AXIS_Y + 26, str(tick), size=13))
    return parts


def marker(item: Marker) -> list[str]:
    """Desenha um valor de teste: ponto na linha, texto e nota acima.

    Args:
        item: O valor de teste.

    Returns:
        Os elementos do marcador.
    """
    x = scale(item.value)
    return [
        f'<line x1="{x:g}" y1="{AXIS_Y - 48}" x2="{x:g}" y2="{AXIS_Y}" '
        f'stroke="{COLORS[item.color]}" stroke-width="2" '
        f'stroke-dasharray="4 3"/>',
        f'<circle cx="{x:g}" cy="{AXIS_Y}" r="7" '
        f'fill="{COLORS[item.color]}"/>',
        text(x, AXIS_Y - 72, item.label, size=15, fill=item.color,
             weight="bold"),
        text(x, AXIS_Y - 54, item.note, size=12, fill=item.color),
    ]


def invalid_box(x: float, y: float, note: str) -> list[str]:
    """Desenha a caixa do texto "abc", que não vira número.

    Args:
        x: Canto esquerdo da caixa.
        y: Topo da caixa.
        note: Explicação ao lado da caixa.

    Returns:
        Os elementos da caixa.
    """
    return [
        f'<rect x="{x:g}" y="{y:g}" width="70" height="30" rx="6" '
        f'fill="{COLORS["invalid"]}" stroke="{COLORS["hot"]}" '
        f'stroke-width="2"/>',
        text(x + 35, y + 20, '"abc"', size=15, fill="hot", weight="bold"),
        text(x + 82, y + 20, note, size=13, fill="hot", anchor="start"),
    ]


def ex0() -> str:
    """Ex0: "25" vira número; "abc" nem chega à linha.

    Returns:
        O SVG.
    """
    body = axis((-50, 0, 25, 100))
    body += marker(Marker(25, '"25"', "vira o inteiro 25", "ok"))
    body += invalid_box(
        LEFT, 196, "não é número: int() lança ValueError antes de existir "
        "uma temperatura",
    )
    return svg(246, body)


def ex1() -> str:
    """Ex1: a faixa de 0 a 40 e os quatro valores de teste.

    Returns:
        O SVG.
    """
    low, high = scale(0), scale(40)
    body = [
        f'<rect x="{low:g}" y="{AXIS_Y - 30}" width="{high - low:g}" '
        f'height="40" fill="{COLORS["zone"]}"/>',
        f'<line x1="{low:g}" y1="{AXIS_Y - 30}" x2="{low:g}" '
        f'y2="{AXIS_Y + 10}" stroke="{COLORS["zone_edge"]}" '
        f'stroke-width="2"/>',
        f'<line x1="{high:g}" y1="{AXIS_Y - 30}" x2="{high:g}" '
        f'y2="{AXIS_Y + 10}" stroke="{COLORS["zone_edge"]}" '
        f'stroke-width="2"/>',
        text((low + high) / 2, AXIS_Y + 48, "aceita: de 0 a 40, com 0 e 40",
             size=12, fill="ok"),
    ]
    body += axis((-50, 0, 25, 40, 100))
    body += marker(Marker(25, '"25"', "aceita", "ok"))
    body += marker(Marker(100, '"100"', "quente demais", "hot"))
    body += marker(Marker(-50, '"-50"', "fria demais", "cold"))
    body += invalid_box(
        LEFT, 196, "não é número: int() falha antes de conferir a faixa",
    )
    return svg(246, body)


def main() -> None:
    """Grava as imagens em static/img/."""
    images = {
        "ex0/temperaturas.svg": ex0(),
        "ex1/faixa-de-temperatura.svg": ex1(),
    }
    for name, content in images.items():
        path = ROOT / "static" / "img" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
