---
sidebar_position: 2
title: "Passo (a): abrir os becos"
---

# Passo (a): abrir os becos

Para desfazer um beco real, basta abrir uma de suas paredes fechadas: a célula passa a ter duas
passagens e deixa de ser beco. O passo (a) faz isso com cada beco, em ordem aleatória.

## O código

```python
    def _remove_dead_ends(self, maze: Maze, rng: random.Random) -> None:
        """Open one wall of every real dead end, in random order.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        dead_ends = maze.dead_ends()
        rng.shuffle(dead_ends)
        for cell in dead_ends:
            if len(maze.passages(cell)) != 1:
                # An earlier opening already linked this cell.
                continue
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break
```

## A ordem é sorteada

`maze.dead_ends()` lista os becos na ordem de `maze.cells()`: linha a linha, de cima para
baixo. Percorrer nessa ordem favoreceria sempre os becos de cima, que abrem primeiro e às vezes
resolvem os de baixo de graça. `rng.shuffle` embaralha a lista com o mesmo `random.Random` do
`Carver`, então a seed continua fixando o resultado.

`shuffle` só é reprodutível porque a lista de entrada vem sempre na mesma ordem: `dead_ends()`
devolve uma `list` montada linha a linha, nunca um `set`.

## O `continue`

A lista é calculada **antes** de abrir qualquer parede. Se dois becos são vizinhos e a parede
aberta para o primeiro é justamente a que os separa, os dois deixam de ser becos com uma abertura
só. Quando o laço chega ao segundo, ele já tem duas passagens: `len(maze.passages(cell)) != 1`
e o `continue` o pula.

Sem esse teste, o `Braider` abriria uma segunda parede numa célula que já não precisava.

## Qual parede abrir

```python
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break
```

- `closed_sides` só lista lados fechados que dão para uma célula livre: nunca a borda, nunca o
  "42".
- A ordem dos candidatos também é sorteada, para o beco não abrir sempre para o mesmo lado.
- `_open_without_3x3` abre a parede e a fecha de volta se ela completar um bloco 3x3 aberto,
  devolvendo `False` ([página 4](./04-a-regra-do-3x3.md)). Nesse caso, o laço tenta o próximo lado.
- `break` no primeiro lado aceito: uma parede por beco basta.

Se todos os lados completariam um 3x3, o beco fica. É raro, e o `MazeGenerator` confere o
resultado no fim (parte 9).

## Uma passada basta

Abrir uma parede só **aumenta** o número de passagens das duas células envolvidas. Nenhuma
abertura transforma uma célula em beco. Por isso não é preciso recalcular a lista nem repetir o
passo: o que era beco foi tratado, e nenhum beco novo surgiu.

## O resultado

Num labirinto 20x15 com seed 42, o passo (a) abre 32 paredes, uma para cada beco real. À
esquerda o labirinto perfeito com os becos em amarelo; à direita o tabuleiro, com as paredes
abertas marcadas em verde:

![Labirinto 20 por 15 antes e depois do braiding, com 32 becos em amarelo e as 32 paredes abertas em verde](/img/braider/antes-depois.svg)

Os dois becos em laranja, dentro do "42", são os cercados: continuam lá.

Cada parede aberta numa árvore liga duas células que já estavam ligadas por outro caminho, e por
isso cria exatamente **um ciclo**. As 32 aberturas dão 32 ciclos, muito mais que os 2 exigidos.
Em grades desse tamanho, o passo (a) sozinho já cumpre a regra dos ciclos.
