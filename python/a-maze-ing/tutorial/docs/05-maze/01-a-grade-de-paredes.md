---
sidebar_position: 1
title: A grade de paredes
---

# A grade de paredes

Gerar um labirinto é abrir paredes, uma a uma, numa grade que começa toda fechada. Os
algoritmos das próximas partes precisam de um lugar para guardar essas paredes enquanto
trabalham, e esse lugar precisa impedir que eles quebrem as regras do enunciado. Esta parte
constrói esse lugar: a classe `Maze`, em `mazegen/entities/maze.py`.

## Onde o `Maze` entra

O `Maze` é o labirinto **em construção**: a grade com as paredes de cada célula. Cada algoritmo
recebe o mesmo `Maze` e mexe nele, um depois do outro. O diagrama mostra a ordem em que eles
**rodam** ao gerar um labirinto:

```mermaid
flowchart LR
    novo["Maze novo<br/>tudo fechado"] --> carver["1. Carver<br/>cava os corredores"]
    carver --> braider["2. Braider<br/>abre paredes extras,<br/>só no modo Pac-Man"]
    braider --> solver["3. Solver<br/>acha o caminho mais curto"]
    solver --> pronto["grade pronta,<br/>copiada para fora do Maze"]
```

- O **Carver** cava um labirinto perfeito: um único caminho entre quaisquer duas células.
- O **Braider** transforma o labirinto perfeito num tabuleiro Pac-Man, abrindo paredes extras
  para criar rotas alternativas.
- O **Solver** acha o caminho mais curto da entrada à saída, no labirinto já pronto.
- No fim, a grade pronta sai do `Maze` como uma cópia, pelo método `rows`
  ([A cópia da grade](./08-a-copia-da-grade.md)).

A ordem em que o tutorial **constrói** essas classes é outra: o Carver na
[parte 6](../06-carver/01-labirinto-perfeito.md), o Solver na
[parte 7](../07-solver/01-busca-em-largura.md) e o Braider na
[parte 8](../08-braider/01-becos-sem-saida.md). O número da parte não é a ordem de execução.

## Por que o `Maze` é uma entidade

Uma **entidade** é um objeto cujo estado muda, mas que protege as próprias regras: nenhum dos
seus métodos deixa o objeto num estado proibido (os papéis estão na
[parte 2](../02-arquitetura/04-papeis-das-classes.md)). O `Maze` é a única entidade do gerador:
as paredes mudam o tempo todo, mas três regras do enunciado nunca podem quebrar:

- **coerência**: duas células vizinhas concordam sobre a parede que dividem. Se uma diz que tem
  parede à direita, a vizinha da direita diz que tem parede à esquerda;
- **borda fechada**: a volta toda da grade é parede;
- **"42" fechado**: as células que desenham o "42" mantêm as quatro paredes.

O `Maze` garante as três por conta própria. Nenhum algoritmo consegue quebrá-las, nem por
engano, porque toda mudança de parede passa por métodos do `Maze` que as conferem.

## Tudo começa fechado

```python
ALL_WALLS = 15
```

Relembrando a [parte 1](../01-o-problema/02-paredes-em-bits.md): as paredes de uma célula são um
número de 0 a 15. Cada lado da célula (Norte em cima, Leste à direita, Sul embaixo, Oeste à
esquerda) ocupa um **bit**, um dígito 0 ou 1 do número escrito em binário, e vale 1, 2, 4 ou 8:
o bit fica em 1 quando a parede está fechada. `15` é `1111` em binário (8 + 4 + 2 + 1): as quatro
paredes fechadas.

Toda célula nasce assim, e gerar o labirinto é **abrir** paredes. Começar fechado tem uma
vantagem: a borda e o "42" já nascem certos, e continuam certos só porque ninguém tem permissão
de abri-los.

## O que vem

O `Maze` é grande demais para uma página só. Ele é construído aos poucos, ao longo desta parte,
num único arquivo, `mazegen/entities/maze.py`:

| Página | Métodos | O problema que resolvem |
|---|---|---|
| [O construtor](./09-o-construtor.md) | `__init__` | criar a grade com todas as paredes fechadas |
| [Consultar a grade](./02-consultar-a-grade.md) | `__contains__`, `cells`, `walls` | a posição existe? quais são as células? quais paredes uma célula tem? |
| [Vizinhos: a borda e o "42"](./03-vizinhos.md) | `neighbour`, `is_open` | quem está do outro lado de uma parede? dá para passar? |
| [Abrir e fechar paredes](./04-abrir-e-fechar.md) | `open_wall`, `close_wall`, `_other_side` | mudar uma parede sem quebrar as regras |
| [Passagens e becos](./05-passagens-e-becos.md) | `passages`, `closed_sides`, `dead_ends` | por onde se anda? onde estão os becos sem saída? |
| [Contar ciclos](./06-contar-ciclos.md) | `loop_count` | o tabuleiro Pac-Man tem rotas alternativas suficientes? |
| [Áreas abertas 3x3](./07-areas-abertas-3x3.md) | `has_open_3x3`, `_window_open` | algum bloco 3x3 ficou sem paredes por dentro? |
| [A cópia da grade](./08-a-copia-da-grade.md) | `rows` | entregar a grade pronta sem deixar ninguém mexer nela |
