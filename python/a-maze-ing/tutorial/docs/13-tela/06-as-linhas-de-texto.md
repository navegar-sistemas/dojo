---
sidebar_position: 7
title: As linhas de texto
---

# As linhas de texto

Depois das quatro camadas, o quadro está pronto, mas ainda são três tabelas: uma de caracteres,
uma de cores do texto e uma de cores do fundo. O terminal não entende tabelas; ele entende
**texto**, com sequências de cor no meio. O passo final do `render` transforma cada linha do
quadro numa string que o terminal pinta.

```python
        return [self._join(row, text_row, back_row)
                for row, text_row, back_row in zip(chars, texts, backs)]
```

O `zip` anda nas três tabelas ao mesmo tempo e entrega, a cada volta, a mesma linha das três: os
caracteres, as cores do texto e as cores do fundo. O método `_join` ("juntar") transforma essas
três listas numa string, e a compreensão de lista junta as strings de todas as linhas.

## Uma sequência por troca de cor

```python
        parts: list[str] = []
        current: tuple[Rgb, Rgb] | None = None
        for char, text, back in zip(chars, texts, backs):
            if (text, back) != current:
                current = (text, back)
                parts.append(Ansi.colours(text, back))
            parts.append(char)
        return "".join(parts) + Ansi.RESET
```

Linha por linha:

- `parts` ("partes") é a lista dos pedaços da string, que só são colados no fim. A anotação
  `list[str]` diz ao mypy o que vai dentro de uma lista que nasce vazia.
- `current` ("atual") guarda o par de cores da última sequência escrita: `(texto, fundo)`. A
  anotação `tuple[Rgb, Rgb] | None` quer dizer "um par de cores **ou** `None`"; o `|` entre dois
  tipos é o "ou" das anotações. Ele começa em `None`, nenhum par, para que o primeiro caractere
  sempre abra uma sequência.
- Para cada caractere, se o par de cores dele é diferente do `current`, a linha ganha a sequência
  `Ansi.colours(text, back)` ([parte 10](../10-utilitarios/04-cores-ansi.md)), e o `current`
  passa a ser esse par. Depois vem o caractere.
- No fim, `"".join(parts)` cola os pedaços, um depois do outro. O `join` junta uma sequência de
  strings usando como separador a string da esquerda; aqui ela é vazia, `""`, então os pedaços
  ficam grudados. O `+ Ansi.RESET` acrescenta, no fim da linha, a sequência que volta às cores
  normais.

Uma sequência só aparece no começo da linha e onde o par de cores muda. A borda de cima do 4x3,
toda grafite sobre branco, vira uma sequência, os 17 caracteres e o reset:

```python
'\x1b[38;2;31;41;55;48;2;255;255;255m┏━━━━━━━━━━━┳━━━┓\x1b[0m'
```

Uma linha com a entrada tem três trechos, um por par de cores, como na
[linha separada em trechos da parte 10](../10-utilitarios/04-cores-ansi.md#reset-e-colours).

Escrever a sequência só na troca de cor é escolha do projeto. A sequência de grafite sobre
branco tem 33 caracteres; repetida antes de cada caractere, uma linha de 81 caracteres do
labirinto 20x15 passaria de 2.700 caracteres, e quase todas as sequências repetiriam a
anterior. A cor continua valendo até a próxima sequência, então repetir não muda nada na tela.

## O reset no fim da linha

`Ansi.RESET` é `\x1b[0m`, a sequência que volta o terminal às cores normais. Ela vem **uma vez**,
no fim de cada linha. Sem ela, as cores do último caractere (a borda, grafite sobre branco)
continuariam ligadas depois do desenho: o menu, o texto que o usuário digita e até o prompt do
terminal, depois que o programa termina, sairiam com fundo branco.

Pôr o reset em **toda** linha, e não só na última, faz cada linha devolvida pelo `render` ser
completa sozinha: se o programa for interrompido no meio do desenho, nenhuma cor fica ligada. E,
como cada linha começa com a sua própria sequência, nenhuma depende das cores da anterior.

As linhas não terminam com quebra de linha (`\n`). Quem as imprime, com `print`, é o `Menu`
([parte 14](../14-menu-e-main/03-mostrar-o-labirinto.md)), e o `print` acrescenta a quebra.

## As cores saem sempre

O terminal permite **redirecionar** a saída de um programa para um arquivo com `>`: o que iria
para a tela vai para o arquivo. Muitos programas, como o `ls` e o `grep` com a opção
`--color=auto`, conferem se a saída é um terminal e desligam as cores quando ela vai para um
arquivo, para o arquivo não ficar cheio de sequências invisíveis.

O `render` não faz essa conferência; é uma escolha do projeto. Sem as cores, as paredes
continuariam lá, mas a entrada, a saída e o "42" sumiriam, e o caminho se confundiria com as
paredes. Num arquivo redirecionado, as sequências de cor vão junto, e o comando `cat`, que mostra
o conteúdo de um arquivo, reproduz o mesmo desenho colorido. O comando abaixo grava o desenho
num arquivo, mostra o arquivo e o apaga. Ele só funciona com o programa pronto e roda na
[parte 14](../14-menu-e-main/09-o-programa-rodando.md). O `printf '4\n' |`
responde `4`, "sair", ao menu ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)).

