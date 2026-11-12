---
sidebar_position: 5
title: Entrada, saída e prioridades
---

# Entrada, saída e prioridades

A última passada pinta a entrada de magenta e a saída de vermelho.

```python
        ex, ey = maze.entry
        sx, sy = maze.exit
        canvas[2 * ey + 1][2 * ex + 1] = Ansi.MAGENTA
        canvas[2 * sy + 1][2 * sx + 1] = Ansi.RED
```

`maze.entry` e `maze.exit` são tuplas `(x, y)`, e o desempacotamento dá nome a cada
coordenada. `sx, sy` vem de *saída*: `exit` já é o nome do campo, e `ex` ficou com a entrada.

## Por que por último

Entrada e saída também são células do caminho. Se fossem pintadas antes, a passada do caminho
as cobriria de ciano, e o usuário não saberia onde o caminho começa e termina. Pintando por
último, elas vencem qualquer outra regra.

O subject exige que o desenho mostre "claramente as paredes, a entrada, a saída e o caminho da
solução". Entrada e saída aparecem sempre, com o caminho oculto ou visível; o ciano só liga e
desliga o que fica entre elas.

## A tabela de prioridades

Cada posição recebe a cor da primeira regra que se aplica, de cima para baixo:

| # | Posição | Cor | SGR |
|---|---|---|---|
| 1 | canto | cor atual das paredes | da paleta |
| 2 | parede fechada, inclusive a borda | cor atual das paredes | da paleta |
| 3 | célula do "42" | cinza | `100` |
| 4 | entrada | magenta | `45` |
| 5 | saída | vermelho | `41` |
| 6 | célula do caminho, caminho visível | ciano | `46` |
| 7 | passagem entre células consecutivas do caminho, caminho visível | ciano | `46` |
| 8 | qualquer outra célula ou passagem | fundo padrão | `49` |

O código aplica a tabela **de baixo para cima**: escreve primeiro o que tem menos prioridade e
deixa as escritas seguintes cobrirem. A correspondência:

| Escrita no código | Regras |
|---|---|
| tela inicial com `state.wall_colour` | 1 e 2 (cantos e paredes nunca são reescritos) |
| célula cinza ou `DEFAULT`, parede aberta `DEFAULT` | 3 e 8 |
| caminho em `CYAN` | 6 e 7 |
| `MAGENTA` e `RED` | 4 e 5 |

As regras 1 e 2 estão no topo da tabela e são as primeiras escritas no código, e mesmo assim
nunca são cobertas: nenhuma passada posterior escreve num canto ou numa parede fechada. A
segunda passada só abre paredes abertas, e o caminho só passa por elas.

## Regras que nunca brigam

Algumas regras nunca disputam a mesma posição:

- O "42" e o caminho: as células do "42" têm as quatro paredes fechadas, o solver nunca entra
  nelas, e o ciano nunca cobre o cinza.
- O "42" e a entrada ou a saída: o config recusa `ENTRY` e `EXIT` em cima do "42" (parte 11).
- A entrada e a saída: o config recusa as duas iguais.

Por isso a ordem entre cinza, magenta e vermelho não importa na prática; a ordem que importa é
ciano antes de magenta e vermelho.

## Com uma paleta diferente

Trocar a cor das paredes muda só as regras 1 e 2. O mesmo labirinto 9x7, com o caminho visível,
nas quatro cores da paleta:

![O mesmo labirinto 9 por 7 com paredes brancas, amarelas, verdes e azuis](/img/tela/paleta-9x7.svg)

Cinza, magenta, vermelho e ciano não aparecem na paleta, então as marcações continuam visíveis
em todas as cores de parede.
