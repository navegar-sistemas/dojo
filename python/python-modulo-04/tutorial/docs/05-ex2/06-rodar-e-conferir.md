---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Rodar como no enunciado

```bash
python3 ex2/ft_stream_management.py foo
```

```text
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
```

```bash
python3 ex2/ft_stream_management.py ancient_fragment.txt
```

Na pergunta, digite `vault.txt`, o arquivo sem permissão de escrita criado no [exercício
1](../04-ex1/08-rodar-e-conferir.md). As últimas linhas são:

```text
Enter new file name (or empty): vault.txt
Saving data to 'vault.txt'
[STDERR] Error opening file 'vault.txt': [Errno 13] Permission denied: 'vault.txt'
Data not saved.
```

## Cada mensagem no seu canal

Separando as saídas, cada linha tem de estar no canal certo. A saída padrão, com a de erro
descartada:

```bash
diff <(python3 ex2/ft_stream_management.py foo 2> /dev/null) - <<'FIM'
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
FIM
```

A saída de erro, guardada em `erros.txt`, com a padrão descartada:

```bash
python3 ex2/ft_stream_management.py foo > /dev/null 2> erros.txt
diff erros.txt - <<'FIM'
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
FIM
rm erros.txt
```

Nenhum dos dois `diff` imprime nada.

## A ordem, com tudo junto

Com `2>&1`, as duas saídas vão juntas para o `diff`, passando por um pipe. É o caso em que, sem o
`flush` de `report_error`, o erro sairia fora de ordem ([Escrever no
stderr](./03-escrever-no-stderr.md)):

```bash
diff <(printf 'vault.txt\n' | python3 ex2/ft_stream_management.py ancient_fragment.txt 2>&1) - <<'FIM'
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
Enter new file name (or empty): Saving data to 'vault.txt'
[STDERR] Error opening file 'vault.txt': [Errno 13] Permission denied: 'vault.txt'
Data not saved.
FIM
```

Sem nenhuma linha impressa, a ordem está certa. Como no [exercício
1](../04-ex1/08-rodar-e-conferir.md), a resposta vinda do `printf` não aparece na tela.

## A entrada

Gravar, não gravar e entrada vazia:

```bash
printf 'new_fragment.txt\n' | python3 ex2/ft_stream_management.py ancient_fragment.txt | tail -n 2
printf '\n' | python3 ex2/ft_stream_management.py ancient_fragment.txt | tail -n 1
python3 ex2/ft_stream_management.py ancient_fragment.txt < /dev/null | tail -n 2
```

```text
Enter new file name (or empty): Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
Enter new file name (or empty): Not saving data.
Enter new file name (or empty): 
Not saving data.
```

E nenhum `input()` no arquivo:

```bash
grep -n "input(" ex2/ft_stream_management.py
```

O `grep` procura o texto `input(` no arquivo e imprime cada linha em que o acha, com o número da
linha na frente (é o que o `-n` faz). Não imprime nada: não há `input(` no arquivo.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
Success: no issues found in 1 source file
```
