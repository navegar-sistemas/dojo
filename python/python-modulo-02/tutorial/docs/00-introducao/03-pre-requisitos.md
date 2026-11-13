---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

O tutorial usa, sem explicação longa, o básico de Python:

| Assunto | Exemplo |
|---|---|
| variáveis, `int` e `str` | `temperature = 25`, `name = "Tomato"` |
| `if`, `elif` e comparações | `if temperature > 40:` |
| laço `for` sobre uma sequência | `for name in ("Tomato", "Lettuce"):` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| `print()` | `print("Hello")` |
| f-strings: texto com valores dentro de `{}` | `f"Temperature is now {temperature}°C"` vira `Temperature is now 25°C` |
| tuplas: valores separados por vírgula, em geral entre parênteses | `("25", "abc")` |
| o básico de classes: `class`, `__init__` e `self` | `class Plant:` com `def __init__(self, name: str) -> None:` |

Três detalhes de texto aparecem bastante:

- `"\n"` dentro de um texto é uma **quebra de linha**. `print("\nTesting")` imprime uma linha
  vazia e depois `Testing`.
- Um texto entre aspas duplas pode conter aspas simples: `f"Input data is '{temp_str}'"` imprime
  `Input data is '25'`.
- O símbolo `°` (grau) é um caractere comum dentro do texto; o Python 3 aceita qualquer caractere
  num arquivo `.py`.

Também é preciso saber abrir um **terminal** (a janela onde se digitam comandos) e andar entre
pastas com `cd`. Os comandos do tutorial funcionam no terminal do Linux e do macOS.
