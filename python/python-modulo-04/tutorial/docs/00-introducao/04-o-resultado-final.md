---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto, nos casos que o enunciado mostra. Os comandos são rodados na
pasta do projeto, onde fica o arquivo `ancient_fragment.txt` ([A pasta do
projeto](../01-ambiente/02-a-pasta-do-projeto.md)), e só funcionam depois que os arquivos existirem:
a página "Rodar e conferir" de cada exercício os roda.

Três diferenças em relação aos exemplos do enunciado:

- o arquivo protegido é `/etc/sudoers`, que só o administrador lê e existe no macOS e em todo Linux
  com o `sudo` instalado, no lugar do `/etc/master.passwd`, que só existe no macOS ([Quando o open
  falha](../02-arquivos/05-quando-o-open-falha.md));
- a mensagem de uso mostra o caminho do programa como ele foi digitado, `ex0/ft_ancient_text.py`,
  porque os comandos são rodados da pasta do projeto ([O uso](../03-ex0/02-o-uso.md));
- a gravação que falha usa o `vault.txt`, um arquivo sem permissão de escrita criado no [exercício
  1](../04-ex1/08-rodar-e-conferir.md), no lugar do `/etc/passwd`, que no macOS abre uma janela do
  sistema pedindo para "administrar o computador".

## Exercício 0

```bash
python3 ex0/ft_ancient_text.py
```

```text
Usage: ex0/ft_ancient_text.py <file>
```

```bash
python3 ex0/ft_ancient_text.py foo
```

```text
=== Cyber Archives Recovery ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

```bash
python3 ex0/ft_ancient_text.py /etc/sudoers
```

```text
=== Cyber Archives Recovery ===
Accessing file '/etc/sudoers'
Error opening file '/etc/sudoers': [Errno 13] Permission denied: '/etc/sudoers'
```

```bash
python3 ex0/ft_ancient_text.py ancient_fragment.txt
```

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

## Exercício 1

O programa para e espera um nome. Abaixo, a pessoa apertou Enter sem digitar nada:

```bash
python3 ex1/ft_archive_creation.py ancient_fragment.txt
```

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.

Transform data:
---

[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#

---
Enter new file name (or empty):
Not saving data.
```

E aqui digitou `new_fragment.txt`; as linhas até `Enter new file name` são as mesmas:

```text
Enter new file name (or empty): new_fragment.txt
Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
```

```bash
cat new_fragment.txt
```

```text
[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
[FRAGMENT 003] Every byte saved is a victory against oblivion#
```

## Exercício 2

As linhas que começam com `[STDERR]` saem pela saída de erro; no terminal elas aparecem misturadas
às outras, no lugar em que acontecem.

```bash
python3 ex2/ft_stream_management.py foo
```

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

Com `ancient_fragment.txt`, a saída é a do exercício 1 até o pedido do nome. Digitando `vault.txt`,
um arquivo que ninguém pode alterar:

```text
Enter new file name (or empty): vault.txt
Saving data to 'vault.txt'
[STDERR] Error opening file 'vault.txt': [Errno 13] Permission denied: 'vault.txt'
Data not saved.
```

## Exercício 3

```bash
python3 ex3/ft_vault_security.py
```

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

A linha do terceiro resultado é longa: o terminal a quebra na largura da janela, mas é uma linha só.
