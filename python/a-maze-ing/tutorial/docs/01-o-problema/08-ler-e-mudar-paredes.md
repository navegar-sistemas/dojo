---
sidebar_position: 3
title: Ler e mudar uma parede
---

# Ler e mudar uma parede

Para cavar um labirinto, o gerador passa o tempo todo fazendo duas coisas com as paredes de uma
célula: perguntar ("esta célula tem parede no Leste?") e abrir ou fechar uma parede. Como as
paredes de uma célula são guardadas num número de 0 a 15
([página anterior](./02-paredes-em-bits.md)), as duas coisas se fazem com **operações de bit**:
contas que comparam dois números casa a casa, escritos em binário. Esta página mostra as três
que o projeto usa: `&`, `~` e `|`.

Nas tabelas abaixo, cada coluna é uma casa do binário, na ordem em que ele se escreve (Oeste à
esquerda, Norte à direita), e a última coluna é o número em decimal.

## Perguntar por uma parede: `&`

O operador `&` se chama **"e" bit a bit**. Ele compara os dois números casa a casa e só deixa 1
nas casas em que **os dois** têm 1.

Para perguntar pela parede Leste, que vale 2, faz-se `walls & 2`, onde `walls` é o número das
paredes da célula. Numa célula com as quatro paredes fechadas (15):

| | Oeste (8) | Sul (4) | Leste (2) | Norte (1) | Número |
|---|---|---|---|---|---|
| `walls` | 1 | 1 | 1 | 1 | 15 |
| `2` | 0 | 0 | 1 | 0 | 2 |
| `walls & 2` | 0 | 0 | 1 | 0 | 2 |

O `2` só tem 1 na casa do Leste, então o `&` zera todas as outras casas e só a do Leste
sobrevive. O resultado diferente de 0 quer dizer: a parede Leste está fechada.

Numa célula 9 (paredes no Oeste e no Norte), a mesma pergunta dá 0, ou seja, o Leste é passagem:

| | Oeste (8) | Sul (4) | Leste (2) | Norte (1) | Número |
|---|---|---|---|---|---|
| `walls` | 1 | 0 | 0 | 1 | 9 |
| `2` | 0 | 0 | 1 | 0 | 2 |
| `walls & 2` | 0 | 0 | 0 | 0 | 0 |

## Abrir uma parede: `~` e `&`

O operador `~` (til) **inverte** cada bit: troca 0 por 1 e 1 por 0. Nas quatro casas de uma
célula, `~2` fica `1101`: 1 em todas as casas, menos a do Leste. Um `&` com esse número zera a
casa do Leste e deixa as outras como estavam:

| | Oeste (8) | Sul (4) | Leste (2) | Norte (1) | Número |
|---|---|---|---|---|---|
| `walls` | 1 | 1 | 1 | 1 | 15 |
| `~2` (nas quatro casas) | 1 | 1 | 0 | 1 | 13 |
| `walls & ~2` | 1 | 1 | 0 | 1 | 13 |

O resultado é 13, o caractere `d`: Oeste, Sul e Norte fechados, Leste aberto.

Um detalhe do Python: `print(~2)` mostra `-3`, não `13`. Um inteiro do Python não tem um número
fixo de casas, e para ele `~x` é sempre `-(x + 1)`. Isso não atrapalha a conta: as casas além
das quatro da célula valem 0 em `walls`, e o `&` com 0 dá 0. Por isso `15 & ~2` dá 13, como na
tabela.

Abrir com subtração (`walls - 2`) parece mais simples, mas só funciona se a parede estiver
fechada. Na célula 9, que já tem o Leste aberto, `9 - 2` dá 7, que é `0111`: Sul, Leste e Norte
fechados, uma célula completamente diferente. Já `9 & ~2` continua 9: abrir uma parede que já
está aberta não muda nada.

## Fechar uma parede: `|`

O operador `|` se chama **"ou" bit a bit**. Ele deixa 1 nas casas em que **pelo menos um** dos
dois números tem 1. Para fechar de novo o Leste da célula 13:

| | Oeste (8) | Sul (4) | Leste (2) | Norte (1) | Número |
|---|---|---|---|---|---|
| `walls` | 1 | 1 | 0 | 1 | 13 |
| `2` | 0 | 0 | 1 | 0 | 2 |
| `walls \| 2` | 1 | 1 | 1 | 1 | 15 |

## Resumo em Python

```python
walls = 15                 # 1111 em binário: as quatro paredes fechadas
walls & 2                  # 2: diferente de 0, a parede Leste está fechada
walls = walls & ~2         # 13, que é 1101 em binário ("d"): o Leste abriu
walls & 2                  # 0: a parede Leste agora está aberta
walls = walls | 2          # 15 de novo: o Leste fechou
```

| Operação | Efeito |
|---|---|
| `walls & valor` | diferente de 0 se a parede está fechada |
| `walls & ~valor` | abre a parede (põe 0 no bit dela) |
| `walls \| valor` | fecha a parede (põe 1 no bit dela) |

`valor` é o valor do lado, a coluna "quanto vale" da
[tabela da página anterior](./02-paredes-em-bits.md): 1 para Norte, 2 para Leste, 4 para Sul e
8 para Oeste.

Essas contas voltam no código da [parte 4](../04-value-objects/02-direction-bits.md), onde cada
lado ganha o seu valor, e da [parte 5](../05-maze/04-abrir-e-fechar.md), que abre e fecha as
paredes do labirinto.
