---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e o que conta é só o que está no repositório.
Vão os oito arquivos da tabela de [Conferir tudo](./01-conferir-tudo.md#os-arquivos), e nada
mais.

## Copiar os arquivos para o repositório

O repositório fica num serviço de hospedagem de Git (como o GitHub ou o GitLab), e o endereço (a
URL) dele aparece na página do repositório. O `git clone` e o `git push` podem pedir login ou uma
**chave SSH**, conforme o serviço. Uma chave SSH é um par de arquivos que identifica o seu
computador para o serviço, no lugar de uma senha; a documentação do serviço explica como criar a
chave e cadastrá-la. A partir da
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

Troque `<endereço-do-repositório>` pelo endereço do seu repositório e, se a pasta do projeto tem outro nome,
troque `the-matrix` pelo nome dela nos comandos `cp`. O `git clone` baixa o repositório; o
`mkdir -p` cria as pastas dos exercícios (o `-p` não reclama se elas já existirem), e cada `cp`
copia os arquivos listados para a pasta do fim da linha.

## O autor dos registros

Todo registro do Git leva o nome e o e-mail de quem o fez. Antes do primeiro registro, defina os
dois **dentro da pasta `entrega`**, com os seus dados no lugar dos do exemplo:

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

Os comandos não imprimem nada. Sem a opção `--global`, a configuração vale só para este
repositório, e não muda nada nos outros.

## Marcar os arquivos

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
pode variar: esta é a saída de um repositório vazio (`No commits yet`, "nenhum
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

## Registrar e enviar

```bash
git commit -m "Add exercises 0 to 2"
```

```text
[main (root-commit) e99ed85] Add exercises 0 to 2
 8 files changed, 338 insertions(+)
 create mode 100644 ex0/construct.py
 create mode 100644 ex1/loading.py
 create mode 100644 ex1/pyproject.toml
 create mode 100644 ex1/requirements.txt
 create mode 100644 ex2/.env.example
 create mode 100644 ex2/.gitignore
 create mode 100644 ex2/oracle.py
 create mode 100644 ex2/requirements.txt
```

`git commit` registra os arquivos marcados, com a mensagem do `-m`. A primeira linha mostra o
ramo e o código do registro (`e99ed85`, outro a cada registro); `root-commit` quer dizer que é o
primeiro registro do repositório. Depois vem a lista dos oito arquivos criados.

```bash
git push
```

`git push` envia o registro para o repositório no serviço de hospedagem.

### Se o Git inventou um autor

Sem o `git config` de [O autor dos registros](#o-autor-dos-registros), o `git commit` pode não
recusar: em vários sistemas (o macOS, por exemplo), ele monta um nome e um e-mail a partir do
usuário e do nome do computador, registra assim mesmo e só avisa. No meio da saída do commit
aparece:

```text
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
```

("O seu nome e endereço de e-mail foram configurados automaticamente a partir do seu usuário e do
nome do computador. Confira se estão corretos.") Essa mensagem quer dizer que o registro saiu com
um autor errado. Para corrigir, antes do `git push`, rode os dois `git config` e refaça o último
registro com o autor novo:

```bash
git commit --amend --reset-author --no-edit
```

```text
[main e99ed85] Add exercises 0 to 2
 8 files changed, 338 insertions(+)
 create mode 100644 ex0/construct.py
 create mode 100644 ex1/loading.py
 create mode 100644 ex1/pyproject.toml
 create mode 100644 ex1/requirements.txt
 create mode 100644 ex2/.env.example
 create mode 100644 ex2/.gitignore
 create mode 100644 ex2/oracle.py
 create mode 100644 ex2/requirements.txt
```

`--amend` refaz o último registro; `--reset-author` troca o autor dele pelo configurado; `--no-edit`
mantém a mensagem. O código do registro depende do autor e da hora, e pode mudar.

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
([Recriar tudo a partir do repositório](./03-perguntas-de-revisao.md#recriar-tudo-a-partir-do-repositório)).
Depois, a pasta `conferencia` pode ser apagada (`cd .. && rm -rf conferencia`).
