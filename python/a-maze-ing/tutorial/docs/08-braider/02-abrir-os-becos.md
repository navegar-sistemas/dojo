---
sidebar_position: 2
title: "Passo (a): abrir os becos"
---

# Passo (a): abrir os becos

O enunciado tolera no máximo um ou dois becos sem saída no tabuleiro Pac-Man, e o labirinto
perfeito costuma ter dezenas. O primeiro passo do `Braider` elimina os becos reais: para cada
um, derruba mais uma parede, e a célula passa a ter duas passagens. Esta página mostra o método
que faz isso, `_remove_dead_ends` ("remover becos").

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

O sublinhado no começo do nome (`_remove_dead_ends`) é a convenção do Python para "método interno":
só a própria classe o chama. Os parâmetros são o labirinto, alterado no lugar, e o `rng`, o
sorteador único do gerador ([parte 6](../06-carver/04-a-seed.md)).

## A ordem dos becos é sorteada

```python
        dead_ends = maze.dead_ends()
        rng.shuffle(dead_ends)
```

`maze.dead_ends()` devolve a lista dos becos reais na ordem da grade: linha a linha, de cima para
baixo. A ordem importa quando duas aberturas disputam o mesmo canto: uma parede que deixaria um
bloco 3x3 todo aberto é recusada (a regra do 3x3, na [página 4](./04-a-regra-do-3x3.md)). Se
duas aberturas, juntas, completariam um bloco 3x3, a primeira tentada fica e a segunda é
recusada. Com a lista sempre de cima para baixo, quem perderia seria sempre o beco de baixo, em
todo tabuleiro; embaralhar a lista sorteia quem perde. `rng.shuffle` embaralha a lista com o mesmo sorteador do `Carver`, então a
semente continua fixando o resultado.

O embaralhamento só sai igual com a mesma semente porque a lista de entrada vem sempre na mesma
ordem: `dead_ends()` devolve uma `list` montada linha a linha, nunca um `set`, que não tem ordem
garantida.

## O `continue`: becos que já se resolveram

```python
        for cell in dead_ends:
            if len(maze.passages(cell)) != 1:
                # An earlier opening already linked this cell.
                continue
```

A lista de becos é calculada **uma vez, antes** de derrubar qualquer parede. Se dois becos são
vizinhos e a parede derrubada para o primeiro é justamente a que separa os dois, o segundo também
ganha uma passagem e deixa de ser beco. Quando o laço chega a ele, `len(maze.passages(cell))`
(o número de lados abertos) já é 2, diferente de 1, e o `continue` pula para o próximo da lista.

![Grade 4 por 3 em três quadros: perfeita com 2 becos vizinhos; depois do passo (a), uma única parede verde resolveu os dois; depois do passo (b), mais uma parede verde](/img/braider/passos-4x3.svg)

Linhas escuras são paredes; a verde é a parede derrubada naquele passo; laranja marca os becos
reais. No primeiro quadro (semente 32), os dois becos laranja estão um em cima do outro. No
segundo, a parede verde entre eles foi derrubada para o primeiro, e o segundo já não precisa de
nada. Sem o teste, o `Braider` derrubaria uma segunda parede numa célula que já não era beco. O
terceiro quadro é o passo seguinte, explicado na [página 3](./03-criar-ciclos.md).

## Qual parede derrubar

```python
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break
```

- `closed_sides` lista só os lados fechados que dão para uma célula livre: nunca a borda, nunca o
  "42".
- A ordem dos candidatos também é sorteada, para o beco não abrir sempre para o mesmo lado.
- `_open_without_3x3` derruba a parede e a fecha de novo se ela tiver formado um bloco 3x3 todo
  aberto, que o enunciado proíbe. Ele devolve `True` quando a parede ficou aberta e `False` quando
  precisou desfazer ([página 4](./04-a-regra-do-3x3.md)). Com `False`, o laço tenta o próximo
  lado.
- `break` sai do laço no primeiro lado aceito: uma parede por beco basta.

Se todos os lados formariam um 3x3, o beco fica. É raro, e o `MazeGenerator` confere o resultado
no fim ([parte 9](../09-gerador/03-generate.md)).

## Uma passada basta

Derrubar uma parede só **aumenta** o número de passagens das duas células que a dividem. Nenhuma
abertura transforma uma célula em beco. Por isso não é preciso recalcular a lista nem repetir o
passo: todo beco da lista foi tratado, e nenhum beco novo surgiu.

## O resultado

Num labirinto 20x15 com a semente 42, o labirinto perfeito tem 32 becos reais, e o passo (a)
derruba 32 paredes. Aqui nenhum par de becos era vizinho, então nenhuma parede resolveu dois de
uma vez, como no 4x3 acima: cada beco precisou da sua. À esquerda, o labirinto perfeito com os
becos reais em laranja; à direita, o tabuleiro, com as paredes derrubadas marcadas em verde. Nos
dois, cinza é o "42" e amarelo são os dois becos cercados, dentro do "42", que continuam lá:

![Labirinto 20 por 15 antes e depois do braiding, com 32 becos reais em laranja e as 32 paredes abertas em verde](/img/braider/antes-depois.svg)

Antes da primeira abertura, o labirinto é uma árvore: liga todas as células livres. Por isso
qualquer parede derrubada liga duas células que **já** estavam ligadas por outro caminho e
acrescenta exatamente **um ciclo** ([página 3](./03-criar-ciclos.md)). Depois dela, o labirinto
deixa de ser árvore, mas continua ligando todas as células, e o mesmo vale para a abertura
seguinte, e para a outra: cada parede derrubada acrescenta um ciclo. As 32 aberturas dão 32
ciclos, muito mais que os 2 exigidos. Em grades desse tamanho, o passo (a) sozinho já cumpre a
regra dos ciclos.
