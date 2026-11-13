---
sidebar_position: 1
title: O problema
---

# O problema

Nos exercícios anteriores, cada arquivo aberto exigiu um `try` com `finally` só para garantir o
`close()`. O exercício 3 troca essa estrutura pela instrução `with`, que fecha o arquivo sozinha, e
reúne leitura e escrita numa única função segura.

## O que o enunciado pede

Um arquivo `ex3/ft_vault_security.py` com uma função **`secure_archive()`** que:

- usa a instrução `with` para abrir os arquivos ([O with](./02-o-with.md));
- serve para **ler** ou **escrever** qualquer arquivo;
- devolve uma **tupla** `(True ou False, str)`: o booleano diz se a operação deu certo, e o texto é
  o conteúdo do arquivo (na leitura que deu certo) ou uma mensagem (no resto);
- recebe três parâmetros: o nome do arquivo, **obrigatório**; a ação a executar, ler ou escrever,
  **opcional**, como `int` ou `str` (a escolha é sua); e o texto a escrever, **opcional**.

Na avaliação, a estrutura do código é conferida contra esses requisitos. O programa só pode usar
`open()`, `read()`, `write()` e `print()`; não há `import`.

## A saída esperada

O programa não recebe argumentos: ele demonstra a função com quatro chamadas.

```text
=== Cyber Archives Security ===

Using 'secure_archive' to read from a nonexistent file:
(False, "[Errno 2] No such file or directory: '/not/existing/file'")

Using 'secure_archive' to read from an inaccessible file:
(False, "[Errno 13] Permission denied: '/etc/sudoers'")

Using 'secure_archive' to read from a regular file:
(True, '[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] Knowledge must survive the entropy wars\n[FRAGMENT 003] Every byte saved is a victory against oblivion\n')

Using 'secure_archive' to write previous content to a new file:
(True, 'Content successfully written to file')
```

Cada linha de resultado é a tupla devolvida, impressa diretamente com `print`. O arquivo inacessível
é o `/etc/sudoers`, como nos outros exercícios ([Quando o open
falha](../02-arquivos/05-quando-o-open-falha.md)).
