---
sidebar_position: 3
title: "Direction: oposto, passo e letra"
---

# `Direction`: oposto, passo e letra

Saber que um lado vale 1, 2, 4 ou 8 não basta para o gerador. Para abrir uma parede ele precisa
do lado **oposto** na célula vizinha; para andar até a vizinha, de **quanto `x` e `y` mudam**;
para escrever o caminho mais curto, da **letra** do lado. Esta página acrescenta essas três
respostas à `Direction` (criada na [página anterior](./02-direction-bits.md)) e mostra o arquivo
completo.

## As três respostas

| Propriedade | `NORTH` | `EAST` | `SOUTH` | `WEST` | Quem usa |
|---|---|---|---|---|---|
| `opposite` | `SOUTH` | `WEST` | `NORTH` | `EAST` | o `Maze`, a grade de paredes ([parte 5](../05-maze/04-abrir-e-fechar.md)), para manter as duas células de uma parede de acordo |
| `dx` | `0` | `1` | `0` | `-1` | o método `step` da `Cell`, a posição de uma célula (página [Cell](./04-cell.md)), para andar um passo |
| `dy` | `-1` | `0` | `1` | `0` | o mesmo `step` da `Cell` |
| `letter` | `"N"` | `"E"` | `"S"` | `"W"` | o `Solver`, que acha o caminho mais curto ([parte 7](../07-solver/02-pais-e-letras.md)), para escrever o caminho |

### `opposite`: o mesmo muro visto do outro lado

A parede Leste de uma célula é **a mesma** parede que a Oeste da vizinha da direita. O enunciado
exige que as duas células concordem sobre ela (a regra de **coerência**): se uma diz "fechada", a
outra também diz. Por isso, ao abrir o Leste da célula `x,y`, o `Maze`
([parte 5](../05-maze/04-abrir-e-fechar.md)) também abre o `EAST.opposite`, isto é, o Oeste, da
célula `x+1,y`.

### `dx` e `dy`: quanto anda um passo

Relembrando as coordenadas: `x` é a coluna (cresce para a direita) e `y` é a linha (cresce **para
baixo**, porque a linha 0 é a de cima). `dx` e `dy` dizem quanto `x` e `y` mudam num passo para
aquele lado. Como `y` cresce para baixo, subir (Norte) é `dy = -1`:

![Os quatro deltas em volta de uma célula](/img/value-objects/direction-deltas.svg)

### `letter`: a letra do caminho

O caminho mais curto é gravado no arquivo de saída com uma letra por passo (`N`, `E`, `S` ou
`W`). `side.letter` dá a letra sem depender do `str()` do enum, que muda entre versões do Python.

## `@property`: um método lido como atributo

```python
    @property
    def opposite(self) -> "Direction":
        return _OPPOSITE[self.value]
```

`@property`, escrito na linha de cima do `def`, é um **decorador**: ele muda o jeito de usar o
método. Com ele, o método é chamado **sem parênteses**, como se fosse um atributo:
`Direction.EAST.opposite`, e não `Direction.EAST.opposite()`. Combina com o que ele é: um dado
fixo do lado, não uma ação.

`self.value` é o número do membro (2 para `EAST`), usado como chave da tabela `_OPPOSITE`.

`-> "Direction"` é a anotação do tipo de retorno: o método devolve uma `Direction`. Ela vai entre
aspas porque, enquanto o Python ainda está criando a classe, o nome `Direction` não existe. A
anotação em texto é lida depois, pelo mypy, quando a classe já está pronta.

## As tabelas

Cada propriedade só consulta um dicionário, indexado pelo valor do lado:

```python
_OPPOSITE: dict[int, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}
_DELTA: dict[int, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
```

- `dict[int, Direction]` é a anotação de tipo do dicionário: chaves `int`, valores `Direction`.
  As chaves podem ser escritas como `Direction.NORTH` porque, num `IntEnum`, o membro **é** um
  inteiro (o 1), e por isso cabe onde a anotação pede `int`.
