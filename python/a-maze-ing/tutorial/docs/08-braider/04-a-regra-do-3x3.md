---
sidebar_position: 4
title: A regra do 3x3
---

# A regra do 3x3

## O que o subject proíbe

"O labirinto não pode ter grandes áreas abertas. Corredores não podem ter mais de 2 células de
largura. Por exemplo, você pode ter uma área aberta 2x3 ou 3x2, mas nunca uma área aberta 3x3."

![Um bloco 3 por 3 todo aberto, proibido, ao lado de blocos 2 por 3 e 3 por 2 abertos, permitidos](/img/braider/area-3x3.svg)

Um bloco 3x3 está **aberto** quando suas 12 paredes internas estão abertas: as 6 paredes Leste
das duas primeiras colunas e as 6 paredes Sul das duas primeiras linhas. As paredes da volta do
bloco não contam. O `Maze` da parte 5 testa cada janela 3x3 da grade em `has_open_3x3()`.

## Onde o 3x3 pode aparecer

- **No labirinto perfeito, nunca.** Um 3x3 aberto tem 12 passagens entre 9 células, e uma
  árvore só comporta 8. O `Carver` não precisa checar nada.
- **No braiding, sim.** Cada parede aberta pelo `Braider` cria um ciclo, e ciclos suficientes no
  mesmo canto completam um 3x3.

Por isso **toda** abertura do `Braider`, nos dois passos, passa pelo mesmo método:
`_open_without_3x3`.

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

1. abre a parede;
2. pergunta ao `Maze` se agora existe algum 3x3 aberto;
3. se existe, foi esta parede que o completou, porque antes não havia nenhum: fecha de volta e
   devolve `False`;
4. senão, a parede fica aberta e o método devolve `True`.

![Bloco 3 por 3 com 11 paredes abertas e a candidata em vermelho; aberta, o bloco fica todo aberto; close_wall a fecha de novo](/img/braider/desfazer.svg)

`close_wall` (parte 5) existe para isto: é o único lugar do pacote que fecha uma parede depois de
aberta.

## Por que abrir para depois testar

A alternativa seria **prever**: antes de abrir, examinar as janelas 3x3 que contêm a parede e
calcular se alguma ficaria completa. Abrir e testar é mais simples:

- a regra do 3x3 fica escrita num lugar só, `has_open_3x3`, e o `Braider` só a consulta;
- a parede é testada no estado real da grade, sem simular nada;
- desfazer é uma linha, porque `close_wall` é o espelho exato de `open_wall`.

O custo é percorrer todas as janelas da grade depois de cada abertura. Em 100x100 são 98 × 98 =
9604 janelas, mas quase todas param na primeira parede fechada que encontram, então o
tabuleiro Pac-Man 100x100 sai em poucos segundos. Testar só as janelas em volta da parede aberta
(no máximo 6 numa parede interna) seria mais rápido e é mais código.

## Por que `@staticmethod`

O método não usa `self`: tudo de que precisa chega por parâmetro. `@staticmethod` deixa isso
explícito. Ele continua sendo chamado como `self._open_without_3x3(...)` pelos dois passos.

## O valor devolvido

| Quem chama | O que faz com o `bool` |
|---|---|
| passo (a) | `True` encerra a busca por uma parede para aquele beco; `False` tenta o próximo lado |
| passo (b) | ignora: a parede recusada fica fechada e o laço segue para a próxima |
