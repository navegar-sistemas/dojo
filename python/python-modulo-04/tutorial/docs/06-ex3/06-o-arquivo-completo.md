---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

```python title="ex3/ft_vault_security.py"
def secure_archive(file_name: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "read":
            with open(file_name) as file:
                return (True, file.read())
        if action == "write":
            with open(file_name, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
    except (OSError, UnicodeDecodeError) as error:
        return (False, str(error))
    return (False, f"Unknown action '{action}'")


def main() -> None:
    print("=== Cyber Archives Security ===")
    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/sudoers"))
    print("\nUsing 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)
    print("\nUsing 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_archive.txt", "write", result[1]))


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `open()`, `read()`, `write()` e `print()`, além do
construtor `str()` e da própria função. Nenhum `import`, e o `with` aparece só neste exercício.
