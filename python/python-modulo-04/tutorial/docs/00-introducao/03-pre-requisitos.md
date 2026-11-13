---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int` e `str` | `count = 3`, `name = "foo"` |
| `if`, `elif` e comparações | `if name == "":` |
| laço `for` sobre uma sequência | `for line in lines:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| `print()` | `print("Hello")` |
| f-strings: texto com valores dentro de `{}` | `f"Accessing file '{name}'"` vira `Accessing file 'foo'` |
| listas e tuplas | `["a", "b"]`, `(True, "ok")` |
| `try` e `except`: capturar um erro para o programa não parar | `except ValueError as error:` |

## Exceções, em resumo

Quando algo dá errado, o Python cria uma **exceção**: um objeto que descreve o erro, com um **tipo**
(como `ValueError`) e uma **mensagem**. Se nenhum `except` a captura, o programa para e imprime um
relatório de erro chamado **traceback**. Um bloco `try` com `except` captura a exceção, e o programa
continua:

```python
try:
    number = int("abc")
except ValueError as error:
    print(f"Caught: {error}")
```

```text
Caught: invalid literal for int() with base 10: 'abc'
```

`as error` guarda a exceção na variável `error`, e `{error}` imprime a mensagem dela. Os tipos de
exceção formam uma família: um `except` de um tipo captura também os tipos que **herdam** dele (os
casos particulares). Esse ponto volta em [Quando o open
falha](../02-arquivos/05-quando-o-open-falha.md).

O bloco `finally`, que roda sempre ao fim do `try`, é explicado em [close e o
recurso](../02-arquivos/04-close-e-o-recurso.md).

## Três detalhes de texto

- `"\n"` dentro de um texto é uma **quebra de linha**: um caractere só, que manda o que vem depois
  para a linha de baixo. `print("---\n")` imprime `---` e depois uma linha vazia.
- Um texto entre aspas duplas pode conter aspas simples: `f"Accessing file '{name}'"`.
- `print()` acrescenta uma quebra de linha no fim do que imprime.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd` e
listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos funcionam no
terminal do Linux e do macOS, e os poucos que diferem entre os dois trazem a saída de cada sistema.
