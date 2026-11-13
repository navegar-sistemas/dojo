---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

O comando `diff` compara duas listas de linhas e mostra só as diferenças. Abaixo, ele compara a
saída do programa com o texto esperado:

- `<(...)` entrega a saída de um comando como se fosse um arquivo;
- `-` diz ao `diff` que a segunda lista vem da entrada, que é o texto entre `<<'FIM'` e `FIM`.

```bash
diff <(python3 ex0/ft_ancient_text.py ancient_fragment.txt) - <<'FIM'
=== Cyber Archives Recovery ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.
FIM
```

Sem nenhuma linha impressa, a saída é idêntica à esperada. Os outros casos:

```bash
diff <(python3 ex0/ft_ancient_text.py) - <<'FIM'
Usage: ex0/ft_ancient_text.py <file>
FIM
diff <(python3 ex0/ft_ancient_text.py foo) - <<'FIM'
=== Cyber Archives Recovery ===
Accessing file 'foo'
Error opening file 'foo': [Errno 2] No such file or directory: 'foo'
FIM
diff <(python3 ex0/ft_ancient_text.py /etc/sudoers) - <<'FIM'
=== Cyber Archives Recovery ===
Accessing file '/etc/sudoers'
Error opening file '/etc/sudoers': [Errno 13] Permission denied: '/etc/sudoers'
FIM
```

Nenhum dos três imprime nada.

## As outras falhas

Uma pasta no lugar do arquivo:

```bash
python3 ex0/ft_ancient_text.py ex0
```

```text
=== Cyber Archives Recovery ===
Accessing file 'ex0'
Error opening file 'ex0': [Errno 21] Is a directory: 'ex0'
```

Argumentos a mais:

```bash
python3 ex0/ft_ancient_text.py ancient_fragment.txt foo
```

```text
Usage: ex0/ft_ancient_text.py <file>
```

Um arquivo que não é texto, o programa `/bin/ls`:

```bash
python3 ex0/ft_ancient_text.py /bin/ls
```

```text
=== Cyber Archives Recovery ===
Accessing file '/bin/ls'
Error reading file '/bin/ls': 'utf-8' codec can't decode byte 0xb7 in position 18: invalid start byte
File '/bin/ls' closed.
```

O byte e a posição mudam de sistema para sistema. O arquivo abriu, a leitura falhou, e o `finally` o
fechou ([Ler e fechar](./04-ler-e-fechar.md)).

## Nenhum caso trava

O **código de saída** é um número que todo programa devolve ao terminal ao terminar: `0` quer dizer
"terminou bem", e um programa que trava com uma exceção devolve `1`. O comando `echo $?` mostra o
código do último programa:

```bash
python3 ex0/ft_ancient_text.py /bin/ls > /dev/null
echo $?
```

```text
0
```

(`> /dev/null` descarta a saída do programa, que já foi conferida.) Todos os casos desta página
terminam com `0`.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema.
