---
sidebar_position: 1
title: Busca em largura
---

# Busca em largura

O `Solver` encontra o **caminho mais curto** da entrada até a saída e o devolve em letras `N`,
`E`, `S`, `W`, uma por passo. O `MazeGenerator` o chama uma vez por labirinto e guarda o
resultado em `solution` (parte 9); dali ele vai para a terceira linha do rodapé do arquivo de
saída e para o desenho do caminho na tela.

## Camadas de distância

A **busca em largura** (BFS, *breadth-first search*) explora o labirinto em camadas:

1. a entrada está a distância 0;
2. as células ligadas a ela por uma passagem estão a distância 1;
3. as células ligadas às de distância 1, e ainda não vistas, estão a distância 2;
4. e assim por diante, até não sobrar célula alcançável.

Num tabuleiro Pac-Man 9x7 (`seed=4`), o número em cada célula é a distância até a entrada `(0, 0)`;
quanto mais escuro, mais longe:

![Tabuleiro 9 por 7 com a distância até a entrada escrita em cada célula](/img/solver/camadas.svg)

A saída, no canto de baixo à direita, está a 14 passos. Seguir os números de 14 até 0, sempre
para uma vizinha com o número anterior, desenha um caminho mais curto:

![O mesmo tabuleiro com o caminho mais curto de 14 passos em ciano](/img/solver/caminho.svg)

## A fila

Para visitar as células em ordem de distância, a BFS usa uma **fila** (*FIFO*: o primeiro a
entrar é o primeiro a sair):

1. põe a entrada na fila;
2. tira a célula da frente;
3. põe no fim da fila cada vizinha alcançável por uma passagem e ainda não descoberta;
4. repete enquanto a fila tiver células.

Todas as células de distância `d` entram na fila antes de qualquer uma de distância `d + 1`,
porque só são descobertas a partir das de distância `d − 1`, que saíram antes. A fila sempre
contém, da frente para o fim, distâncias que só crescem.

## Por que o primeiro caminho encontrado é o mais curto

Toda passagem custa 1 passo. Quando uma célula é descoberta pela primeira vez, ela vem de uma
célula da camada mais baixa possível: se existisse um caminho mais curto até ela, ela teria sido
descoberta antes, numa camada anterior. Logo, a distância da primeira descoberta é a mínima, e
isso vale para a saída também.

## Por que não outro algoritmo

| Alternativa | Por que não |
|---|---|
| busca em profundidade (a do `Carver`) | encontra **um** caminho, não o mais curto. No modo perfeito o caminho é único e daria certo, mas no Pac-Man há ciclos e ela pode dar a volta longa |
| Dijkstra | resolve caminhos com custos diferentes por passagem; aqui todo passo custa 1, e com custo igual Dijkstra faz exatamente o que a BFS faz, com uma fila de prioridade a mais |
| A* | acelera a busca com uma estimativa da distância restante; 100x100 são 10 000 células e a BFS já as percorre num instante |

## `deque` em vez de `list`

A fila é um `collections.deque`. Tirar da frente com `deque.popleft()` custa sempre o mesmo;
`list.pop(0)` desloca todos os elementos restantes uma posição para a esquerda, e o custo cresce
com o tamanho da fila.
