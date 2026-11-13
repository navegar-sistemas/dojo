---
sidebar_position: 6
title: O MazeConfig completo
---

# O `MazeConfig` completo

As páginas anteriores construíram o `MazeConfig` em pedaços: os campos, a conversão de cada
texto e as sete regras. Esta página junta tudo no arquivo
`amazeing/domain/value_objects/maze_config.py` e roda os exemplos que dependiam dele.

## Os `import` do topo

| Import | Para quê |
|---|---|
| `Callable`, `Mapping` | anotações de tipo: "função" e "algo que se lê como dicionário" |
| `dataclass` | o decorador que escreve o construtor a partir dos campos |
| `TypeVar` | a variável de tipo `_T` do `_parse` |
| `ConfigError` | a exceção de configuração ([parte 10](../10-utilitarios/05-a-hierarquia-app-error.md)) |
| `ValueParser` | os conversores de texto ([parte 10](../10-utilitarios/02-inteiros-sem-surpresa.md)) |
| `MIN_SIZE`, `MAX_SIZE`, `Cell`, `Pattern42` | os limites de tamanho e as peças do "42", vindas do `mazegen` |

`Callable` e `Mapping` vêm de `collections.abc`, o módulo da biblioteca padrão que descreve as
coleções e as funções de forma abstrata; desde o Python 3.9 é de lá que a documentação manda
importá-los. `TypeVar` não existe em `collections.abc` e vem de `typing`.

`MIN_SIZE`, `MAX_SIZE`, `Cell` e `Pattern42` são importados pelo caminho interno do `mazegen`
(`mazegen.generator` e `mazegen.value_objects...`), porque o pacote só oferece diretamente
`MazeGenerator` e `MazeError` (os dois nomes do `mazegen/__init__.py`,
[parte 9](../09-gerador/05-documentacao-do-modulo.md)).

Isso foge um pouco da ideia da [parte 2](../02-arquitetura/02-dois-pacotes.md): a aplicação usa
o `mazegen` como usaria uma biblioteca instalada, e o miolo do pacote fica escondido de quem o
instala. A aplicação pode abrir essa exceção porque mora no mesmo repositório e muda junto com o
`mazegen`: se um caminho interno mudar, a aplicação é ajustada no mesmo passo. Um projeto de
fora, que instala o `mazegen` pelo arquivo do pacote, não deveria usar o caminho interno, que pode
mudar de uma versão para outra sem aviso.

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

`_parse` aparece depois da classe no arquivo e mesmo assim funciona: o Python só procura o nome
`_parse` quando o `create` é **chamado**, e a essa altura o arquivo inteiro já foi carregado.

## Experimente

Os exemplos rodam na raiz do projeto. O primeiro cria uma configuração válida, com uma chave
desconhecida (`COLOR`) e o booleano em minúsculas, e depois tenta mudar um campo:

```bash
.venv/bin/python - <<'EOF'
from amazeing.domain.value_objects.maze_config import MazeConfig

config = MazeConfig.create({"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0",
                            "EXIT": "19,14", "OUTPUT_FILE": "maze.txt",
                            "PERFECT": "false", "COLOR": "red"})
print(config)
try:
    config.width = 0
except Exception as error:
    print(type(error).__name__, "->", error)
EOF
```

```text
MazeConfig(width=20, height=15, entry=(0, 0), exit=(19, 14), output_file='maze.txt', perfect=False, seed=None)
FrozenInstanceError -> cannot assign to field 'width'
```

O `print` mostra o texto que o `@dataclass` escreve: cada campo já no seu tipo, a `seed` como
`None` (não havia `SEED`) e nenhum sinal do `COLOR`, que o `create` nunca leu. A troca de
`width` é recusada pelo `frozen=True`.

O segundo troca um valor de cada vez numa configuração válida e mostra a mensagem de erro.
`{**base, **change}` monta um dicionário novo com tudo de `base` e, por cima, as chaves de
`change`. `"9" * 100000` é um texto com 100 000 noves:

```bash
.venv/bin/python - <<'EOF'
from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.errors import ConfigError

base = {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0", "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt", "PERFECT": "True"}
changes = [{"WIDTH": "abc"}, {"WIDTH": "9" * 100000}, {"ENTRY": "0;0"},
           {"SEED": "4.2"}, {"ENTRY": "6,5"}]
for change in changes:
    try:
        MazeConfig.create({**base, **change})
    except ConfigError as error:
        print(error)
EOF
```

```text
WIDTH must be an integer, got 'abc'
WIDTH has more than 18 digits
ENTRY must be 'x,y' with integers, got '0;0'
SEED must be an integer, got '4.2'
ENTRY=6,5 lies on the "42" pattern
```

O terceiro mostra a ordem das regras ([página 3](./03-a-ordem-das-validacoes.md)). Cada um dos
quatro primeiros casos quebra duas regras, e só a primeira, na ordem, é acusada. O último não
tem quatro das seis chaves obrigatórias, e todas aparecem numa mensagem só:

```bash
.venv/bin/python - <<'EOF'
from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.errors import ConfigError

base = {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0", "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt", "PERFECT": "True"}
for change in [{"WIDTH": "abc", "HEIGHT": "0"},
               {"WIDTH": "0", "ENTRY": "50,50"},
               {"ENTRY": "30,30", "EXIT": "30,30"},
               {"ENTRY": "6,5", "EXIT": "6,5"}]:
    try:
        MazeConfig.create({**base, **change})
    except ConfigError as error:
        print(error)
try:
    MazeConfig.create({"WIDTH": "20", "HEIGHT": "15"})
except ConfigError as error:
    print(error)
EOF
```

```text
WIDTH must be an integer, got 'abc'
WIDTH must be between 1 and 100, got 0
ENTRY=30,30 is outside the maze (x in 0..19, y in 0..14)
ENTRY and EXIT must differ
missing mandatory key(s): ENTRY, EXIT, OUTPUT_FILE, PERFECT
```

No quarto caso, `6,5` é também uma célula do "42", mas a regra 5 (entrada diferente da saída)
vem antes da 7 (fora do "42").
