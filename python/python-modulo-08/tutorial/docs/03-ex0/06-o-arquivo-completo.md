---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

```python title="ex0/construct.py"
import os
import site
import sys


def inside_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def show_outside() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")


def show_package_path() -> None:
    print()
    print("Package installation path:")
    print(site.getsitepackages()[0])


def main() -> None:
    print()
    if inside_virtual_env():
        show_inside()
    else:
        show_outside()
    show_package_path()


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: os módulos `sys` (`prefix`, `base_prefix`,
`executable`), `os` (`path.basename`) e `site` (`getsitepackages`), e a função `print`.
