---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O código precisa passar por duas ferramentas, o **flake8** e o **mypy**. Elas não vêm com o Python:
são instaladas com o `pip`, o instalador de bibliotecas do Python.

Instalar com `pip` direto no Python do sistema mistura essas ferramentas com tudo o que o sistema
usa, e muitos sistemas Linux nem deixam. O jeito comum é criar um **ambiente virtual** (*virtual
environment*, ou **venv**): uma pasta que aponta para o Python instalado e guarda bibliotecas
próprias, só deste projeto.

O venv é escolha do projeto: funciona igual em qualquer Linux e no macOS, sem `sudo`. Outra opção
seriam os pacotes da distribuição (no Debian e no Ubuntu, `sudo apt install flake8 mypy`), em
versões que variam de sistema para sistema.

## Criar o venv

Na pasta `code-cultivation`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, uma ferramenta que já vem com ele e cria
  ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e
  faz o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

## Instalar o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o
  `pip` instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade` instala a versão mais nova de cada pacote listado, inclusive do próprio `pip`, o
  que evita o aviso de "nova versão disponível";
- `flake8 mypy` são as duas ferramentas.

A última linha da saída lista o que foi instalado, começando por `Successfully installed`. As
ferramentas ficam em `.venv/bin/`, e cada uma responde com a sua versão:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

O flake8 imprime o número da versão dele, das peças que ele usa e do Python; o mypy imprime
`mypy` seguido do número da versão. Os números variam de máquina para máquina; o que importa é
que os dois comandos respondem.

Os programas dos exercícios não precisam do venv: eles só usam o que vem com o Python e são
rodados com `python3`. O venv existe só para as duas ferramentas.
