---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, e só o que estiver no repositório conta.
Ele também avisa: entregue só os arquivos pedidos. Vão os três `.py`; ficam de fora a pasta
`.venv`, a `experimentos`, a `tools` (com os dados gerados), o `data_generator.tar`, as pastas
`__pycache__`, que o Python cria ao importar um arquivo, e a `.mypy_cache`, que o mypy cria.

O Pydantic também não vai no repositório: ele é instalado com o `pip` em cada máquina que roda os
programas ([O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md)).

## Copiar os arquivos para o repositório

O repositório fica num servidor Git, e o endereço (a URL) dele é o que o serviço que o hospeda
mostra. O `git clone` e o `git push` podem pedir login ou uma **chave SSH**, conforme o servidor.
Uma chave SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de
uma senha; o serviço que hospeda o repositório explica como criar a chave e cadastrá-la. A partir da
pasta `cosmic-data`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os
arquivos `.py` de cada exercício:

```bash
cd ..
git clone <endereço-do-repositório> entrega
for ex in ex0 ex1 ex2; do
    mkdir -p "entrega/$ex"
    cp "cosmic-data/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço do seu repositório e, se a pasta do projeto tiver outro
nome, troque `cosmic-data` pelo nome da sua pasta. O `git clone` baixa o repositório; o
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
	new file:   ex0/space_station.py
	new file:   ex1/alien_contact.py
	new file:   ex2/space_crew.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os três arquivos. O
resto pode variar: esta é a saída de um repositório vazio (`No commits yet`, "nenhum
registro ainda"); num repositório que já tem registros, essa linha não aparece. A primeira
linha mostra o **ramo** (*branch*), a linha de histórico em que os registros entram; o nome
padrão pode ser `main` ou `master`.

Antes do primeiro registro, diga ao git quem é o autor, com o seu nome e o seu e-mail. Dentro
da pasta `entrega`, sem `--global`, a configuração vale só para este repositório:

```bash
git config user.name "Seu Nome"
git config user.email "voce@exemplo.com"
```

Os dois comandos não imprimem nada. Sem eles, o git pode recusar o registro com
`Please tell me who you are` ("diga quem você é") ou, como no macOS, aceitá-lo com um nome e um
e-mail deduzidos do usuário e do nome do computador. Nesse segundo caso, a saída do `git commit`
traz o aviso `Your name and email address were configured automatically based on your username
and hostname` ("seu nome e e-mail foram configurados automaticamente"): é o sinal de que o registro
saiu com a identidade errada. Para corrigir o último registro depois de configurar, use
`git commit --amend --reset-author`.

```bash
git commit -m "Add exercises 0 to 2"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório no servidor.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte, `conferencia`, ao lado de `cosmic-data`, e rode um programa dela com o Python do venv do
projeto:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
ls conferencia/ex0 conferencia/ex1 conferencia/ex2
cosmic-data/.venv/bin/python conferencia/ex2/space_crew.py
```

Os três arquivos aparecem, e o programa imprime a mesma saída que na pasta do projeto. Depois, a
pasta `conferencia` pode ser apagada (`rm -rf conferencia`).
