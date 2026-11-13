---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório é avaliado.
Vão os oito arquivos da tabela de [Conferir tudo](./01-conferir-tudo.md#os-arquivos), e nada
mais.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `the-matrix`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os
arquivos pedidos:

```bash
cd ..
git clone <endereço-do-repositório> entrega
mkdir -p entrega/ex0 entrega/ex1 entrega/ex2
cp the-matrix/ex0/construct.py entrega/ex0/
cp the-matrix/ex1/loading.py the-matrix/ex1/requirements.txt the-matrix/ex1/pyproject.toml entrega/ex1/
cp the-matrix/ex2/oracle.py the-matrix/ex2/requirements.txt the-matrix/ex2/.env.example the-matrix/ex2/.gitignore entrega/ex2/
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço recebido. O `git clone` baixa o repositório; o
`mkdir -p` cria as pastas dos exercícios (o `-p` não reclama se elas já existirem), e cada `cp`
copia os arquivos listados para a pasta do fim da linha.

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
	new file:   ex0/construct.py
	new file:   ex1/loading.py
	new file:   ex1/pyproject.toml
	new file:   ex1/requirements.txt
	new file:   ex2/.env.example
	new file:   ex2/.gitignore
	new file:   ex2/oracle.py
	new file:   ex2/requirements.txt

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os oito arquivos. O resto
pode variar: esta é a saída de um repositório de entrega vazio (`No commits yet`, "nenhum
registro ainda"); num repositório que já tem registros, essa linha não aparece. A primeira linha
mostra o **ramo** (*branch*), a linha de histórico em que os registros entram; o nome padrão pode
ser `main` ou `master`.

## O .env nunca entra

O `.env` nem foi copiado. Mas, se um dia ele cair na pasta `ex2` do repositório, o `.gitignore`
entregue o protege. O Git confirma:

```bash
git check-ignore -v ex2/.env
```

```text
ex2/.gitignore:1:.env	ex2/.env
```

`git check-ignore` responde se um caminho seria ignorado, e o `-v` diz por quê: a regra da linha 1
do `ex2/.gitignore`, `.env`, cobre o caminho `ex2/.env`. Um `git add ex2` não o adicionaria.

## Enviar

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
parte e confira os arquivos:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls -A ex0 ex1 ex2
```

```text
ex0:
construct.py

ex1:
loading.py
pyproject.toml
requirements.txt

ex2:
.env.example
.gitignore
oracle.py
requirements.txt
```

Os oito arquivos estão lá, e nenhum ambiente nem `.env`. Para rodar os programas a partir de uma
cópia assim, os ambientes são recriados
([Recriar tudo a partir da entrega](./03-as-perguntas-do-enunciado.md#recriar-tudo-a-partir-da-entrega)).
Depois, a pasta `conferencia` pode ser apagada (`cd .. && rm -rf conferencia`).
