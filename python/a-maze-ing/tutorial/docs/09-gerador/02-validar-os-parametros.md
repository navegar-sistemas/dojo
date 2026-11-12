---
sidebar_position: 2
title: Validar os parâmetros
---

# Validar os parâmetros

## Por que o construtor valida

A aplicação `amazeing` vai validar o arquivo de configuração por conta própria (parte 11). Mesmo
assim, o `MazeGenerator` valida de novo, porque ele é uma biblioteca: um projeto futuro pode
chamá-lo direto, sem arquivo de configuração nenhum.

Os erros aparecem **no construtor**, antes de qualquer trabalho. Um `MazeGenerator` que existe
sempre tem parâmetros possíveis, e `generate()` não precisa conferir nada.

A exceção é sempre `MazeError` (parte 4), e a mensagem **cita o nome do parâmetro**. Quem
recebe o erro sabe o que corrigir sem ler o código.

## Tamanho

```python
        for name, value in (("width", width), ("height", height)):
            if not MIN_SIZE <= value <= MAX_SIZE:
                raise MazeError(f"{name} must be between {MIN_SIZE} and "
                                f"{MAX_SIZE}, got {value}")
```

O laço sobre pares `(nome, valor)` evita escrever o mesmo `if` duas vezes. `width` vem antes de
`height`: com os dois errados, o erro fala de `width`.

## Entrada e saída na grade

```python
        if exit is None:
            exit = (width - 1, height - 1)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise MazeError(f"{name} ({x}, {y}) is outside the maze")
        if entry == exit:
            raise MazeError("entry and exit must differ")
```

- O `None` vira o canto de baixo à direita antes das checagens, para valerem as mesmas regras.
- `for name, (x, y) in ...` desmonta a tupla direto no laço.
- O subject exige entrada e saída diferentes e dentro dos limites.

## Tamanho possível para o Pac-Man

```python
        if not perfect and (width - 1) * (height - 1) < 2:
            raise MazeError(
                "perfect=False needs (width - 1) x (height - 1) >= 2 for a "
                f"Pac-Man board, got {width}x{height}")
```

Uma grade `W x H` com todas as paredes internas abertas tem `(W − 1) × (H − 1)` ciclos (parte
1). Se esse número é menor que 2, nem abrindo tudo o tabuleiro chega aos 2 ciclos exigidos:
1xN, Nx1 e 2x2 são impossíveis no modo Pac-Man. Recusar aqui evita gastar as tentativas de
`generate()` numa grade que nunca vai dar certo.

## Entrada e saída fora do "42"

```python
        pattern42 = Pattern42.for_size(width, height)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if Cell(x, y) in pattern42:
                raise MazeError(f'{name} ({x}, {y}) lies on the "42" pattern')
```

O "42" depende só do tamanho, então é calculado uma vez, aqui. Uma entrada ou saída dentro dele
seria uma célula fechada nos quatro lados, impossível de alcançar. `Pattern42.__contains__` só
aceita `Cell` (parte 4), por isso a tupla vira `Cell(x, y)` antes do `in`.

## Guardar o estado

```python
        self._width = width
        self._height = height
        self._entry = Cell(*entry)
        self._exit = Cell(*exit)
        self._perfect = perfect
        self._pattern42 = pattern42
        self._rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.solution = ""
        self.pattern: set[tuple[int, int]] = {
            cell.as_tuple() for cell in pattern42.cells
        }
```

- Os atributos com sublinhado são internos; `entry` e `exit` passam a ser `Cell` aqui dentro.
- `random.Random(seed)` é o **único** gerador de números do pacote. Com `seed=None`, o Python o
  inicializa com uma fonte aleatória do sistema operacional, e cada execução sai diferente.
- `pattern` volta a ser um conjunto de tuplas: é o formato de fora do pacote.

## Experimente

```python
from mazegen import MazeError, MazeGenerator

for kwargs in [
    {"width": 0, "height": 15},
    {"width": 20, "height": 101},
    {"width": 20, "height": 15, "entry": (20, 0)},
    {"width": 20, "height": 15, "exit": (0, 0)},
    {"width": 2, "height": 2},
    {"width": 20, "height": 15, "entry": (6, 5)},
]:
    try:
        MazeGenerator(**kwargs)
    except MazeError as error:
        print(error)
```

```text
width must be between 1 and 100, got 0
height must be between 1 and 100, got 101
entry (20, 0) is outside the maze
entry and exit must differ
perfect=False needs (width - 1) x (height - 1) >= 2 for a Pac-Man board, got 2x2
entry (6, 5) lies on the "42" pattern
```

Em 20x15, o canto do "42" fica em `(6, 5)`.
