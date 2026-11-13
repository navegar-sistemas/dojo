---
sidebar_position: 4
title: Células e paredes abertas
---

# Células e paredes abertas

O quadro começa todo na cor das paredes ([página anterior](./02-a-grade-de-posicoes.md)). Agora é
preciso "cavar" os corredores: pintar cada célula e cada parede **aberta** com o fundo do
terminal. Para isso o programa tem de descobrir, para cada parede, se ela está aberta ou
fechada, e essa informação está nos bits do número de cada célula. Esta página mostra a
primeira passada, que faz essa leitura.

## Percorrer a grade

```python
        for y, row in enumerate(maze.grid):
            for x, walls in enumerate(row):
```

`enumerate` entrega cada item de uma lista junto com o seu índice. No labirinto 4x3 da página
anterior, a grade é `((13, 5, 3, 11), (9, 7, 12, 2), (12, 5, 5, 6))`, então:

- a primeira volta do laço de fora dá `y = 0` e `row = (13, 5, 3, 11)`, a primeira linha;
- dentro dela, o laço de dentro dá `x = 0, walls = 13`, depois `x = 1, walls = 5`, e assim por
  diante.

Ao fim, cada célula `x,y` passou uma vez pelo corpo do laço, com `walls` igual a `grid[y][x]`:
o número que diz quais paredes da célula estão fechadas.

Relembrando o formato desse número ([parte 1](../01-o-problema/02-paredes-em-bits.md)): cada
lado da célula ocupa um **bit** (um dígito 0 ou 1 da escrita binária do número), e o bit vale 1
quando há parede.

| Lado | Onde fica | Valor do bit |
|---|---|---|
| Norte | em cima | 1 |
| Leste | à direita | 2 |
| Sul | embaixo | 4 |
| Oeste | à esquerda | 8 |

## A célula

```python
                if (x, y) in maze.pattern:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.GREY
                else:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.DEFAULT
```

A célula `x,y` fica na posição `2x + 1, 2y + 1` do desenho. No quadro, a linha vem primeiro:
`canvas[2 * y + 1][2 * x + 1]`.

`maze.pattern` é o conjunto das células que desenham o "42": o número 42 que o enunciado manda
desenhar no meio do labirinto com células de quatro paredes fechadas
([parte 1](../01-o-problema/06-o-padrao-42.md)). Ele é um `frozenset`, um conjunto que não pode
ser alterado. Perguntar `(x, y) in maze.pattern` num conjunto é rápido mesmo com muitas células,
porque o Python não compara item por item, como faria numa lista.

Por que aqui a pergunta usa a tupla `(x, y)`, se na
[parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md) `(x, y) in pattern` dava sempre
`False`? Porque são conjuntos diferentes. Lá, `pattern` era o `Pattern42` do `mazegen`, que guarda
objetos `Cell` e só reconhece um `Cell`. Aqui, `maze` é o `GeneratedMaze`, e o `maze.pattern`
dele é um `frozenset` de tuplas `(x, y)`, copiado do `pattern` do `MazeGenerator`
([parte 12](../12-geracao-e-saida/01-o-retrato-generated-maze.md)). Num conjunto de tuplas, a
pergunta certa é com uma tupla.

- Célula do "42": cinza (`Ansi.GREY`, código `100`).
- Qualquer outra célula: `Ansi.DEFAULT` (código `49`), que significa "o fundo padrão do
  terminal". O corredor não tem cor própria: aparece com o fundo que o terminal do usuário já
  usa, claro ou escuro.

Só a posição da **célula** do "42" fica cinza. As paredes entre duas células do "42" continuam
fechadas e ficam na cor das paredes, como qualquer parede fechada. Por isso os algarismos
aparecem como quadrados cinza separados por paredes. O labirinto 9x7 do modo Pac-Man gerado
com a semente 4, entrada `0,0` e saída `8,6`, como o terminal o mostra:

![Labirinto 9 por 7 desenhado no terminal: à esquerda como o terminal mostra, à direita com as 18 células do 42 contornadas](/img/tela/quarenta-e-dois-9x7.svg)

Cores do terminal: claro = parede, preto = fundo do terminal (corredor), cinza = célula do "42",
magenta = entrada, vermelho = saída. À direita, o mesmo desenho com as 18 células do "42"
contornadas em laranja, só para mostrar onde estão o 4 e o 2.

## Como saber se uma parede está aberta

