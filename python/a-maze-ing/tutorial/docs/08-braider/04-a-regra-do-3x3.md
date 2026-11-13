---
sidebar_position: 4
title: A regra do 3x3
---

# A regra do 3x3

Cada parede que o `Braider` derruba aproxima o labirinto de um salão aberto, e o enunciado proíbe
salões. Toda abertura feita nos passos (a) e (b) precisa, então, ser conferida e desfeita se
quebrar a regra. Esta página mostra a regra e o método que abre uma parede só se ela não a quebrar.

## O que o enunciado proíbe

Nas palavras do enunciado: "O labirinto não pode ter grandes áreas abertas. Corredores não podem
ter mais de 2 células de largura. Por exemplo, você pode ter uma área aberta 2x3 ou 3x2, mas nunca
uma área aberta 3x3."

![Um bloco 3 por 3 todo aberto, proibido, ao lado de blocos 2 por 3 e 3 por 2 abertos, permitidos](/img/braider/area-3x3.svg)

Linhas cheias são paredes fechadas e linhas tracejadas são passagens. Vermelho claro marca o
bloco proibido; verde, os permitidos.

Um bloco de 3x3 células está **aberto** quando as 12 paredes de dentro dele estão abertas: as 6
paredes Leste das duas primeiras colunas e as 6 paredes Sul das duas primeiras linhas. As paredes
da volta do bloco não contam: um bloco todo aberto por dentro é um salão, mesmo cercado.

![Bloco 3 por 3 com as 6 paredes Leste internas em azul e as 6 paredes Sul internas em laranja](/img/braider/paredes-internas-3x3.svg)

Para encontrar um salão, o `Maze` confere todos os blocos 3x3 que cabem na grade, chamados de
**janelas**, no método `has_open_3x3()` ([parte 5](../05-maze/07-areas-abertas-3x3.md)). Numa
grade 5x4 cabem 3 × 2 = 6 janelas:

![As 6 janelas 3 por 3 de uma grade 5 por 4, cada uma destacada em amarelo](/img/braider/janelas-5x4.svg)

Cada quadro destaca uma janela em amarelo; a legenda dá a célula do canto de cima à esquerda da
janela. O canto vai de `0,0` a `2,1`: 3 posições na horizontal (5 − 3 + 1) vezes 2 na vertical
(4 − 3 + 1).

## Onde um 3x3 aberto pode aparecer

- **No labirinto perfeito, nunca.** Um 3x3 aberto tem 12 passagens entre 9 células, e uma árvore
  de 9 células só tem 8 ([parte 6](../06-carver/01-labirinto-perfeito.md)). O `Carver` não precisa
  conferir nada.
- **No braiding, sim.** Cada parede derrubada pelo `Braider` cria um ciclo, e ciclos suficientes
  no mesmo canto acabam abrindo um 3x3 inteiro.

Por isso **toda** abertura do `Braider`, nos dois passos, passa pelo mesmo método:
`_open_without_3x3` ("abrir sem 3x3").

## Abrir, olhar e desfazer

```python
    @staticmethod
    def _open_without_3x3(maze: Maze, cell: Cell, side: Direction) -> bool:
        """Open a wall and undo it when a 3x3 window becomes fully open.

        Args:
            maze: Maze changed in place.
            cell: Cell on one side of the wall.
            side: Side of the wall.

        Returns:
            True when the wall stayed open.
        """
        maze.open_wall(cell, side)
        if maze.has_open_3x3():
            maze.close_wall(cell, side)
            return False
        return True
```

1. derruba a parede: `open_wall` abre o lado `side` da célula `cell` e o lado oposto da vizinha
   ([parte 5](../05-maze/04-abrir-e-fechar.md));
2. pergunta ao `Maze` se agora existe algum 3x3 aberto;
3. se existe, foi esta parede que o completou, porque antes não havia nenhum: o labirinto
   perfeito não tem nenhum 3x3 aberto, e toda abertura anterior passou por esta mesma
   conferência, que desfaz qualquer uma que tenha completado um. `close_wall` fecha a parede de
   novo, e o método devolve `False`;
4. senão, a parede fica aberta e o método devolve `True`.

![Bloco 3 por 3 com 11 paredes abertas e a candidata em vermelho; aberta, o bloco fica todo aberto; close_wall a fecha de novo](/img/braider/desfazer.svg)

Nos três quadros, linha cheia é parede fechada e linha tracejada é parede aberta (passagem). No
primeiro, a parede vermelha é a candidata, ainda fechada. No segundo, ela foi aberta e o bloco
inteiro, em vermelho claro, ficou aberto. No terceiro, `close_wall` a fechou de novo.

`close_wall` existe para isto: é o único lugar do pacote que fecha uma parede depois de aberta.

## Por que abrir para depois conferir

A alternativa seria **prever**: antes de abrir, examinar as janelas 3x3 que contêm a parede e
calcular se alguma ficaria toda aberta. Abrir e conferir é mais simples:

- a regra do 3x3 fica escrita num lugar só, `has_open_3x3`, e o `Braider` só a consulta;
- a parede é conferida no estado real da grade, sem simular nada;
- desfazer é uma linha, porque `close_wall` é o espelho exato de `open_wall`.

O custo é percorrer todas as janelas da grade depois de cada abertura. Em 100x100 são 98 × 98 =
9604 janelas, mas quase todas param de ser examinadas na primeira parede fechada encontrada, e o
tabuleiro Pac-Man 100x100 sai em poucos segundos. Conferir só as janelas que contêm a parede
derrubada seria mais rápido, com mais código; a versão simples é escolha do projeto.

Quantas janelas contêm uma parede? Pegue a parede Leste da célula `x,y`, entre as colunas `x` e
`x+1`. Uma janela a contém por dentro quando as duas colunas cabem nas 3 colunas da janela: o
canto esquerdo da janela pode estar na coluna `x − 1` ou `x` (2 opções). Na vertical, a linha `y`
precisa estar entre as 3 linhas da janela: o canto de cima pode estar em `y − 2`, `y − 1` ou `y`
(3 opções). São 2 × 3 = 6 janelas, no máximo; perto da borda, menos. Para uma parede Sul, a conta
é a mesma com linhas e colunas trocadas.

## Por que `@staticmethod`

Um método comum recebe o próprio objeto como primeiro parâmetro, `self`. Este método não usa
`self`: tudo de que precisa chega pelos parâmetros. O `@staticmethod` (um **decorador**, a linha com
`@` logo acima do `def`, que muda o comportamento da função) diz ao Python que o método não recebe
`self`, e deixa isso explícito para quem lê.

Um `@staticmethod` pode ser chamado de dois jeitos, e os dois fazem a mesma coisa: pelo nome da
classe, `Braider._open_without_3x3(maze, cell, side)`, ou por um objeto da classe,
`self._open_without_3x3(maze, cell, side)`. Em nenhum dos dois o Python passa o objeto como
primeiro parâmetro. Os dois passos usam a forma com `self`, porque já estão dentro de um método
do objeto.

## O valor devolvido

O `-> bool` da assinatura diz que o método devolve `True` ou `False`:

| Quem chama | O que faz com o resultado |
|---|---|
| passo (a), um beco | `True` encerra a busca de uma parede para aquele beco; `False` tenta o próximo lado |
| passo (b), os ciclos | ignora: a parede recusada fica fechada e o laço segue para a próxima |
