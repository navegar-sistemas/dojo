---
sidebar_position: 5
title: "Pattern42: o desenho e a posição"
---

# `Pattern42`: o desenho e a posição

## O que é

O conjunto das células que desenham o "42" numa grade de um tamanho dado. Está em
`mazegen/value_objects/pattern42.py`. O `Maze` guarda um `Pattern42` e trata essas células como
paredes maciças: nenhum algoritmo entra nelas.

## As constantes

```python
GLYPHS = ("X...XXX", "X.....X", "XXX.XXX", "..X.X..", "..X.XXX")
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5
MIN_WIDTH = 9
MIN_HEIGHT = 7
```

| Constante | Significado |
|---|---|
| `GLYPHS` | o desenho da parte 1, uma string por linha: `X` é célula do "42", `.` é célula comum |
| `PATTERN_WIDTH`, `PATTERN_HEIGHT` | o tamanho do bloco: 7 colunas por 5 linhas |
| `MIN_WIDTH`, `MIN_HEIGHT` | o bloco mais uma célula de corredor de cada lado: 7 + 2 e 5 + 2 |

O desenho fica em texto porque assim ele é **legível no código**: quem abre o arquivo vê o "4" e
o "2". Uma lista de 18 coordenadas faria o mesmo trabalho, mas ninguém enxergaria o desenho
nela, nem perceberia um erro de digitação.

## `@dataclass(frozen=True)` com `frozenset`

```python
@dataclass(frozen=True)
class Pattern42:
    cells: frozenset[Cell]
```

O padrão é um value object: o mesmo tamanho de grade dá sempre as mesmas células, e nada as
altera depois.

O campo é um `frozenset`, o `set` imutável do Python. Com um `set` comum, `frozen=True` impediria
trocar o campo, mas não impediria `pattern.cells.add(...)`. Além disso, o `__hash__` gerado pelo
`@dataclass` calcula o hash dos campos, e um `set` comum não tem hash.

## `for_size`: o construtor a partir do tamanho

```python
    @classmethod
    def for_size(cls, width: int, height: int) -> "Pattern42":
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return cls(frozenset())
```

O `__init__` gerado pelo `@dataclass` recebe as células prontas. Quem cria um padrão, porém, só
sabe o tamanho da grade. `for_size` é um **método de fábrica**: um `@classmethod` que recebe o
tamanho, calcula as células e chama o construtor (`cls(...)`).

A primeira decisão é se o "42" cabe. Abaixo de 9x7, o resultado é um padrão **vazio**. Não é um
erro: o labirinto é gerado sem o desenho, e o programa só avisa.

```python
        x0 = (width - PATTERN_WIDTH) // 2
        y0 = (height - PATTERN_HEIGHT) // 2
```

`(x0, y0)` é o canto de cima à esquerda do bloco 7x5. A sobra de colunas (`width - 7`) é
dividida entre esquerda e direita; com sobra ímpar, a divisão inteira `//` põe a coluna extra à
direita. O mesmo vale para as linhas.

```python
        return cls(frozenset(
            Cell(x0 + dx, y0 + dy)
            for dy, row in enumerate(GLYPHS)
            for dx, char in enumerate(row)
            if char == "X"
        ))
```

Percorre o desenho linha a linha (`dy`) e caractere a caractere (`dx`), e cria uma `Cell`
deslocada por `(x0, y0)` para cada `X`. São 18 células.

## Três tamanhos

Em 9x7, o tamanho mínimo, sobra exatamente uma célula de corredor em volta do bloco (tracejado):

![O 42 numa grade 9 por 7](/img/value-objects/pattern42-9x7.svg)

Em 20x15, o tamanho do `config.txt`:

![O 42 numa grade 20 por 15](/img/value-objects/pattern42-20x15.svg)

Em 8x7, `x0 = (8 - 7) // 2 = 0`: o bloco encostaria na borda esquerda, e a coluna 0 do "4"
fecharia o corredor da borda. Por isso o padrão fica vazio:

![Em 8 por 7 o bloco encostaria na borda](/img/value-objects/pattern42-8x7.svg)

### A margem vale em todo tamanho permitido

Com `width >= 9`, `x0 = (width - 7) // 2` é pelo menos 1, e a última coluna do bloco,
`x0 + 6`, fica no máximo em `width - 2`. O mesmo raciocínio vale para as linhas com
`height >= 7`. Os quatro cantos da grade nunca são do "42", e sempre há corredor em volta dele.

## Experimente

```python
from mazegen.value_objects.pattern42 import Pattern42

p = Pattern42.for_size(20, 15)
xs = [cell.x for cell in p.cells]
ys = [cell.y for cell in p.cells]
print(len(p.cells), min(xs), max(xs), min(ys), max(ys))
print(Pattern42.for_size(8, 7))
```

```text
18 6 12 5 9
Pattern42(cells=frozenset())
```

Em 20x15, o "42" ocupa as colunas 6 a 12 e as linhas 5 a 9.
