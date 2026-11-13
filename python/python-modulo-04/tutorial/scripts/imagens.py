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
    "newline": "#2563eb",
    "newline_fill": "#dbeafe",
    "mark": "#dc2626",
    "mark_fill": "#fee2e2",
    "ok": "#16a34a",
    "ok_fill": "#dcfce7",
    "warn": "#d97706",
    "warn_fill": "#fef3c7",
}

WIDTH = 760
CHAR = 7.8
FRAGMENT = (
    "[FRAGMENT 001] Digital preservation protocols established 2087\n"
    "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
    "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
)
SUDOERS = "-r--r----- 1 root root 1714 Apr 11  2026 /etc/sudoers"


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


def code_line(x: float, y: float, line: str) -> str:
    """Escreve uma linha de código com largura fixa por caractere.

    Args:
        x: Posição horizontal do começo.
        y: Posição vertical da linha de base.
        line: O texto.

    Returns:
        O elemento <text>.
    """
    return text(x, y, line, size=13, mono=True, length=len(line) * CHAR)


def newline_chip(x: float, y: float) -> list[str]:
    """Desenha a caixinha azul de um caractere \\n.

    Args:
        x: Canto esquerdo.
        y: Topo.

    Returns:
        Os elementos da caixinha.
    """
    return [
        rect(x, y, 30, 22, fill="newline_fill", edge="newline"),
        text(x + 15, y + 16, "\\n", size=13, fill="newline", anchor="middle",
             weight="bold", mono=True),
    ]


def texto_lido() -> str:
    """O str devolvido por read() e o que o print mostra dele.

    Returns:
        O SVG.
    """
    lines = FRAGMENT.split("\n")[:-1]
    body = [text(20, 30, "o str que read() devolve: "
                 f"{len(FRAGMENT)} caracteres", size=15, weight="bold")]
    y = 50
    for line in lines:
        body.append(code_line(20, y + 16, line))
        body += newline_chip(24 + len(line) * CHAR, y)
        y += 30
    body.append(text(20, y + 14, "cada linha do arquivo termina com um "
                     "\\n, inclusive a última", size=13, fill="newline"))
    y += 50
    body.append(text(20, y, "o que print(content) mostra no terminal",
                     size=15, weight="bold"))
    y += 12
    body.append(rect(20, y, WIDTH - 40, 4 * 26 + 14))
    for index, line in enumerate(lines):
        body.append(code_line(32, y + 26 + index * 26, line))
    body.append(text(32, y + 26 + 3 * 26, "(linha vazia)", size=13,
                     fill="muted"))
    body.append(text(WIDTH - 32, y + 26 + 3 * 26, "← o \\n do arquivo "
                     "termina a linha 3; o \\n do print gera esta",
                     size=12, fill="newline", anchor="end"))
    return svg(int(y + 4 * 26 + 30), body)


def permissoes() -> str:
    """Os pedaços de uma linha real de ls -l.

    Returns:
        O SVG.
    """
    char = 12.0
    x0, line_y = 40, 128
    body = [
        text(x0, 30, "ls -l /etc/sudoers", size=14, fill="muted", mono=True),
    ]
    fills = {"muted": "box", "ok": "ok_fill", "warn": "warn_fill",
             "mark": "mark_fill"}
    pieces = [
        (0, "-", "tipo: - é arquivo comum, d é pasta", "muted", 3),
        (1, "r--", "dono: só lê (r)", "ok", 2),
        (4, "r--", "grupo: só lê (r)", "warn", 1),
        (7, "---", "outros: nada", "mark", 0),
    ]
    for column, chunk, label, color, row in pieces:
        start = x0 + column * char
        width = len(chunk) * char
        body.append(
            f'<rect x="{start - 1:g}" y="{line_y - 20}" '
            f'width="{width + 2:g}" height="27" rx="3" '
            f'fill="{COLORS[fills[color]]}" fill-opacity="0.6" '
            f'stroke="{COLORS[color]}"/>'
        )
        middle = start + width / 2
        label_y = line_y + 44 + row * 26
        body.append(
            f'<line x1="{middle:g}" y1="{line_y + 8}" x2="{middle:g}" '
            f'y2="{label_y - 5}" stroke="{COLORS[color]}" '
            f'stroke-width="1.5"/>'
        )
        body.append(text(middle + 8, label_y, label, size=13, fill=color,
                         weight="bold"))
    owner = SUDOERS.index("root")
    group = SUDOERS.index("root", owner + 1)
    for column, label, label_y in (
        (owner, "dono do arquivo: root", 60),
        (group, "grupo do arquivo: root", 86),
    ):
        middle = x0 + (column + 2) * char
        body.append(
            f'<line x1="{middle:g}" y1="{label_y + 6}" x2="{middle:g}" '
            f'y2="{line_y - 22}" stroke="{COLORS["line"]}" '
            f'stroke-width="1.5"/>'
        )
        body.append(text(middle + 8, label_y, label, size=13))
    body.append(text(x0, line_y, SUDOERS, size=20, mono=True, weight="bold",
                     length=len(SUDOERS) * char))
    note_y = line_y + 44 + 4 * 26 + 10
    body.append(text(x0, note_y, "Um usuário comum não é o dono nem está "
                     "no grupo root: cai em \"outros\" e não pode ler.",
                     size=13, fill="muted"))
    return svg(note_y + 22, body)


