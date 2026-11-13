---
sidebar_position: 2
title: Convertendo um valor
---

# Convertendo um valor

Antes de conferir qualquer regra, cada texto do arquivo de configuração precisa virar o seu
tipo: `"20"` vira `20`, `"0,0"` vira `(0, 0)`, `"False"` vira `False`. Os conversores já existem
(o `ValueParser`, da [parte 10](../10-utilitarios/02-inteiros-sem-surpresa.md)). O que falta é
transformar a falha deles numa mensagem que o usuário entenda. Esta página cria a função que faz
isso.

## O problema

Quando um texto não serve, o `ValueParser` levanta uma exceção que só carrega o texto:

- `ValueError("abc")` quando o formato está errado;
- `OverflowError(...)` quando o número tem mais de 18 dígitos.

Ele não sabe de qual chave o texto veio. O usuário, porém, precisa ler a chave e o problema:

```text
WIDTH must be an integer, got 'abc'
ENTRY must be 'x,y' with integers, got '0;0'
PERFECT must be True or False, got 'yes'
WIDTH has more than 18 digits
```

Seis chaves passam por um conversor: todas as obrigatórias menos `OUTPUT_FILE`, que já é texto
e fica como está, mais a `SEED`, quando aparece. Escrever um `try`/`except` para cada uma
repetiria o mesmo bloco seis vezes. Uma função auxiliar, `_parse`, escreve esse bloco uma vez
só.

## A função `_parse`

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
| `raw` | o dicionário montado a partir do arquivo | de onde sai o texto |
| `key` | `"WIDTH"` | a chave, que entra na mensagem |
| `parser` | `ValueParser.to_int` | a função que converte |
| `expected` | `"an integer"` | o formato aceito, como aparece na mensagem |

`_parse` não usa nada do `MazeConfig` (nem `cls`, nem campo) e por isso é uma função do arquivo,
fora da classe. O `_` na frente é a convenção do Python para "interna a este arquivo".

Linha a linha (o `from None` do fim dos dois `raise` é explicado mais abaixo):

1. `value = raw[key]` pega o texto da chave, por exemplo `"abc"`.
2. `return parser(value)` tenta converter. Se der certo, a função termina aqui com o valor.
3. Cada `except` troca o erro do conversor por um `ConfigError`, a exceção de configuração da
   [parte 10](../10-utilitarios/05-a-hierarquia-app-error.md): o `OverflowError` vira a mensagem do limite de dígitos; o
   `ValueError`, a mensagem com a chave, o formato esperado e o texto lido.

### Uma função como parâmetro

`parser` recebe a **própria função**, sem parênteses: `ValueParser.to_int`, e não
`ValueParser.to_int(...)`. Em Python, uma função é um valor como outro qualquer: pode ser
guardada numa variável e passada adiante. Quem a chama é o `_parse`, na linha `parser(value)`.
Assim a mesma função auxiliar serve para inteiro, coordenada e booleano:

```python
width = _parse(raw, "WIDTH", ValueParser.to_int, "an integer")
entry = _parse(raw, "ENTRY", ValueParser.to_coordinate,
               "'x,y' with integers")
```

`Callable[[str], _T]` é a anotação de tipo de "uma função que recebe um `str` e devolve um
`_T`" (o `_T` é explicado mais abaixo).

### As duas mensagens

- No formato errado, a mensagem cita o valor entre aspas. O usuário vê exatamente o que o
  programa leu, inclusive o que ele achou que seria ignorado. Exemplo: o `#` só marca um
  comentário quando começa a linha ([página 9](./06-linha-a-linha.md)); um `#` depois do valor
  faz parte do valor. Com `WIDTH=20 # largura`, o texto lido é `20 # largura`, e a mensagem diz
  `got '20 # largura'`.
- Nos dígitos demais, a mensagem **não** cita o valor, que pode ter 100 000 caracteres.

### `raise ... from None`

Quando um `raise` acontece **dentro** de um `except`, o Python guarda a exceção original junto
com a nova. Se a nova chegar a aparecer num *traceback* (a listagem de erro que o Python imprime
quando uma exceção não é tratada), as duas aparecem. Na raiz do projeto:

```bash
.venv/bin/python -c '
from amazeing.errors import ConfigError

try:
    int("abc")
except ValueError:
    raise ConfigError("WIDTH must be an integer, got '"'"'abc'"'"'")
'
```

```text
Traceback (most recent call last):
  File "<string>", line 5, in <module>
    int("abc")
    ~~~^^^^^^^
ValueError: invalid literal for int() with base 10: 'abc'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<string>", line 7, in <module>
    raise ConfigError("WIDTH must be an integer, got 'abc'")
amazeing.errors.ConfigError: WIDTH must be an integer, got 'abc'
```

(O `'"'"'` no comando é o jeito do terminal de pôr uma aspa simples dentro de um texto entre
aspas simples; o Python recebe só `'`.)

Com `from None` no fim do `raise`, o Python descarta a original: tudo até a linha
`During handling of the above exception...` some, e sobra só o segundo traceback.

O usuário nunca vê traceback nenhum: o `main` captura o `ConfigError` e imprime só a linha
`Error: ...` ([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)). O `from None` vale para
quem estiver depurando o programa: o `ValueError` interno não diz nada que o `ConfigError` já não
diga melhor, e só atrapalharia a leitura.

## O tipo de volta: `TypeVar`

```python
_T = TypeVar("_T")
```

`_parse` devolve um `int` quando recebe `to_int`, uma tupla quando recebe `to_coordinate` e um
`bool` quando recebe `to_bool`. Uma anotação fixa, como `-> int`, estaria errada para dois
deles.

Uma **variável de tipo** (`TypeVar`) resolve: ela representa "algum tipo", e o mesmo `_T` na
entrada e na saída diz que os dois são **o mesmo** tipo. Lendo a assinatura: "`parser` recebe
`str` e devolve algum tipo `_T`; `_parse` devolve esse mesmo `_T`". O `mypy`, a ferramenta que
confere os tipos do código antes de ele rodar, deduz o `_T` em cada chamada: `width` sai `int`, e
`entry` sai `tuple[int, int]`.

O `_parse` só roda dentro do `MazeConfig.create`, completo na
[página 6](./08-o-maze-config-completo.md), cujo Experimente mostra estas mensagens de verdade.
