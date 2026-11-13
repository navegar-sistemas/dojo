"""Gera as imagens SVG do tutorial em static/img/.

Uso: python3 scripts/imagens.py

Só usa a biblioteca padrão. Rodar de novo gera arquivos idênticos.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = 'font-family="ui-sans-serif, system-ui, sans-serif"'
MONO = 'font-family="ui-monospace, SFMono-Regular, Menlo, monospace"'

COLORS = {
    "background": "#ffffff",
    "text": "#111827",
    "muted": "#6b7280",
    "line": "#1f2937",
    "box": "#f3f4f6",
    "box_edge": "#9ca3af",
    "blue": "#2563eb",
    "blue_fill": "#dbeafe",
    "mark": "#dc2626",
    "mark_fill": "#fee2e2",
    "ok": "#16a34a",
    "ok_fill": "#dcfce7",
    "warn": "#d97706",
    "warn_fill": "#fef3c7",
}

WIDTH = 760
FIRST_BATCH = (
    ("'Hello world'", "text"),
    ("[3.14, -1, 2.71]", "numeric"),
    ("[log WARNING, log INFO]", "log"),
    ("42", "numeric"),
    ("['Hi', 'five']", "text"),
)
PROCESSORS = {
    "numeric": ("Numeric Processor", "blue"),
    "text": ("Text Processor", "ok"),
    "log": ("Log Processor", "warn"),
}


def text(x: float, y: float, value: str, *, size: int = 14,
         fill: str = "text", anchor: str = "start",
         weight: str = "normal", mono: bool = False,
         length: float = 0) -> str:
    """Escreve um texto SVG.

    Args:
        x: Posição horizontal.
        y: Posição vertical da linha de base.
        value: O texto.
        size: Tamanho da fonte.
        fill: Nome da cor na paleta.
        anchor: Alinhamento horizontal (start, middle ou end).
        weight: Peso da fonte.
        mono: Usa fonte de largura fixa.
        length: Largura exata do texto em pixels; 0 deixa a da fonte.

    Returns:
        O elemento <text>.
    """
    family = MONO if mono else FONT
    fit = ""
    if length:
        fit = (f' textLength="{length:g}" '
               f'lengthAdjust="spacingAndGlyphs"')
    return (
        f'<text x="{x:g}" y="{y:g}" {family} font-size="{size}" '
        f'font-weight="{weight}" fill="{COLORS[fill]}" '
        f'text-anchor="{anchor}"{fit} xml:space="preserve">'
        f'{escape(value)}</text>'
    )


def rect(x: float, y: float, width: float, height: float, *,
         fill: str = "box", edge: str = "box_edge") -> str:
    """Desenha um retângulo de cantos arredondados.

    Args:
        x: Canto esquerdo.
        y: Topo.
        width: Largura.
        height: Altura.
        fill: Nome da cor de preenchimento.
        edge: Nome da cor da borda.

    Returns:
        O elemento <rect>.
    """
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="5" fill="{COLORS[fill]}" stroke="{COLORS[edge]}" '
        f'stroke-width="1.5"/>'
    )


def arrow(x1: float, y1: float, x2: float, y2: float, *,
          color: str = "line", label: str = "") -> list[str]:
    """Desenha uma seta reta de (x1, y1) até (x2, y2).

    Args:
        x1: Início, horizontal.
        y1: Início, vertical.
        x2: Ponta, horizontal.
        y2: Ponta, vertical.
        color: Nome da cor.
        label: Texto escrito no meio da seta.

    Returns:
        Os elementos da seta.
    """
    parts = [
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{COLORS[color]}" stroke-width="2" '
        f'marker-end="url(#head-{color})"/>',
    ]
    if label:
        parts.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 8, label, size=13,
                          fill=color, anchor="middle", weight="bold"))
    return parts


def svg(height: int, body: list[str], colors: tuple[str, ...] = ()) -> str:
    """Monta o documento SVG com fundo branco.

    Args:
        height: Altura do desenho.
        body: Os elementos do desenho.
        colors: Cores que precisam de ponta de seta.

    Returns:
        O SVG completo.
    """
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{height}" viewBox="0 0 {WIDTH} {height}">'
    )
    markers = [
        f'<marker id="head-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{COLORS[name]}"/></marker>'
        for name in colors
    ]
    defs = ["<defs>", *markers, "</defs>"] if markers else []
    background = (
        f'<rect width="{WIDTH}" height="{height}" '
        f'fill="{COLORS["background"]}" rx="8"/>'
    )
    return "\n".join([head, *defs, background, *body, "</svg>"]) + "\n"


def item_box(x: float, y: float, rank: int, value: str, *,
             color: str = "") -> list[str]:
    """Desenha um item da fila: o rank em cima e o texto embaixo.

    Args:
        x: Canto esquerdo.
        y: Topo.
        rank: O rank do item.
        value: O texto guardado.
        color: Nome da cor de destaque; vazio deixa a caixa cinza.

    Returns:
        Os elementos da caixa.
    """
    fill, edge = (f"{color}_fill", color) if color else ("box", "box_edge")
    return [
        rect(x, y, 96, 46, fill=fill, edge=edge),
        text(x + 48, y + 17, f"rank {rank}", size=12, fill="muted",
             anchor="middle"),
        text(x + 48, y + 37, value, size=13, anchor="middle", mono=True,
             weight="bold"),
    ]


def fila() -> str:
    """Os passos do experimento da fila.

    Returns:
        O SVG.
    """
    left = 300
    step = 106
    body = [
        text(left, 26, "← começo: pop(0)", size=12, fill="muted"),
        text(left + 3 * step - 10, 26, "fim: append →", size=12,
             fill="muted", anchor="end"),
    ]
    y = 56
    body.append(text(20, y, "1. append de '10', '20' e '30'", size=14,
                     weight="bold"))
    for index, value in enumerate(["10", "20", "30"]):
        body += item_box(left + index * step, y + 14, index, f"'{value}'")
    body.append(text(left + 3 * step + 6, y + 44, "próximo rank: 3",
                     size=13, fill="blue"))
    y += 100
    body.append(text(20, y, "2. pop(0) devolve (0, '10')", size=14,
                     weight="bold"))
    body += item_box(150, y + 14, 0, "'10'", color="mark")
    body += arrow(left - 6, y + 37, 252, y + 37, color="mark")
    for index, value in enumerate(["20", "30"]):
        body += item_box(left + index * step, y + 14, index + 1,
                         f"'{value}'")
    body.append(text(left + 3 * step + 6, y + 44, "próximo rank: 3",
                     size=13, fill="blue"))
    y += 100
    body.append(text(20, y, "3. append de '40': entra com rank 3", size=14,
                     weight="bold"))
    for index, value in enumerate(["20", "30"]):
        body += item_box(left + index * step, y + 14, index + 1,
                         f"'{value}'")
    body += item_box(left + 2 * step, y + 14, 3, "'40'", color="ok")
    body += arrow(WIDTH - 24, y + 37, left + 2 * step + 100, y + 37,
                  color="ok")
    y += 100
    body.append(text(20, y, "4. três pop(0) devolvem (1, '20'), (2, '30') "
                     "e (3, '40'); a fila fica vazia", size=14,
                     weight="bold"))
    body.append(
        f'<rect x="{left}" y="{y + 14}" width="{3 * step - 10}" '
        f'height="46" rx="5" fill="none" stroke="{COLORS["box_edge"]}" '
        f'stroke-dasharray="5 4"/>'
    )
    body.append(text(left + (3 * step - 10) / 2, y + 42,
                     "vazia: mais um pop(0) lança IndexError", size=13,
                     fill="mark", anchor="middle"))
    return svg(y + 80, body, colors=("mark", "ok"))


def roteamento_painel(top: float, title: str,
                      targets: dict[str, float]) -> list[str]:
    """Um cenário do roteamento do primeiro lote.

    Args:
        top: Topo do painel.
        title: Título do cenário.
        targets: Posição vertical de cada destino, pelo nome do
            processador; "error" é a mensagem de recusa.

    Returns:
        Os elementos do painel.
    """
    body = [text(20, top, title, size=15, weight="bold")]
    target_x = 470
    for name, target_y in targets.items():
        if name == "error":
            label, color = "DataStream error", "mark"
        else:
            label, color = PROCESSORS[name]
        body.append(rect(target_x, target_y, 270, 44,
                         fill=f"{color}_fill", edge=color))
        body.append(text(target_x + 135, target_y + 28, label, size=15,
                         anchor="middle", weight="bold", fill=color))
    for index, (value, kind) in enumerate(FIRST_BATCH):
        y = top + 16 + index * 46
        body.append(rect(20, y, 250, 34))
        body.append(text(32, y + 22, value, size=13, mono=True))
        destination = kind if kind in targets else "error"
        color = "mark" if destination == "error" else PROCESSORS[kind][1]
        body += arrow(274, y + 17, target_x - 4,
                      targets[destination] + 22, color=color)
    return body


def roteamento() -> str:
    """O primeiro lote com um processador e com os três.

    Returns:
        O SVG.
    """
    body = roteamento_painel(
        30, "Só o Numeric Processor registrado",
        {"numeric": 80, "error": 170},
    )
    body += roteamento_painel(
        300, "Os três processadores registrados",
        {"numeric": 330, "text": 410, "log": 490},
    )
    body.append(
        f'<line x1="20" y1="276" x2="{WIDTH - 20}" y2="276" '
        f'stroke="{COLORS["box_edge"]}" stroke-dasharray="4 4"/>'
    )
    return svg(560, body, colors=("blue", "ok", "warn", "mark"))


def pipeline() -> str:
    """O output_pipeline com nb = 3 e o plugin CSV.

    Returns:
        O SVG.
    """
    rows = (
        ("numeric", ["3.14", "-1", "2.71", "42"],
         "3.14,-1,2.71"),
        ("text", ["Hello world", "Hi", "five"],
         "Hello world,Hi,five"),
        ("log", ["WARNING: …", "INFO: …"],
         "WARNING: Telnet access! Use ssh instead,"
         "INFO: User wil is connected"),
    )
    body = [text(20, 28, "stream.output_pipeline(3, CSVExportPlugin())",
                 size=14, mono=True, fill="muted")]
    y = 56
    for kind, values, line in rows:
        name, color = PROCESSORS[kind]
        taken = min(3, len(values))
        body.append(text(20, y + 14, name, size=15, weight="bold",
                         fill=color))
        for index, value in enumerate(values):
            body += item_box(20 + index * 106, y + 24, index, value,
                             color=color if index < taken else "")
        body.append(text(458, y + 44,
                         f"output() × {taken}: restam "
                         f"{len(values)} → {len(values) - taken}",
                         size=13, fill=color))
        body.append(text(458, y + 64, "a lista vai para process_output",
                         size=13, fill="muted"))
        body += arrow(20 + taken * 53, y + 74, 20 + taken * 53, y + 98,
                      color=color)
        body.append(rect(20, y + 100, WIDTH - 40, 50))
        body.append(text(32, y + 120, "CSV Output:", size=13, mono=True))
        body.append(text(32, y + 140, line, size=13, mono=True))
        y += 172
    return svg(int(y - 6), body, colors=("blue", "ok", "warn"))


def main() -> None:
    """Grava as imagens em static/img/."""
    images = {
        "conceitos/a-fila.svg": fila(),
        "ex1/roteamento.svg": roteamento(),
        "ex2/pipeline.svg": pipeline(),
    }
    for name, content in images.items():
        path = ROOT / "static" / "img" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
