---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Rodar digitando

```bash
(cd ex2 && python3 ft_coordinate_system.py)
```

Digite as mesmas respostas do enunciado, uma por pergunta, cada uma seguida de Enter:
`hello world`, `1.0 , 2.5, 3.0`, `4,abc,5` e `4,5,6`. A tela fica igual à saída do enunciado:

```text
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': hello world
Invalid syntax
Enter new coordinates as floats in format 'x,y,z': 1.0 , 2.5, 3.0
Got a first tuple: (1.0, 2.5, 3.0)
It includes: X=1.0, Y=2.5, Z=3.0
Distance to center: 4.0311

Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': 4,abc,5
Error on parameter 'abc': could not convert string to float: 'abc'
Enter new coordinates as floats in format 'x,y,z': 4,5,6
Distance between the 2 sets of coordinates: 4.9244
```

## Rodar com as respostas prontas

Para não digitar tudo a cada teste, as respostas podem ir prontas para o programa:

```bash
(cd ex2 && printf 'hello world\n1.0 , 2.5, 3.0\n4,abc,5\n4,5,6\n' | python3 ft_coordinate_system.py)
```

```text
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': Invalid syntax
Enter new coordinates as floats in format 'x,y,z': Got a first tuple: (1.0, 2.5, 3.0)
It includes: X=1.0, Y=2.5, Z=3.0
Distance to center: 4.0311

Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': Error on parameter 'abc': could not convert string to float: 'abc'
Enter new coordinates as floats in format 'x,y,z': Distance between the 2 sets of coordinates: 4.9244
```

- `printf '...'` imprime o texto entre aspas, com cada `\n` virando uma quebra de linha: são as
  quatro respostas, uma por linha;
- a barra vertical `|` (*pipe*, "cano") liga a saída do `printf` à entrada do programa: cada
  `input()` lê a próxima linha, como se ela tivesse sido digitada.

A saída é a mesma do enunciado, sem o texto digitado. Ao digitar, é o terminal que mostra na
tela as teclas apertadas, e a linha só muda quando o Enter é apertado. Com o `|`, nada é
digitado: as respostas não aparecem, e o que o programa imprime depois de cada pergunta cai na
mesma linha dela.

## Comparar letra por letra

Com as respostas prontas, o `diff` confere a saída inteira contra a versão esperada sem o texto
digitado:

```bash
diff <(cd ex2 && printf 'hello world\n1.0 , 2.5, 3.0\n4,abc,5\n4,5,6\n' | python3 ft_coordinate_system.py) - <<'FIM'
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': Invalid syntax
Enter new coordinates as floats in format 'x,y,z': Got a first tuple: (1.0, 2.5, 3.0)
It includes: X=1.0, Y=2.5, Z=3.0
Distance to center: 4.0311

Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': Error on parameter 'abc': could not convert string to float: 'abc'
Enter new coordinates as floats in format 'x,y,z': Distance between the 2 sets of coordinates: 4.9244
FIM
```

O `diff` não imprime nada.

## A entrada que acaba antes da hora

Com uma única resposta, inválida, a entrada acaba enquanto o programa ainda espera uma posição.
O `input()` seguinte lança `EOFError`, e o programa termina com a mensagem, sem traceback:

```bash
(cd ex2 && printf '1,2\n' | python3 ft_coordinate_system.py)
echo $?
```

```text
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': Invalid syntax
Enter new coordinates as floats in format 'x,y,z': 
Input interrupted - leaving the coordinate system
0
```

O código de saída `0` ([echo $?](../03-ex0/06-rodar-e-conferir.md#um-argumento-que-não-é-utf-8))
quer dizer que o programa terminou bem. Um programa que trava termina com um código diferente de
`0`: `1` numa exceção comum.

Rodando com o teclado, Ctrl-D numa linha vazia ou Ctrl-C no meio de uma pergunta mostram a mesma
mensagem.

## Valores fora da faixa

`1e200`, `nan` e `inf` são recusados um por um, e a posição seguinte, válida, é aceita:

```bash
(cd ex2 && printf '1e200,0,0\nnan,1,2\ninf,0,0\n1,2,3\n4,5,6\n' | python3 ft_coordinate_system.py)
```

```text
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': Error on parameter '1e200': out of range
Enter new coordinates as floats in format 'x,y,z': Error on parameter 'nan': out of range
Enter new coordinates as floats in format 'x,y,z': Error on parameter 'inf': out of range
Enter new coordinates as floats in format 'x,y,z': Got a first tuple: (1.0, 2.0, 3.0)
It includes: X=1.0, Y=2.0, Z=3.0
Distance to center: 3.7417

Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': Distance between the 2 sets of coordinates: 5.1962
```

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
Success: no issues found in 1 source file
```
