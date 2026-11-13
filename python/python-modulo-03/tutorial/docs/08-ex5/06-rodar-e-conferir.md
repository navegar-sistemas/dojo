---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

```bash
(cd ex5 && python3 ft_data_stream.py)
```

São 1022 linhas: o título, 1000 eventos, a lista de dez e duas linhas para cada um dos dez
eventos consumidos. Para ver só o começo ou só o fim, a saída pode passar por outro comando com a
barra vertical `|`, que liga a saída do programa à entrada do comando seguinte:

- `sed -n '1,4p'` imprime só as linhas 1 a 4: o `-n` desliga a impressão de todas as linhas, e o
  `1,4p` imprime (*print*) as linhas de 1 a 4;
- `tail -n 5` ("cauda") imprime só as 5 últimas.

```bash
(cd ex5 && python3 ft_data_stream.py | sed -n '1,4p')
```

```text
=== Game Data Stream Processor ===
Event 0: Player charlie did action grab
Event 1: Player dylan did action swim
Event 2: Player dylan did action sleep
```

```bash
(cd ex5 && python3 ft_data_stream.py | tail -n 5)
```

```text
Remains in list: [('charlie', 'grab'), ('alice', 'eat')]
Got event from list: ('charlie', 'grab')
Remains in list: [('alice', 'eat')]
Got event from list: ('alice', 'eat')
Remains in list: []
```

Cada execução sorteia outros eventos, então as suas linhas serão outras.

## Conferir as contagens

Os sorteios mudam, mas as quantidades não. O comando `grep -c` conta as linhas que combinam com
um padrão; o `^` no começo do padrão exige que o texto esteja no começo da linha:

```bash
(cd ex5 && python3 ft_data_stream.py | grep -c '^Event ')
(cd ex5 && python3 ft_data_stream.py | grep -c '^Got event from list')
(cd ex5 && python3 ft_data_stream.py | tail -n 1)
```

```text
1000
10
Remains in list: []
```

São mil eventos, dez eventos consumidos, e a lista termina vazia.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex5
.venv/bin/mypy --disallow-untyped-defs ex5
```

```text
Success: no issues found in 1 source file
```
