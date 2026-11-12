---
sidebar_position: 4
title: O "42" e o MazeConfig completo
---

# O "42" e o `MazeConfig` completo

## 7. Entrada e saída fora do "42"

As células do "42" ficam fechadas e fora do labirinto. Uma entrada ou saída em cima delas não
teria por onde sair, então o config recusa:

```python
pattern = Pattern42.for_size(width, height)
for key, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
    if Cell(x, y) in pattern:
        raise ConfigError(f'{key}={x},{y} lies on the "42" pattern')
```

- `Pattern42.for_size` é a mesma função que o gerador usa (parte 4): o config e o gerador
  calculam exatamente as mesmas células, sem copiar a fórmula do centro.
- Quando o "42" não cabe (grade menor que 9x7), o padrão vem vazio e a regra nunca acusa nada. O
  labirinto é gerado sem o "42", com o aviso da parte 1.
- É a última regra porque `for_size` precisa de um tamanho válido, e a pergunta "está no 42?"
  só faz sentido para uma célula que está dentro da grade.

A mensagem usa aspas simples por fora (`f'...'`) porque o texto tem aspas duplas em volta do
`"42"`.

### Por que `Cell(x, y)` e não `(x, y)`

`entry` é uma tupla, mas o `Pattern42` guarda células `Cell`. O `__contains__` dele só reconhece
`Cell`:

```bash
.venv/bin/python -c '
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

pattern = Pattern42.for_size(20, 15)
print(Cell(6, 5) in pattern)
print((6, 5) in pattern)
'
```

```text
True
False
```

Escrever `(x, y) in pattern` não daria erro nenhum: daria sempre `False`, e a regra nunca
dispararia. É o tipo de bug que passa despercebido, porque o programa continua rodando; só o
gerador, depois, recusaria com a mensagem dele, em minúsculas. Por isso a conversão para `Cell` é
explícita.

## O objeto pronto

```python
return cls(width, height, entry, exit, output_file, perfect, seed)
```

Chegando aqui, todas as regras passaram. `cls` é a própria classe (`MazeConfig`), e os valores já
estão convertidos. Chaves que não estão em `MANDATORY_KEYS` nem são `SEED` nunca foram lidas, e
por isso são ignoradas sem esforço nenhum:

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.maze_config import MazeConfig

raw = {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0", "EXIT": "19,14",
       "OUTPUT_FILE": "maze.txt", "PERFECT": "false", "COLOR": "red"}
print(MazeConfig.create(raw))
'
```

```text
MazeConfig(width=20, height=15, entry=(0, 0), exit=(19, 14), output_file='maze.txt', perfect=False, seed=None)
```

## As mensagens, sem o nome do arquivo

| Regra | Mensagem |
|---|---|
| 1 | `missing mandatory key(s): WIDTH, HEIGHT` |
| 2 | `WIDTH must be an integer, got 'abc'` |
| 2 | `WIDTH has more than 18 digits` |
| 2 | `ENTRY must be 'x,y' with integers, got '0;0'` |
| 2 | `OUTPUT_FILE must not be empty` |
| 2 | `PERFECT must be True or False, got 'yes'` |
| 2 | `SEED must be an integer, got '4.2'` |
| 3 | `WIDTH must be between 1 and 100, got 0` |
| 4 | `ENTRY=20,0 is outside the maze (x in 0..19, y in 0..14)` |
| 5 | `ENTRY and EXIT must differ` |
| 6 | `PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a Pac-Man board, got 1x10` |
| 7 | `ENTRY=6,5 lies on the "42" pattern` |

Nenhuma cita o arquivo: o `MazeConfig` não sabe de onde vieram os textos. Quem acrescenta o
`config.txt: ` na frente é o repositório, na última página desta parte.

## O arquivo completo

```python title="amazeing/domain/value_objects/maze_config.py"
"""Validated configuration of one run."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from amazeing.errors import ConfigError
from amazeing.utils.value_parser import ValueParser
from mazegen.generator import MAX_SIZE, MIN_SIZE
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

MANDATORY_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")

_T = TypeVar("_T")


@dataclass(frozen=True)
class MazeConfig:
    """Configuration that passed every rule of the configuration file.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell as (x, y).
        exit: Exit cell as (x, y).
        output_file: Path of the output file.
        perfect: True for a perfect maze, False for a Pac-Man board.
        seed: Seed of the random source; None when SEED is absent.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None

    @classmethod
    def create(cls, raw: Mapping[str, str]) -> "MazeConfig":
        """Validate the raw values, stopping at the first broken rule.

        The generator checks the same rules, but checking them here lets
        the message name the key of the file instead of the parameter.

        Args:
            raw: Upper-case keys mapped to stripped values.

        Returns:
            The configuration.

        Raises:
            ConfigError: A rule is broken; the message has no file prefix.
        """
        missing = [key for key in MANDATORY_KEYS if key not in raw]
        if missing:
            raise ConfigError(
                "missing mandatory key(s): " + ", ".join(missing))
        width = _parse(raw, "WIDTH", ValueParser.to_int, "an integer")
        height = _parse(raw, "HEIGHT", ValueParser.to_int, "an integer")
        entry = _parse(raw, "ENTRY", ValueParser.to_coordinate,
                       "'x,y' with integers")
        exit = _parse(raw, "EXIT", ValueParser.to_coordinate,
                      "'x,y' with integers")
        output_file = raw["OUTPUT_FILE"]
        if not output_file:
            raise ConfigError("OUTPUT_FILE must not be empty")
        perfect = _parse(raw, "PERFECT", ValueParser.to_bool,
                         "True or False")
        seed = None
        if "SEED" in raw:
            seed = _parse(raw, "SEED", ValueParser.to_int, "an integer")
        for key, value in (("WIDTH", width), ("HEIGHT", height)):
            if not MIN_SIZE <= value <= MAX_SIZE:
                raise ConfigError(f"{key} must be between {MIN_SIZE} and "
                                  f"{MAX_SIZE}, got {value}")
        for key, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise ConfigError(
                    f"{key}={x},{y} is outside the maze "
                    f"(x in 0..{width - 1}, y in 0..{height - 1})")
        if entry == exit:
            raise ConfigError("ENTRY and EXIT must differ")
        if not perfect and (width - 1) * (height - 1) < 2:
            raise ConfigError(
                "PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a "
                f"Pac-Man board, got {width}x{height}")
        pattern = Pattern42.for_size(width, height)
        for key, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
            if Cell(x, y) in pattern:
                raise ConfigError(f'{key}={x},{y} lies on the "42" pattern')
        return cls(width, height, entry, exit, output_file, perfect, seed)


def _parse(raw: Mapping[str, str], key: str, parser: Callable[[str], _T],
           expected: str) -> _T:
    """Convert one value and turn a parser error into a ConfigError.

    Args:
        raw: Upper-case keys mapped to stripped values.
        key: Key to convert.
        parser: ValueParser function for the type of the key.
        expected: Accepted format, as quoted in the message.

    Returns:
        The converted value.

    Raises:
        ConfigError: The value has the wrong format or too many digits.
    """
    value = raw[key]
    try:
        return parser(value)
    except OverflowError:
        raise ConfigError(
            f"{key} has more than {ValueParser.MAX_DIGITS} digits") from None
    except ValueError:
        raise ConfigError(f"{key} must be {expected}, got '{value}'") from None
```

`_parse` vem depois da classe no arquivo e mesmo assim funciona: o Python só procura o nome
`_parse` quando `create` é **chamado**, e a essa altura o módulo inteiro já foi carregado.