```python
                if not walls & Direction.EAST:
                    canvas[2 * y + 1][2 * x + 2] = Ansi.DEFAULT
                if not walls & Direction.SOUTH:
                    canvas[2 * y + 2][2 * x + 1] = Ansi.DEFAULT
```

Uma nota de leitura antes: o Python calcula o `&` **antes** do `not`. Então
`not walls & Direction.EAST` é o mesmo que `not (walls & Direction.EAST)`: primeiro a conta com
os bits, depois o `not` sobre o resultado.

`Direction` é uma **enumeração** (um tipo com um conjunto fixo de valores, cada um com nome) dos
quatro lados de uma célula, criada na [parte 4](../04-value-objects/02-direction-bits.md). Cada
lado tem como valor o próprio bit:
`Direction.NORTH` vale 1, `Direction.EAST` vale 2, `Direction.SOUTH` vale 4 e `Direction.WEST`
vale 8. Ela é um `IntEnum`, um tipo cujos membros se comportam como números inteiros, então
`walls & Direction.EAST` faz a mesma conta que `walls & 2`.

O `&` ("e" bit a bit) compara dois números bit a bit e só mantém os bits que valem 1 nos dois.
Com um dos lados sendo um bit só, o resultado responde se esse bit está ligado em `walls`:

- se a parede está **fechada**, o bit está ligado, e o resultado é o próprio valor do bit;
- se a parede está **aberta**, o bit está desligado, e o resultado é `0`.

Para a célula `0,0` do 4x3, `walls` é `13`, `1101` em binário: Norte, Sul e Oeste fechados,
Leste aberto. Em Python, um número escrito com o prefixo `0b` está em binário: `0b1101` é o
mesmo número que `13`, e é assim que a figura abaixo o escreve.

![Os bits de 13: Oeste 1, Sul 1, Leste 0, Norte 1](/img/tela/bits-13.svg)

```text
13 & Direction.EAST  ->  1101 & 0010  ->  0000  ->  0   (Leste aberto)
13 & Direction.SOUTH ->  1101 & 0100  ->  0100  ->  4   (Sul fechado)
```

O `not` vira a resposta do avesso. Em Python, `0` conta como falso e qualquer outro número como
verdadeiro: `not 0` é `True` e `not 4` é `False`. Então `if not walls & Direction.EAST` quer
dizer "se a parede Leste está aberta".

Para a célula `0,0`, a parede Leste está aberta, e a posição dela, `2,1` (uma coluna à direita
da célula), vira corredor. A parede Sul está fechada, e a posição `1,2` (uma linha abaixo)
continua na cor das paredes:

![As posições em volta da célula 0,0: o Leste aberto vira corredor, o Sul fechado continua parede](/img/tela/leitura-0-0.svg)

O `Direction` vem do `mazegen` (`mazegen.value_objects.direction`), o mesmo usado para gerar o
labirinto e gravar o arquivo de saída. O `RenderService` não declara um `EAST = 2` próprio: os
bits do desenho e os do arquivo vêm da mesma definição e não têm como divergir.

## Por que só Leste e Sul

Cada parede de dentro do labirinto pertence a duas células. A parede Norte da célula `x,y` é a
parede Sul da célula de cima; a parede Oeste de `x,y` é a parede Leste da célula da esquerda.
Olhando só o Leste e o Sul de cada célula, cada parede de dentro é lida **uma** vez.

E as paredes que sobram?

- O Norte da primeira linha e o Oeste da primeira coluna são borda. A borda é sempre fechada e
  já nasceu pintada no quadro inicial.
- O Leste da última coluna e o Sul da última linha também são borda. O laço testa esses bits,
  mas eles estão sempre fechados, então o `if` nunca abre a borda.

Ler um lado só funciona porque as duas células vizinhas sempre **concordam** sobre a parede que
dividem, a regra de **coerência** do enunciado
([parte 1](../01-o-problema/01-a-grade-e-as-celulas.md)). O `Maze`, a classe que guarda as
paredes durante a geração, garante isso: o único jeito de abrir uma parede é o `open_wall`, que
abre os dois lados de uma vez e nunca abre a borda
([parte 5](../05-maze/04-abrir-e-fechar.md)).

## Depois da primeira passada

As células e as paredes abertas já estão no quadro. Cantos, borda e paredes fechadas continuam na
cor das paredes. Com o caminho escondido, só faltam a entrada e a saída para o desenho ficar
pronto.
