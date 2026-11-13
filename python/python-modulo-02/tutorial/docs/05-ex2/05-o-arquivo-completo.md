---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

Crie `ex2/ft_different_errors.py` com o conteúdo completo:

```python title="ex2/ft_different_errors.py"
def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        # mypy reports this line on purpose: it is the TypeError being shown
        "abc" + 5


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


if __name__ == "__main__":
    test_error_types()
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva. Os avisos do flake8 sobre o fim
do arquivo estão em [O fim do arquivo](../03-ex0/06-rodar-e-conferir.md#o-fim-do-arquivo).

As funções chamadas são `int()`, `open()` e `print()`, as três autorizadas, e as do próprio
arquivo.
