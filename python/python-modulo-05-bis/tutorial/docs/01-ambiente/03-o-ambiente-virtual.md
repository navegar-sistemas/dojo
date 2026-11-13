---
sidebar_position: 3
title: O ambiente virtual
---

# O ambiente virtual

O enunciado exige que o código passe por duas ferramentas, o **flake8** e o **mypy**. Elas não
vêm com o Python: são instaladas com o **pip**, o instalador de bibliotecas do Python.

Instalar com `pip` direto no Python do sistema mistura essas ferramentas com tudo o que o sistema
usa, e muitos sistemas Linux recusam, com o erro `externally-managed-environment` ("ambiente
gerenciado pelo sistema"). O jeito comum é criar um **ambiente virtual** (*virtual environment*,
ou **venv**): uma pasta com um Python próprio e as bibliotecas dele, só para este projeto. O
exercício 0 inteiro é sobre ambientes virtuais e mostra como eles funcionam por dentro
([O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md)); por enquanto,
basta um ambiente para as ferramentas.

## Criar o venv das ferramentas

Na pasta `the-codex`:

```bash
python3 -m venv .venv
```

- `python3 -m venv` pede ao Python que rode o `venv`, uma ferramenta que já vem instalada com
  ele e cria ambientes virtuais. O `-m` quer dizer "rode esta ferramenta do Python";
- `.venv` é o nome da pasta criada. O ponto no começo é o costume para pastas de ferramentas, e
  faz o `ls` comum escondê-la.

O comando não imprime nada quando dá certo.

No Debian e no Ubuntu, a parte do `python3` que cria ambientes virtuais vem num pacote
separado, o `python3-venv`. Sem ele, o comando acima falha com uma mensagem que
fala em `ensurepip` e manda instalar esse pacote. Nesse caso, instale-o (a mensagem pode pedir o
nome com a versão, como `python3.12-venv`; use o nome que ela mostrar), apague a pasta criada pela
metade e crie o venv de novo:

```bash
sudo apt install python3-venv
rm -rf .venv
python3 -m venv .venv
```

`rm -rf .venv` apaga a pasta `.venv` e tudo o que está dentro dela.

## Instalar o flake8 e o mypy

```bash
.venv/bin/python -m pip install --upgrade pip flake8 mypy
```

- `.venv/bin/python` é o Python **de dentro** do venv. O `-m pip` roda o `pip` com ele, e o
  `pip` instala as bibliotecas dentro da pasta `.venv`;
- `--upgrade pip` atualiza também o próprio `pip`, o que evita o aviso de "nova
  versão disponível" no fim da saída;
- `flake8 mypy` são as duas ferramentas.

A última linha da saída lista o que foi instalado, começando por `Successfully installed`. As
ferramentas ficam em `.venv/bin/`:

```bash
.venv/bin/flake8 --version
.venv/bin/mypy --version
```

```text
7.5.0 (mccabe: 0.7.0, pycodestyle: 2.15.0, pyflakes: 4.1.0) CPython 3.15.2 on
Darwin
mypy 2.4.1 (compiled: yes)
```

Os números podem ser outros na sua máquina, e a última palavra da primeira saída é o nome do
sistema (`Linux`, `Darwin` no macOS). O flake8 quebra essa saída conforme a largura do terminal:
num terminal de 80 colunas ela ocupa as duas linhas de cima, num mais largo cabe numa só, e num
mais estreito a quebra cai em outro ponto. O que importa é que os dois comandos respondem.

O tutorial chama as ferramentas sempre pelo caminho, `.venv/bin/flake8` e `.venv/bin/mypy`, e
nunca "ativa" este venv (ativar é assunto do exercício 0). Assim, elas funcionam do mesmo jeito
em qualquer momento, com ou sem o ambiente do laboratório ativado.
