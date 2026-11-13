---
sidebar_position: 1
title: O problema
---

# O problema

Num jogo em 3D, a posição de um jogador são três números: `x` (para os lados), `y` (para a
frente e para trás) e `z` (para cima e para baixo). O programa pede ao usuário duas posições,
digitadas no teclado, e calcula a distância entre elas. Uma posição digitada errada não pode
travar o programa: ele avisa e pergunta de novo.

## O que o enunciado pede

Um arquivo `ex2/ft_coordinate_system.py`, que pode usar `import math`, `math.sqrt()`, `input()`,
`round()` e `print()`, com uma função **`get_player_pos()`** que:

- pede ao usuário as coordenadas no formato `x,y,z`, três números separados por vírgula;
- trata as entradas erradas;
- pergunta de novo até receber uma posição válida;
- devolve a posição como uma **tupla** `(x, y, z)`.

Com ela, o programa:

1. lê uma primeira posição;
2. mostra a tupla e depois cada coordenada separada;
3. calcula a distância dessa posição até o centro do mundo, `(0, 0, 0)`;
4. lê uma segunda posição;
5. calcula a distância entre a segunda e a primeira.

## A saída esperada

O texto depois de cada `'x,y,z': ` é o que o usuário digitou:

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

Dois tipos de erro aparecem:

- `hello world` não tem três partes separadas por vírgula: `Invalid syntax` ("sintaxe
  inválida");
- `4,abc,5` tem três partes, mas `abc` não é número: a mensagem diz qual parte falhou e repete o
  erro do Python.

Já `1.0 , 2.5, 3.0`, com espaços em volta das vírgulas, é aceito. As distâncias saem com quatro
casas depois do ponto.
