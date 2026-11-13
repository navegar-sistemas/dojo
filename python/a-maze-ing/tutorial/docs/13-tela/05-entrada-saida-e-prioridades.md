---
sidebar_position: 6
title: Entrada, saída e prioridades
---

# Entrada, saída e prioridades

A entrada e a saída também são células do caminho. Se a passada do caminho pintasse as duas de
ciano, o usuário não saberia onde o caminho começa e onde termina. A terceira e última passada
pinta a entrada de magenta e a saída de vermelho, **por cima** de tudo o que veio antes.

```python
        ex, ey = maze.entry
        sx, sy = maze.exit
        canvas[2 * ey + 1][2 * ex + 1] = Ansi.MAGENTA
        canvas[2 * sy + 1][2 * sx + 1] = Ansi.RED
```

`maze.entry` e `maze.exit` são tuplas `(x, y)`. A linha `ex, ey = maze.entry` desempacota a
tupla: guarda o primeiro número em `ex` e o segundo em `ey`. `ex, ey` são o x e o y da entrada
(*entry*); `sx, sy` os da saída (o `s` de saída, porque `exit` também começaria com `e`).
Depois, cada uma é pintada na sua posição do desenho, `2x + 1, 2y + 1`.

## Por que por último

O enunciado pede que o desenho mostre "claramente as paredes, a entrada, a saída e o caminho da
solução". Pintadas por último, a entrada e a saída vencem qualquer outra regra, e aparecem
sempre, com o caminho escondido ou visível; o ciano só liga e desliga o que fica entre elas.

## As prioridades

Uma posição pode se encaixar em mais de uma regra de cor: a saída é uma célula, é parte do
caminho e é a saída. Antes de ver quem vence, vale separar dois grupos de posições.

**Posições que nunca são corredor**: os cantos e as posições de parede fechada, inclusive a
borda. Elas ficam sempre na cor atual das paredes, a da paleta. Nenhuma passada escreve nelas:
a primeira só escreve em células e em paredes **abertas**, e o caminho só passa por células e
paredes abertas.

**Células e passagens** (paredes abertas): estas podem receber mais de uma cor. A tabela vai da
regra mais forte para a mais fraca; numa posição, vence a primeira que se aplica:

| Prioridade | Posição | Cor | Código | Por quê |
|---|---|---|---|---|
| 1 | entrada | magenta | `45` | marca onde o caminho começa |
| 2 | saída | vermelho | `41` | marca onde o caminho termina |
| 3 | célula do caminho, ou passagem entre duas células seguidas dele, com o caminho visível | ciano | `46` | o caminho, contínuo |
| 4 | célula do "42" | cinza | `100` | o "42" tem de ficar visível |
| 5 | qualquer outra célula ou passagem | fundo do terminal | `49` | o corredor comum |

O código aplica a tabela **de baixo para cima**: escreve primeiro o que tem menos prioridade e
deixa as escritas seguintes cobrirem. A correspondência:

| Escrita no código | O que ela pinta |
|---|---|
| quadro inicial com `state.wall_colour` | tudo na cor das paredes; cantos e paredes fechadas ficam assim até o fim |
| primeira passada: célula cinza ou `DEFAULT`, parede aberta `DEFAULT` | prioridades 4 e 5 |
| segunda passada: caminho em `CYAN` | prioridade 3 |
| terceira passada: `MAGENTA` e `RED` | prioridades 1 e 2 |

## Regras que nunca brigam

Algumas regras nunca disputam a mesma posição:

- **O "42" e o caminho.** As células do "42" têm as quatro paredes fechadas, então o caminho
  nunca entra nelas, e o ciano nunca cobre o cinza.
- **O "42" e a entrada ou a saída.** A leitura do arquivo de configuração recusa uma `ENTRY` ou
  uma `EXIT` em cima de uma célula do "42", com uma mensagem de erro
  ([parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)).
- **A entrada e a saída.** A mesma leitura recusa as duas na mesma célula
  ([parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)).

Por isso a ordem entre cinza, magenta e vermelho não importa na prática. A ordem que importa é
a do ciano **antes** do magenta e do vermelho.

## Com uma paleta diferente

Trocar a cor das paredes (opção `3` do menu) muda só os cantos e as paredes fechadas. O mesmo
labirinto 9x7 (modo Pac-Man, semente 4, entrada `0,0`, saída `8,6`), com o caminho visível, nas
quatro cores da paleta:

![O mesmo labirinto 9 por 7 com paredes brancas, amarelas, verdes e azuis](/img/tela/paleta-9x7.svg)

Cores do terminal: a cor das paredes muda em cada quadro; preto = fundo do terminal, cinza =
"42", ciano = caminho, magenta = entrada, vermelho = saída.

Cinza, magenta, vermelho e ciano não estão na paleta das paredes, então a entrada, a saída, o
caminho e o "42" continuam visíveis em todas as cores de parede.
