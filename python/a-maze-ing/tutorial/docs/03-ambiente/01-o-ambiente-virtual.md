---
sidebar_position: 1
title: O ambiente virtual
---

# O ambiente virtual

## O que é

Um **ambiente virtual** é uma pasta com um Python próprio e um `pip` próprio. O que se instala
nele fica só nele: não mexe no Python do sistema nem nos outros projetos da máquina.

O projeto usa uma pasta `.venv` na raiz:

```bash
python3 -m venv .venv
```

Depois desse comando, `.venv/bin/python` é um interpretador separado. Tudo o que o projeto
precisa (flake8, mypy e build) é instalado com ele:

```bash
.venv/bin/python -m pip install flake8 mypy build
```

## Por que um ambiente virtual

- **Isolamento**: a máquina do avaliador pode ter outro flake8 ou outro mypy, ou nenhum. Com o
  `.venv`, as ferramentas são as que o projeto escolheu.
- **Nada global**: não é preciso `sudo` nem `pip install --user`, e apagar a pasta `.venv`
  desfaz tudo.
- **O subject recomenda**: o capítulo III sugere `venv` ou `conda` para isolar dependências.

## Sem `activate`

O jeito comum de usar um ambiente virtual é "ativá-lo" (`source .venv/bin/activate`), o que
troca o `python` do terminal atual. O projeto não depende disso: o `Makefile` chama
`.venv/bin/python` pelo caminho completo.

Assim, `make lint` usa sempre o Python do `.venv`, esteja o terminal ativado ou não. E se o
`.venv` ainda não existe, o comando falha na hora:

```text
make: .venv/bin/python: No such file or directory
```

Não há recurso silencioso ao Python do sistema. Um recurso desses rodaria, sem avisar, outra
versão das ferramentas, e um erro de lint poderia aparecer numa máquina e sumir na outra.

## O que o programa precisa

O programa em si **não tem dependência**: o `mazegen` e o `amazeing` só usam a biblioteca padrão
do Python. As três ferramentas do `.venv` servem para verificar e empacotar o código:

| Ferramenta | Usada por |
|---|---|
| `flake8` | `make lint` e `make lint-strict` |
| `mypy` | `make lint` e `make lint-strict` |
| `build` | `make build` |

## Começando a pasta do projeto

Crie a raiz do projeto, vazia, e entre nela:

```bash
mkdir a-maze-ing
cd a-maze-ing
```

O `.venv` não é criado à mão: a regra `install` do `Makefile`, na próxima página, faz isso.
