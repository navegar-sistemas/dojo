---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

```python title="ex0/ft_ancient_text.py"
import sys
import typing


def display(content: str) -> None:
    print("---\n")
    print(content)
    print("---")


def recover_archive(file_name: str) -> None:
    print(f"Accessing file '{file_name}'")
    try:
        file: typing.IO[str] = open(file_name)
    except OSError as error:
        print(f"Error opening file '{file_name}': {error}")
        return
    try:
        display(file.read())
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{file_name}': {error}")
    finally:
        file.close()
        print(f"File '{file_name}' closed.")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery ===")
    recover_archive(sys.argv[1])


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `import sys`, `sys.argv`, `len()`, `open()`,
`import typing`, `typing.IO`, `read()`, `close()` e `print()`, além das próprias funções.
