---
sidebar_position: 4
title: Vários except num try
---

# Vários except num try

A função de teste roda as operações de 0 a 4 e precisa dizer **qual** tipo de erro aconteceu em
cada uma.

```python
def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for operation_number in (0, 1, 2, 3, 4):
        print(f"Testing operation {operation_number}...")
        try:
            garden_operations(operation_number)
            print("Operation completed successfully")
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")
    print("\nAll error types tested successfully!")
```

## Um try, quatro except

Um bloco `try` pode ter vários `except`, um embaixo do outro. Quando uma exceção é lançada, o
Python testa os `except` **de cima para baixo** e roda **só o primeiro** cujo tipo combina; os
outros são ignorados. Assim, um único `try` captura os quatro tipos de erro, e cada tipo tem a
sua reação. O enunciado aceita capturar os tipos separadamente ou em conjunto; aqui eles são
capturados separadamente, dentro de um único `try`, porque a saída de exemplo escreve o nome de
cada tipo.

Cada `except` escreve o nome do tipo **no próprio texto** (`"Caught ValueError: "`), porque
`{error}` imprime só a mensagem, sem o tipo (página
[A mensagem do erro](../02-excecoes/04-a-mensagem-do-erro.md)).

## Por que não um except só, com type()

Existe uma forma mais curta de capturar vários tipos: uma tupla de tipos num só `except`. Um
experimento, `experimentos/tupla.py`, que divide 10 pelo número de cada texto:

```python
for text in ("abc", "0"):
    try:
        print(10 / int(text))
    except (ValueError, ZeroDivisionError) as error:
        print(f"Caught: {error}")
```

```bash
python3 experimentos/tupla.py
```

```text
Caught: invalid literal for int() with base 10: 'abc'
Caught: division by zero
```

Os dois erros caem no mesmo bloco, e o código do bloco é o mesmo para os dois. Para escrever o
nome do tipo, seria preciso perguntar ao objeto qual é o tipo dele, e o jeito comum é
`type(error)`, que o enunciado proíbe. Com um `except` por tipo, cada bloco já sabe qual erro
capturou, sem precisar perguntar.

## O laço e a operação 4

O `for` passa pelos números de 0 a 4, e o `try` fica dentro dele, como no
[exercício 0](../03-ex0/03-test-temperature.md): cada erro é capturado e o laço segue para a
operação seguinte. Na operação 4, `garden_operations` não lança nada, a linha
`Operation completed successfully` roda e nenhum `except` é usado.

No fim, a linha vazia (`\n`) e a mensagem final mostram que o programa sobreviveu às quatro
falhas.

## O main

```python
if __name__ == "__main__":
    test_error_types()
```
