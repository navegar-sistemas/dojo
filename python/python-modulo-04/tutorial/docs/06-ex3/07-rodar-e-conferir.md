---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex3/ft_vault_security.py) - <<'FIM'
=== Cyber Archives Security ===

Using 'secure_archive' to read from a nonexistent file:
(False, "[Errno 2] No such file or directory: '/not/existing/file'")

Using 'secure_archive' to read from an inaccessible file:
(False, "[Errno 13] Permission denied: '/etc/sudoers'")

Using 'secure_archive' to read from a regular file:
(True, '[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] Knowledge must survive the entropy wars\n[FRAGMENT 003] Every byte saved is a victory against oblivion\n')

Using 'secure_archive' to write previous content to a new file:
(True, 'Content successfully written to file')
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## O arquivo gravado

```bash
diff new_archive.txt ancient_fragment.txt
```

O `diff` não imprime nada: o arquivo novo é uma cópia exata do fragmento.

## O with só no exercício 3

O enunciado proíbe o `with` antes deste exercício. O `grep` procura a palavra nos quatro arquivos e
mostra onde ela aparece:

```bash
grep -n "with " ex0/*.py ex1/*.py ex2/*.py ex3/*.py
```

```text
ex3/ft_vault_security.py:5:            with open(file_name) as file:
ex3/ft_vault_security.py:8:            with open(file_name, "w") as file:
```

O terminal troca `ex0/*.py` pelos nomes de todos os arquivos `.py` da pasta `ex0` antes de rodar o
`grep`: o `*` vale qualquer sequência de caracteres. O mesmo vale para as outras três pastas.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3
.venv/bin/mypy --disallow-untyped-defs ex3
```

```text
Success: no issues found in 1 source file
```
