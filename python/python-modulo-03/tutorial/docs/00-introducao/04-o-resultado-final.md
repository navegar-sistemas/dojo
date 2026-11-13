---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Nos exercícios 0, 1, 2 e 4, a saída de cada programa pronto é igual, letra por letra, à que o
enunciado mostra. Os exercícios 3, 5 e 6 sorteiam valores, então cada execução imprime uma
saída diferente, com a mesma forma.

O enunciado roda cada programa de dentro da pasta do exercício, e a saída dos exercícios 0 e 1
depende disso, porque eles imprimem o nome do programa do jeito que foi digitado
([O nome do programa](../03-ex0/02-a-linha-de-comando.md#o-nome-do-programa)). Por isso, os
comandos abaixo entram na pasta antes de rodar: `(cd ex0 && python3 ft_command_quest.py)` entra
em `ex0` e roda o programa. Os parênteses rodam os dois comandos numa cópia do **shell** (o
programa do terminal que lê e executa os comandos), então o `cd` não muda a pasta do terminal.

Esses comandos rodam da pasta do projeto, criada em
[A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md), depois que cada exercício estiver
escrito. A página "Rodar e conferir" de cada exercício volta a eles.

## Exercício 0

```bash
(cd ex0 && python3 ft_command_quest.py)
(cd ex0 && python3 ft_command_quest.py hello world 42)
(cd ex0 && python3 ft_command_quest.py "Data Quest")
```

```text
=== Command Quest ===
Program name: ft_command_quest.py
No arguments provided!
Total arguments: 1
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 3
Argument 1: hello
Argument 2: world
Argument 3: 42
Total arguments: 4
=== Command Quest ===
Program name: ft_command_quest.py
Arguments received: 1
Argument 1: Data Quest
Total arguments: 2
```

## Exercício 1

```bash
(cd ex1 && python3 ft_score_analytics.py 1500 2300 1800 2100 1950)
(cd ex1 && python3 ft_score_analytics.py)
(cd ex1 && python3 ft_score_analytics.py ab ac)
```

```text
=== Player Score Analytics ===
Scores processed: [1500, 2300, 1800, 2100, 1950]
Total players: 5
Total score: 9650
Average score: 1930.0
High score: 2300
Low score: 1500
Score range: 800
=== Player Score Analytics ===
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
=== Player Score Analytics ===
Invalid parameter: 'ab'
Invalid parameter: 'ac'
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
```

## Exercício 2

Este programa pergunta as posições pelo teclado. Na sessão abaixo, o texto depois de cada
`'x,y,z': ` foi digitado, seguido de Enter:

```bash
(cd ex2 && python3 ft_coordinate_system.py)
```

```text
=== Game Coordinate System ===

Get a first set of coordinates
Enter new coordinates as floats in format 'x,y,z': hello world
Invalid syntax
Enter new coordinates as floats in format 'x,y,z': 1.0 , 2.5, 3.0
Got a first tuple: (1.0, 2.5, 3.0)
It includes: X=1.0, Y=2.5, Z=3.0
Distance to center: 4.0311

Get a second set of coordinates
Enter new coordinates as floats in format 'x,y,z': 4,abc,5
Error on parameter 'abc': could not convert string to float: 'abc'
Enter new coordinates as floats in format 'x,y,z': 4,5,6
Distance between the 2 sets of coordinates: 4.9244
```

## Exercício 3

```bash
(cd ex3 && python3 ft_achievement_tracker.py)
```

```text
=== Achievement Tracker System ===

Player Alice: {'Boss Slayer', 'Fire Walker', 'First Steps', 'Lucky Strike', 'Speed Runner', 'Potion Brewer', 'Night Owl', 'Merchant', 'Lone Wolf', 'Last Stand', 'Hidden Path Finder', 'Legend', 'Survivor', 'Night Rider', 'Shield Bearer', 'Lock Picker', 'Pearl Diver', 'Iron Will', 'Master Explorer', 'Collector Supreme', 'Treasure Hunter', 'Pacifist', 'Sharpshooter', 'Team Captain', 'Cartographer', 'Giant Killer', 'Team Player', 'Monster Hunter', 'Flawless Victory', 'Quick Draw', 'Sky Diver', 'Storm Chaser', 'Puzzle Master'}
Player Bob: {'Perfectionist', 'Boss Slayer', 'Fire Walker', 'Stealth Master', 'Gold Hoarder', 'Speed Runner', 'Potion Brewer', 'Unstoppable', 'Rune Reader', 'Dragon Tamer', 'Hidden Path Finder', 'Star Gazer', 'Legend', 'Survivor', 'Sharp Mind', 'Ice Breaker', 'Shield Bearer', 'Trap Master', 'Untouchable', 'Iron Will', 'Treasure Hunter', 'Comeback King', 'Sharpshooter', 'Cartographer', 'Team Player', 'Ruin Raider', 'Monster Hunter', 'Sky Diver', 'Storm Chaser', 'Puzzle Master'}
Player Charlie: {'Boss Slayer', 'Stealth Master', 'First Steps', 'Fire Walker', 'Gold Hoarder', 'Night Owl', 'Mountain King', 'Master Chef', 'Last Stand', 'Hidden Path Finder', 'World Savior', 'Star Gazer', 'Night Rider', 'Lock Picker', 'Speed Demon', 'Untouchable', 'Iron Will', 'Collector Supreme', 'Comeback King', 'Pacifist', 'Wall Climber', 'Team Captain', 'Cartographer', 'Giant Killer', 'Ruin Raider', 'Team Player', 'Spell Weaver', 'Sky Diver'}
Player Dylan: {'Perfectionist', 'Gold Hoarder', 'Night Owl', 'Merchant', 'Unstoppable', 'Daredevil', 'Mountain King', 'Dragon Tamer', 'Rune Reader', 'Last Stand', 'Hidden Path Finder', 'World Savior', 'Ghost Hunter', 'Star Gazer', 'Sharp Mind', 'Beast Whisperer', 'Night Rider', 'Ice Breaker', 'Pearl Diver', 'Speed Demon', 'Iron Will', 'Treasure Hunter', 'Comeback King', 'Pacifist', 'Wall Climber', 'Crafting Genius', 'Cartographer', 'Quick Draw', 'Marathon Runner', 'Sky Diver', 'Puzzle Master'}

All distinct achievements: {'Perfectionist', 'Boss Slayer', 'Stealth Master', 'Potion Brewer', 'Night Owl', 'Merchant', 'Mountain King', 'Master Chef', 'World Savior', 'Ghost Hunter', 'Survivor', 'Beast Whisperer', 'Ice Breaker', 'Lock Picker', 'Pearl Diver', 'Untouchable', 'Comeback King', 'Pacifist', 'Cartographer', 'Ruin Raider', 'Monster Hunter', 'Quick Draw', 'Storm Chaser', 'Fire Walker', 'First Steps', 'Lucky Strike', 'Gold Hoarder', 'Speed Runner', 'Unstoppable', 'Rune Reader', 'Dragon Tamer', 'Daredevil', 'Lone Wolf', 'Last Stand', 'Hidden Path Finder', 'Star Gazer', 'Legend', 'Sharp Mind', 'Night Rider', 'Shield Bearer', 'Trap Master', 'Speed Demon', 'Iron Will', 'Master Explorer', 'Collector Supreme', 'Treasure Hunter', 'Sharpshooter', 'Wall Climber', 'Crafting Genius', 'Team Captain', 'Giant Killer', 'Team Player', 'Flawless Victory', 'Spell Weaver', 'Marathon Runner', 'Sky Diver', 'Puzzle Master'}

Common achievements: {'Iron Will', 'Sky Diver', 'Cartographer', 'Hidden Path Finder'}

Only Alice has: {'Lucky Strike', 'Master Explorer', 'Flawless Victory', 'Lone Wolf'}
Only Bob has: {'Trap Master'}
Only Charlie has: {'Spell Weaver', 'Master Chef'}
Only Dylan has: {'Beast Whisperer', 'Ghost Hunter', 'Marathon Runner', 'Daredevil', 'Crafting Genius'}

Alice is missing: {'Perfectionist', 'Stealth Master', 'Gold Hoarder', 'Unstoppable', 'Rune Reader', 'Mountain King', 'Daredevil', 'Dragon Tamer', 'Master Chef', 'World Savior', 'Ghost Hunter', 'Star Gazer', 'Silent Step', 'Sharp Mind', 'Beast Whisperer', 'Ice Breaker', 'Trap Master', 'Speed Demon', 'Untouchable', 'Comeback King', 'Wall Climber', 'Crafting Genius', 'Archivist', 'Ruin Raider', 'Spell Weaver', 'Strategist', 'Marathon Runner'}
Bob is missing: {'First Steps', 'Lucky Strike', 'Night Owl', 'Merchant', 'Daredevil', 'Mountain King', 'Lone Wolf', 'Master Chef', 'Last Stand', 'World Savior', 'Ghost Hunter', 'Silent Step', 'Beast Whisperer', 'Night Rider', 'Lock Picker', 'Pearl Diver', 'Speed Demon', 'Master Explorer', 'Collector Supreme', 'Pacifist', 'Wall Climber', 'Crafting Genius', 'Team Captain', 'Giant Killer', 'Archivist', 'Flawless Victory', 'Spell Weaver', 'Quick Draw', 'Strategist', 'Marathon Runner'}
Charlie is missing: {'Perfectionist', 'Lucky Strike', 'Speed Runner', 'Potion Brewer', 'Merchant', 'Unstoppable', 'Rune Reader', 'Daredevil', 'Dragon Tamer', 'Lone Wolf', 'Ghost Hunter', 'Legend', 'Survivor', 'Silent Step', 'Sharp Mind', 'Beast Whisperer', 'Ice Breaker', 'Shield Bearer', 'Pearl Diver', 'Trap Master', 'Master Explorer', 'Treasure Hunter', 'Sharpshooter', 'Crafting Genius', 'Archivist', 'Monster Hunter', 'Flawless Victory', 'Quick Draw', 'Strategist', 'Marathon Runner', 'Storm Chaser', 'Puzzle Master'}
Dylan is missing: {'Boss Slayer', 'Fire Walker', 'Stealth Master', 'First Steps', 'Lucky Strike', 'Speed Runner', 'Potion Brewer', 'Lone Wolf', 'Master Chef', 'Legend', 'Survivor', 'Silent Step', 'Shield Bearer', 'Lock Picker', 'Trap Master', 'Untouchable', 'Master Explorer', 'Collector Supreme', 'Sharpshooter', 'Team Captain', 'Giant Killer', 'Archivist', 'Team Player', 'Monster Hunter', 'Ruin Raider', 'Flawless Victory', 'Spell Weaver', 'Strategist', 'Storm Chaser'}
```

## Exercício 4

```bash
(cd ex4 && python3 ft_inventory_system.py sword:1 potion:5 shield:2 armor:3 helmet:1 sword:2 hello key:value)
```

```text
=== Inventory System Analysis ===
Redundant item 'sword' - discarding
Error - invalid parameter 'hello'
Quantity error for 'key': invalid literal for int() with base 10: 'value'
Got inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1}
Item list: ['sword', 'potion', 'shield', 'armor', 'helmet']
Total quantity of the 5 items: 12
Item sword represents 8.3%
Item potion represents 41.7%
Item shield represents 16.7%
Item armor represents 25.0%
Item helmet represents 8.3%
Item most abundant: potion with quantity 5
Item least abundant: sword with quantity 1
Updated inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1, 'magic_item': 1}
```

## Exercício 5

O programa imprime 1000 linhas de eventos. Abaixo, as linhas `Event 4` a `Event 992` foram
cortadas:

```bash
(cd ex5 && python3 ft_data_stream.py)
```

```text
=== Game Data Stream Processor ===
Event 0: Player charlie did action grab
Event 1: Player dylan did action swim
Event 2: Player dylan did action sleep
Event 3: Player charlie did action move
[...]
Event 993: Player alice did action move
Event 994: Player bob did action move
Event 995: Player alice did action eat
Event 996: Player alice did action release
Event 997: Player dylan did action use
Event 998: Player charlie did action grab
Event 999: Player dylan did action climb
Built list of 10 events: [('alice', 'grab'), ('charlie', 'grab'), ('bob', 'run'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('alice', 'move'), ('charlie', 'run'), ('bob', 'run'), ('bob', 'grab')]
Got event from list: ('alice', 'move')
Remains in list: [('alice', 'grab'), ('charlie', 'grab'), ('bob', 'run'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('charlie', 'run'), ('bob', 'run'), ('bob', 'grab')]
Got event from list: ('bob', 'grab')
Remains in list: [('alice', 'grab'), ('charlie', 'grab'), ('bob', 'run'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('charlie', 'run'), ('bob', 'run')]
Got event from list: ('bob', 'run')
Remains in list: [('alice', 'grab'), ('charlie', 'grab'), ('bob', 'run'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('charlie', 'run')]
Got event from list: ('alice', 'grab')
Remains in list: [('charlie', 'grab'), ('bob', 'run'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('charlie', 'run')]
Got event from list: ('bob', 'run')
Remains in list: [('charlie', 'grab'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat'), ('charlie', 'run')]
Got event from list: ('charlie', 'run')
Remains in list: [('charlie', 'grab'), ('dylan', 'grab'), ('charlie', 'climb'), ('alice', 'eat')]
Got event from list: ('charlie', 'climb')
Remains in list: [('charlie', 'grab'), ('dylan', 'grab'), ('alice', 'eat')]
Got event from list: ('dylan', 'grab')
Remains in list: [('charlie', 'grab'), ('alice', 'eat')]
Got event from list: ('charlie', 'grab')
Remains in list: [('alice', 'eat')]
Got event from list: ('alice', 'eat')
Remains in list: []
```

## Exercício 6

```bash
(cd ex6 && python3 ft_data_alchemist.py)
```

```text
=== Game Data Alchemist ===

Initial list of players: ['Alice', 'bob', 'Charlie', 'dylan', 'Emma', 'Gregory', 'john', 'kevin', 'Liam']
New list with all names capitalized: ['Alice', 'Bob', 'Charlie', 'Dylan', 'Emma', 'Gregory', 'John', 'Kevin', 'Liam']
New list of capitalized names only: ['Alice', 'Charlie', 'Emma', 'Gregory', 'Liam']

Score dict: {'Alice': 875, 'Bob': 700, 'Charlie': 580, 'Dylan': 659, 'Emma': 924, 'Gregory': 455, 'John': 207, 'Kevin': 558, 'Liam': 554}
Score average is 612.44
High scores: {'Alice': 875, 'Bob': 700, 'Dylan': 659, 'Emma': 924}
```
