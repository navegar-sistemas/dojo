---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa perde tudo o que guarda nas variáveis quando termina. Para que um dado sobreviva ao fim
do programa, ele precisa ir para um **arquivo**: um conjunto de dados com nome, guardado no disco.
Ler e escrever um arquivo pode falhar: o arquivo não existe, falta permissão, o disco recusa a
escrita. Um programa bem feito trata cada falha e continua de pé.

O projeto se chama **Data Archivist** ("arquivista de dados"). O tema é um arquivo digital do ano de
2087 que precisa preservar fragmentos de texto antigos. O tema só dá nome às coisas; o assunto de
verdade é a leitura e a escrita de arquivos e os três canais de comunicação de um programa com o
terminal.

## Quatro programas pequenos

O projeto tem quatro **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria.
Os exercícios 1 e 2 partem do código do anterior; o 3 é um programa novo. Cada um acrescenta uma
ferramenta:

| Exercício | Arquivo | O que ensina |
|---|---|---|
| 0 | `ex0/ft_ancient_text.py` | **abrir**, **ler** e **fechar** um arquivo cujo nome vem do terminal, e tratar cada falha |
| 1 | `ex1/ft_archive_creation.py` | **transformar** o texto lido e **gravar** o resultado num arquivo novo, com o nome digitado pelo usuário |
| 2 | `ex2/ft_stream_management.py` | os **três fluxos** de um programa: mandar as mensagens de erro para a saída de erro e ler o teclado sem `input()` |
| 3 | `ex3/ft_vault_security.py` | a instrução **`with`**, que fecha o arquivo sozinha, numa função que lê ou grava qualquer arquivo |

Um exemplo, o exercício 0 lendo o arquivo `ancient_fragment.txt`:

```text
=== Cyber Archives Recovery ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.
```

E o mesmo programa com um nome de arquivo que não existe:

```text
=== Cyber Archives Recovery ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

O programa avisa o erro e termina normalmente, sem a mensagem de erro do próprio Python. As
mensagens são em inglês porque o enunciado do projeto mostra a saída de cada programa, e essa saída
é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). A [próxima página](./02-o-enunciado-em-linguagem-simples.md) resume tudo o que
ele pede.

## As partes

| Parte | Conteúdo |
|---|---|
| Ambiente | prepara o Python, a pasta do projeto e as duas ferramentas que conferem o código (flake8 e mypy) |
| O que é um arquivo | explica, com experimentos pequenos, caminhos, `open()`, `read()`, `close()`, as falhas possíveis e os argumentos do terminal |
| Exercícios 0 a 3 | constroem os quatro programas, um por parte |
| Fechamento | confere tudo, mostra como entregar e responde às perguntas que o enunciado deixa para a avaliação |

Cada exercício termina com o arquivo completo. Os termos novos estão reunidos no
[glossário](./05-glossario.md).
