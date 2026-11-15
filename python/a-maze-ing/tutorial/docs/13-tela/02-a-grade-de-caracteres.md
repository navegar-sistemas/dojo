---
sidebar_position: 3
title: A grade de caracteres
---

# A grade de caracteres

O labirinto está guardado como números: um por célula, com as paredes fechadas em bits
([parte 1](../01-o-problema/02-paredes-em-bits.md)). O terminal só mostra linhas de texto. Algo
precisa transformar a grade de números num desenho colorido, e esse algo é o `RenderService`.
Esta página mostra onde cada pedaço do labirinto cai nas linhas de texto e as tabelas em que o
desenho é montado.

## O `RenderService`

O `RenderService` é um **service**: uma classe que só executa uma operação, sem guardar estado
([parte 2](../02-arquitetura/04-papeis-das-classes.md)). A operação é um método só:

```python
    def render(self, maze: GeneratedMaze, state: ViewState) -> list[str]:
```

- `maze` é o labirinto a desenhar, o retrato `GeneratedMaze` com as paredes, a entrada, a saída,
  o caminho e as células do "42" ([parte 12](../12-geracao-e-saida/01-o-retrato-generated-maze.md));
- `state` é o `ViewState` das [páginas 1 e 2](./01-o-estado-da-tela.md): o caminho visível ou
  não e a cor das paredes;
- o `-> list[str]` diz que ele devolve uma lista de textos, um por linha do desenho.

O `render` **não imprime** nada. Quem imprime é o `Menu`
([parte 14](../14-menu-e-main/03-mostrar-o-labirinto.md)), a única classe que conversa com o
usuário. Separado assim, o desenho não depende do terminal: a mesma lista de linhas pode ser
impressa, gravada num arquivo ou comparada com outro texto, sem mudar o `RenderService`.

## Do labirinto ao desenho

Este é um labirinto perfeito real de 4 colunas por 3 linhas, gerado com `seed=1`, com a entrada
`0,0` em magenta e a saída `3,2` em vermelho:

![Labirinto perfeito 4 por 3 com entrada e saída](/img/tela/labirinto-4x3.svg)

E este é o mesmo labirinto como o `render` o desenha no terminal: paredes como linhas grafite,
fundo branco, a entrada e a saída como blocos coloridos dentro das suas células.

![O labirinto 4 por 3 desenhado com caracteres de caixa: paredes em linhas grafite sobre fundo branco, entrada magenta e saída vermelha](/img/tela/desenho-4x3.svg)

As linhas são **caracteres de caixa**: caracteres como `━`, `┃` e `┏`, cujos traços encostam
nas bordas e se emendam com os do vizinho
([parte 10](../10-utilitarios/09-caracteres-de-caixa.md)). O desenho inteiro é texto: cada linha
dele é uma string, e cada ponto dele é um caractere.

## Onde cada pedaço cai

O desenho é uma grade de caracteres, com linhas e colunas contadas de 0 a partir do canto de
cima à esquerda. Para não confundir com a coordenada `x,y` de uma célula, o tutorial fala em
**linha** e **coluna do desenho**.

![Grade de 7 linhas por 17 colunas do labirinto 4 por 3: cantos, lugares de parede e interior de cada célula](/img/tela/grade-4x3.svg)

Este é um esquema, não o desenho do terminal: as cores dizem o **tipo** de cada lugar.

- **Cantos** (escuro): linha par e coluna múltipla de 4. Os cantos formam uma grade própria,
  com uma coluna a mais e uma linha a mais que a de células; o canto `i,j` dessa grade fica na
  linha `2j`, coluna `4i`. É ali que até quatro paredes se encontram.
- **Interior das células** (amarelo): a célula `x,y` ocupa a linha `2y + 1`, colunas `4x + 1` a
  `4x + 3`. A coluna do meio, `4x + 2`, é o **centro** da célula (o amarelo mais forte). A
  célula `3,2`, por exemplo, ocupa a linha 5, colunas 13 a 15, com o centro na 14.
- **Lugares de parede** (azul): o resto. A parede Oeste da célula `x,y` é o caractere da coluna
  `4x`, na linha da célula; a parede Norte são os três caracteres da linha `2y`, colunas `4x + 1`
  a `4x + 3`, logo acima do interior.

Duas células vizinhas dividem a mesma parede, e essa parede ocupa **um** lugar só: a parede
Leste de `0,0` e a parede Oeste de `1,0` são o mesmo caractere, na coluna 4 da linha 1.

### O tamanho

Com `W` colunas de células, cada célula ocupa 4 colunas do desenho (a parede da esquerda e os
três caracteres do interior), e a última parede, a da borda direita, mais uma: `4W + 1` colunas.
Na altura, cada célula ocupa 2 linhas (a parede de cima e o interior), e a borda de baixo mais
uma: `2H + 1` linhas. O 4x3 tem 7 linhas de 17 caracteres; o 20x15 do `config.txt`, 31 linhas
de 81.

Por que 4 colunas por célula? Um caractere de terminal é mais ou menos duas vezes mais
alto do que largo. Com 4 colunas e 2 linhas por célula, uma célula fica quase quadrada na tela.
O código guarda esse número numa constante, com um comentário que explica a conta:

```python
# Three columns of interior plus one of wall make a cell about as wide as
# its two lines are tall in a terminal font.
STEP = 4
```

