---
sidebar_position: 1
title: O problema
---

# O problema

Um programa de jardim pode dar errado de vários jeitos: um dado que não é número, uma conta que
divide por zero, um arquivo que não existe, uma operação entre tipos que não combinam. O Python
tem um tipo de exceção para cada situação, e o programa pode reagir a cada uma de um jeito.

## O que o enunciado pede

Um arquivo `ex2/ft_different_errors.py`, que só pode chamar `print()`, `open()` e `int()`, com:

- uma função **`garden_operations(operation_number)`** com código defeituoso de propósito. Para
  cada número de 0 a 3, um trecho diferente lança um tipo de erro:

  | `operation_number` | Erro | Situação |
  |---|---|---|
  | 0 | `ValueError` | um dado ruim, como `"abc"` no lugar de um número para o `int()` |
  | 1 | `ZeroDivisionError` | uma divisão por zero |
  | 2 | `FileNotFoundError` | abrir um arquivo que não existe |
  | 3 | `TypeError` | misturar tipos que não se misturam, como somar um texto com um número |

  Com qualquer outro número, a função não faz nada de errado e só retorna;
- uma função **`test_error_types()`** que mostra cada erro acontecendo, captura cada um e diz o
  que deu errado, mostra que o programa continua depois de cada erro, e mostra como capturar
  **vários tipos de erro com um único `try`**.

O enunciado faz duas observações. Não se pode usar a função `type()` (que devolve o tipo de um
objeto); e o mypy vai acusar um erro no trecho do `TypeError`, de propósito.

## A saída esperada

```text
=== Garden Error Types Demo ===
Testing operation 0...
Caught ValueError: invalid literal for int() with base 10: 'abc'
Testing operation 1...
Caught ZeroDivisionError: division by zero
Testing operation 2...
Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
Testing operation 3...
Caught TypeError: can only concatenate str (not "int") to str
Testing operation 4...
Operation completed successfully

All error types tested successfully!
```

Cada linha `Caught` traz o **nome do tipo** do erro e a mensagem do Python. A operação 4 não tem
defeito e termina bem. A saída também fixa os detalhes de cada operação: o texto `'abc'` e o
caminho `/non/existent/file`.
