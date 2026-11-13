---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório é avaliado.
Vão os três programas de teste, na raiz do repositório, e as três pastas de pacote, com os seus
arquivos `.py`. A pasta `.venv`, a pasta `experimentos`, as pastas `__pycache__` e a pasta
`.mypy_cache` ficam de fora.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `datadeck`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os arquivos
`.py`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
cp datadeck/battle.py datadeck/capacitor.py datadeck/tournament.py entrega/
for ex in ex0 ex1 ex2; do
    mkdir -p "entrega/$ex"
    cp "datadeck/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço recebido. O `git clone` baixa o repositório; o
primeiro `cp` copia os três programas para a raiz da `entrega`; o `for` cria cada pasta de
exercício dentro dela (o `-p` do `mkdir` não reclama se a pasta já existir) e copia os arquivos
`.py` do pacote. O `*.py` deixa a `__pycache__` para trás.

## Registrar e enviar

```bash
git add battle.py capacitor.py tournament.py ex0 ex1 ex2
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   battle.py
	new file:   capacitor.py
	new file:   ex0/__init__.py
	new file:   ex0/creature.py
	new file:   ex0/factory.py
	new file:   ex1/__init__.py
	new file:   ex1/capability.py
	new file:   ex1/creature.py
	new file:   ex1/factory.py
	new file:   ex2/__init__.py
	new file:   ex2/strategy.py
	new file:   tournament.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem os doze arquivos. O resto pode
variar: esta é a saída de um repositório de entrega vazio (`No commits yet`, "nenhum registro
ainda"); num repositório que já tem registros, essa linha não aparece. A primeira linha mostra o
**ramo** (*branch*), a linha de histórico em que os registros entram; o nome padrão pode ser
`main` ou `master`.

O `git commit` precisa saber quem é o autor. Se ele pedir (`Please tell me who you are`),
informe o seu nome e e-mail uma vez, e rode o `git commit` de novo:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email"
```

```bash
git commit -m "Add exercises 0 to 2"
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
ls -1 *.py ex0 ex1 ex2
python3 tournament.py
```

Os doze arquivos aparecem, e o programa imprime a mesma saída que na pasta do projeto: os pacotes
foram junto, e os imports funcionam a partir da raiz. Depois, a pasta `conferencia` pode ser
apagada (`cd .. && rm -rf conferencia`).