```bash
printf '4\n' | .venv/bin/python a_maze_ing.py config.txt > desenho_terminal.txt
cat desenho_terminal.txt
rm desenho_terminal.txt
```

## O desenho pronto

O labirinto 9x7 do modo Pac-Man (semente 4, entrada `0,0`, saída `8,6`), como o terminal o
mostra, com o caminho escondido e com o caminho visível:

![Desenho do labirinto 9 por 7 com o caminho oculto e com o caminho visível](/img/tela/desenho-9x7.svg)

Paredes em grafite sobre o fundo branco, o "42" em cinza, a entrada em magenta, a saída em
vermelho e, à direita, o caminho em ciano. A moldura escura é o terminal em volta do desenho.

## O arquivo completo

```python title="amazeing/services/render_service.py"
"""Box-drawing picture of a maze with 24-bit ANSI colours."""

from amazeing.domain.entities.view_state import ViewState
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.utils.ansi import Ansi, Rgb
from amazeing.utils.box import Box
from mazegen.value_objects.direction import Direction

# Three columns of interior plus one of wall make a cell about as wide as
# its two lines are tall in a terminal font.
STEP = 4


class RenderService:
    """Turn a maze into lines of coloured box-drawing characters."""

    def render(self, maze: GeneratedMaze, state: ViewState) -> list[str]:
        """Draw the maze on 2 * height + 1 lines of 4 * width + 1 characters.

        The corner between cells sits on line 2j, column 4i; cell (x, y)
        fills line 2y + 1, columns 4x + 1 to 4x + 3. Every character starts
        as a space in the wall colour on white; the layers then write over
        that base, in order: walls, the "42", entry and exit, then the path.
        No layer writes where an earlier layer already wrote.

        Args:
            maze: Maze to draw.
            state: Path visibility and wall colour.

        Returns:
            One string per line, each ending with the reset.
        """
        height = len(maze.grid)
        width = len(maze.grid[0])
        lines = 2 * height + 1
        columns = STEP * width + 1
        chars = [[" "] * columns for _ in range(lines)]
        texts = [[state.wall_colour] * columns for _ in range(lines)]
        backs = [[Ansi.WHITE] * columns for _ in range(lines)]
        self._draw_walls(maze.grid, chars)
        self._fill_pattern(maze.pattern, backs)
        for (x, y), colour in ((maze.entry, Ansi.MAGENTA),
                               (maze.exit, Ansi.RED)):
            for column in range(STEP * x + 1, STEP * x + STEP):
                backs[2 * y + 1][column] = colour
        if state.show_path:
            self._draw_path(maze.path(), chars, texts)
        return [self._join(row, text_row, back_row)
                for row, text_row, back_row in zip(chars, texts, backs)]

    def _draw_walls(self, grid: tuple[tuple[int, ...], ...],
                    chars: list[list[str]]) -> None:
        """Draw every closed wall, then pick each corner from its arms.

        Args:
            grid: Wall masks of the maze, one row per line of cells.
            chars: Characters of the drawing, changed in place.
        """
        for y, row in enumerate(grid):
            for x, walls in enumerate(row):
                left = STEP * x
                if walls & Direction.NORTH:
                    for column in range(left + 1, left + STEP):
                        chars[2 * y][column] = Box.HORIZONTAL
                if walls & Direction.SOUTH:
                    for column in range(left + 1, left + STEP):
                        chars[2 * y + 2][column] = Box.HORIZONTAL
                if walls & Direction.WEST:
                    chars[2 * y + 1][left] = Box.VERTICAL
                if walls & Direction.EAST:
                    chars[2 * y + 1][left + STEP] = Box.VERTICAL
        last_line = len(chars) - 1
        last_column = len(chars[0]) - 1
        for line in range(0, last_line + 1, 2):
            for column in range(0, last_column + 1, STEP):
                arms = 0
                if line > 0 and chars[line - 1][column] == Box.VERTICAL:
                    arms |= Direction.NORTH
                if (column < last_column
                        and chars[line][column + 1] == Box.HORIZONTAL):
                    arms |= Direction.EAST
                if (line < last_line
                        and chars[line + 1][column] == Box.VERTICAL):
                    arms |= Direction.SOUTH
                if column > 0 and chars[line][column - 1] == Box.HORIZONTAL:
                    arms |= Direction.WEST
                chars[line][column] = Box.glyph(arms)

    def _fill_pattern(self, pattern: frozenset[tuple[int, int]],
                      backs: list[list[Rgb]]) -> None:
        """Paint the "42" grey, walls between its cells included.

        Args:
            pattern: Cells of the "42".
            backs: Background colours of the drawing, changed in place.
        """
        for x, y in pattern:
            left = STEP * x
            for column in range(left + 1, left + STEP):
                backs[2 * y + 1][column] = Ansi.GREY
            if (x + 1, y) in pattern:
                backs[2 * y + 1][left + STEP] = Ansi.GREY
            if (x, y + 1) in pattern:
                for column in range(left + 1, left + STEP):
                    backs[2 * y + 2][column] = Ansi.GREY

    def _draw_path(self, path: list[tuple[int, int]],
                   chars: list[list[str]], texts: list[list[Rgb]]) -> None:
        """Draw the path as a cyan line through the centres of its cells.

        Args:
            path: Cells from entry to exit.
            chars: Characters of the drawing, changed in place.
            texts: Text colours of the drawing, changed in place.
        """
        for index, (x, y) in enumerate(path):
            arms = 0
            for neighbour in path[max(index - 1, 0):index + 2]:
                for side in Direction:
                    if (x + side.dx, y + side.dy) == neighbour:
                        arms |= side
            chars[2 * y + 1][STEP * x + 2] = Box.glyph(arms)
            texts[2 * y + 1][STEP * x + 2] = Ansi.CYAN
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            if y1 == y2:
                line = 2 * y1 + 1
                start = STEP * min(x1, x2) + 3
                for column in range(start, start + STEP - 1):
                    chars[line][column] = Box.HORIZONTAL
                    texts[line][column] = Ansi.CYAN
            else:
                line = 2 * min(y1, y2) + 2
                chars[line][STEP * x1 + 2] = Box.VERTICAL
                texts[line][STEP * x1 + 2] = Ansi.CYAN

    def _join(self, chars: list[str], texts: list[Rgb],
              backs: list[Rgb]) -> str:
        """Turn one line of the drawing into text with colour sequences.

        A sequence opens the line and comes back only where the pair of
        colours changes.

        Args:
            chars: Characters of the line.
            texts: Text colour of each character.
            backs: Background colour of each character.

        Returns:
            The line, ending with the reset.
        """
        parts: list[str] = []
        current: tuple[Rgb, Rgb] | None = None
        for char, text, back in zip(chars, texts, backs):
            if (text, back) != current:
                current = (text, back)
                parts.append(Ansi.colours(text, back))
            parts.append(char)
        return "".join(parts) + Ansi.RESET
```

