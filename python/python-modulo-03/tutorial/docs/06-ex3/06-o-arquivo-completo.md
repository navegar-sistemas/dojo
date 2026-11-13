---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

O `main` junta as quatro partes e imprime as linhas vazias da saída do enunciado: o `\n` no fim
do título, antes de `All distinct` e antes e depois de `Common achievements`, e o `print()` sem
nada, que imprime só uma linha vazia, entre os "só ele tem" e os "faltam".

```python title="ex3/ft_achievement_tracker.py"
import random

ACHIEVEMENTS = [
    "Crafting Genius", "Strategist", "World Savior", "Speed Runner",
    "Survivor", "Master Explorer", "Treasure Hunter", "Unstoppable",
    "First Steps", "Collector Supreme", "Untouchable", "Sharp Mind",
    "Boss Slayer", "Hidden Path Finder", "Night Owl", "Pacifist",
    "Sharpshooter", "Lucky Strike", "Dragon Tamer", "Puzzle Master",
    "Marathon Runner", "Gold Hoarder", "Team Player", "Lone Wolf",
    "Perfectionist", "Daredevil", "Archivist", "Beast Whisperer",
    "Stealth Master", "Legend", "Iron Will", "Quick Draw", "Master Chef",
    "Cartographer", "Monster Hunter", "Shield Bearer", "Potion Brewer",
    "Sky Diver", "Pearl Diver", "Wall Climber", "Fire Walker",
    "Ice Breaker", "Storm Chaser", "Silent Step", "Last Stand",
    "Comeback King", "Flawless Victory", "Merchant", "Ruin Raider",
    "Night Rider", "Giant Killer", "Spell Weaver", "Rune Reader",
    "Lock Picker", "Trap Master", "Ghost Hunter", "Team Captain",
    "Speed Demon", "Mountain King", "Star Gazer",
]
PLAYERS = ["Alice", "Bob", "Charlie", "Dylan"]


def gen_player_achievements() -> set[str]:
    """Pick a random number of distinct achievements for one player."""
    count = random.randint(27, 33)
    return set(random.sample(ACHIEVEMENTS, count))


def main() -> None:
    """Generate the players and compare their achievement sets."""
    print("=== Achievement Tracker System ===\n")
    players: list[tuple[str, set[str]]] = []
    for name in PLAYERS:
        achievements = gen_player_achievements()
        players.append((name, achievements))
        print(f"Player {name}: {achievements}")

    distinct: set[str] = set()
    common = players[0][1]
    for _, achievements in players:
        distinct = distinct.union(achievements)
        common = common.intersection(achievements)
    print(f"\nAll distinct achievements: {distinct}")
    print(f"\nCommon achievements: {common}\n")

    for name, achievements in players:
        others: set[str] = set()
        for other_name, other_achievements in players:
            if other_name != name:
                others = others.union(other_achievements)
        print(f"Only {name} has: {achievements.difference(others)}")
    print()

    every_achievement = set(ACHIEVEMENTS)
    for name, achievements in players:
        missing = every_achievement.difference(achievements)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, `    main()`, que o botão de copiar não leva.

As linhas em branco dentro do `main` separam as quatro etapas; o Python e o flake8 as aceitam.

O arquivo usa `print()`, `random.randint`, `random.sample`, `set()` e os três métodos de set
autorizados. A lista, a tupla e o método `append` vêm dos exercícios anteriores.

## Mais jogadores

O enunciado pede no mínimo quatro jogadores. Para ter cinco, basta acrescentar um nome a
`PLAYERS`: nenhum outro trecho conta os jogadores, porque todos os laços percorrem a lista
`players`.