def transformacao() -> str:
    """As linhas antes e depois do # do exercício 1.

    Returns:
        O SVG.
    """
    lines = FRAGMENT.split("\n")[:-1]
    body = [text(20, 30, "antes: o texto lido do arquivo", size=15,
                 weight="bold")]
    y = 46
    for line in lines:
        body.append(code_line(20, y + 16, line))
        body += newline_chip(24 + len(line) * CHAR, y)
        y += 30
    body += arrow(WIDTH / 2, y + 6, WIDTH / 2, y + 40, color="mark",
                  label="")
    body.append(text(WIDTH / 2 + 14, y + 28, "transform(): cada linha "
                     "ganha um # antes do \\n", size=13, fill="mark"))
    y += 74
    body.append(text(20, y, "depois: o texto que será exibido e gravado",
                     size=15, weight="bold"))
    y += 16
    for line in lines:
        body.append(code_line(20, y + 16, line))
        hash_x = 24 + len(line) * CHAR
        body.append(rect(hash_x, y, 18, 22, fill="mark_fill",
                         edge="mark"))
        body.append(text(hash_x + 9, y + 16, "#", size=14, fill="mark",
                         anchor="middle", weight="bold", mono=True))
        body += newline_chip(hash_x + 24, y)
        y += 30
    return svg(int(y + 16), body, colors=("mark",))


def fluxos() -> str:
    """Os três fluxos de um programa, sem e com redirecionamento.

    Returns:
        O SVG.
    """
    body: list[str] = []
    panels = (
        (0, "python3 programa.py", "terminal", "terminal"),
        (380, "python3 programa.py 2> erros.txt", "terminal",
         "arquivo erros.txt"),
    )
    for left, command, out_target, err_target in panels:
        middle = left + 190
        body.append(text(middle, 28, command, size=13, anchor="middle",
                         mono=True, fill="muted"))
        body.append(rect(left + 20, 48, 120, 40))
        body.append(text(left + 80, 73, "teclado", size=14,
                         anchor="middle"))
        body.append(rect(middle - 60, 150, 140, 50, fill="ok_fill",
                         edge="ok"))
        body.append(text(middle + 10, 180, "programa", size=15,
                         anchor="middle", weight="bold"))
        body += arrow(left + 80, 88, middle - 40, 150, color="newline")
        body.append(text(left + 34, 128, "0 stdin", size=13,
                         fill="newline", weight="bold"))
        body.append(rect(left + 20, 262, 140, 40))
        body.append(text(left + 90, 287, out_target, size=14,
                         anchor="middle"))
        body += arrow(middle - 20, 200, left + 90, 262, color="ok")
        body.append(text(left + 34, 236, "1 stdout", size=13, fill="ok",
                         weight="bold"))
        err_fill = "mark_fill" if err_target != "terminal" else "box"
        body.append(rect(left + 200, 262, 160, 40, fill=err_fill,
                         edge="mark" if err_fill == "mark_fill"
                         else "box_edge"))
        body.append(text(left + 280, 287, err_target, size=14,
                         anchor="middle"))
        body += arrow(middle + 40, 200, left + 280, 262, color="mark")
        body.append(text(left + 296, 236, "2 stderr", size=13, fill="mark",
                         weight="bold"))
    body.append(
        f'<line x1="380" y1="40" x2="380" y2="310" '
        f'stroke="{COLORS["box_edge"]}" stroke-dasharray="4 4"/>'
    )
    return svg(326, body, colors=("newline", "ok", "mark"))


def main() -> None:
    """Grava as imagens em static/img/."""
    images = {
        "arquivos/o-texto-lido.svg": texto_lido(),
        "arquivos/permissoes.svg": permissoes(),
        "ex1/transformacao.svg": transformacao(),
        "ex2/os-tres-fluxos.svg": fluxos(),
    }
    for name, content in images.items():
        path = ROOT / "static" / "img" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
