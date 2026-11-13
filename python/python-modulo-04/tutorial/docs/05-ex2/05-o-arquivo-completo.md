---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

```python title="ex2/ft_stream_management.py"
import sys
import typing


def report_error(message: str) -> None:
    sys.stdout.flush()
    print(f"[STDERR] {message}", file=sys.stderr)


def display(content: str) -> None:
    print("---\n")
    print(content)
    print("---")


def recover_archive(file_name: str) -> str | None:
    print(f"Accessing file '{file_name}'")
    try:
        file: typing.IO[str] = open(file_name)
    except OSError as error:
        report_error(f"Error opening file '{file_name}': {error}")
        return None
    content: str | None = None
    try:
        content = file.read()
        display(content)
    except (OSError, UnicodeDecodeError) as error:
        report_error(f"Error reading file '{file_name}': {error}")
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
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    try:
        line = sys.stdin.readline()
    except KeyboardInterrupt:
        line = ""
    if line == "":
        print()
    return line.rstrip("\n")


def save_archive(file_name: str, content: str) -> bool:
    try:
        file: typing.IO[str] = open(file_name, "w")
    except OSError as error:
        report_error(f"Error opening file '{file_name}': {error}")
        return False
    try:
        try:
            file.write(content)
        finally:
            file.close()
    except OSError as error:
        report_error(f"Error writing file '{file_name}': {error}")
        return False
    return True


def main() -> None:
    if len(sys.argv) != 2:
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

O que o arquivo usa, todos autorizados: `import sys`, `sys.argv`, `sys.stdin`, `sys.stdout`,
`sys.stderr`, `len()`, `open()`, `import typing`, `typing.IO`, `read()`, `readline()`, `write()`,
`flush()`, `close()` e `print()`, além dos métodos `splitlines()` e `rstrip()` de `str` e das
próprias funções. `input()` não aparece.
