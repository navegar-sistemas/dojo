---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório é avaliado.
Um **repositório** é uma pasta acompanhada pelo git, com o histórico dos arquivos; ele fica num
servidor, e cada pessoa trabalha numa cópia baixada dele.
Só os cinco arquivos pedidos precisam ir. Ficam de fora a pasta `.venv`, a pasta
`experimentos` e a pasta `.mypy_cache`, onde o mypy guarda resultados (escondida pelo ponto no
nome, como a `.venv`).

## Antes de começar

Você precisa de duas coisas:

- o **endereço** (a URL) do repositório de entrega, informado por quem organiza a entrega do
  projeto;
- **acesso** a esse repositório: o `git clone` e o `git push` podem pedir que você se identifique
  no servidor (com usuário e senha, um token ou uma chave SSH já cadastrada). Use a forma de
  acesso indicada por quem organiza a entrega.

## Baixar o repositório

Nos comandos desta página, troque `<endereço-do-repositório>` pelo endereço recebido, **antes**
de rodar: os sinais `<` e `>` têm outro significado no terminal, e o comando copiado como está
falha. A partir da pasta `garden-guardian`, suba um nível e baixe o repositório numa pasta
`entrega`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
```

Se o repositório de entrega ainda estiver vazio, o `git clone` avisa
`warning: You appear to have cloned an empty repository.` ("parece que você clonou um
repositório vazio"). É o esperado, não um erro. Se aparecer `fatal:`, o clone falhou: confira o
endereço e o acesso e rode o `git clone` de novo, antes de seguir.

Num endereço por SSH (os que começam com `git@`), a primeira conexão com o servidor faz o git
perguntar `Are you sure you want to continue connecting (yes/no/[fingerprint])?` ("tem certeza
de que quer continuar conectando?"). É uma confirmação de que o servidor é o esperado: responda
com a palavra inteira `yes` (só `y` não é aceito). Responder `no` encerra o clone com `fatal:`,
mesmo com o endereço certo.

## Copiar os arquivos

Copie só os arquivos `.py` de cada exercício para dentro de `entrega`:

```bash
for ex in ex0 ex1 ex2 ex3 ex4; do
    mkdir -p "entrega/$ex"
    cp "garden-guardian/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

O `for` cria cada pasta de exercício dentro de `entrega` e copia para ela os arquivos `.py`; o
`cd entrega` entra no repositório, e **todos os comandos git daqui em diante rodam de dentro da
pasta `entrega`** (fora dela, o git responde `fatal: not a git repository`). Se a
pasta do projeto tiver outro nome, troque `garden-guardian` por ele no `cp`.

## Dizer ao git quem você é

No git, um **registro** (*commit*) é uma fotografia dos arquivos marcados, guardada no
histórico do repositório; é ele que o `git push` envia. Cada registro leva o nome e o e-mail do
autor. Antes do primeiro registro neste
computador, confira se eles já estão configurados:

```bash
git config --global user.name
git config --global user.email
```

Se os dois comandos imprimirem o seu nome e o seu e-mail, siga para a próxima seção. Se algum
não imprimir nada, configure-os (só uma vez por computador), com os seus dados no lugar dos de
exemplo:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email"
```

Sem essa configuração, o git pode recusar o registro ou, em alguns sistemas, registrá-lo com um
autor inventado a partir do nome do usuário e da máquina.

## Registrar e enviar

```bash
git add ex0 ex1 ex2 ex3 ex4
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   ex0/ft_first_exception.py
	new file:   ex1/ft_raise_exception.py
	new file:   ex2/ft_different_errors.py
	new file:   ex3/ft_custom_errors.py
	new file:   ex4/ft_finally_block.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado.
A lista `Changes to be committed` ("mudanças a registrar") tem exatamente os cinco arquivos. O
resto pode variar: esta é a saída de um repositório de entrega vazio (`No commits yet`, "nenhum
registro ainda"); num repositório que já tem registros, essa linha não aparece. A primeira
linha diz o **ramo** (*branch*), a linha de histórico em que os registros entram; o padrão se
chama `main` ou `master`, conforme o repositório.

```bash
git commit -m "Add exercises 0 to 4"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório de entrega. O `git push` só tem o que enviar depois de um `git commit` que deu
certo. Se o commit falhar, o push não envia os arquivos: num repositório vazio ele responde
`failed to push`; num repositório que já tem registros, responde `Everything up-to-date`
("tudo atualizado") sem ter enviado nada. Por isso a seção seguinte confere o que chegou de
fato.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode os programas nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls ex0 ex1 ex2 ex3 ex4
python3 ex4/ft_finally_block.py
```

Os cinco arquivos aparecem, e o programa roda como na sua pasta. Os `diff` das páginas "Rodar e
conferir" também podem ser repetidos aqui. Depois, a pasta `conferencia` pode ser apagada
(`cd .. && rm -rf conferencia`).
