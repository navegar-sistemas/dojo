---
sidebar_position: 3
title: "Passo (b): até dois ciclos"
---

# Passo (b): até dois ciclos

O enunciado pede, no modo Pac-Man, pelo menos **duas rotas independentes**, para que um jogador
perseguido sempre tenha uma alternativa; e diz com todas as letras que um labirinto perfeito com
uma única parede removida, que tem um ciclo só, não basta. Na maioria das grades o passo (a) já
deixa ciclos de sobra, mas não em todas. O segundo passo do `Braider` garante o mínimo: derruba
paredes sorteadas até o labirinto ter 2 ciclos. Antes do código, é preciso saber contar ciclos.

## Ciclos independentes

Um **ciclo** é um caminho que sai de uma célula e volta a ela por outro lado, sem repetir
passagem. Numa grade 3x2 sem nenhuma parede por dentro, dá para desenhar três voltas:

![Grade 3 por 2 aberta, três vezes: o ciclo do quadrado da esquerda, o do quadrado da direita e a volta inteira](/img/braider/ciclos-independentes.svg)

As linhas tracejadas são as passagens, e a faixa ciano é a volta de cada quadro.

Mas a volta inteira não é uma rota nova. Olhe para as passagens que cada ciclo usa:

- o ciclo 1, o quadrado da esquerda, usa 4 passagens, entre elas a do meio (entre `1,0` e `1,1`);
- o ciclo 2, o quadrado da direita, usa outras 4, entre elas a mesma passagem do meio;
- juntando as 8 e tirando a do meio, que aparece nas duas, sobram 6 passagens: exatamente as da
  volta inteira.

Ou seja, a volta inteira é feita só de pedaços dos dois quadrados. Quem já tem os dois quadrados
como rotas de fuga não ganha nada de novo com ela. Ciclos **independentes** são os que não se
montam assim, com pedaços de outros. Nessa grade são 2, os dois quadrados, e é esse número que a
regra do enunciado conta.

## A conta: passagens − células + 1

O `Maze` conta os ciclos independentes no método `loop_count()`
([parte 5](../05-maze/06-contar-ciclos.md)), com uma conta simples:

```text
ciclos = passagens − células livres + 1
```

O raciocínio:

1. um labirinto perfeito é uma árvore: liga as `C` células livres com exatamente `C − 1`
   passagens e não tem ciclo nenhum ([parte 6](../06-carver/01-labirinto-perfeito.md));
2. cada passagem **a mais** liga duas células que já estavam ligadas e cria exatamente uma rota
   nova: um ciclo independente;
3. então o número de ciclos é o número de passagens que sobram além das `C − 1` da árvore:
   `passagens − (C − 1)`, que é o mesmo que `passagens − C + 1`.

Na grade 3x2 aberta: 7 passagens, 6 células, `7 − 6 + 1 = 2`.

## Quando o passo (a) não basta

Em grades grandes, o passo (a) derruba dezenas de paredes e deixa dezenas de ciclos. Em grades
pequenas há poucos becos, e às vezes dois deles são vizinhos e se resolvem com uma parede só.
Numa grade 4x3 com a semente 32, cada quadro mostra a conta dos ciclos:

![Grade 4 por 3: perfeita com 11 passagens e 0 ciclos; depois do passo (a) com 12 passagens e 1 ciclo; depois do passo (b) com 13 passagens e 2 ciclos](/img/braider/passos-4x3.svg)

Laranja marca os becos reais, e verde a parede derrubada naquele passo.

1. o labirinto perfeito tem 12 células e 11 passagens: 0 ciclos, 2 becos;
2. o passo (a) derruba a parede entre os dois becos (em verde). Os dois deixam de ser becos com
   uma parede só, e sobra 1 ciclo, menos que os 2 exigidos;
3. o passo (b) derruba mais uma parede sorteada: 13 passagens, 2 ciclos.

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

`_add_loops` quer dizer "acrescentar ciclos" (*loop* é outro nome para ciclo).

## A lista de paredes candidatas

O trecho entre colchetes é uma **compreensão de lista** (em inglês, *list comprehension*): um
jeito curto de montar uma lista com laços. Ele equivale a:

```python
walls = []
for cell in maze.cells():
    for side in maze.closed_sides(cell):
        if side in (Direction.EAST, Direction.SOUTH):
            walls.append((cell, side))
```

Ou seja: para cada célula livre, para cada lado fechado que dá para outra célula livre, se o lado
for Leste ou Sul, guarda o par.

Cada item é um par `(célula, lado)` que identifica uma parede; a anotação
`list[tuple[Cell, Direction]]` diz exatamente isso.

O filtro `if side in (Direction.EAST, Direction.SOUTH)` existe porque toda parede interna tem dois
nomes: o Leste de `x,y` é o Oeste de `x+1,y`, e o Sul de `x,y` é o Norte de `x,y+1`. Listar os
quatro lados de cada célula poria cada parede duas vezes na lista, e ela teria o dobro de chance de
ser sorteada. Ficando só com Leste e Sul, cada parede aparece uma vez. Como `closed_sides` já
descarta a borda e o "42", a lista tem exatamente as paredes internas fechadas que podem ser
derrubadas.

## Parar na hora certa

- `rng.shuffle(walls)` sorteia a ordem com o mesmo sorteador de sempre.
- `for cell, side in walls:` desmonta cada par em duas variáveis.
- Antes de cada tentativa, `maze.loop_count() >= MIN_LOOPS` confere se já há ciclos suficientes; se
  há, `return` encerra o método. Quando o passo (a) já deixou 2 ciclos ou mais, isso acontece na
  primeira volta, e nenhuma parede é derrubada.
- O resultado de `_open_without_3x3` é ignorado: se a parede formaria um 3x3 aberto, ela volta a
  ficar fechada e o laço passa para a próxima da lista.

`loop_count()` percorre o labirinto inteiro a cada chamada. Isso só pesaria se o passo (b)
derrubasse muitas paredes, e ele só trabalha de verdade em grades pequenas, onde percorrer tudo é
barato.

## `MIN_LOOPS`

`MIN_LOOPS = 2` é uma constante no topo do módulo, junto de `MAX_DEAD_ENDS = 2`:

```python
MIN_LOOPS = 2
MAX_DEAD_ENDS = 2
```

São os números das regras do enunciado: pelo menos 2 ciclos e no máximo 2 becos. O `Braider` usa
`MIN_LOOPS` para saber quando parar, e o `MazeGenerator` importa as duas para conferir o resultado
([parte 9](../09-gerador/03-generate.md)). Os números ficam escritos num lugar só.
