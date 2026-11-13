---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

É preciso já ter escrito programas pequenos em Python. Estes itens aparecem sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float` e `str` | `height = 25`, `height = 25.0`, `name = "Rose"` |
| `+=`: somar ao valor que a variável já tem | `height += 0.8` é o mesmo que `height = height + 0.8` |
| `if`, `else` e comparações | `if height < 0:` |
| laço `for` sobre uma sequência | `for name in ("Rose", "Oak"):` |
| listas e tuplas | `[1, 2, 3]` (lista, entre colchetes) e `(30, 400)` (tupla, entre parênteses) |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| `True` e `False`, o tipo `bool` | `25 > 0` vale `True` |
| `print()` | `print("Hello")` |
| f-strings: texto com valores dentro de `{}` | `f"Plant: {name}"` vira `Plant: Rose` |

Classes **não** são pré-requisito: elas começam do zero em
[Classe e objeto](../03-ex1/02-classe-e-objeto.md).

Dois detalhes de texto aparecem bastante:

- Um texto entre aspas duplas pode conter aspas simples: `"height can't be negative"` imprime
  `height can't be negative`.
- `print()` sem nada entre os parênteses imprime uma **linha vazia**.

Também é preciso saber abrir um **terminal** (a janela onde se digitam comandos) e andar entre
pastas com `cd`. Os comandos funcionam no terminal do Linux e do macOS.
