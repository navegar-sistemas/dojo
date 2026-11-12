---
sidebar_position: 2
title: A grade de posições
---

# A grade de posições

`RenderService.render(maze, state)` transforma um `GeneratedMaze` nas linhas coloridas que o
menu imprime. Ele não imprime nada: devolve uma lista de strings. Quem decide quando e onde
escrever é o `Menu`, a única camada de interface; o service só sabe desenhar, e por isso não
depende do terminal.

O desenho é feito em duas etapas: primeiro uma **tela** (uma matriz com um código de cor por
posição), depois a conversão da tela em texto. Separar as duas deixa cada regra de cor ser uma
simples atribuição numa matriz, sem pensar em sequências ANSI.

## Por que `2W + 1` por `2H + 1`

A parte 1 mostrou que cada célula, cada parede e cada canto ocupam uma posição do desenho. Este é
um labirinto perfeito 4x3 real (`seed=1`):

![Labirinto perfeito 4 por 3 com entrada e saída](/img/tela/labirinto-4x3.svg)

e esta é a sua grade de posições, 9 colunas por 7 linhas, com o tipo de cada posição:

![Grade de 9 por 7 posições do labirinto 4 por 3, com células, cantos, paredes fechadas e paredes abertas](/img/tela/posicoes-4x3.svg)

- As **células** ficam nas posições ímpares: a célula `(x, y)` está na coluna `2x + 1` e na
  linha `2y + 1`.
- Os **cantos** ficam nas posições pares nos dois eixos. Um canto encosta em quatro paredes e
  nunca é corredor: é sempre cor de parede.
- As **paredes** ficam entre duas células, com um eixo par e o outro ímpar. Cada parede
  compartilhada ocupa uma única posição: a parede Leste de `(0, 0)` e a parede Oeste de `(1, 0)`
  são a mesma posição `(2, 1)`.
- A primeira e a última linha e a primeira e a última coluna são a **borda**, sempre fechada.

Com `W` colunas de células há `W + 1` colunas de paredes (uma antes de cada célula e mais uma no
fim), total `2W + 1`. O mesmo vale para as linhas.

## A tela começa toda fechada

```python
        height = len(maze.grid)
        width = len(maze.grid[0])
        canvas = [[state.wall_colour] * (2 * width + 1)
                  for _ in range(2 * height + 1)]
```

- `maze.grid` tem `height` linhas de `width` máscaras, então as dimensões saem dele, sem
  consultar o config.
- `canvas[py][px]` guarda o código SGR da posição: primeiro a linha, depois a coluna, porque é
  assim que as linhas do desenho são impressas.
- Toda posição começa com a cor atual das paredes.

Começar tudo fechado e **abrir** o que for corredor é mais simples do que o contrário. Cantos,
borda e paredes fechadas já estão certos e nunca mais precisam ser tocados: só as células e as
paredes abertas são escritas depois. Começar vazio exigiria pintar cantos, borda e cada parede
fechada, três regras a mais.

A compreensão de lista cria uma lista nova por linha. Escrever `[[cor] * largura] * altura`
repetiria a **mesma** lista em todas as linhas, e pintar uma posição pintaria a coluna inteira.

## A ordem das escritas é a prioridade

Depois da tela inicial, o render faz três passadas, cada uma sobrescrevendo a anterior onde
precisa:

1. células (cinza no "42", fundo padrão nas outras) e paredes abertas;
2. o caminho em ciano, quando visível;
3. a entrada em magenta e a saída em vermelho.

![As quatro etapas do desenho do labirinto 4 por 3](/img/tela/etapas-4x3.svg)

Como cada passada escreve por cima da anterior, a última vence. Uma tabela de prioridades vira
uma sequência de atribuições, sem nenhum `if` para decidir qual regra se aplica a uma posição.
As próximas páginas tratam de cada passada.
