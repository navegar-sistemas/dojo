---
sidebar_position: 5
title: construct.py completo
---

# construct.py completo

```python title="ex0/construct.py"
import os
import site
import sys


def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def show_open_laboratory() -> None:
    print("LABORATORY STATUS: You are working in the open")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You are in the global environment!")
    print("Every reagent you install here leaks into the whole system.")
    print()
    print("To seal the laboratory, run:")
    print("python3 -m venv lab_env")
    print("source lab_env/bin/activate # On Unix")
    print("lab_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")


def show_sealed_laboratory() -> None:
    print("LABORATORY STATUS: The laboratory is sealed")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You are working in an isolated environment!")
    print("Safe to install reagents without affecting")
    print("the global system.")
    print()
    print("Reagent installation path:")
    print(site.getsitepackages()[0])


def main() -> None:
    print()
    if in_virtual_env():
        show_sealed_laboratory()
    else:
        show_open_laboratory()


if __name__ == "__main__":
    main()
```

## Fora do laboratório

Com o `lab_env` **desativado** (se o prompt mostra `(lab_env)`, rode `deactivate` antes):

```bash
python3 ex0/construct.py
```

```text

LABORATORY STATUS: You are working in the open

Current Python: /path/to/python3.15
Virtual Environment: None detected

WARNING: You are in the global environment!
Every reagent you install here leaks into the whole system.

To seal the laboratory, run:
python3 -m venv lab_env
source lab_env/bin/activate # On Unix
lab_env\Scripts\activate  # On Windows

Then run this program again.
```

A linha `Current Python` mostra o caminho completo do Python global, que muda de máquina para
máquina; `/path/to/` está no lugar das pastas. Num Linux com o Python do sistema, a linha costuma
ser `Current Python: /usr/bin/python3`, e o enunciado mostra `/usr/bin/python3.11`. O resto é
igual ao enunciado, linha por linha.

## Dentro do laboratório

O `lab_env` já existe ([O ambiente virtual por dentro](./02-o-ambiente-virtual-por-dentro.md)).
Ative-o e rode o mesmo comando:

```bash
source lab_env/bin/activate
python3 ex0/construct.py
```

```text

LABORATORY STATUS: The laboratory is sealed

Current Python: /path/to/the-codex/lab_env/bin/python3
Virtual Environment: lab_env
Environment Path: /path/to/the-codex/lab_env

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting
the global system.

Reagent installation path:
/path/to/the-codex/lab_env/lib/python3.15/site-packages
```

- `/path/to/the-codex` está no lugar do caminho da pasta do projeto, e o `python3.15` muda com a
  versão do Python;
- `Current Python` termina em `bin/python3`, e não em `bin/python` como no enunciado, porque o
  comando digitado foi `python3`: `sys.executable` mostra o nome pelo qual o Python foi chamado.
  Com `python ex0/construct.py` (o ambiente ativado também tem o nome `python`), a linha termina
  em `bin/python`.

O mesmo arquivo, o mesmo comando, duas saídas: o que mudou foi só qual Python o nome `python3`
chamou. Deixe o `lab_env` ativado para a parte 2.