- A consulta usa `self.value`, o número do membro (1, 2, 4 ou 8). Para um dicionário, o número 1
  e o membro `Direction.NORTH` são a mesma chave, porque são iguais (`==`) e têm o mesmo hash
  (o número que o dicionário usa para achar a chave). `_OPPOSITE[self]` acharia a mesma entrada;
  o projeto escolhe a anotação `int` e o `self.value` para deixar escrito que as tabelas são
  consultadas pelo bit do lado.
- `_DELTA` guarda o par `(dx, dy)` de cada lado: a propriedade `dx` lê a posição `[0]` do par, e
  `dy` a posição `[1]`.
- O `_` no começo do nome é a convenção do Python para "uso interno deste arquivo": ninguém de
  fora deve ler essas tabelas diretamente.

## Por que as tabelas ficam fora da classe

Dentro do corpo de um `Enum`, **toda atribuição vira um membro**. Uma tabela escrita ali dentro
viraria um quinto "lado", e o `IntEnum` tentaria transformá-la em número inteiro:

```python
class Direction(IntEnum):
    NORTH = 1
    SOUTH = 4
    _OPPOSITE = {NORTH: SOUTH}
```

A classe nem chega a ser criada. O Python levanta este erro:

```text
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'dict'
```

Além disso, dentro do corpo, `NORTH` ainda é só o inteiro `1`, não o membro `Direction.NORTH`: a
tabela guardaria números, e `opposite` devolveria um `int` em vez de uma `Direction`.

Escritas **depois** da classe, as tabelas já encontram os membros prontos; e as propriedades só
as leem quando chamadas, com o arquivo inteiro já carregado.

### E um `if`/`elif`?

Cada propriedade poderia testar os quatro lados com `if`. Seriam quatro blocos de oito linhas
quase iguais, e um erro de digitação num deles passaria despercebido. As tabelas põem os valores
lado a lado, onde dá para conferir de uma vez.

## As docstrings

O arquivo completo, abaixo, tem uma **docstring** (o texto entre `"""` que documenta) na classe
e em cada método: o enunciado exige docstrings em funções e classes. Elas seguem o estilo Google,
escolha do projeto ([parte 3](../03-ambiente/07-pacotes-do-mazegen.md)): uma frase de resumo e
seções com nome, como `Returns:`, o que o método devolve.

## O arquivo completo

```python title="mazegen/value_objects/direction.py"
"""The four sides of a cell and the wall bit of each one."""

from enum import IntEnum


class Direction(IntEnum):
    """Side of a cell; the value is the wall bit in the output file.

    Iterating the enum yields NORTH, EAST, SOUTH and WEST, the neighbour
    order of the breadth-first search.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Side that faces this one across a shared wall.

        Returns:
            The opposite direction.
        """
        return _OPPOSITE[self.value]

    @property
    def dx(self) -> int:
        """Column offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][0]

    @property
    def dy(self) -> int:
        """Row offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][1]

    @property
    def letter(self) -> str:
        """Letter of this side in the shortest path.

        Returns:
            "N", "E", "S" or "W".
        """
        return _LETTER[self.value]


_OPPOSITE: dict[int, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}
_DELTA: dict[int, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
_LETTER: dict[int, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W",
}
```

## Experimente

Com o arquivo acima gravado em `mazegen/value_objects/direction.py`, na raiz do projeto
([como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos)):

```bash
.venv/bin/python - <<'EOF'
from mazegen.value_objects.direction import Direction

for side in Direction:
    print(side.name, side.opposite.name, side.dx, side.dy, side.letter)
EOF
```

```text
NORTH SOUTH 0 -1 N
EAST WEST 1 0 E
SOUTH NORTH 0 1 S
WEST EAST -1 0 W
```

Cada linha é um lado: o nome, o nome do oposto, o `dx`, o `dy` e a letra.
