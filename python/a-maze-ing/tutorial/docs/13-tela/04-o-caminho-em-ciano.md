---
sidebar_position: 4
title: O caminho em ciano
---

# O caminho em ciano

Com `state.show_path` ligado, a segunda passada pinta de ciano o caminho mais curto: as células
dele **e** as passagens entre células consecutivas. Pintar só as células deixaria quadrados
ciano soltos, separados por corredores sem cor, e o olho não veria um caminho contínuo.

## De onde vem o caminho

```python
        if state.show_path:
            path = maze.path()
```

`GeneratedMaze.path()` (parte 12) refaz a lista de células a partir da entrada e das letras de
`solution`: `EESES` vira `[(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2)]`. É a mesma
`solution` que o arquivo de saída grava na última linha, então o caminho desenhado é sempre o
do arquivo. O render não chama nenhum solver: resolver o labirinto é trabalho do `mazegen`, e o
desenho só mostra o resultado.

## Pares de células consecutivas

```python
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
```

`zip(path, path[1:])` junta cada célula com a seguinte: `((0, 0), (1, 0))`, `((1, 0), (2, 0))`,
e assim por diante, até `((3, 1), (3, 2))`. Um caminho de `n` passos dá `n` pares. O
desempacotamento `(x1, y1), (x2, y2)` já entrega as quatro coordenadas com nome.

## A passagem entre duas células

```python
                canvas[y1 + y2 + 1][x1 + x2 + 1] = Ansi.CYAN
```

As posições das duas células são `(2x1 + 1, 2y1 + 1)` e `(2x2 + 1, 2y2 + 1)`. A passagem fica
exatamente no meio delas, na média das duas posições:

```text
((2x1 + 1) + (2x2 + 1)) / 2 = x1 + x2 + 1
((2y1 + 1) + (2y2 + 1)) / 2 = y1 + y2 + 1
```

![Duas células vizinhas e a passagem entre elas](/img/tela/passagem.svg)

A fórmula vale para qualquer direção, sem `if`:

| Passo | Células | Passagem |
|---|---|---|
| Leste | `(1, 0)` → `(2, 0)` | `(4, 1)`: a parede Leste de `(1, 0)` |
| Sul | `(2, 0)` → `(2, 1)` | `(5, 2)`: a parede Sul de `(2, 0)` |
| Oeste | `(2, 0)` → `(1, 0)` | `(4, 1)`: a mesma parede do passo Leste |
| Norte | `(2, 1)` → `(2, 0)` | `(5, 2)`: a mesma parede do passo Sul |

Duas células consecutivas do caminho sempre têm a parede entre elas aberta: o solver só anda
por passagens. Pintar a posição não abre parede nenhuma, só colore um corredor que já existe.

## A célula de chegada

```python
                canvas[2 * y2 + 1][2 * x2 + 1] = Ansi.CYAN
```

Cada par pinta a célula **de chegada**. Com isso, todas as células do caminho, menos a primeira,
ficam ciano. A primeira é a entrada, que a próxima passada pinta de magenta de qualquer jeito;
a última é a saída, pintada de ciano agora e de vermelho logo depois.

## O resultado

No 4x3, a linha 1 do desenho (a das células `(x, 0)`) com o caminho oculto e com o caminho
visível, como o render a devolve:

```python
# caminho oculto
'\x1b[47m  \x1b[45m  \x1b[49m  \x1b[49m  \x1b[49m  \x1b[49m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
# caminho visível
'\x1b[47m  \x1b[45m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[46m  \x1b[47m  \x1b[49m  \x1b[47m  \x1b[0m'
```

As quatro posições entre a entrada e a parede fechada de `(2, 0)` trocaram `49` (fundo padrão)
por `46` (ciano): a passagem `(2, 1)`, a célula `(1, 0)`, a passagem `(4, 1)` e a célula
`(2, 0)`. A célula `(3, 0)` continua `49`, porque o caminho desce antes de chegar nela.
