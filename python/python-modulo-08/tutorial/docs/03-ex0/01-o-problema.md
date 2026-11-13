---
sidebar_position: 1
title: O problema
---

# O problema

Antes de instalar qualquer biblioteca, é preciso saber **em qual Python** ela vai cair: no global,
que o sistema inteiro usa, ou num ambiente virtual do projeto. O exercício 0 é um programa que
responde a essa pergunta sozinho: roda, descobre onde está e diz o que fazer.

## O que o enunciado pede

Um arquivo `ex0/construct.py` (o "construto" do filme é o espaço de treino isolado, aqui o
ambiente virtual) que:

1. **detecta** se está rodando dentro de um ambiente virtual;
2. **mostra informações** sobre o Python em uso;
3. se não há ambiente virtual, **ensina** a criar e ativar um;
4. **mostra a diferença** entre o lugar onde os pacotes são instalados no Python global e num
   ambiente virtual.

O programa precisa funcionar dentro e fora de um ambiente virtual, com uma saída diferente para
cada caso. Só pode usar os módulos `sys`, `os` e `site`, e a função `print`.

O enunciado também avisa: o ambiente virtual **não** vai para o repositório. Quem baixa o
projeto cria um novo, com os comandos que o próprio programa ensina.

## As saídas do enunciado

Fora de um ambiente virtual:

```console
$> python construct.py

MATRIX STATUS: You're still plugged in

Current Python: /usr/bin/python3.11
Virtual Environment: None detected

WARNING: You're in the global environment!
The machines can see everything you install.

To enter the construct, run:
python -m venv matrix_env
source matrix_env/bin/activate # On Unix
matrix_env\Scripts\activate  # On Windows

Then run this program again.
```

Dentro do ambiente virtual `matrix_env`:

```console
$> python construct.py

MATRIX STATUS: Welcome to the construct

Current Python: /path/to/matrix_env/bin/python
Virtual Environment: matrix_env
Environment Path: /path/to/matrix_env

SUCCESS: You're in an isolated environment!
Safe to install packages without affecting
the global system.

Package installation path:
/path/to/matrix_env/lib/python3.11/site-packages
```

- a linha `$> python construct.py` é o comando digitado; a saída do programa começa logo abaixo,
  com uma **linha vazia**;
- `/usr/bin/python3.11` é o Python global da máquina de quem escreveu o enunciado, e
  `/path/to/` ("caminho até") está no lugar da pasta onde fica o `matrix_env`. Os dois mudam em
  cada máquina, e o `3.11` muda com a versão do Python;
- as três linhas depois de `To enter the construct, run:` são os comandos que criam e ativam o
  ambiente. No Windows, o ativador fica em `matrix_env\Scripts\activate`; na linha do Windows há
  **dois** espaços antes do `#`, e na do Unix, um.

O enunciado roda `python`, e não `python3`. Dentro de um ambiente virtual os dois nomes existem e
são o mesmo programa; fora dele, muitos sistemas só têm `python3`, e é ele que o tutorial usa.

## Os testes pedidos

O enunciado manda rodar o programa fora do venv e depois dentro de um venv novo, criado e
ativado com os comandos que o próprio programa sugere:

```console
$> python3 construct.py
# Should detect no virtual environment and provide instructions
```

```console
$> python3 -m venv matrix_env
$> source matrix_env/bin/activate
(matrix_env) $> python3 construct.py
# Should detect virtual environment and show details
```

O `(matrix_env)` no começo da linha é o *prompt* do terminal com o ambiente ativado
([Ativar e desativar](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar)).
A página [Rodar e conferir](./07-rodar-e-conferir.md) faz os dois testes e mais um: o Python do
venv chamado pelo caminho, sem ativar nada.
