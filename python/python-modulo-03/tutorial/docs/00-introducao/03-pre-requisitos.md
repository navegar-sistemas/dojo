---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam, sem explicação longa, o básico de Python:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float` e `str` | `score = 1500`, `x = 2.5`, `name = "Alice"` |
| `if`, `elif`, `else` e comparações | `if score > high:` |
| laços `for` e `while` | `while True:` |
| `continue` e `break` dentro de um laço | `continue` pula para a próxima volta; `break` sai do laço |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| `print()` | `print("Hello")` |
| f-strings: texto com valores dentro de `{}` | `f"Total score: {total}"` vira `Total score: 9650` |
| `try` e `except` para capturar um erro | `try: int("abc")` seguido de `except ValueError as error:` |

O tratamento de erros com `try` e `except` aparece sempre do mesmo jeito neste projeto: o código
que pode falhar vai no `try`, e o `except ValueError as error` captura o erro e guarda a mensagem
em `error`. Um `ValueError` é o
erro que o Python lança quando uma conversão recebe um texto que não serve, como `int("abc")`.

Três detalhes de texto aparecem bastante:

- `"\n"` dentro de um texto é uma **quebra de linha**. `print("\nTesting")` imprime uma linha
  vazia e depois `Testing`.
- Um texto entre aspas duplas pode conter aspas simples: `f"Invalid parameter: '{text}'"`
  imprime `Invalid parameter: 'ab'`.
- Dois textos escritos lado a lado, sem nada entre eles, viram um texto só:
  `"Data " "Quest"` é o mesmo que `"Data Quest"`. Isso permite quebrar um texto comprido em duas
  linhas de código.

Também é preciso saber abrir um **terminal** (a janela onde se digitam comandos) e andar entre
pastas com `cd`. Os comandos funcionam no terminal do Linux e do macOS.
