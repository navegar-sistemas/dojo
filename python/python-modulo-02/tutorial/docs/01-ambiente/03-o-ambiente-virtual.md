---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O enunciado exige que o código passe por duas ferramentas, o **flake8** e o **mypy**. Elas não
vêm com o Python: são instaladas com o `pip`, o instalador de bibliotecas do Python.

Instalar com `pip` direto no Python do sistema mistura essas ferramentas com tudo o que o sistema
usa, e muitos sistemas Linux nem deixam. O jeito comum é criar um **ambiente virtual** (*virtual
environment*, ou **venv**): uma pasta com as bibliotecas só deste projeto e um comando `python`
próprio, que usa o Python já instalado mas enxerga só essas bibliotecas.

## Criar o venv

Na pasta `garden-guardian`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, uma ferramenta que já vem instalada com
  ele e cria ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e
  faz o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

## Instalar o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o
  `pip` instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade pip` atualiza o próprio `pip` antes, o que evita o aviso de "nova versão
  disponível";
- `flake8 mypy` são as duas ferramentas.

A última linha da saída lista o que foi instalado, começando por `Successfully installed`. As
ferramentas ficam em `.venv/bin/`:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

```text
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.14.5 on
Darwin
mypy 2.4.1 (compiled: yes)
```

Os números podem ser outros na sua máquina, e a última palavra da primeira saída é o nome do
sistema (`Linux`, `Darwin` no macOS). O que importa é que os dois comandos respondem.

Os programas dos exercícios não precisam do venv: eles só usam o que vem com o Python e são
rodados com `python3`. O venv existe só para as duas ferramentas.
