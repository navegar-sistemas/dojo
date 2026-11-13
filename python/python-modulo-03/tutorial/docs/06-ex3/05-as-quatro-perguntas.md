---
sidebar_position: 5
title: As quatro perguntas
---

# As quatro perguntas

O exemplo do enunciado, em forma de tabela: cada linha é uma das 14 conquistas da lista, cada
coluna um jogador, e um ponto marca quem tem a conquista.

![Tabela das 14 conquistas do exemplo do enunciado por jogador, Alice, Bob, Charlie e Dylan. A linha Untouchable tem ponto nas quatro colunas: é a única comum. Survivor, Treasure Hunter, First Steps e Sharp Mind só têm ponto na coluna de Charlie: são as exclusivas dele. A linha Hidden Path Finder não tem ponto nenhum: ninguém a tem, e ela falta para todos](/img/ex3/conquistas.svg)

Nessa tabela, cada pergunta do exercício é um jeito de ler as linhas:

| Pergunta | Na tabela | Operação |
|---|---|---|
| conquistas distintas | linhas com pelo menos um ponto | união dos quatro sets |
| conquistas comuns | linhas com ponto nas quatro colunas | interseção dos quatro sets |
| só o jogador tem | linhas com ponto **só** na coluna dele | o set dele menos a união dos outros três |
| faltam ao jogador | linhas **sem** ponto na coluna dele | a lista inteira menos o set dele |

## Os jogadores

Cada jogador é um par: o nome e o set de conquistas. Um par de significado fixo é uma tupla, e os
quatro pares ficam numa lista:

```python
PLAYERS = ["Alice", "Bob", "Charlie", "Dylan"]

players: list[tuple[str, set[str]]] = []
for name in PLAYERS:
    achievements = gen_player_achievements()
    players.append((name, achievements))
    print(f"Player {name}: {achievements}")
```

- `list[tuple[str, set[str]]]` lê-se de fora para dentro: uma lista de tuplas, e cada tupla tem
  um texto e um set de textos;
- `players.append((name, achievements))` tem parênteses duplos: os de fora são da chamada do
  `append`, os de dentro criam a tupla;
- `{achievements}` dentro da f-string imprime o set com chaves, como no enunciado.

Um `for` sobre `players` pode desempacotar cada tupla direto: `for name, achievements in
players:` dá o nome e o set de cada jogador em cada volta.

## Distintas e comuns

```python
distinct: set[str] = set()
common = players[0][1]
for _, achievements in players:
    distinct = distinct.union(achievements)
    common = common.intersection(achievements)
```

- `distinct` começa vazio e acumula a união;
- `common` começa com o set do primeiro jogador: `players[0]` é a primeira tupla, e `[1]` é o
  segundo elemento dela, o set. A cada volta, a interseção corta o que o jogador da vez não tem;
- o nome do jogador não é usado neste laço, e o `_` marca isso.

Na primeira volta, `common` faz a interseção do primeiro set com ele mesmo, que não muda nada.

## Só ele tem

```python
for name, achievements in players:
    others: set[str] = set()
    for other_name, other_achievements in players:
        if other_name != name:
            others = others.union(other_achievements)
    print(f"Only {name} has: {achievements.difference(others)}")
```

Para cada jogador, o laço de dentro junta as conquistas de **todos os outros** (os nomes
diferentes do dele) em `others`. O que é dele e não está em `others` é exclusivo dele. Se não
sobrar nada, a linha sai `set()`.

## O que falta

```python
every_achievement = set(ACHIEVEMENTS)
for name, achievements in players:
    missing = every_achievement.difference(achievements)
    print(f"{name} is missing: {missing}")
```

`set(ACHIEVEMENTS)` transforma a lista fixa num set, uma vez só, antes do laço. O que falta a
cada jogador é a lista inteira menos o que ele tem. É por isso que uma conquista que ninguém
sorteou, como a `Hidden Path Finder` do exemplo, falta para todos.
