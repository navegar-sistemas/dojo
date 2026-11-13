---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa costuma receber dados de vários tipos: números, textos, registros de log. Cada tipo
pede um tratamento diferente, mas o resto do programa não quer saber de cada detalhe: quer
entregar um dado e receber o resultado. Duas ferramentas da programação orientada a objetos
resolvem isso:

- a **classe abstrata**, uma classe que serve só de molde: não gera objetos, lista os métodos que
  toda classe filha precisa escrever e pode já trazer pronto o que é igual para todas;
- o **polimorfismo**, que permite chamar o mesmo método em objetos de classes diferentes e
  deixar cada um responder do seu jeito.

O projeto se chama **Code Nexus**. O tema é uma central de dados do ano de 2087, em Neo-Tokyo,
por onde passam fluxos de informação de todo tipo. O tema só dá nome às coisas; o assunto de
verdade é herança, classes abstratas, sobrescrita de métodos e polimorfismo.

## Três programas, um construído sobre o outro

O projeto tem três **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria, e
cada exercício copia o código do anterior e acrescenta uma peça:

| Exercício | Arquivo | O que constrói |
|---|---|---|
| 0 | `ex0/data_processor.py` | uma classe abstrata `DataProcessor` e três **processadores**, um para números, um para textos e um para logs, que guardam os dados recebidos e os devolvem um de cada vez |
| 1 | `ex1/data_stream.py` | uma classe `DataStream` que recebe uma lista com dados misturados e entrega cada um ao processador certo, sem saber de que classe ele é |
| 2 | `ex2/data_pipeline.py` | a saída do sistema: **plugins** que exportam os dados processados em CSV ou em JSON |

Um trecho da saída do exercício 1. O `DataStream` recebe uma lista com textos, números e logs, e
por enquanto só existe o processador de números:

```text
Registering Numeric Processor

Send first batch of data on stream: ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]
DataStream error - Can't process element in stream: Hello world
DataStream error - Can't process element in stream: [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}]
DataStream error - Can't process element in stream: ['Hi', 'five']
== DataStream statistics ==
Numeric Processor: total 4 items processed, remaining 4 on processor
```

Os números (`3.14`, `-1`, `2.71` e `42`) foram aceitos; o resto foi recusado com uma mensagem, e
o programa seguiu. As mensagens são em inglês porque o enunciado, o documento oficial do projeto,
mostra a saída de cada programa em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o
que ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| Classes abstratas e polimorfismo | explica, com experimentos pequenos, sobrescrita de métodos, classes abstratas, os type hints `Any` e `int \| float`, polimorfismo e a fila que guarda os dados |
| Exercícios 0 a 2 | constroem os três programas, um por parte |
| Fechamento | confere tudo, mostra como entregar e responde a perguntas de revisão sobre o projeto |

Cada exercício termina com o arquivo completo. Os termos novos estão reunidos no
[glossário](./05-glossario.md).
