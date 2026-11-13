---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório é avaliado.
Só os arquivos pedidos precisam ir: os seis `.py` da raiz e os `.py` das pastas `ex3` e `ex4`. A
pasta `.venv`, a pasta `experimentos`, as pastas `__pycache__`, que o Python cria ao importar um
módulo, e a pasta `.mypy_cache`, que o mypy cria, ficam de fora.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `code-nexus`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os
arquivos `.py`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
cp code-nexus/*.py entrega/
mkdir -p entrega/ex3 entrega/ex4
cp code-nexus/ex3/*.py entrega/ex3/
cp code-nexus/ex4/*.py entrega/ex4/
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço recebido e, nos três `cp`, troque `code-nexus`
pelo nome da sua pasta do projeto, se for outro. O `git clone` baixa o repositório; o
primeiro `cp` copia os seis arquivos da raiz; o `mkdir -p` cria as pastas dos pacotes (o `-p` não
reclama se elas já existirem); os dois últimos `cp` copiam só os `.py` de cada pacote, deixando
as pastas `__pycache__` para trás.

## Registrar e enviar

```bash
git add *.py ex3 ex4
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   battle.py
	new file:   capacitor.py
	new file:   data_pipeline.py
	new file:   data_processor.py
	new file:   data_stream.py
	new file:   ex3/__init__.py
	new file:   ex3/capability.py
	new file:   ex3/creature.py
	new file:   ex3/factory.py
	new file:   ex3/flame.py
	new file:   ex3/transform.py
	new file:   ex4/__init__.py
	new file:   ex4/aggressive.py
	new file:   ex4/normal.py
	new file:   ex4/strategy.py
	new file:   tournament.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os dezesseis arquivos. O
resto pode variar: esta é a saída de um repositório de entrega vazio (`No commits yet`, "nenhum
registro ainda"); num repositório que já tem registros, essa linha não aparece. A primeira
linha mostra o **ramo** (*branch*), a linha de histórico em que os registros entram; o nome
padrão pode ser `main` ou `master`.

O `git commit` grava o nome e o e-mail do autor em cada registro. Antes do primeiro, configure os
dois dentro do repositório de entrega, com o seu nome e o seu e-mail (sem `--global`, a
configuração vale só para este repositório):

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

Sem essa configuração, o `git` não necessariamente recusa o registro: no macOS, por exemplo, ele
monta um nome e um e-mail a partir do usuário e do nome do computador, grava o registro com eles
e só avisa com a mensagem `Your name and email address were configured automatically based on
your username and hostname` ("seu nome e e-mail foram configurados automaticamente a partir do
seu usuário e do nome do computador"). Se essa mensagem aparecer, o registro saiu com a
identidade errada: configure os dois valores e corrija o registro com
`git commit --amend --reset-author`, como a própria mensagem indica.

```bash
git commit -m "Add exercises 0 to 4"
```

```text
[main (root-commit) ed12881] Add exercises 0 to 4
 16 files changed, 896 insertions(+)
 create mode 100644 battle.py
 create mode 100644 capacitor.py
 create mode 100644 data_pipeline.py
 create mode 100644 data_processor.py
 create mode 100644 data_stream.py
 create mode 100644 ex3/__init__.py
 create mode 100644 ex3/capability.py
 create mode 100644 ex3/creature.py
 create mode 100644 ex3/factory.py
 create mode 100644 ex3/flame.py
 create mode 100644 ex3/transform.py
 create mode 100644 ex4/__init__.py
 create mode 100644 ex4/aggressive.py
 create mode 100644 ex4/normal.py
 create mode 100644 ex4/strategy.py
 create mode 100644 tournament.py
```

O código depois de `root-commit` identifica o registro e muda a cada vez; `root-commit` só aparece
no primeiro registro do repositório. Depois, envie:

```bash
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório de entrega.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode um programa nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls ex3 ex4
python3 tournament.py
```

As pastas `ex3` e `ex4` aparecem com os seus arquivos `.py`, e o torneio imprime a mesma saída
que na pasta do projeto: os pacotes foram enviados inteiros. Depois, a pasta `conferencia` pode
ser apagada (`cd .. && rm -rf conferencia`).
