---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa Python de verdade raramente vive sozinho. Ele usa **bibliotecas** escritas por outras
pessoas (código pronto que se instala, como o `pandas`), precisa de **configuração** que muda de
máquina para máquina (o endereço de um banco de dados, uma senha) e, quando cresce, é dividido em
muitos arquivos que se chamam uns aos outros com `import`. Cada uma dessas três coisas tem um
jeito certo de ser feita, e um jeito errado que só aparece quando algo explode:

- bibliotecas instaladas direto no Python do sistema se misturam com tudo o que o sistema usa. O
  remédio é o **ambiente virtual**: uma pasta com um Python e bibliotecas só daquele projeto;
- senhas escritas no código vão parar no repositório, à vista de quem o lê. O remédio são as
  **variáveis de ambiente** e o arquivo `.env`, que ficam fora do código;
- arquivos que se importam de qualquer jeito acabam importando um ao outro em círculo. O remédio
  é entender como o `import` funciona: **módulos**, **pacotes**, imports **absolutos** e
  **relativos**.

O projeto se chama **The Codex**. O tema é um laboratório de alquimia: o ambiente virtual é o
laboratório selado, as bibliotecas são os reagentes, a configuração secreta é o oráculo, e os
arquivos de código são fórmulas num grimório (o livro de feitiços dos alquimistas). O tema só dá
nome às coisas; o assunto de verdade é a caixa de ferramentas de quem programa em Python.

## Cinco exercícios, um laboratório

| Exercício | Arquivos | O que constrói |
|---|---|---|
| 0 | `ex0/construct.py`, `ex0/loading.py`, `ex0/requirements.txt`, `ex0/pyproject.toml` | um programa que descobre se está rodando num ambiente virtual, e outro que confere se as bibliotecas `pandas` e `numpy` estão instaladas, instaladas de dois jeitos: com o **pip** e com o **Poetry** |
| 1 | `ex1/oracle.py`, `ex1/requirements.txt`, `ex1/.env.example`, `ex1/.gitignore` | um programa que lê a configuração de variáveis de ambiente e de um arquivo `.env`, sem nenhum segredo dentro do código |
| 2 | `elements.py`, `alchemy/__init__.py`, `alchemy/elements.py`, `ft_alembic_0.py`, `ft_alembic_1.py` | o começo do pacote `alchemy` e dois programas que o usam de jeitos diferentes |
| 3 | `alchemy/potions.py`, `alchemy/transmutation/`, `ft_distillation_0.py`, `ft_transmutation_0.py` | módulos que importam código de outros módulos, dentro e fora do pacote, e um subpacote |
| 4 | `alchemy/grimoire/`, `ft_kaboom_0.py`, `ft_kaboom_1.py` | dois pares de arquivos que precisam um do outro: um par funciona, o outro explode |

Os exercícios 0 e 1 vivem cada um na sua pasta. Os exercícios 2 a 4 constroem juntos uma única
pasta, `alchemy`, na raiz do projeto, e os programas que a testam ficam ao lado dela.

A saída dos dois programas de teste do exercício 4; no segundo, as reticências (`...`) marcam
linhas e um caminho de pasta omitidos aqui, que aparecem por inteiro no
[resultado final](./04-o-resultado-final.md):

```text
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

```text
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
Traceback (most recent call last):
  ...
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.dark_spellbook' (most likely due to a circular import) (...)
```

O primeiro registra um feitiço. O segundo para com um erro de propósito: dois arquivos que se
importam um ao outro no topo, e o Python não consegue terminar de carregar nenhum dos dois. As
mensagens são em inglês porque o enunciado do projeto mostra a saída de cada programa, e essa
saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| Exercício 0 | ambientes virtuais por dentro, `construct.py`, pip, Poetry e `loading.py` |
| Exercício 1 | variáveis de ambiente, o arquivo `.env`, o `.gitignore` e `oracle.py` |
| Módulos e pacotes | explica, com experimentos pequenos, como o `import` encontra e carrega o código: módulos, pacotes, `__init__.py`, imports absolutos e relativos, e o import circular |
| Exercícios 2 a 4 | constroem o pacote `alchemy` e os seis programas de teste |
| Fechamento | confere tudo, mostra como entregar num repositório Git e responde às perguntas de revisão de cada exercício |

Cada exercício termina com os arquivos completos e uma página de rodar e conferir. Os termos
novos estão reunidos no [glossário](./05-glossario.md).
