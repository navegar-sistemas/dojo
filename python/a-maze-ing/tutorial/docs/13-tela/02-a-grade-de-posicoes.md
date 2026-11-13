---
sidebar_position: 3
title: A grade de posições
---

# A grade de posições

O labirinto está guardado como números: um por célula, com as paredes fechadas em bits
([parte 1](../01-o-problema/02-paredes-em-bits.md)). O terminal só mostra linhas de texto. Algo
precisa transformar a grade de números num desenho colorido, e esse algo é o `RenderService`.
Esta página mostra a grade de posições sobre a qual o desenho é montado.

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

O desenho é feito em duas etapas:

1. montar um **quadro** (em inglês, *canvas*): uma tabela com um código de cor por posição do
   desenho;
2. converter cada linha do quadro em texto ([última página desta parte](./06-as-linhas-de-texto.md)).

Na primeira etapa, cada regra de cor vira uma simples atribuição numa tabela de números, sem
pensar ainda nas sequências que o terminal entende. Nesta parte, "quadro" é sempre essa tabela;
"tela" e "terminal" são a janela onde o programa roda.

## As posições do desenho

Cada pedaço do labirinto ocupa um quadrado do desenho, e não só as células: a parede (ou a
passagem) entre duas células também precisa de um quadrado, e os cantos onde as paredes se
encontram também ([parte 1](../01-o-problema/07-o-desenho-e-o-menu.md)).

Este é um labirinto perfeito real de 4 colunas por 3 linhas, gerado com `seed=1`, com a entrada
`0,0` em magenta e a saída `3,2` em vermelho:

![Labirinto perfeito 4 por 3 com entrada e saída](/img/tela/labirinto-4x3.svg)

E esta é a sua grade de posições, com 9 colunas por 7 linhas. Para não confundir com a
coordenada `x,y` de uma célula, uma posição do desenho se escreve `px,py`: `px` é a coluna do
desenho e `py` a linha do desenho, as duas contando de 0 a partir do canto de cima à esquerda.

![Grade de 9 por 7 posições do labirinto 4 por 3, com células, cantos, paredes fechadas e paredes abertas](/img/tela/posicoes-4x3.svg)

Este é um esquema, não o desenho do terminal. As cores dizem o **tipo** de cada posição, e são
as mesmas em todos os esquemas de posições do tutorial: amarelo = célula, escuro = canto, azul =
posição de parede fechada, verde = posição de parede aberta (passagem).

Cada tipo de posição tem um lugar fixo:

- **Células** (amarelo): `px` e `py` ímpares. A célula `x,y` fica na posição `2x + 1, 2y + 1`.
  A célula `3,2`, por exemplo, fica em `7,5`.
- **Cantos** (escuro): `px` e `py` pares. Um canto é o ponto onde até quatro paredes se
  encontram. Ele nunca é corredor porque não liga duas células: as vizinhas de uma célula ficam
  ao lado ou em cima e embaixo, nunca na diagonal, e o caminho entre duas vizinhas passa sempre
  por uma posição de parede. Por isso o canto tem sempre a cor das paredes.
- **Paredes** (azul quando fechadas, verde quando abertas): um eixo par e o outro ímpar. A
  parede Leste (à direita) da célula `x,y` fica em `2x + 2, 2y + 1`, logo à direita da célula; a
  parede Sul (embaixo) fica em `2x + 1, 2y + 2`, logo abaixo.
- **Borda**: a primeira e a última linha, e a primeira e a última coluna. É sempre fechada.

Duas células vizinhas dividem a mesma parede, e essa parede ocupa **uma** posição só: a parede
Leste de `0,0` e a parede Oeste de `1,0` são a mesma posição `2,1`.

A conta do tamanho: com `W` colunas de células, há `W + 1` colunas de paredes (uma antes de cada
célula e mais uma no fim), total `2W + 1`. Para 4 colunas, 9. O mesmo vale para as linhas: 3
linhas de células dão 7 linhas de desenho.

## O quadro começa todo fechado

```python
        height = len(maze.grid)
        width = len(maze.grid[0])
        canvas = [[state.wall_colour] * (2 * width + 1)
                  for _ in range(2 * height + 1)]
```

Linha por linha:

- `maze.grid` é a grade de paredes do retrato: uma tupla de linhas, e cada linha uma tupla de
  números, um por célula. `len(maze.grid)` é o número de linhas, a altura. `maze.grid[0]` é a
  primeira linha, e o tamanho dela é a largura. As dimensões saem da própria grade, sem consultar o
  arquivo de configuração.
- `[state.wall_colour] * (2 * width + 1)` cria uma lista com o mesmo número repetido: para o
  4x3 com paredes brancas, nove vezes `47`.
- `[... for _ in range(2 * height + 1)]` é uma **compreensão de lista** (*list
  comprehension*): repete a expressão da esquerda uma vez para cada volta do `for` e junta os
  resultados numa lista. O `_` é o nome
  costumeiro de uma variável cujo valor não é usado. Para o 4x3, o resultado são 7 listas de 9
  números.

Toda posição do quadro começa com a cor atual das paredes. Para ler ou escrever uma posição, a
linha vem primeiro: `canvas[py][px]`, do mesmo jeito que a célula `x,y` é `grid[y][x]`. É a ordem em que
as linhas do desenho são impressas, de cima para baixo.

### Por que começar fechado

Começar com tudo na cor das paredes e depois **abrir** o que é corredor dá menos trabalho do que
o contrário. Cantos, borda e paredes fechadas já nascem certos e nunca mais são tocados; depois
só as células e as paredes abertas são escritas. Começar com tudo vazio exigiria três regras a
mais: pintar os cantos, pintar a borda e pintar cada parede fechada.

### Por que a compreensão de lista

O atalho `[[cor] * largura] * altura` parece fazer o mesmo, mas não faz: ele repete a **mesma**
lista em todas as linhas. Mudar uma posição muda a coluna inteira:

```python
quadro = [[47] * 3] * 2
quadro[0][0] = 49
print(quadro)    # [[49, 47, 47], [49, 47, 47]]: as duas linhas mudaram

quadro = [[47] * 3 for _ in range(2)]
quadro[0][0] = 49
print(quadro)    # [[49, 47, 47], [47, 47, 47]]: só a primeira mudou
```

A compreensão de lista roda a expressão `[47] * 3` uma vez por linha e cria uma lista nova a
cada volta.

## A ordem das escritas é a prioridade

Algumas posições recebem mais de uma cor. A saída, por exemplo, é uma célula (fundo do
terminal) e também a última célula do caminho (ciano), mas precisa aparecer em vermelho.
Depois do quadro inicial, o `render` faz três **passadas** (três laços que escrevem cores no
quadro), e cada uma escreve por cima da anterior onde precisa:

1. as células (cinza no "42", fundo do terminal nas outras) e as paredes abertas;
2. o caminho em ciano, quando está visível;
3. a entrada em magenta e a saída em vermelho.

![As quatro etapas do desenho do labirinto 4 por 3](/img/tela/etapas-4x3.svg)

Esta figura imita o terminal, com as cores reais do programa (cores do terminal: claro = parede
branca, preto = fundo do terminal, o corredor; ciano = caminho; magenta = entrada; vermelho =
saída).

Como cada passada escreve por cima da anterior, a **última vence**. Assim, a ordem das passadas
resolve os conflitos sozinha, sem nenhum `if` para decidir qual regra vale numa posição. As
próximas páginas tratam de cada passada.
