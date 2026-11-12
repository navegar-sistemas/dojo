---
sidebar_position: 2
title: Células e paredes em bits
---

# Células e paredes em bits

## Uma célula tem quatro paredes

Um labirinto é uma grade de células. Cada célula tem quatro lados (Norte, Leste, Sul e Oeste), e
cada lado está **fechado** (há parede) ou **aberto** (há passagem para a vizinha).

São 4 lados com 2 estados cada: 2⁴ = 16 combinações, de 0 a 15. Cabem exatamente num dígito
hexadecimal (`0` a `f`).

## Um bit por lado

O subject define qual bit representa cada lado. Bit ligado = parede **fechada**:

| Bit | Valor | Lado |
|---|---|---|
| 0 | 1 | Norte |
| 1 | 2 | Leste |
| 2 | 4 | Sul |
| 3 | 8 | Oeste |

O valor da célula é a soma dos lados fechados. Na figura, as paredes cheias estão fechadas e as
tracejadas, abertas:

![Célula com Norte e Oeste fechados, valor 9](/img/problema/celula-9.svg)

![Célula com as quatro paredes fechadas, valor 15](/img/problema/celula-15.svg)

| Dígito | Binário | Fechadas |
|---|---|---|
| `0` | 0000 | nenhuma |
| `3` | 0011 | Norte e Leste |
| `5` | 0101 | Norte e Sul |
| `a` | 1010 | Leste e Oeste |
| `c` | 1100 | Sul e Oeste |
| `f` | 1111 | todas |

## Ler e mudar uma parede com operações de bits

Com esse formato, consultar e alterar paredes é aritmética simples:

```python
walls = 15                 # 0b1111: tudo fechado
walls & 2                  # 2 → a parede Leste está fechada
walls = walls & ~2         # desliga o bit 1: 13 = 0b1101 = "d"
walls & 2                  # 0 → a parede Leste está aberta
```

- `walls & bit` diz se a parede está fechada (resultado diferente de 0).
- `walls & ~bit` abre a parede (desliga o bit).
- `walls | bit` fecha a parede (liga o bit).

## Paredes compartilhadas

A parede Leste da célula `(3, 4)` é **a mesma** parede que a Oeste da célula `(4, 4)`. O arquivo
guarda as duas, então elas precisam concordar: se uma diz "fechada", a outra também diz.

![Duas células vizinhas compartilhando a parede do meio](/img/problema/parede-compartilhada.svg)

Toda vez que o gerador abrir uma passagem, ele mexe nas **duas** células. Essa regra se chama
**coerência**, e a entidade `Maze` (parte 5) é construída para nunca quebrá-la.

## A borda

As paredes da borda da grade ficam sempre fechadas, inclusive nas células de entrada e de
saída: a entrada e a saída são células marcadas, não buracos na borda.
