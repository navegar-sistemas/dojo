---
sidebar_position: 2
title: Entregar
---

# Entregar

A entrega é feita num **repositório Git**, e só o que estiver no repositório conta. Só os quatro
arquivos pedidos precisam ir; a pasta `.venv`, a pasta `experimentos`, os arquivos de teste
(`ancient_fragment.txt`, `new_fragment.txt`, `new_archive.txt`, `vault.txt`) e a pasta
`.mypy_cache`, que o mypy cria, ficam de fora.

## Copiar os arquivos para o repositório

O repositório tem um endereço (a URL), que o serviço onde ele está hospedado mostra. O `git clone` e
o `git push` podem pedir login ou uma chave SSH (um par de arquivos que identifica o seu computador
para esse serviço, no lugar da senha), conforme o serviço. A partir da pasta `data-archivist`, suba
um nível, baixe o repositório numa pasta `entrega` e copie só os arquivos `.py` de cada exercício:

```bash
cd ..
git clone <endereço-do-repositório> entrega
for ex in ex0 ex1 ex2 ex3; do
    mkdir -p "entrega/$ex"
    cp "data-archivist/$ex/"*.py "entrega/$ex/"
done
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço do repositório. O `git clone` baixa o repositório;
se ele ainda estiver vazio, avisa `warning: You appear to have cloned an empty repository.`, o que é
normal num repositório novo. O `for` cria cada pasta de exercício dentro de `entrega` (o `-p` do
`mkdir` não reclama se ela já existir) e copia para ela os arquivos `.py` com `cp`.

## Registrar e enviar

```bash
git add ex0 ex1 ex2 ex3
git status
```

```text
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   ex0/ft_ancient_text.py
	new file:   ex1/ft_archive_creation.py
	new file:   ex2/ft_stream_management.py
	new file:   ex3/ft_vault_security.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A lista
`Changes to be committed` ("mudanças a registrar") tem exatamente os quatro arquivos. O resto pode
variar: esta é a saída de um repositório vazio (`No commits yet`, "nenhum registro ainda"); num
repositório que já tem registros, essa linha não aparece. O nome do ramo (*branch*, a sequência de
registros em que o `git` está trabalhando) na primeira linha também pode ser outro, como `main`.

Todo registro leva o nome e o e-mail do autor. Antes do primeiro `git commit` num computador,
informe os seus (uma vez só; o `--global` vale para todos os repositórios desse computador). Sem
isso, o `git` recusa o registro com `Please tell me who you are` ou, conforme o sistema, grava um
autor inventado a partir do seu usuário e do nome do computador:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email"
```

```bash
git commit -m "Add exercises 0 to 3"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o repositório
remoto, o que foi baixado com o `git clone`.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode um programa nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
ls ex0 ex1 ex2 ex3
python3 ex0/ft_ancient_text.py ../data-archivist/ancient_fragment.txt
```

Os quatro arquivos aparecem, e o programa lê o fragmento como na pasta do projeto. Depois, a pasta
`conferencia` pode ser apagada com `cd .. && rm -rf conferencia`: o `&&` roda o segundo comando só
se o primeiro deu certo, e o `-rf` faz o `rm` apagar a pasta com tudo o que há dentro, sem pedir
confirmação.
