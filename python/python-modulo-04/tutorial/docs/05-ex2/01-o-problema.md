---
sidebar_position: 1
title: O problema
---

# O problema

Todo programa tem duas saídas de texto: a **saída padrão**, por onde sai o resultado, e a **saída
de erro**, reservada aos avisos de erro. No terminal, as duas aparecem na mesma tela ([Os três
fluxos](./02-os-tres-fluxos.md)).

No exercício 1, as mensagens de erro saem pela saída padrão, o mesmo caminho do texto do arquivo.
Quem quiser guardar só o texto num arquivo, ou só os erros num registro, não consegue separar um do
outro. O exercício 2 manda cada tipo de mensagem pelo seu canal.

## O que o enunciado pede

Um arquivo `ex2/ft_stream_management.py` que parte do código do exercício 1 e muda duas coisas:

- as mensagens de erro vindas de exceções saem pela **saída de erro**, e não pela saída padrão, com
  um prefixo claro: `[STDERR]`;
- o nome do arquivo é lido **sem** a função `input()`.

`input()` sai da lista de autorizados. Entram `sys.stdin`, `sys.stdout` e `sys.stderr` (os três
fluxos), `readline()` e `flush()`.

## A saída esperada

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

Com `ancient_fragment.txt`, tudo é igual ao exercício 1 até a pergunta. Gravando no `vault.txt`, o
arquivo sem permissão de escrita criado no [exercício 1](../04-ex1/08-rodar-e-conferir.md) (o
enunciado usa o `/etc/passwd`):

```text
Enter new file name (or empty): vault.txt
Saving data to 'vault.txt'
[STDERR] Error opening file 'vault.txt': [Errno 13] Permission denied: 'vault.txt'
Data not saved.
```

No terminal, as linhas aparecem nessa ordem, misturadas. A diferença só se vê quando os canais são
separados, assunto da [próxima página](./02-os-tres-fluxos.md).

## O que muda no código

| Função | Mudança |
|---|---|
| `report_error(message)` | nova: imprime uma mensagem de erro na saída de erro, com o prefixo |
| `recover_archive` e `save_archive` | as mensagens de erro passam por `report_error` |
| `ask_file_name()` | lê a resposta com `sys.stdin.readline()` em vez de `input()` |

`display`, `transform` e `main` ficam como no exercício 1. Mensagens que não vêm de exceções, como
`Data not saved.` e a mensagem de uso, continuam na saída padrão.
