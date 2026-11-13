---
sidebar_position: 4
title: Dentro do venv
---

# Dentro do venv

Dentro de um ambiente virtual, o programa confirma o isolamento e mostra qual é o ambiente. A
função entra depois de `show_outside`:

```python
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
```

- `sys.executable` é o Python do venv, como `/…/matrix_env/bin/python3`;
- `sys.prefix` é a pasta do ambiente, como `/…/matrix_env`: é o `Environment Path`;
- o nome do ambiente é a última parte desse caminho. `os.path.basename` devolve justamente a
  última parte de um caminho: `os.path.basename("/a/b/matrix_env")` dá `"matrix_env"`.

O nome sai do caminho, e não de um texto fixo: um venv criado com outro nome, como `.venv`,
aparece com o nome dele.

## Por que as mensagens dizem "isolado"

`SUCCESS: You're in an isolated environment!` não é só um enfeite: dentro do venv, o pip instala
no `site-packages` do ambiente, e o Python global continua igual. Apagar a pasta `matrix_env`
apaga tudo o que foi instalado nela, sem deixar resto nenhum no sistema. A
[próxima página](./05-onde-ficam-os-pacotes.md) mostra essa pasta na saída.
