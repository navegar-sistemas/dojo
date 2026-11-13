---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

Crie `ex0/ft_ancient_text.py` com o conteúdo abaixo, que junta os pedaços das páginas anteriores:

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
    if len(sys.argv) != 2 or not sys.argv[1].isprintable():
        print(f"Usage: {sys.argv[0]} <file>")
        return
    print("=== Cyber Archives Recovery ===")
    recover_archive(sys.argv[1])


if __name__ == "__main__":
    main()
```

O botão de copiar, no canto do bloco, não leva a quebra de linha do fim do arquivo. Depois de
colar, se o cursor ficar no fim da última linha, `    main()`, aperte Enter uma vez antes de salvar;
alguns editores já fazem isso ao salvar. Sem essa quebra, o flake8 acusa
`W292 no newline at end of file` ("sem quebra de linha no fim do arquivo"); com mais de uma, acusa
`W391 blank line at end of file` ("linha em branco no fim do arquivo").

O que o arquivo usa, todos autorizados: `import sys`, `sys.argv`, `len()`, `open()`,
`import typing`, `typing.IO`, `read()`, `close()` e `print()`, além do método `isprintable()` de
`str` e das próprias funções.
