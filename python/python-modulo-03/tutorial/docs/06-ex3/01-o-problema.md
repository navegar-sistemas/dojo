---
sidebar_position: 1
title: O problema
---

# O problema

Jogos dão **conquistas** (*achievements*) a quem cumpre desafios: "Boss Slayer" por derrotar um
chefe, "Speed Runner" por terminar rápido. Cada jogador tem as suas, sem repetição: ganhar a
mesma conquista duas vezes não a duplica. O programa sorteia as conquistas de quatro jogadores e
compara os grupos: o que todos têm, o que só um tem, o que falta a cada um.

## O que o enunciado pede

Um arquivo `ex3/ft_achievement_tracker.py`, que pode usar `len()`, `print()`, `import random`,
qualquer função de `random`, `set()` e os métodos `union`, `intersection` e `difference` do set.

Uma função **`gen_player_achievements()`** que, a partir de uma lista grande e fixa de
conquistas, sorteia uma quantidade e depois sorteia essa quantidade de conquistas da lista,
devolvendo-as num **set**.

Com ela, o programa:

- gera o set de conquistas de pelo menos quatro jogadores;
- mostra todas as conquistas **distintas**, juntando as de todos os jogadores;
- mostra as conquistas **comuns**, que todos os jogadores têm;
- para cada jogador, mostra as conquistas que **só ele** tem;
- para cada jogador, mostra as conquistas que **faltam** para ele ter todas as da lista.

O enunciado também pede para ajustar o tamanho da lista e a quantidade sorteada de modo que os
resultados tenham boa chance de não sair vazios, e pergunta como o Python imprime um set vazio, e
por quê.

## A saída esperada

O exemplo do enunciado, com uma lista de 14 conquistas:

```text
=== Achievement Tracker System ===

Player Alice: {'Crafting Genius', 'World Savior', 'Master Explorer', 'Collector Supreme', 'Untouchable', 'Boss Slayer'}
Player Bob: {'Crafting Genius', 'Strategist', 'World Savior', 'Master Explorer', 'Unstoppable', 'Collector Supreme', 'Untouchable'}
Player Charlie: {'Strategist', 'Speed Runner', 'Survivor', 'Master Explorer', 'Treasure Hunter', 'First Steps', 'Collector Supreme', 'Untouchable', 'Sharp Mind'}
Player Dylan: {'Strategist', 'Speed Runner', 'Unstoppable', 'Untouchable', 'Boss Slayer'}

All distinct achievements: {'Crafting Genius', 'Strategist', 'World Savior', 'Speed Runner', 'Survivor', 'Master Explorer', 'Treasure Hunter', 'Unstoppable', 'First Steps', 'Collector Supreme', 'Untouchable', 'Sharp Mind', 'Boss Slayer'}

Common achievements: {'Untouchable'}

Only Alice has: set()
Only Bob has: set()
Only Charlie has: {'Survivor', 'Treasure Hunter', 'First Steps', 'Sharp Mind'}
Only Dylan has: set()

Alice is missing: {'Strategist', 'Speed Runner', 'Survivor', 'Treasure Hunter', 'Unstoppable', 'Hidden Path Finder', 'First Steps', 'Sharp Mind'}
Bob is missing: {'Speed Runner', 'Survivor', 'Treasure Hunter', 'Hidden Path Finder', 'First Steps', 'Sharp Mind', 'Boss Slayer'}
Charlie is missing: {'Crafting Genius', 'World Savior', 'Hidden Path Finder', 'Unstoppable', 'Boss Slayer'}
Dylan is missing: {'Crafting Genius', 'World Savior', 'Survivor', 'Master Explorer', 'Treasure Hunter', 'Hidden Path Finder', 'First Steps', 'Collector Supreme', 'Sharp Mind'}
```

A conquista `Hidden Path Finder` aparece em todos os "missing" e em nenhuma outra linha: ninguém
a sorteou. Isso mostra que "o que falta" é calculado contra a **lista inteira** de conquistas, e
não só contra as que algum jogador tem.

Como tudo é sorteado, cada execução imprime conquistas diferentes. A forma da saída é que é fixa:
título e linha vazia, uma linha por jogador, e os blocos separados por linhas vazias.
