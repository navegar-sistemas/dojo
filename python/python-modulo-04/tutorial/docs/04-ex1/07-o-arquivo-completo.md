---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

Crie `ex1/ft_archive_creation.py` com o conteúdo abaixo, que junta os pedaços das páginas
anteriores:

```python title="ex1/ft_archive_creation.py"
import sys
import typing


def display(content: str) -> None:
    print("---\n")
    print(content)
    print("---")


def recover_archive(file_name: str) -> str | None:
    print(f"Accessing file '{file_name}'")
    try:
        file: typing.IO[str] = open(file_name)
    except OSError as error:
        print(f"Error opening file '{file_name}': {error}")
        return None
    content: str | None = None
    try:
        content = file.read()
        display(content)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{file_name}': {error}")
    finally:
        file.close()
        print(f"File '{file_name}' closed.")
    return content


def transform(content: str) -> str:
    result = ""
    for line in content.splitlines():
        result += line + "#\n"
    return result


def ask_file_name() -> str:
    try:
        return input("Enter new file name (or empty): ")
    except (EOFError, KeyboardInterrupt, UnicodeDecodeError):
        print()
        return ""


def save_archive(file_name: str, content: str) -> bool:
    try:
        file: typing.IO[str] = open(file_name, "w")
    except (OSError, ValueError) as error:
        print(f"Error opening file '{file_name}': {error}")
        return False
    try:
        try:
            file.write(content)
        finally:
            file.close()
    except OSError as error:
        print(f"Error writing file '{file_name}': {error}")
        return False
    return True


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isprintable():
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery & Preservation ===")
    content = recover_archive(sys.argv[1])
    if content is None:
        return
    print("\nTransform data:")
    new_content = transform(content)
    display(new_content)
    file_name = ask_file_name()
    if file_name == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{file_name}'")
    if save_archive(file_name, new_content):
        print(f"Data saved in file '{file_name}'.")
    else:
        print("Data not saved.")


if __name__ == "__main__":
    main()
```

Depois de colar, confira a quebra de linha depois de `    main()`, como no [exercício
0](../03-ex0/05-o-arquivo-completo.md).

O que o arquivo usa, todos autorizados: `import sys`, `sys.argv`, `len()`, `open()`,
`import typing`, `typing.IO`, `read()`, `write()`, `close()`, `print()` e `input()`, além dos
métodos `splitlines()` e `isprintable()` de `str` e das próprias funções.
