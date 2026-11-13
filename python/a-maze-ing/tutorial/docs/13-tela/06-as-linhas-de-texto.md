---
sidebar_position: 7
title: As linhas de texto
---

# As linhas de texto

Depois das três passadas, o quadro está pronto, mas ainda é uma tabela de números: um código de
cor por posição. O terminal não entende números soltos; ele entende **texto** com sequências de
cor no meio. O último passo do `render` transforma cada linha do quadro numa string que o
terminal pinta.

```python
        return [
            "".join(Ansi.background(code) + "  " for code in line)
            + Ansi.RESET
            for line in canvas
        ]
```

## Lendo de dentro para fora

O trecho tem três camadas.

1. `Ansi.background(code) + "  "`: para **uma** posição, a sequência que troca a cor de fundo,
   seguida de dois espaços. `Ansi.background(47)` devolve `'\x1b[47m'`: o caractere especial
   ESC (escrito `\x1b` em Python), um `[`, o código da cor e um `m`. O terminal não mostra esses
   caracteres; ele os lê como a ordem "a partir daqui, fundo branco"
   ([parte 10](../10-utilitarios/08-sequencias-ansi.md)).
2. `"".join(... for code in line)`: faz isso para cada código de uma linha do quadro e cola os
   pedaços, um depois do outro. O `join` junta uma sequência de strings usando como separador a
   string da esquerda; aqui ela é vazia, `""`, então os pedaços ficam grudados. Depois, o
   `+ Ansi.RESET` acrescenta, no fim da linha, a sequência que volta às cores normais.
3. `[... for line in canvas]`: uma compreensão de lista que repete tudo isso para cada linha do
   quadro e devolve a lista de strings.

Para uma linha curta, de três posições com os códigos `47`, `45` e `49`:

```python
'\x1b[47m  \x1b[45m  \x1b[49m  \x1b[0m'
```

## Dois espaços por posição

Cada posição vira dois espaços com o fundo pintado. Um caractere de terminal é mais ou menos
duas vezes mais alto do que largo; dois lado a lado formam quase um quadrado, e o labirinto não
sai achatado.

O desenho não tem nenhum caractere visível: só espaços com o fundo colorido. O enunciado pede
uma renderização **ASCII** no terminal. ASCII é a tabela básica de 128 caracteres da
[parte 10](../10-utilitarios/08-sequencias-ansi.md): os visíveis são as letras sem acento, os
dígitos, a pontuação e o espaço; os outros são caracteres invisíveis de controle, como o ESC
que começa as sequências de cor. O desenho só usa espaços e sequências de cor, todos da tabela,
então não depende da fonte do terminal nem de caracteres especiais de desenho, como `█`.

## Uma sequência em toda posição

A sequência de cor vem antes de **cada** posição, mesmo quando repete a anterior. Uma parede de
três posições sai como `\x1b[47m  \x1b[47m  \x1b[47m  `, e não como `\x1b[47m      `. Juntar
posições iguais economizaria alguns bytes, mas criaria uma regra a mais para acertar. Com uma
sequência por posição, a string é uma tradução direta do quadro, e cada posição não depende das
vizinhas.

## O reset no fim da linha

`Ansi.RESET` é `\x1b[0m`, a sequência que volta o terminal às cores normais. Ela vem **uma vez**,
no fim de cada linha. Sem ela, a cor da última posição (a borda, na cor das paredes) continuaria
ligada depois do desenho: o menu, o texto que o usuário digita e até o prompt do terminal,
depois que o programa termina, sairiam com fundo branco.

Pôr o reset em **toda** linha, e não só na última, faz cada linha devolvida pelo `render` ser
completa sozinha: se o programa for interrompido no meio do desenho, nenhuma cor fica ligada.

As linhas não terminam com quebra de linha (`\n`). Quem as imprime, com `print`, é o `Menu`
([parte 14](../14-menu-e-main/03-mostrar-o-labirinto.md)), e o `print` acrescenta a quebra.

## As cores saem sempre

O terminal permite **redirecionar** a saída de um programa para um arquivo com `>`: o que iria
para a tela vai para o arquivo. Muitos programas, como o `ls` e o `grep`, conferem se a saída é
um terminal e desligam as cores quando ela vai para um arquivo, para o arquivo não ficar cheio
de sequências invisíveis.

O `render` não faz essa conferência; é uma escolha do projeto. Sem as cores, o desenho seria só
espaços em branco, e não há outra forma de mostrar o labirinto. Num arquivo redirecionado, as
sequências de cor vão junto, e o comando `cat`, que mostra o conteúdo de um arquivo, reproduz o
mesmo desenho colorido. O comando abaixo grava o desenho num arquivo, mostra o arquivo e o
apaga. Ele só funciona com o programa pronto: é rodado de verdade no
[fim da parte 14](../14-menu-e-main/09-o-programa-rodando.md). O `printf '4\n' |` responde `4`,
"sair", ao menu ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)).

```bash
printf '4\n' | .venv/bin/python a_maze_ing.py config.txt > desenho_terminal.txt
cat desenho_terminal.txt
rm desenho_terminal.txt
```

## O desenho pronto

O labirinto 9x7 do modo Pac-Man (semente 4, entrada `0,0`, saída `8,6`), como o terminal o
mostra, com o caminho escondido e com o caminho visível:

![Desenho do labirinto 9 por 7 com o caminho oculto e com o caminho visível](/img/tela/desenho-9x7.svg)

Cores do terminal: claro = parede, preto = fundo do terminal (corredor), cinza = "42", ciano =
caminho, magenta = entrada, vermelho = saída.

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
'\x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[0m'
'\x1b[47m  \x1b[45m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
'\x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[47m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
```

A primeira é a borda Norte, toda branca. A terceira (`py = 2`) tem ciano na coluna `px = 5`: a
passagem Sul da célula `2,0`, por onde o caminho desce.

Para ver o desenho colorido, troque `[:3]` por nada e `print(repr(line))` por `print(line)`: o
terminal mostra o 4x3 com paredes brancas e o caminho `EESES` em ciano.
