---
sidebar_position: 2
title: Entregar
---

# Entregar

A entrega é feita no repositório Git do projeto, e só o que está nele é avaliado. Entram só os
sete arquivos pedidos, cada um na sua pasta:

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
copiada entre máquinas. O repositório de entrega é criado vazio no servidor da escola, com um
endereço próprio. `git clone` baixa uma cópia dele para uma pasta nova. Na pasta `data-quest`:

```bash
git clone <endereço-do-repositório> entrega
```

No lugar de `<endereço-do-repositório>` vai o endereço do seu repositório de entrega; `entrega` é
o nome da pasta criada. Copie para ela as pastas `ex0` a `ex6` da `data-quest` e entre na pasta
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

```bash
git commit -m "Data Quest: exercises 0 to 6"
git push
```

`git commit` registra os arquivos com uma mensagem, e `git push` os envia para o repositório de
entrega.

## Na avaliação

Quem avalia pode pedir que você explique por que escolheu cada coleção, demonstre operações com
elas ou acrescente uma funcionalidade a um dos programas
([Perguntas da avaliação](./03-perguntas-da-avaliacao.md)).
