---
sidebar_position: 2
title: Entregar
---

# Entregar

A entrega é feita num repositório Git, e o que não estiver nele não faz parte do trabalho
entregue. Entram só os sete arquivos pedidos, cada um na sua pasta:

| Pasta | Arquivo |
|---|---|
| `ex0/` | `ft_command_quest.py` |
| `ex1/` | `ft_score_analytics.py` |
| `ex2/` | `ft_coordinate_system.py` |
| `ex3/` | `ft_achievement_tracker.py` |
| `ex4/` | `ft_inventory_system.py` |
| `ex5/` | `ft_data_stream.py` |
| `ex6/` | `ft_data_alchemist.py` |

As pastas `experimentos/`, `.venv/` e `.mypy_cache/` (criada pelo mypy) ficam de fora.

## Baixar o repositório

Um **repositório Git** é uma pasta cujo histórico de mudanças o Git guarda, e que pode ser
copiada entre máquinas. Os passos abaixo partem de um repositório vazio que já existe num serviço
de hospedagem de Git, como o GitHub ou o GitLab, com um endereço próprio. `git clone` baixa uma
cópia dele para uma pasta nova. Na pasta `data-quest`:

```bash
git clone <endereço-do-repositório> entrega
```

No lugar de `<endereço-do-repositório>` vai o endereço do seu repositório; `entrega` é
o nome da pasta criada. Como o repositório está vazio, o `git clone` avisa
`warning: You appear to have cloned an empty repository.` ("parece que você clonou um repositório
vazio"); o aviso é esperado. Copie para ela as pastas `ex0` a `ex6` da `data-quest` e entre na pasta
`entrega`:

```bash
cp -r ex0 ex1 ex2 ex3 ex4 ex5 ex6 entrega/
cd entrega
```

O `-r` (recursivo) faz o `cp` copiar as pastas com tudo o que há dentro delas.

## Acrescentar só os sete arquivos

Dentro da pasta `entrega`:

```bash
git add ex0/ft_command_quest.py ex1/ft_score_analytics.py ex2/ft_coordinate_system.py \
  ex3/ft_achievement_tracker.py ex4/ft_inventory_system.py ex5/ft_data_stream.py \
  ex6/ft_data_alchemist.py
git status
```

- `git add` marca os arquivos para entrar no próximo registro (*commit*). A barra invertida `\` no
  fim da linha continua o comando na linha de baixo;
- `git status` lista o que vai entrar, em "Changes to be committed". Confira que são os sete
  arquivos, com os nomes exatos, e nada mais.

## Registrar e enviar

O commit guarda também o nome e o e-mail de quem o fez. `git config user.name` e
`git config user.email` mostram os que o Git conhece; se não mostrarem nada, o `git commit`
recusa com `Author identity unknown` ("identidade do autor desconhecida") ou registra um nome e um
e-mail adivinhados a partir do usuário e do nome do computador. Nesse caso, grave os seus antes do
commit, uma vez só:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email"
```

`--global` grava a configuração para todos os repositórios do seu usuário. Depois, registre e
envie:

```bash
git commit -m "Data Quest: exercises 0 to 6"
git push
```

`git commit` registra os arquivos com uma mensagem, e `git push` os envia para o repositório no
servidor.

## Revisar

As [Perguntas de revisão](./03-perguntas-de-revisao.md) reúnem o que vale saber explicar sobre o
projeto: por que cada coleção foi escolhida, como as operações com elas funcionam e onde mexer
para acrescentar uma funcionalidade a um dos programas.