## Experimente

Na raiz do projeto, o trecho gera o labirinto 4x3 das páginas anteriores, tira o retrato com a
entrada `0,0` e a saída `3,2`, liga o caminho e imprime as três primeiras linhas do desenho com
`repr`, que mostra a string como ela é escrita em Python, com os `\x1b` à vista:

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
for line in RenderService().render(maze, state)[:3]:
    print(repr(line))
'
```

```text
'\x1b[38;2;31;41;55;48;2;255;255;255m┏━━━━━━━━━━━┳━━━┓\x1b[0m'
'\x1b[38;2;31;41;55;48;2;255;255;255m┃\x1b[38;2;31;41;55;48;2;217;70;239m \x1b[38;2;34;211;238;48;2;217;70;239m╺━\x1b[38;2;34;211;238;48;2;255;255;255m━━━━━━┓\x1b[38;2;31;41;55;48;2;255;255;255m ┃   ┃\x1b[0m'
'\x1b[38;2;31;41;55;48;2;255;255;255m┣━━━━━━━┓ \x1b[38;2;34;211;238;48;2;255;255;255m┃\x1b[38;2;31;41;55;48;2;255;255;255m ╹   ┃\x1b[0m'
```

A primeira é a borda Norte, uma sequência só. A segunda tem cinco: a borda, o começo da entrada
(magenta), o caminho sobre a entrada (ciano sobre magenta), o caminho sobre o branco e as
paredes de novo em grafite. A terceira tem o `┃` ciano na coluna 10: o trecho do caminho que
desce da célula `2,0` para a `2,1`.

Para ver o desenho colorido, troque `[:3]` por nada e `print(repr(line))` por `print(line)`: o
terminal mostra o 4x3 com paredes grafite e o caminho `EESES` em ciano.
