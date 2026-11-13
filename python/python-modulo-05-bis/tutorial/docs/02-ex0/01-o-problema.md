---
sidebar_position: 1
title: O problema
---

# O problema

Um projeto Python usa bibliotecas externas, e cada projeto pode precisar de uma versão diferente
da mesma biblioteca. Instaladas todas no Python do sistema, elas brigam entre si: atualizar a
biblioteca de um projeto quebra o outro, e ninguém sabe mais o que está instalado nem por quê. O
exercício 0 resolve isso em duas metades:

- **selar o laboratório:** trabalhar dentro de um **ambiente virtual**, uma pasta com um Python e
  bibliotecas só do projeto;
- **abastecer os reagentes:** declarar num arquivo quais bibliotecas o projeto usa, para que
  qualquer pessoa reproduza o mesmo ambiente com um comando. Isso é o **gerenciamento de
  dependências** (uma **dependência** é uma biblioteca de que o projeto precisa para rodar).

## O que o enunciado pede

Quatro arquivos na pasta `ex0/`. Os `import` permitidos são `os`, `sys`, `site` e `importlib`, que
vêm com o Python, e as bibliotecas externas `pandas` e `numpy`.

### Parte 1: `construct.py`

Um programa que:

- descobre se está rodando dentro de um ambiente virtual;
- mostra informações do Python em uso;
- se não houver ambiente virtual, ensina a criar um e a ativá-lo;
- mostra a diferença entre o lugar onde as bibliotecas são instaladas no ambiente global (o Python
  do sistema) e num ambiente virtual.

O programa precisa funcionar dentro e fora de um ambiente virtual, com uma saída claramente
diferente em cada caso. O ambiente virtual em si não é entregue: na avaliação, você pode precisar
criar um novo.

### Parte 2: `loading.py`, `requirements.txt` e `pyproject.toml`

- `requirements.txt` declara as dependências `pandas` e `numpy` para o **pip**;
- `pyproject.toml` declara as mesmas dependências para o **Poetry**, outro gerenciador;
- `loading.py` importa cada dependência e mostra a versão instalada, e mostra na saída a
  diferença entre o pip e o Poetry. Se faltar alguma, o programa não pode travar: mostra uma
  mensagem com o comando de instalação para os dois gerenciadores.

## A saída esperada de construct.py

Fora de um ambiente virtual:

```text

LABORATORY STATUS: You are working in the open

Current Python: /usr/bin/python3.11
Virtual Environment: None detected

WARNING: You are in the global environment!
Every reagent you install here leaks into the whole system.

To seal the laboratory, run:
python3 -m venv lab_env
source lab_env/bin/activate # On Unix
lab_env\Scripts\activate  # On Windows

Then run this program again.
```

Dentro do ambiente virtual `lab_env`:

```text

LABORATORY STATUS: The laboratory is sealed

Current Python: /path/to/lab_env/bin/python
Virtual Environment: lab_env
Environment Path: /path/to/lab_env

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting
the global system.

Reagent installation path:
/path/to/lab_env/lib/python3.11/site-packages
```

- as duas saídas começam com uma linha vazia;
- os caminhos dependem da máquina: `/path/to/` é o jeito do enunciado de dizer "a pasta onde o
  ambiente está", e o `python3.11` muda com a versão do Python;
- na linha do Windows há **dois** espaços antes do `#`, e na do Unix, um. É assim no enunciado.

## A saída esperada de loading.py

Com as duas bibliotecas instaladas:

```text

REAGENT STATUS: Loading reagents...

Checking dependencies:
[OK] pandas (2.1.0) - Data manipulation ready
[OK] numpy (1.25.0) - Numerical computation ready

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

All reagents present and accounted for.
```

Os números entre parênteses são as versões instaladas, e mudam com o tempo. As três linhas
depois de `pip vs Poetry:` começam com dois espaços. Sem as bibliotecas, o enunciado não mostra a
saída: pede só que ela mostre o que falta e como instalar.

## O roteiro de testes do enunciado

| Situação | Comandos |
|---|---|
| fora de um ambiente virtual | `python3 ex0/construct.py` |
| dentro de um ambiente virtual | `python3 -m venv lab_env`, `source lab_env/bin/activate`, `python3 ex0/construct.py` |
| sem as bibliotecas | `python3 ex0/loading.py` |
| instalando com o pip | `pip install -r ex0/requirements.txt`, `python3 ex0/loading.py` |
| instalando com o Poetry | `poetry install`, `poetry run python ex0/loading.py` |

Os dois comandos do Poetry precisam de um ajuste, porque o
`pyproject.toml` fica em `ex0/` e não na pasta de onde os comandos são rodados
([Instalar com o Poetry](./11-instalar-com-poetry.md)).
