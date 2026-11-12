---
sidebar_position: 3
title: Células e paredes abertas
---

# Células e paredes abertas

A primeira passada percorre a grade célula por célula e abre, na tela, o que é corredor.

```python
        for y, row in enumerate(maze.grid):
            for x, walls in enumerate(row):
```

`maze.grid[y][x]` é a máscara de paredes fechadas da célula `(x, y)`, com os bits do arquivo de
saída: Norte `1`, Leste `2`, Sul `4`, Oeste `8`. `enumerate` entrega os índices junto com os
valores, e o laço segue a mesma ordem das linhas do desenho.

## A célula

```python
                if (x, y) in maze.pattern:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.GREY
                else:
                    canvas[2 * y + 1][2 * x + 1] = Ansi.DEFAULT
```

A posição da célula `(x, y)` é `(2x + 1, 2y + 1)`. Na tela, a linha vem primeiro:
`canvas[2 * y + 1][2 * x + 1]`.

- Célula do "42": cinza (`Ansi.GREY`, código `100`). `maze.pattern` é um `frozenset`, então o
  `in` custa o mesmo para qualquer tamanho.
- Qualquer outra célula: `Ansi.DEFAULT` (`49`), o fundo padrão do terminal. O corredor não tem
  cor própria: aparece com o fundo que o terminal do usuário já usa, claro ou escuro.

Só a posição da célula do "42" fica cinza. As paredes entre duas células do "42" continuam
fechadas, então ficam na cor das paredes, como qualquer parede fechada. É assim que os
algarismos aparecem como blocos de quadrados cinza separados por paredes:

![Labirinto 9 por 7 com o "42" em cinza, caminho oculto e caminho visível](/img/tela/desenho-9x7.svg)

## As paredes abertas

```python
                if not walls & Direction.EAST:
                    canvas[2 * y + 1][2 * x + 2] = Ansi.DEFAULT
                if not walls & Direction.SOUTH:
                    canvas[2 * y + 2][2 * x + 1] = Ansi.DEFAULT
```

`walls & Direction.EAST` isola o bit Leste: dá `2` se a parede está fechada e `0` se está aberta.
`not` transforma o `0` em `True`. Para a célula `(0, 0)` do 4x3, de máscara `d` (`13`, Norte +
Sul + Oeste):

```text
13 & Direction.EAST  -> 0   (Leste aberto: a posição (2, 1) vira corredor)
13 & Direction.SOUTH -> 4   (Sul fechado: a posição (1, 2) fica cor de parede)
```

O `Direction` é o mesmo enum do `mazegen` (parte 4), importado de
`mazegen.value_objects.direction`. O service não declara `EAST = 2` próprio: os bits do desenho
e os do arquivo vêm da mesma definição e não podem divergir.

A posição da parede Leste fica uma coluna à direita da célula (`2x + 2`); a da parede Sul, uma
linha abaixo (`2y + 2`).

## Por que só Leste e Sul

Cada parede interna pertence a duas células. A parede Norte de `(x, y)` é a parede Sul de
`(x, y − 1)`, e a parede Oeste de `(x, y)` é a parede Leste de `(x − 1, y)`. Olhando só Leste e Sul de
toda célula, cada parede interna é visitada exatamente uma vez.

E as paredes que sobram?

- O Norte da primeira linha e o Oeste da primeira coluna são borda: sempre fechados, já pintados
  pela tela inicial.
- O Leste da última coluna e o Sul da última linha também são borda. O laço testa esses bits,
  mas eles estão sempre fechados, então o `if` nunca abre a borda.

Essa garantia vem da **coerência** que a entidade `Maze` mantém (parte 5): `open_wall` abre
sempre os dois lados da parede, e a borda nunca é aberta. Por isso basta ler um dos lados.

## Depois da primeira passada

Células e paredes abertas estão na tela. Cantos, borda e paredes fechadas continuam com a cor da
paleta. Com o caminho oculto, só faltam a entrada e a saída para o desenho ficar pronto.
