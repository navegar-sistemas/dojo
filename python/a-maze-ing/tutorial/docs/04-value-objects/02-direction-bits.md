---
sidebar_position: 2
title: "Direction: um lado, um bit"
---

# `Direction`: um lado, um bit

## O que é

Os quatro lados de uma célula: Norte, Leste, Sul e Oeste. Está em
`mazegen/value_objects/direction.py` e é usada por todo o gerador: para abrir uma parede, para
andar até a vizinha, para escrever o caminho em letras.

## O valor é o bit da parede

```python
from enum import IntEnum


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
```

Cada membro vale exatamente o bit do lado no arquivo de saída (parte 1). Assim, não existe
tabela de conversão entre "direção" e "bit": a direção **é** o bit.

## Por que `IntEnum`

Um `Enum` comum dá nomes a um conjunto fechado de valores: `Direction.NORTH` em vez de um `1`
solto, e o mypy recusa um `int` qualquer onde se espera uma `Direction`.

`IntEnum` é um `Enum` cujos membros **também são inteiros**. Isso permite usar a direção direto
numa operação de bits com a máscara da célula:

```python
walls = 15
walls & Direction.EAST     # 2: a parede Leste está fechada
walls & ~Direction.EAST    # 13: a mesma máscara com a parede Leste aberta
```

O resultado é um `int` comum, que é o que a grade guarda.

| Alternativa | Problema |
|---|---|
| `Enum` | `walls & Direction.EAST` levanta `TypeError`; cada uso precisaria de `.value` |
| `IntFlag` | `NORTH \| EAST` vira um terceiro valor do próprio tipo, uma "direção" que não é lado nenhum |
| constantes soltas (`N = 1`) | nada impede passar `3` ou `16` onde se espera um lado |

## A ordem é `N, E, S, W`

Iterar um `Enum` percorre os membros **na ordem em que foram declarados**:

```python
>>> list(Direction)
[<Direction.NORTH: 1>, <Direction.EAST: 2>, <Direction.SOUTH: 4>, <Direction.WEST: 8>]
```

Essa ordem não é estética. A busca em largura (parte 7) visita os vizinhos de cada célula na
ordem Norte, Leste, Sul, Oeste, e `for side in Direction` dá exatamente essa ordem, sem lista
extra. Os métodos do `Maze` que devolvem lados (`passages`, `closed_sides`) também seguem essa
ordem.

## Nunca `str(direction)`

O texto que `str()` produz para um `IntEnum` mudou entre versões do Python: no 3.10 é
`Direction.NORTH`, do 3.11 em diante é `1`. O código nunca depende disso. Quando precisa do
número, usa `int(side)`; quando precisa da letra, usa a propriedade `letter`, da próxima página.

## O que falta

A classe ainda não sabe responder "qual é o lado oposto?", "para onde anda um passo?" nem "qual
é a letra?". Essas três perguntas são propriedades, e moram em tabelas fora da classe: o porquê
está na [próxima página](./03-direction-propriedades.md).
