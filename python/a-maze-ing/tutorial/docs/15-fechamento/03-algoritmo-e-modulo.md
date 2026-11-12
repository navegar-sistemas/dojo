---
sidebar_position: 3
title: Algoritmo e módulo reutilizável
---

# Algoritmo e módulo reutilizável

## Algorithm

O subject pede duas coisas separadas: **qual** algoritmo e **por que** ele. A seção tem um
tópico por peça do gerador, cada um com o nome da técnica e o motivo da escolha.

- **Labirinto perfeito: recursive backtracker iterativo.** Uma busca em profundidade aleatória,
  com pilha explícita, a partir da entrada, sem entrar no "42". Os motivos vêm com números
  medidos: a estrutura é só uma pilha e uma lista de vizinhos; cada célula entra e sai da pilha
  uma vez; os corredores saem longos, com poucos becos (de 24 a 37 em 20x15, contra 74 a 95 do
  Kruskal e 77 a 97 do Prim, nas seeds 1 a 100). Menos becos são menos paredes a abrir no modo
  Pac-Man.
- **Tabuleiro Pac-Man: braiding.** O mesmo labirinto perfeito, depois uma parede aberta em cada
  beco e, se ainda faltar, paredes extras até 2 ciclos; com mais de 2 becos reais ou menos de 2
  ciclos, o gerador refaz a grade, até 20 tentativas.
- **Nenhum 3x3 aberto.** Como a regra é implementada **e como é verificada**: o labirinto
  perfeito é uma árvore e não comporta um 3x3 aberto, que teria ciclos; no Pac-Man,
  `Maze.has_open_3x3` percorre todas as janelas 3x3 depois de cada abertura, e `close_wall`
  desfaz a abertura que completaria uma. O avaliador pergunta isso na defesa, e a resposta já
  está escrita.
- **Caminho mais curto:** busca em largura a partir da entrada, vizinhos na ordem N, E, S, W.
- **O "42":** os dois glifos, o tamanho do bloco e a fórmula do canto superior esquerdo.

"Por que" não é "porque é o mais conhecido". É o que o algoritmo dá de concreto ao projeto: aqui,
poucos becos, que é exatamente o que o modo padrão precisa eliminar. As partes 6 a 8 explicam
cada escolha em detalhe; o README resume.

Se você mediu outros números, ou escolheu outro algoritmo, escreva os seus. O motivo precisa
ser verdadeiro para o **seu** código.

## Reusable module

O subject pede que o README principal também tenha a documentação curta do módulo: como
instanciar, como passar parâmetros, como ler a estrutura gerada e uma solução, com um exemplo.

A seção começa dizendo **qual** parte é reutilizável e **como** obtê-la:

```markdown
The reusable part of the project is the `mazegen` package; it is the only
code that goes into the wheel. Install it with
`pip install mazegen-1.0.0-py3-none-any.whl`.
```

Depois vem o mesmo texto da docstring de `mazegen/__init__.py` (parte 9): cada parâmetro com
nome, tipo, valor padrão e exemplo; os erros do construtor; `grid`, `solution` e `pattern` e
como lê-los. Repetir o texto, em vez de escrever outro, mantém uma só documentação: quem lê o
README no GitHub e quem faz `help(mazegen)` depois de instalar o wheel leem a mesma coisa.

A diferença está no exemplo. Na docstring ele vem indentado depois de `Example:`; no README, num
bloco de código Python, para ser destacado e copiado:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
walls = gen.grid[0][0]
print("north wall of (0, 0) closed:", bool(walls & 1))
print(len(gen.pattern), "cells draw the 42")
print(gen.solution)
```

Num venv com o wheel instalado, ele imprime:

```text
north wall of (0, 0) closed: True
18 cells draw the 42
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

O exemplo mostra as três coisas que o subject pede: instanciar com parâmetros (`width`,
`height`, `seed`), ler a estrutura (`grid`, com o bit Norte) e ler uma solução (`solution`).
