---
sidebar_position: 2
title: "Direction: um lado, um bit"
---

# `Direction`: um lado, um bit

O gerador fala o tempo todo de um **lado** de uma célula: abrir a parede do Leste, andar um
passo para o Norte, escrever `N` no caminho mais curto. Esta página cria o tipo que representa
um lado, a classe `Direction`, em `mazegen/value_objects/direction.py`.

## Relembrando: cada lado é um bit

Cada célula tem quatro lados, **Norte** (em cima), **Leste** (à direita), **Sul** (embaixo) e
**Oeste** (à esquerda). No arquivo de saída, as paredes de uma célula viram um número de 0 a 15
em que cada lado ocupa um **bit** (um dígito binário, 0 ou 1): 1 quer dizer parede fechada, 0
quer dizer passagem. A [parte 1](../01-o-problema/02-paredes-em-bits.md) explica a conta; o que
importa aqui é quanto cada lado vale quando está fechado:

| Lado | Vale |
|---|---|
| Norte | 1 |
| Leste | 2 |
| Sul | 4 |
| Oeste | 8 |

Uma célula com Norte e Oeste fechados vale 1 + 8 = 9. Com tudo fechado, 15.

## O valor de cada lado é o bit da parede

```python
from enum import IntEnum


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
```

Cada **membro** da classe (`NORTH`, `EAST`, `SOUTH`, `WEST`) vale exatamente o número do seu lado
na tabela acima. Assim, não existe conversão entre "direção" e "bit": a direção **é** o bit.

Este trecho ainda não é o arquivo pronto: a classe ganha docstrings e mais três respostas na
[próxima página](./03-direction-propriedades.md), que termina com o arquivo completo de
`mazegen/value_objects/direction.py`. Dá para criar o arquivo já com este trecho e completá-lo
lá, ou esperar e copiar a versão completa.

## O que é um `Enum`

Um **`Enum`** (de *enumeração*) é uma classe com uma lista **fechada** de valores com nome. Os
membros são criados uma vez, junto com a classe, e não aparecem outros depois. Usar
`Direction.NORTH` em vez de um `1` solto deixa o código legível, e o mypy (o verificador de
tipos) recusa um `int` qualquer onde se espera uma `Direction`.

Um membro tem um nome e um valor:

```python
Direction.EAST.name    # "EAST"
Direction.EAST.value   # 2
Direction(4)           # Direction.SOUTH: procura o membro pelo valor
```

## Por que `IntEnum`

`IntEnum` é um `Enum` cujos membros **também são números inteiros**: `Direction.EAST == 2` é
`True`. Isso permite usar a direção direto nas operações de bit que mexem nas paredes de uma
célula. São três operadores, que trabalham bit a bit, casa por casa:

| Operador | Nome | Cada bit do resultado é 1 quando... |
|---|---|---|
| `a & b` | "e" bit a bit | os dois bits são 1 |
| `a \| b` | "ou" bit a bit | pelo menos um dos bits é 1 |
| `~a` | "não" bit a bit | o bit de `a` é 0 (inverte todos os bits) |

Com a célula toda fechada, `walls = 15`:

![As operações de bit sobre as paredes de uma célula: walls & EAST, ~EAST, walls & ~EAST e 13 | EAST](/img/value-objects/bits-operacoes.svg)

```python
walls = 15
walls & Direction.EAST     # 2: a parede Leste está fechada
walls & ~Direction.EAST    # 13: a mesma célula com a parede Leste aberta
```

- `walls & Direction.EAST` isola o bit do Leste: dá 2 se a parede está fechada e 0 se está
  aberta. É assim que o código **pergunta** por uma parede.
- `~Direction.EAST` liga todos os bits menos o do Leste. O Python mostra esse número como `-3`,
  por causa do jeito como guarda números negativos, mas nos quatro bits que importam ele é
  `1101`. Fazer `&` com ele **desliga** só o bit do Leste e mantém os outros: é assim que o
  código **abre** uma parede.
- `walls | Direction.EAST` **liga** o bit do Leste: é assim que o código **fecha** uma parede.

O resultado dessas contas é um `int` comum, e é isso que a grade de paredes guarda.

### As alternativas

| Alternativa | Problema |
|---|---|
| `Enum` comum | os membros não são números: `walls & Direction.EAST` levanta `TypeError` (o erro de "tipo errado para esta operação"), e cada conta precisaria de `.value` |
| `IntFlag` (um enum feito para combinar bits) | `Direction.NORTH \| Direction.EAST` vira uma `Direction` que o Python mostra como `<Direction.NORTH\|EAST: 3>`: uma "direção" que não é lado nenhum. Com `IntEnum`, a mesma conta dá só o número `3`, que não se passa por um lado |
| constantes soltas (`N = 1`) | nada impede passar `3` ou `16` onde se espera um lado |

## A ordem é `N, E, S, W`

Percorrer um `Enum` com `for` (ou com `list`) dá os membros **na ordem em que foram escritos**:

```python
print(list(Direction))
```

```text
[<Direction.NORTH: 1>, <Direction.EAST: 2>, <Direction.SOUTH: 4>, <Direction.WEST: 8>]
```

(`<Direction.NORTH: 1>` é como o Python mostra um membro numa lista: o nome e o valor.)

Essa ordem não é enfeite. O algoritmo que acha o caminho mais curto
([parte 7](../07-solver/01-busca-em-largura.md)) olha os vizinhos de cada célula sempre na ordem
Norte, Leste, Sul, Oeste, e `for side in Direction` dá exatamente essa ordem, sem lista extra. Os
métodos do `Maze` que devolvem lados de uma célula ([parte 5](../05-maze/05-passagens-e-becos.md))
também seguem essa ordem.

## Nunca `str(direction)`

O texto que `str()` produz para um membro de `IntEnum` mudou entre versões do Python: no 3.10 é
`Direction.NORTH`, do 3.11 em diante é `1`. O código nunca depende disso. Quando precisa do
número, usa `int(side)`; quando precisa da letra, usa a propriedade `letter`, da
[próxima página](./03-direction-propriedades.md).

## O que falta

A classe ainda não responde três perguntas: "qual é o lado oposto?", "para onde anda um
passo?" e "qual é a letra?". Elas moram em tabelas fora da classe, e o porquê está na
[próxima página](./03-direction-propriedades.md), junto com o arquivo completo.
