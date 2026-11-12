---
sidebar_position: 2
title: Convertendo um valor
---

# Convertendo um valor

Antes das regras, cada texto vira o seu tipo: `"20"` vira `20`, `"0,0"` vira `(0, 0)`, `"False"`
vira `False`. Quem converte é o `ValueParser` (parte 10); o que falta é transformar a falha dele
numa mensagem para o usuário.

## O problema

O `ValueParser` levanta `ValueError("abc")` ou `OverflowError(...)`, sem dizer de qual chave
veio o texto. O usuário precisa ler:

```text
WIDTH must be an integer, got 'abc'
ENTRY must be 'x,y' with integers, got '0;0'
PERFECT must be True or False, got 'yes'
WIDTH has more than 18 digits
```

Escrever um `try`/`except` para cada uma das sete chaves repetiria o mesmo bloco sete vezes. Um
helper, `_parse`, faz isso uma vez.

## O helper `_parse`

```python
def _parse(raw: Mapping[str, str], key: str, parser: Callable[[str], _T],
           expected: str) -> _T:
    value = raw[key]
    try:
        return parser(value)
    except OverflowError:
        raise ConfigError(
            f"{key} has more than {ValueParser.MAX_DIGITS} digits") from None
    except ValueError:
        raise ConfigError(f"{key} must be {expected}, got '{value}'") from None
```

| Parâmetro | Exemplo | Papel |
|---|---|---|
| `raw` | o dicionário do repositório | de onde sai o texto |
| `key` | `"WIDTH"` | a chave, já em maiúsculas, que entra na mensagem |
| `parser` | `ValueParser.to_int` | a função que converte |
| `expected` | `"an integer"` | o formato aceito, como aparece na mensagem |

O `parser` é a própria função, sem parênteses: `_parse` a chama com o texto. Assim o mesmo
helper serve para inteiro, coordenada e booleano.

### As duas mensagens

- `ValueError` (formato errado): a mensagem cita o valor entre aspas, para o usuário ver
  exatamente o que o programa leu, inclusive um comentário no fim da linha que ele achou que
  seria ignorado (`got '20 # largura'`).
- `OverflowError` (dígitos demais): a mensagem **não** cita o valor, que pode ter 100 000
  caracteres. Diz só o limite.

### `from None`

`raise ... from None` substitui a exceção original em vez de encadeá-la. Sem ele, se o erro um
dia aparecesse num traceback, viriam duas exceções (o `ValueError` interno e, "durante o
tratamento dele", o `ConfigError`). O `ValueError("abc")` não diz nada que o `ConfigError` já não
diga melhor; o `from None` deixa só o que importa.

## O tipo de volta: `TypeVar`

```python
_T = TypeVar("_T")
```

`_parse` devolve `int` quando recebe `to_int`, `tuple[int, int]` quando recebe `to_coordinate` e
`bool` quando recebe `to_bool`. Uma anotação fixa (`-> int`) estaria errada para dois deles, e
`-> object` faria o `mypy` perder o tipo de cada campo.

A variável de tipo `_T` liga a entrada à saída: "`parser` é uma função que recebe `str` e devolve
algum tipo `_T`; `_parse` devolve esse mesmo `_T`". O `mypy` deduz o tipo em cada chamada:

```python
width = _parse(raw, "WIDTH", ValueParser.to_int, "an integer")
entry = _parse(raw, "ENTRY", ValueParser.to_coordinate,
               "'x,y' with integers")
```

`width` sai `int` e `entry` sai `tuple[int, int]`, sem nenhum cast.

## Por que uma função do módulo

`_parse` não usa nada do `MazeConfig`: nem `cls`, nem campo. Fica como função do módulo, com `_`
na frente para dizer que é interna ao arquivo e não faz parte do que o `MazeConfig` oferece.

## Experimente

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.errors import ConfigError

base = {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0", "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt", "PERFECT": "True"}
for change in [{"WIDTH": "abc"}, {"WIDTH": "9" * 100000},
               {"ENTRY": "0;0"}, {"SEED": "4.2"}]:
    try:
        MazeConfig.create({**base, **change})
    except ConfigError as error:
        print(error)
'
```

```text
WIDTH must be an integer, got 'abc'
WIDTH has more than 18 digits
ENTRY must be 'x,y' with integers, got '0;0'
SEED must be an integer, got '4.2'
```