("Três colunas de interior e uma de parede deixam a célula quase tão larga quanto as suas duas
linhas são altas, numa fonte de terminal.")

## Três tabelas

Cada caractere do desenho tem três coisas: o próprio caractere, a cor do texto e a cor do fundo
([parte 10](../10-utilitarios/04-cores-ansi.md)). O `render` monta o desenho em três tabelas do
mesmo tamanho, uma para cada coisa, antes de transformar qualquer linha em texto:

```python
        height = len(maze.grid)
        width = len(maze.grid[0])
        lines = 2 * height + 1
        columns = STEP * width + 1
        chars = [[" "] * columns for _ in range(lines)]
        texts = [[state.wall_colour] * columns for _ in range(lines)]
        backs = [[Ansi.WHITE] * columns for _ in range(lines)]
```

Linha por linha:

- `maze.grid` é a grade de paredes do retrato: uma tupla de linhas, e cada linha uma tupla de
  números, um por célula. `len(maze.grid)` é o número de linhas, a altura; `maze.grid[0]` é a
  primeira linha, e o tamanho dela é a largura. As dimensões saem da própria grade, sem consultar
  o arquivo de configuração.
- `chars` ("caracteres") começa todo com espaços: nenhuma parede desenhada ainda.
- `texts` ("textos") guarda a cor do texto de cada caractere e começa toda com a cor atual das
  paredes, a tupla RGB do `ViewState`.
- `backs` (de *background*, "fundo") guarda a cor do fundo e começa toda branca.
- `[... for _ in range(lines)]` é uma **compreensão de lista** (*list comprehension*): repete a
  expressão da esquerda uma vez para cada volta do `for` e junta os resultados numa lista. O `_`
  é o nome costumeiro de uma variável cujo valor não é usado. Para o 4x3, cada tabela tem 7
  listas de 17 itens.

O tutorial chama as três tabelas juntas de **quadro** (em inglês, *canvas*). Para ler ou escrever
um caractere, a linha vem primeiro: `chars[line][column]`, do mesmo jeito que a célula `x,y` é
`grid[y][x]`. É a ordem em que as linhas do desenho são impressas, de cima para baixo.

Os valores com que as tabelas começam são a **base** do desenho: todo caractere é um espaço,
com texto na cor das paredes e fundo branco. Começar assim deixa pouco a escrever depois: o
fundo só muda no "42", na entrada e na saída, e o texto só muda no caminho.

### Por que a compreensão de lista

O atalho `[[" "] * largura] * altura` parece fazer o mesmo, mas não faz: ele repete a **mesma**
lista em todas as linhas. Mudar um caractere muda a coluna inteira:

```python
quadro = [[" "] * 3] * 2
quadro[0][0] = "┃"
print(quadro)    # [['┃', ' ', ' '], ['┃', ' ', ' ']]: as duas linhas mudaram

quadro = [[" "] * 3 for _ in range(2)]
quadro[0][0] = "┃"
print(quadro)    # [['┃', ' ', ' '], [' ', ' ', ' ']]: só a primeira mudou
```

A compreensão de lista roda a expressão `[" "] * 3` uma vez por linha e cria uma lista nova a
cada volta.

## As camadas do desenho

Com a base pronta, o `render` escreve por cima dela em quatro **camadas**, uma depois da outra.
Nesta parte, uma camada é uma etapa do desenho, a palavra que a docstring do `render` usa
(*layer*); não tem relação com as camadas da arquitetura
([parte 2](../02-arquitetura/01-por-que-camadas.md)). Depois da última camada, um passo final
transforma cada linha em texto:

```python
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
```

| Camada | Quem escreve | Tabela | Página |
|---|---|---|---|
| 1. paredes e cantos | `_draw_walls` | `chars` | [Paredes e cantos](./03-paredes-e-cantos.md) |
| 2. o "42" em cinza | `_fill_pattern` | `backs` | [O "42", a entrada e a saída](./04-o-42-a-entrada-e-a-saida.md) |
| 3. entrada e saída | o laço `for (x, y), colour` | `backs` | [O "42", a entrada e a saída](./04-o-42-a-entrada-e-a-saida.md#a-entrada-e-a-saída) |
| 4. o caminho, só quando visível | `_draw_path` | `chars` e `texts` | [O caminho em ciano](./05-o-caminho-em-ciano.md) |

O passo final, `_join`, não é uma camada: ele não escreve nas tabelas, só lê cada linha das três e
a transforma numa string com as sequências de cor ([As linhas de
texto](./06-as-linhas-de-texto.md)).

Os métodos com `_` no começo do nome são internos da classe: só o próprio `render` os chama.

Cada camada escreve por cima da base e nunca num lugar onde uma camada anterior já escreveu. As
duas que escrevem em `backs` pintam lugares diferentes: o cinza do "42" nunca cai na entrada nem
na saída. As duas que escrevem em `chars` também: o caminho só escreve onde as paredes deixaram
espaço. E `texts` só muda na camada do caminho.

As quatro camadas, uma por painel, no labirinto 9x7 do modo Pac-Man gerado com a semente 4,
entrada `0,0` e saída `8,6`:

![As quatro camadas do desenho do labirinto 9 por 7: paredes e cantos, o 42 em cinza, a entrada e a saída, e o caminho em ciano](/img/tela/etapas-9x7.svg)

Cada painel é o que o terminal mostraria se o `render` parasse depois daquela camada e fizesse o
passo final.
