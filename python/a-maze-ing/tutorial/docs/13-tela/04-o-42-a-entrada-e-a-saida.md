---
sidebar_position: 5
title: O "42", a entrada e a saída
---

# O "42", a entrada e a saída

Com as paredes desenhadas ([página anterior](./03-paredes-e-cantos.md)), o labirinto já aparece,
mas três coisas ainda não se distinguem do resto: o "42" no meio, a entrada e a saída. As três
são **lugares**, e não linhas, então ganham cor no **fundo** dos caracteres, na tabela `backs`.
Esta página mostra a segunda e a terceira camadas do desenho
([página 3](./02-a-grade-de-caracteres.md#as-camadas-do-desenho)): o "42" e, depois, a entrada e a
saída.

## O "42" em cinza

`maze.pattern` é o conjunto das células que desenham o "42": o número 42 que o enunciado manda
desenhar no meio do labirinto com células de quatro paredes fechadas
([parte 1](../01-o-problema/06-o-padrao-42.md)). Ele é um `frozenset`, um conjunto que não pode
ser alterado, de tuplas `(x, y)`, copiado do `pattern` do `MazeGenerator`
([parte 12](../12-geracao-e-saida/01-o-retrato-generated-maze.md)).

O método `_fill_pattern` pinta de cinza o fundo dessas células:

```python
        for x, y in pattern:
            left = STEP * x
            for column in range(left + 1, left + STEP):
                backs[2 * y + 1][column] = Ansi.GREY
```

Para cada célula `x,y` do "42", os três caracteres do interior (linha `2y + 1`, colunas
`4x + 1` a `4x + 3`) ficam com fundo cinza.

Pintar só o interior deixaria o "42" como uma fileira de blocos cinza separados por faixas
brancas: as paredes entre duas células do "42" também são caracteres, e o fundo delas continuaria
branco. Para os algarismos aparecerem **inteiros**, o método também pinta o fundo das paredes
entre duas células do "42". É escolha do projeto: as paredes continuam desenhadas, em linha, por
cima do cinza.

```python
            if (x + 1, y) in pattern:
                backs[2 * y + 1][left + STEP] = Ansi.GREY
            if (x, y + 1) in pattern:
                for column in range(left + 1, left + STEP):
                    backs[2 * y + 2][column] = Ansi.GREY
```

- Se a vizinha da direita, `x + 1, y`, também é do "42", a parede entre as duas (coluna `4x + 4`,
  a parede Leste) fica cinza.
- Se a vizinha de baixo, `x, y + 1`, também é, os três caracteres da parede entre as duas (linha
  `2y + 2`) ficam cinza.

Os cantos continuam com fundo branco. Um canto só ficaria todo dentro do cinza se as quatro
células em volta dele fossem do "42", e os traços dos algarismos têm uma célula de largura: o
"42" não tem nenhum bloco de 2x2 células.

Cada célula só olha para a direita e para baixo. A parede entre `x,y` e a vizinha da esquerda é
a parede Leste da vizinha, pintada quando o laço passa por ela; o mesmo vale para a de cima.
Perguntar `(x + 1, y) in pattern` num conjunto é rápido mesmo com muitas células, porque o
Python não compara item por item, como faria numa lista.

O labirinto 9x7 do modo Pac-Man gerado com a semente 4, entrada `0,0` e saída `8,6`, como o
terminal o mostra:

![Labirinto 9 por 7 desenhado no terminal: à esquerda como o terminal mostra, à direita com as paredes cinza entre células do 42 marcadas em laranja](/img/tela/quarenta-e-dois-9x7.svg)

À esquerda, o desenho como ele sai. À direita, o mesmo desenho com os caracteres de parede que
ganharam fundo cinza marcados em laranja: sem eles, cada algarismo seria uma fileira de blocos
soltos.

Por que aqui a pergunta usa a tupla `(x, y)`, se na
[parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md) `(x, y) in pattern` dava sempre
`False`? Porque são conjuntos diferentes. Lá, `pattern` era o `Pattern42` do `mazegen`, que guarda
objetos `Cell` e só reconhece um `Cell`. Aqui, o `pattern` é o do `GeneratedMaze`, um `frozenset`
de tuplas `(x, y)`. Num conjunto de tuplas, a pergunta certa é com uma tupla.

## A entrada e a saída

```python
        for (x, y), colour in ((maze.entry, Ansi.MAGENTA),
                               (maze.exit, Ansi.RED)):
            for column in range(STEP * x + 1, STEP * x + STEP):
                backs[2 * y + 1][column] = colour
```

Este trecho fica no próprio `render`, logo depois do `_fill_pattern`. O laço de fora percorre dois
pares: a entrada com o magenta e a saída com o vermelho. `maze.entry` e `maze.exit` são tuplas
`(x, y)`, então cada par é `((x, y), cor)`, e o `(x, y), colour` do `for` **desempacota** o par:
separa a tupla da cor e a tupla nos seus dois números.

O laço de dentro pinta os três caracteres do interior da célula, como o do "42". Escrever o laço
uma vez para as duas células evita repetir as mesmas três linhas, uma para a entrada e outra
para a saída.

O enunciado pede que o desenho mostre "claramente as paredes, a entrada, a saída e o caminho da
solução". Entrada e saída ficam no **fundo**, e o caminho, na [próxima
página](./05-o-caminho-em-ciano.md), fica no **texto**: o caminho começa e termina dentro das
duas, com a linha ciano passando por cima do bloco magenta e do vermelho, sem esconder nenhum dos
dois. Com o caminho escondido ou visível, a entrada e a saída aparecem sempre.

## Fundos que nunca se cruzam

As duas camadas escrevem por cima da base branca, e nenhuma escreve onde a outra já escreveu: o
cinza do "42", o magenta da entrada e o vermelho da saída nunca disputam o mesmo caractere.

- **O "42" e a entrada ou a saída.** A leitura do arquivo de configuração recusa uma `ENTRY` ou
  uma `EXIT` em cima de uma célula do "42", com uma mensagem de erro
  ([parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)). O cinza das paredes do "42"
  fica entre duas células do "42", nunca dentro de outra célula.
- **A entrada e a saída.** A mesma leitura recusa as duas na mesma célula
  ([parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)).

Por isso o desenho não precisa de nenhum `if` para decidir qual cor de fundo vale num caractere.

## Com uma paleta diferente

Trocar a cor das paredes (opção `3` do menu) muda só o **texto** das paredes e dos cantos; os
fundos são fixos. O mesmo labirinto 9x7, com o caminho visível, nas quatro cores da paleta:

![O mesmo labirinto 9 por 7 com paredes grafite, laranja, verdes e azuis](/img/tela/paleta-9x7.svg)

A entrada, a saída, o caminho e o "42" continuam visíveis nas quatro, pelo critério com que a
[paleta](./01-o-estado-da-tela.md#a-paleta) foi escolhida.
