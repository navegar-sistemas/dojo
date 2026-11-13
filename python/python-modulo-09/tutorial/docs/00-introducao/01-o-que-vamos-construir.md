---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa que recebe dados de fora (de um arquivo, de outro programa, de um formulário) não
pode confiar neles. Uma estação espacial com 25 tripulantes onde só cabem 20, uma data escrita
como texto, um campo obrigatório que não veio: cada um desses casos precisa ser descoberto antes
de o dado entrar no programa. Conferir campo por campo com `if` funciona, mas é longo, repetitivo
e fácil de esquecer.

O **Pydantic** é uma biblioteca do Python que faz essa conferência. Uma **biblioteca** é um
conjunto de código pronto, instalado à parte, que o programa usa com `import`. Com o Pydantic, os
dados são descritos como uma classe: cada campo tem um tipo (`int`, `str`, `datetime`...) e,
quando é preciso, limites (de 1 a 20, no máximo 50 caracteres). Ao criar um objeto, o Pydantic
confere tudo, converte o que dá para converter (o texto `"2024-01-15"` vira uma data) e, se
alguma regra falhar, recusa o objeto com uma mensagem que diz qual campo está errado e por quê.
Essa conferência se chama **validação**.

O projeto se chama **Cosmic Data**. O tema é um observatório que recebe dados de estações
espaciais, de relatos de contato com alienígenas e de missões com tripulação. O tema só dá nome
às coisas; o assunto de verdade é o Pydantic: modelos, limites de campo, regras que envolvem
vários campos e modelos dentro de modelos.

## Três programas, um construído sobre o outro

O projeto tem três **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria, e
cada um acrescenta uma ideia nova do Pydantic:

| Exercício | Arquivo | O que constrói |
|---|---|---|
| 0 | `ex0/space_station.py` | o **modelo** `SpaceStation`, uma classe com oito campos e os limites de cada um |
| 1 | `ex1/alien_contact.py` | o modelo `AlienContact`, com uma lista fechada de tipos de contato e quatro **regras** que comparam campos entre si (um contato telepático precisa de pelo menos 3 testemunhas) |
| 2 | `ex2/space_crew.py` | os modelos `CrewMember` e `SpaceMission`: uma missão guarda uma lista de tripulantes, e cada tripulante é um modelo validado por inteiro |

Cada programa cria um objeto válido, mostra os dados dele, tenta criar um objeto inválido e
mostra a mensagem do erro. A saída do exercício 1:

```text
Alien Contact Log Validation
======================================
Valid contact report:
ID: AC_2024_001
Type: radio
Location: Area 51, Nevada
Signal: 8.5/10
Duration: 45 minutes
Witnesses: 5
Message: 'Greetings from Zeta Reticuli'

======================================
Expected validation error:
Telepathic contact requires at least 3 witnesses
```

O primeiro relato passou por todas as regras; o segundo, um contato telepático com uma única
testemunha, foi recusado. As mensagens são em inglês porque o enunciado do projeto mostra a saída
de cada programa, e essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto, o ambiente virtual com o Pydantic e as duas ferramentas que conferem o código (flake8 e mypy) |
| Pydantic | explica, com experimentos pequenos, cada peça do Pydantic que os exercícios usam |
| Exercícios 0 a 2 | constroem os três programas, um por parte |
| Os dados do gerador | roda as ferramentas de dados que vêm com o enunciado e passa os dados gerados pelos três modelos |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas que o enunciado deixa no ar |

Cada exercício termina com o arquivo completo. Os termos novos estão reunidos no
[glossário](./05-glossario.md).
