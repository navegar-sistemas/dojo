---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O enunciado exige que o código passe por duas ferramentas, o **flake8** e o **mypy**. Elas não vêm
com o Python: são instaladas com o `pip`, o instalador de bibliotecas do Python.

Instalar com `pip` direto no Python do sistema mistura essas ferramentas com tudo o que o sistema
usa, e muitos sistemas Linux recusam, com o erro `externally-managed-environment` ("ambiente
gerenciado pelo sistema"). O jeito comum é criar um **ambiente virtual** (*virtual environment*, ou
**venv**): uma pasta com um Python próprio e as bibliotecas dele, só para este projeto.

## Criar o venv

Na pasta `data-archivist`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, uma ferramenta que já vem instalada com ele e
  cria ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e faz
  o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

No Debian e no Ubuntu, o `venv` vem num pacote à parte, o `python3-venv`, que costuma faltar mesmo
com o `python3` instalado. Sem ele, o comando responde
`The virtual environment was not created successfully` e, logo depois, manda instalar o pacote.
Instale-o (o `sudo` e o `apt` estão em [O Python](./01-o-python.md)) e crie o venv de novo:

```bash
sudo apt install python3-venv
python3 -m venv .venv
```

## Instalar o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o `pip`
  instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade pip` atualiza também o próprio `pip`, na mesma instalação das duas ferramentas, o que
  evita o aviso de "nova versão disponível" no fim da saída;
- `flake8 mypy` são as duas ferramentas.

A última linha da saída lista o que foi instalado, começando por `Successfully installed`. As
ferramentas ficam em `.venv/bin/`:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

```text
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.12.3 on
Linux
mypy 2.4.1 (compiled: yes)
```

Os números podem ser outros na sua máquina, e a última palavra da primeira saída é o nome do sistema
(`Linux`, `Darwin` no macOS). O flake8 quebra essa primeira saída conforme a largura do terminal:
numa janela larga, ela sai numa linha só. O que importa é que os dois comandos respondem.

Os programas dos exercícios não precisam do venv: eles só usam o que vem com o Python e são rodados
com `python3`. O venv existe só para as duas ferramentas.
