---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa pequeno cabe num arquivo só. Quando ele cresce, o código é dividido em vários
arquivos e pastas, e cada arquivo precisa usar funções escritas nos outros. Quem faz essa ligação
no Python é a instrução `import`, que traz para um arquivo o código de outro. Com ela vêm quatro
perguntas:

- como uma pasta de arquivos vira uma peça só, que se importa de uma vez, e o que essa peça mostra
  para quem a importa (o **pacote** e o arquivo `__init__.py`);
- como o Python acha um arquivo que está em outra pasta;
- como escrever o caminho até esse arquivo: a partir da raiz do projeto (import **absoluto**) ou a
  partir do arquivo que importa (import **relativo**);
- o que acontece quando dois arquivos importam um ao outro (o import **circular**), e como evitar.

O projeto se chama **The Codex** ("o códice", nome dado aos livros antigos escritos à mão). O
tema é o laboratório de um alquimista: elementos (fogo, água, terra e ar), poções, uma receita que
transforma chumbo em ouro e um grimório (livro de feitiços). O tema só dá nome às coisas; o
assunto de verdade é o sistema de imports do Python.

## Uma árvore construída em quatro partes

O projeto não tem exercícios em pastas separadas: as quatro partes constroem, juntas, uma única
árvore de arquivos. Cada parte acrescenta peças a essa árvore e alguns **scripts de teste**:
programas curtos, com nome `ft_...py`, que importam as peças de um jeito específico e imprimem o
resultado.

| Parte | O que acrescenta | Scripts de teste | O assunto |
|---|---|---|---|
| I: o alambique | `elements.py` e a pasta `alchemy/`, com `elements.py` e `__init__.py` | `ft_alembic_0.py` a `ft_alembic_5.py` | as duas formas do `import` e o `__init__.py` |
| II: a destilação | `alchemy/potions.py` | `ft_distillation_0.py` e `ft_distillation_1.py` | um arquivo dentro de uma pasta que usa arquivos de outras pastas |
| III: a grande transmutação | a pasta `alchemy/transmutation/` | `ft_transmutation_0.py` a `ft_transmutation_2.py` | import absoluto e import relativo |
| IV: evitar a explosão | a pasta `alchemy/grimoire/` | `ft_kaboom_0.py` e `ft_kaboom_1.py` | o import circular |

Os nomes vêm do inglês: *alembic* é o alambique, *distillation* a destilação, *transmutation* a
transmutação, e *kaboom* é a onomatopeia de uma explosão.

Um trecho da saída: `ft_transmutation_2.py` importa só o pacote `alchemy` e chega a uma receita
que junta peças de quatro arquivos diferentes.

```text
=== Transmutation 2 ===
Import alchemy module only
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
```

Dois scripts falham de propósito, e a falha é o resultado esperado: `ft_alembic_4.py` chama uma
função que o pacote não mostra, e `ft_kaboom_1.py` importa dois arquivos que se importam um ao
outro. As mensagens são em inglês porque o enunciado do projeto mostra a saída de cada script, e
essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| Módulos e imports | mostra, com experimentos pequenos, o que o `import` faz e onde o Python procura os arquivos importados |
| Partes I a IV | constroem a árvore do projeto, uma parte do enunciado por vez |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas que o enunciado deixa para a avaliação |

Cada parte termina com os arquivos completos dela e uma página que roda e confere tudo. Os termos
novos estão reunidos no [glossário](./05-glossario.md).
