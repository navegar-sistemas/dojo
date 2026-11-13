---
sidebar_position: 2
title: Entregar
---

# Entregar

O enunciado pede a entrega num **repositório Git**, com a árvore de arquivos na **raiz** do
repositório: a pasta `alchemy/`, o `elements.py` e os 13 scripts direto na pasta principal, sem
uma pasta `the-codex` em volta. Só o que estiver no repositório é avaliado. A pasta `.venv`, a
pasta `experimentos`, as pastas `__pycache__` e a pasta `.mypy_cache` ficam de fora.

## Copiar os arquivos para o repositório

O endereço (a URL) do repositório de entrega vem junto com o projeto. O `git clone` e o
`git push` podem pedir login ou uma **chave SSH**, conforme o servidor do repositório. Uma chave
SSH é um par de arquivos que identifica o seu computador para o servidor, no lugar de uma senha;
quem fornece o repositório explica como criar a chave e cadastrá-la no servidor. A partir da
pasta `the-codex`, suba um nível, baixe o repositório numa pasta `entrega` e copie só os arquivos
`.py`, pasta por pasta:

```bash
cd ..
git clone <endereço-do-repositório> entrega
cp the-codex/*.py entrega/
mkdir -p entrega/alchemy/grimoire entrega/alchemy/transmutation
cp the-codex/alchemy/*.py entrega/alchemy/
cp the-codex/alchemy/grimoire/*.py entrega/alchemy/grimoire/
cp the-codex/alchemy/transmutation/*.py entrega/alchemy/transmutation/
cd entrega
```

Troque `<endereço-do-repositório>` pelo endereço recebido. O `git clone` baixa o repositório; o
`mkdir -p` cria as pastas de `alchemy` dentro de `entrega` (o `-p` cria também as pastas do meio,
e não reclama se elas já existirem); cada `cp` copia os arquivos `.py` de uma pasta. Copiar
`*.py` pasta por pasta, em vez da pasta `alchemy` inteira, deixa as pastas `__pycache__` para
trás.

## Registrar e enviar

```bash
git add alchemy *.py
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   alchemy/__init__.py
	new file:   alchemy/elements.py
	new file:   alchemy/grimoire/__init__.py
	new file:   alchemy/grimoire/dark_spellbook.py
	new file:   alchemy/grimoire/dark_validator.py
	new file:   alchemy/grimoire/light_spellbook.py
	new file:   alchemy/grimoire/light_validator.py
	new file:   alchemy/potions.py
	new file:   alchemy/transmutation/__init__.py
	new file:   alchemy/transmutation/recipes.py
	new file:   elements.py
	new file:   ft_alembic_0.py
	new file:   ft_alembic_1.py
	new file:   ft_alembic_2.py
	new file:   ft_alembic_3.py
	new file:   ft_alembic_4.py
	new file:   ft_alembic_5.py
	new file:   ft_distillation_0.py
	new file:   ft_distillation_1.py
	new file:   ft_kaboom_0.py
	new file:   ft_kaboom_1.py
	new file:   ft_transmutation_0.py
	new file:   ft_transmutation_1.py
	new file:   ft_transmutation_2.py

```

`git add` marca os arquivos para o próximo registro; `git status` mostra o que está marcado. A
lista `Changes to be committed` ("mudanças a registrar") tem exatamente os 24 arquivos, e nenhum
`__pycache__`. O resto pode variar: esta é a saída de um repositório de entrega vazio
(`No commits yet`, "nenhum registro ainda"); num repositório que já tem registros, essa linha não
aparece. A primeira linha mostra o **ramo** (*branch*), a linha de histórico em que os registros
entram; o nome padrão pode ser `main` ou `master`.

```bash
git commit -m "Add The Codex"
git push
```

`git commit` registra os arquivos com uma mensagem; `git push` envia o registro para o
repositório de entrega. Se o `git commit` responder `Please tell me who you are` ("diga quem você
é"), ele mesmo mostra os dois comandos `git config --global` que gravam o seu nome e o seu
e-mail; rode-os uma vez, com os seus dados, e repita o `git commit`.

## Conferir o que foi enviado

O que conta é o que está **no repositório**, não na sua pasta. Baixe uma cópia nova numa pasta à
parte e rode dois scripts nela:

```bash
cd ..
git clone <endereço-do-repositório> conferencia
cd conferencia
python3 ft_transmutation_2.py
python3 ft_kaboom_0.py
```

```text
=== Transmutation 2 ===
Import alchemy module only
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

Os dois scripts passam por quase toda a árvore: os três `__init__.py`, os dois `elements.py`, as
poções, a receita e o par da luz. Se faltasse um arquivo, um deles pararia com
`ModuleNotFoundError` ou `ImportError`. Depois, a pasta `conferencia` pode ser apagada
(`cd .. && rm -rf conferencia`).
