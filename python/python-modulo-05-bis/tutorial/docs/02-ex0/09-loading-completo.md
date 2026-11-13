---
sidebar_position: 9
title: loading.py completo
---

# loading.py completo

```python title="ex0/loading.py"
import importlib

REAGENTS = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
]


def installed_version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return str(module.__version__)


def check_reagents() -> list[str]:
    missing: list[str] = []
    for name, purpose in REAGENTS:
        version = installed_version(name)
        if version is None:
            print(f"[MISSING] {name} - {purpose} unavailable")
            missing.append(name)
        else:
            print(f"[OK] {name} ({version}) - {purpose} ready")
    return missing


def explain_managers() -> None:
    print("pip vs Poetry:")
    print("  requirements.txt declares what to install;"
          " pip resolves it at install time.")
    print("  pyproject.toml declares the same constraints,"
          " and Poetry pins the resolved")
    print("  versions in poetry.lock so every install is identical.")


def explain_install(missing: list[str]) -> None:
    print(f"Missing reagents: {', '.join(missing)}")
    print("Install them with pip:")
    print("  pip install -r ex0/requirements.txt")
    print("Or with Poetry:")
    print("  poetry -P ex0 install")
    print("  poetry -P ex0 run python ex0/loading.py")


def main() -> None:
    print()
    print("REAGENT STATUS: Loading reagents...")
    print()
    print("Checking dependencies:")
    missing = check_reagents()
    print()
    explain_managers()
    print()
    if missing:
        explain_install(missing)
    else:
        print("All reagents present and accounted for.")


if __name__ == "__main__":
    main()
```

O que o arquivo usa: o módulo `importlib`, permitido no exercício 0, e as funções embutidas
`print` e `str`. A `pandas` e o `numpy` são importados pelo nome, com `importlib.import_module`.

A pasta `ex0` fica com os quatro arquivos do enunciado:

```bash
ls -1 ex0
```

```text
construct.py
loading.py
pyproject.toml
requirements.txt
```
