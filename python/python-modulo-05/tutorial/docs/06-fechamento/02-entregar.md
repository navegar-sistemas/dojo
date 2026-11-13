---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório é avaliado.
Só os três arquivos pedidos precisam ir; a pasta `.venv`, a pasta `experimentos`, as pastas
`__pycache__`, que o Python cria ao importar um arquivo, e a pasta `.mypy_cache`, que o mypy
cria, ficam de fora.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `code-nexus`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os
arquivos `.py` de cada exercício:

```bash
cd ..
git clone <endereço-do-repositório> entrega
for ex in ex0 ex1 ex2; do
    mkdir -p "entrega/$ex"
    cp "code-nexus/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço recebido. O `git clone` baixa o repositório; o
`for` cria cada pasta de exercício dentro de `entrega` (o `-p` do `mkdir` não reclama se ela já
existir) e copia para ela os arquivos `.py` com `cp`.

## Registrar e enviar

```bash
git add ex0 ex1 ex2
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   ex0/data_processor.py
	new file:   ex1/data_stream.py
	new file:   ex2/data_pipeline.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os três arquivos. O
resto pode variar: esta é a saída de um repositório de entrega vazio (`No commits yet`, "nenhum
registro ainda"); num repositório que já tem registros, essa linha não aparece. A primeira
linha mostra o **ramo** (*branch*), a linha de histórico em que os registros entram; o nome
padrão pode ser `main` ou `master`.

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
ls ex0 ex1 ex2
python3 ex2/data_pipeline.py
```

Os três arquivos aparecem, e o programa imprime a mesma saída que na pasta do projeto. Depois, a
pasta `conferencia` pode ser apagada (`cd .. && rm -rf conferencia`).
