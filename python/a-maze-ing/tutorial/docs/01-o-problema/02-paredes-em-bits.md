---
sidebar_position: 2
title: As paredes de uma célula em um número
---

# As paredes de uma célula em um número

O enunciado manda gravar o labirinto num arquivo de texto usando **um único caractere por
célula**. Esse caractere precisa dizer, sozinho, quais dos quatro lados da célula (Norte, Leste,
Sul e Oeste) têm parede. Esta página mostra como quatro respostas "tem parede / não tem" cabem
num número de 0 a 15, e esse número num único caractere.

## Quatro perguntas de sim ou não

Para descrever as paredes de uma célula, basta responder quatro perguntas:

1. Tem parede no Norte?
2. Tem parede no Leste?
3. Tem parede no Sul?
4. Tem parede no Oeste?

Cada resposta é **1** (sim, tem parede) ou **0** (não, é passagem). Um dígito que só pode ser
0 ou 1 se chama **bit**. Quatro bits dão 2 × 2 × 2 × 2 = 16 combinações possíveis, numeradas de
0 a 15.

## Qual bit é qual lado

O enunciado fixa a ordem, e cada lado ganha um número de bit, de 0 a 3:

| Lado da célula | Número do bit | Quanto vale quando é 1 |
|---|---|---|
| Norte | bit 0 | 1 |
| Leste | bit 1 | 2 |
| Sul | bit 2 | 4 |
| Oeste | bit 3 | 8 |

A coluna "quanto vale" vem do jeito de escrever números em binário, explicado a seguir.

## Binário: as casas valem 1, 2, 4, 8, da direita para a esquerda

Um número binário se escreve só com 0 e 1, e se lê como um número comum: a casa da **direita**
é a de menor valor.

No número decimal `352`, o `2` está na casa das unidades (a da direita), o `5` na das dezenas e
o `3` na das centenas: cada casa para a esquerda vale **10 vezes** mais que a anterior. No
binário, cada casa para a esquerda vale **2 vezes** mais: 1, 2, 4, 8.

| Posição no número escrito | esquerda | | | direita |
|---|---|---|---|---|
| Lado da célula | Oeste | Sul | Leste | Norte |
| Número do bit | 3 | 2 | 1 | 0 |
| Vale | 8 | 4 | 2 | 1 |

Então, ao **escrever** os 4 bits de uma célula, o Norte (bit 0) fica no **fim**, à direita, e o
Oeste (bit 3) fica no **começo**, à esquerda. Uma célula com parede no Norte e no Oeste, e
passagem no Leste e no Sul:

![Os bits 1001: Oeste fechado, Sul aberto, Leste aberto, Norte fechado, valor 9](/img/problema/bits-9.svg)

Somando o valor das casas que têm 1: 8 + 1 = **9**. Essa célula é descrita pelo número 9.

O `1001` é simétrico e não revela a ordem de leitura. Um caso assimétrico deixa a ordem clara:
parede no Leste e no Oeste, passagem no Norte e no Sul, dá `1010` = 8 + 2 = **10**:

![Os bits 1010: Oeste fechado, Sul aberto, Leste fechado, Norte aberto, valor 10](/img/problema/bits-a.svg)

## A mesma célula desenhada

Na figura, as paredes cheias são as fechadas e as tracejadas são as passagens:

![Célula com Norte e Oeste fechados, valor 9](/img/problema/celula-9.svg)

## De 0 a 15 num único caractere: hexadecimal

Os números de 0 a 9 cabem num caractere, mas 10 a 15 têm dois dígitos. O **hexadecimal**
resolve isso usando letras depois do 9:

| Número | 0 a 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|
| Hexadecimal | `0` a `9` | `a` | `b` | `c` | `d` | `e` | `f` |

Assim, toda célula vira exatamente um caractere de `0` a `f`. A célula de valor 10 do exemplo
acima é gravada como `a`, e a célula com as quatro paredes fechadas (8 + 4 + 2 + 1 = 15) é
gravada como `f`:

![Célula com as quatro paredes fechadas, valor 15](/img/problema/celula-15.svg)

## Tabela de exemplos

As colunas dos lados estão na mesma ordem em que o binário se escreve:

| Caractere | Oeste (8) | Sul (4) | Leste (2) | Norte (1) | Soma | Paredes |
|---|---|---|---|---|---|---|
| `0` | 0 | 0 | 0 | 0 | 0 | nenhuma |
| `3` | 0 | 0 | 1 | 1 | 2 + 1 | Leste e Norte |
| `5` | 0 | 1 | 0 | 1 | 4 + 1 | Sul e Norte |
| `9` | 1 | 0 | 0 | 1 | 8 + 1 | Oeste e Norte |
| `a` | 1 | 0 | 1 | 0 | 8 + 2 | Oeste e Leste |
| `c` | 1 | 1 | 0 | 0 | 8 + 4 | Oeste e Sul |
| `d` | 1 | 1 | 0 | 1 | 8 + 4 + 1 | Oeste, Sul e Norte |
| `f` | 1 | 1 | 1 | 1 | 8 + 4 + 2 + 1 | todas |

## Ler e mudar uma parede em Python

Guardar as paredes como número deixa as operações simples. O operador `&` ("e" bit a bit)
responde se um bit está ligado; `~` inverte os bits, e `& ~` desliga um bit:

```python
walls = 15                 # 1111 em binário: as quatro paredes fechadas
walls & 2                  # 2 → diferente de 0: a parede Leste (vale 2) está fechada
walls = walls & ~2         # desliga o bit do Leste: 13, que é 1101 em binário, "d"
walls & 2                  # 0 → a parede Leste agora está aberta
```

| Operação | Efeito |
|---|---|
| `walls & valor` | diferente de 0 se a parede está fechada |
| `walls & ~valor` | abre a parede (desliga o bit) |
| `walls \| valor` | fecha a parede (liga o bit) |

`valor` é o número do lado: 1 para Norte, 2 para Leste, 4 para Sul e 8 para Oeste.
