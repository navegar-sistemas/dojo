---
sidebar_position: 6
title: As linhas de texto
---

# As linhas de texto

Com a tela pronta, falta transformar cada linha de códigos numa string que o terminal pinte.

```python
        return [
            "".join(Ansi.background(code) + "  " for code in line)
            + Ansi.RESET
            for line in canvas
        ]
```

## Dois espaços por posição

Cada posição vira `Ansi.background(code) + "  "`: a sequência que troca a cor de fundo,
`\x1b[<código>m`, seguida de **dois** espaços. Um caractere de terminal é mais ou menos duas
vezes mais alto do que largo; dois lado a lado formam um quadrado, e o labirinto não sai
achatado.

O desenho não usa nenhum caractere visível: só espaços com fundo colorido. Assim ele não
depende da fonte do terminal nem de caracteres especiais de desenho, e todo byte é ASCII.

## Uma sequência em toda posição

A sequência de cor vem antes de **cada** posição, mesmo quando repete a anterior. Uma parede de
três posições sai como `\x1b[47m  \x1b[47m  \x1b[47m  `, e não como `\x1b[47m      `. Juntar
posições iguais economizaria bytes e criaria uma regra a mais para errar; com uma sequência por
posição, a string é uma tradução direta da tela, e cada posição é independente das vizinhas.

## O reset no fim da linha

`Ansi.RESET` (`\x1b[0m`) volta o terminal às cores normais. Ele vem **uma vez**, no fim de cada
linha. Sem ele, a cor da última posição (a borda, cor de parede) continuaria valendo depois do
desenho: o menu, o prompt e até o prompt do shell, depois que o programa termina, sairiam com
fundo branco.

Pôr o reset em toda linha, e não só na última, faz cada linha devolvida pelo render ser
completa por si só: se o programa for interrompido entre duas linhas do desenho, nenhuma cor
fica ligada.

O `print` do `Menu` acrescenta a quebra de linha. O render não a inclui: devolve uma lista de
linhas, e quem imprime decide como.

## As cores saem sempre

O render não verifica se a saída é um terminal. Sem as cores, o desenho seria só espaços em
branco, e não há outra representação do labirinto na tela. Com a saída redirecionada para um
arquivo, as sequências vão junto, e `cat` do arquivo num terminal mostra o mesmo desenho.

## O desenho pronto

O labirinto 9x7 do Pac-Man (`seed=4`), como o terminal mostra, com o caminho oculto e com o
caminho visível:

![Desenho do labirinto 9 por 7 com o caminho oculto e com o caminho visível](/img/tela/desenho-9x7.svg)

## Experimente

Na raiz do projeto:

```bash
.venv/bin/python -c '
from amazeing.domain.entities.view_state import ViewState
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.services.render_service import RenderService
from mazegen import MazeGenerator

gen = MazeGenerator(4, 3, perfect=True, seed=1)
gen.generate()
maze = GeneratedMaze.from_generator(gen, (0, 0), (3, 2))
state = ViewState()
state.toggle_path()
for line in RenderService().render(maze, state):
    print(line)
'
```

O terminal mostra o 4x3 com paredes brancas e o caminho `EESES` em ciano. Para ver os bytes,
troque `print(line)` por `print(repr(line))`; as três primeiras linhas são:

```text
'\x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[0m'
'\x1b[47m  \x1b[45m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
'\x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
```

A primeira é a borda Norte, toda branca. A terceira tem ciano na coluna 5: a passagem Sul de
`(2, 0)`, por onde o caminho desce.

## O arquivo completo

```python title="amazeing/services/render_service.py"
"""ASCII drawing of a maze with ANSI background colours."""

from amazeing.domain.entities.view_state import ViewState
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.utils.ansi import Ansi
from mazegen.value_objects.direction import Direction


class RenderService:
    """Turn a maze into lines of coloured double spaces."""

    def render(self, maze: GeneratedMaze, state: ViewState) -> list[str]:
        """Draw the maze on a (2 * height + 1) x (2 * width + 1) canvas.

        Cell (x, y) sits at (2x + 1, 2y + 1); walls and corners sit between
        cells. Entry and exit are painted last, over the path.

        Args:
            maze: Maze to draw.
            state: Path visibility and wall colour.

        Returns:
            One string per canvas line, each ending with the reset.
        """
        height = len(maze.grid)
        width = len(maze.grid[0])
        canvas = [[state.wall_colour] * (2 * width + 1)
                  for _ in range(2 * height + 1)]
        for y, row in enumerate(maze.grid):
            for x, walls in enumerate(row):
                if (x, y) in maze.pattern:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.GREY
                else:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.DEFAULT
                if not walls & Direction.EAST:
                    canvas[2 * y + 1][2 * x + 2] = Ansi.DEFAULT
                if not walls & Direction.SOUTH:
                    canvas[2 * y + 2][2 * x + 1] = Ansi.DEFAULT
        if state.show_path:
            path = maze.path()
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
                canvas[y1 + y2 + 1][x1 + x2 + 1] = Ansi.CYAN
                canvas[2 * y2 + 1][2 * x2 + 1] = Ansi.CYAN
        ex, ey = maze.entry
        sx, sy = maze.exit
        canvas[2 * ey + 1][2 * ex + 1] = Ansi.MAGENTA
        canvas[2 * sy + 1][2 * sx + 1] = Ansi.RED
        return [
            "".join(Ansi.background(code) + "  " for code in line)
            + Ansi.RESET
            for line in canvas
        ]
```
