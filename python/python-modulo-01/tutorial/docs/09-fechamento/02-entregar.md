---
sidebar_position: 2
title: Entregar
---

# Entregar

A entrega é feita num **repositório git** (uma pasta cujo histórico de versões o git guarda e
envia para um servidor), e só o que estiver no repositório é avaliado. Só os sete arquivos
pedidos precisam ir. Ficam de fora a pasta `.venv`, a pasta `experimentos` e as pastas
`__pycache__` e `.mypy_cache` que o Python e o mypy criam.

## Antes de começar

Você precisa de duas coisas:

- o **endereço** (a URL) do repositório de entrega, informado por quem organiza a entrega do
  projeto;
- **acesso** a esse repositório: o `git clone` e o `git push` podem pedir que você se identifique
  no servidor (com usuário e senha, um token ou uma chave SSH já cadastrada). Use a forma de
  acesso indicada por quem organiza a entrega.

## Baixar o repositório

Nos comandos abaixo, troque `<endereço-do-repositório>` pelo endereço recebido, **antes**
de rodar: os sinais `<` e `>` têm outro significado no terminal, e o comando copiado como está
falha. A partir da pasta `code-cultivation`, suba um nível e baixe o repositório numa pasta
`entrega`:

```bash
cd ..
git clone <endereço-do-repositório> entrega
```

Se o repositório de entrega ainda estiver vazio, o `git clone` avisa
`warning: You appear to have cloned an empty repository.` ("parece que você clonou um
repositório vazio"). É o esperado, não um erro. Se aparecer `fatal:`, o clone falhou: confira o
endereço e o acesso e rode o `git clone` de novo, antes de seguir.

## Copiar os arquivos

Copie só os arquivos `.py` de cada exercício para dentro de `entrega`:

```bash
for ex in ex0 ex1 ex2 ex3 ex4 ex5 ex6; do
    mkdir -p "entrega/$ex"
    cp "code-cultivation/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

O `for` cria cada pasta de exercício dentro de `entrega` (o `-p` faz o `mkdir` não reclamar se a
pasta já existir, por exemplo ao repetir o comando) e copia para ela os arquivos `.py`; o
`cd entrega` entra no repositório, e **todos os comandos git daqui em diante rodam de dentro da
pasta `entrega`** (fora dela, o git responde `fatal: not a git repository`). Se a pasta do
projeto tiver outro nome, troque `code-cultivation` por ele no `cp`.

Desenvolver fora do repositório e copiar só os `.py` é escolha do projeto: `.venv`,
`experimentos` e os caches nunca chegam perto da entrega. Outra opção seria trabalhar dentro do
repositório, com um arquivo `.gitignore` listando as pastas que o git deve ignorar.

## Dizer ao git quem você é

No git, um **registro** (*commit*) é uma fotografia dos arquivos marcados, guardada no histórico
do repositório; é ele que o `git push` envia. Cada registro leva o nome e o e-mail do autor.
Antes do primeiro registro neste computador, confira se eles já estão configurados:

```bash
git config --global user.name
git config --global user.email
```

Se os dois comandos imprimirem o seu nome e o seu e-mail, não há nada a configurar. Se algum
não imprimir nada, configure-os (só uma vez por computador), com os seus dados no lugar dos de
exemplo:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email"
```

## Registrar e enviar

```bash
git add ex0 ex1 ex2 ex3 ex4 ex5 ex6
git status
```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") precisa ter exatamente os sete arquivos,
um em cada pasta `ex0` a `ex6`.

```bash
git commit -m "Add exercises 0 to 6"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório de entrega. O `git push` só tem o que enviar depois de um `git commit` que deu
certo: se o commit falhar, o push falha (num repositório vazio, com `failed to push`) ou responde
`Everything up-to-date` sem enviar nada (num repositório que já tem registros). Nos dois casos, o
conserto é refazer o commit e depois o push.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode os programas nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls -1 ex[0-6]/*.py
python3 ex6/ft_garden_analytics.py
```

Os sete arquivos aparecem, e o programa roda como na sua pasta. Os `diff` de cada exercício
também podem ser repetidos aqui. Depois, a pasta `conferencia` pode ser apagada com
`cd .. && rm -rf conferencia`: o `cd ..` sai dela; o `&&` só roda o comando seguinte se o
anterior deu certo; o `rm -rf` apaga a pasta e tudo o que há dentro dela, sem pedir confirmação
e sem passar pela lixeira.

## Na avaliação

Quem avalia vai pedir que você **acrescente o shebang** ao exercício 0, ao vivo
([O shebang](../02-ex0/06-o-shebang.md)). E pode pedir:

- que você **explique** os conceitos
  ([As perguntas do enunciado](./03-as-perguntas-do-enunciado.md));
- que você **mostre as relações de herança**: o diagrama de [Seed](../08-ex6/06-seed.md) mostra a
  família inteira;
- que você **estenda o código** com uma funcionalidade nova: um tipo novo de planta segue os três
  passos de [super()](../07-ex5/03-super.md).
