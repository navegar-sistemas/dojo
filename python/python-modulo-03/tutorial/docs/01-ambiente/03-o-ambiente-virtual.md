---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O código precisa passar por duas ferramentas, o **flake8** e o **mypy**. Elas não vêm com o
Python: são instaladas com o `pip`, o instalador de bibliotecas do Python.

Instalar com `pip` direto no Python do sistema mistura essas ferramentas com tudo o que o sistema
usa, e muitos sistemas Linux nem deixam. O jeito comum é criar um **ambiente virtual** (*virtual
environment*, ou **venv**): uma pasta com um Python próprio do projeto e as bibliotecas dele,
separadas das do sistema.

## Criar o venv

No Debian e no Ubuntu, o módulo que cria ambientes virtuais vem num pacote à parte:

```bash
sudo apt install python3-venv
```

Nas outras distribuições e no macOS, ele já vem com o Python. Na pasta `data-quest`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` roda o módulo `venv`, que vem com o Python e cria ambientes virtuais;
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e
  faz o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

## Instalar o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv; o `pip` que ele roda instala as bibliotecas
  dentro da pasta `.venv`;
- `--upgrade` instala a versão mais nova de cada pacote da lista;
- `pip flake8 mypy` é a lista: o próprio `pip`, atualizado para evitar o aviso de "nova versão
  disponível", e as duas ferramentas.

A última linha da saída lista o que foi instalado, começando por `Successfully installed`. As
ferramentas ficam em `.venv/bin/`:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

```text
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.14.5 on
Linux
mypy 2.4.1 (compiled: yes)
```

Os números podem ser outros na sua máquina, e a última palavra da primeira saída é o nome do
sistema (`Linux`, ou `Darwin` no macOS).

Os programas dos exercícios não precisam do venv: eles só usam o que vem com o Python e são
rodados com `python3`. O venv existe só para as duas ferramentas.
