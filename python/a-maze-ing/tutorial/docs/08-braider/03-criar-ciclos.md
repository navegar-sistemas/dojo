---
sidebar_position: 3
title: "Passo (b): até dois ciclos"
---

# Passo (b): até dois ciclos

O subject pede pelo menos **duas rotas independentes**: um jogador perseguido precisa sempre de
uma alternativa. Um labirinto perfeito com uma única parede removida tem só um ciclo e não
serve.

## Contando ciclos

O `Maze` da parte 5 conta os ciclos independentes com uma fórmula de grafos:

```text
loop_count = passagens − células livres + 1
```

Numa árvore, `passagens = células − 1`, então o resultado é 0. Cada parede aberta depois disso
soma 1.

## Quando o passo (a) não basta

Em grades grandes, o passo (a) abre dezenas de paredes e deixa dezenas de ciclos. Em grades
pequenas e finas há poucos becos, e às vezes dois deles são vizinhos e se resolvem com uma
abertura só. Numa grade 4x3 com seed 32:

![Grade 4 por 3: perfeita com 2 becos; depois do passo (a) com 1 ciclo; depois do passo (b) com 2 ciclos](/img/braider/passos-4x3.svg)

1. o labirinto perfeito tem 2 becos, um em cima do outro, na coluna da esquerda;
2. o passo (a) abre a parede entre eles (em verde): os dois deixam de ser becos, e o
   `continue` pula o segundo. Fica 1 ciclo;
3. o passo (b) abre mais uma parede aleatória: 2 ciclos.

## O código

```python
    def _add_loops(self, maze: Maze, rng: random.Random) -> None:
        """Open random inner walls until the maze has MIN_LOOPS cycles.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        walls: list[tuple[Cell, Direction]] = [
            (cell, side)
            for cell in maze.cells()
            for side in maze.closed_sides(cell)
            # East and South list every inner wall exactly once.
            if side in (Direction.EAST, Direction.SOUTH)
        ]
        rng.shuffle(walls)
        for cell, side in walls:
            if maze.loop_count() >= MIN_LOOPS:
                return
            self._open_without_3x3(maze, cell, side)
```

## Cada parede uma vez

Toda parede interna tem dois nomes: o Leste de `(x, y)` é o Oeste de `(x + 1, y)`; o Sul de
`(x, y)` é o Norte de `(x, y + 1)`. Listar os quatro lados de cada célula poria cada parede duas
vezes na lista, e ela teria o dobro de chances de ser sorteada.

O filtro `side in (Direction.EAST, Direction.SOUTH)` fica só com um dos nomes. Como
`closed_sides` já descarta a borda e o "42", a lista tem exatamente as paredes internas fechadas
que podem ser abertas.

## Parar na hora certa

- `rng.shuffle(walls)` sorteia a ordem com o mesmo `random.Random` de sempre.
- Antes de cada tentativa, `maze.loop_count() >= MIN_LOOPS` encerra o método. Quando o passo (a)
  já deixou 2 ciclos ou mais, o `return` acontece na primeira volta e nenhuma parede é aberta.
- O resultado de `_open_without_3x3` é ignorado: se a parede completaria um 3x3, ela volta a
  ficar fechada e o laço passa para a próxima da lista.

`loop_count()` percorre o labirinto inteiro a cada chamada. Isso só pesa quando o passo (b) abre
muitas paredes, e ele só trabalha em grades pequenas, onde percorrer tudo é barato.

## `MIN_LOOPS`

`MIN_LOOPS = 2` é uma constante do módulo, junto de `MAX_DEAD_ENDS = 2`:

```python
MIN_LOOPS = 2
MAX_DEAD_ENDS = 2
```

O `Braider` usa `MIN_LOOPS` para saber quando parar, e o `MazeGenerator` importa as duas para
conferir o resultado (parte 9). As regras do subject ficam escritas num lugar só.
