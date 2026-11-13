---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

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

Cada execução sorteia de novo, então a sua saída tem outras conquistas, em outra ordem.

## Conferir os resultados

Sem uma saída fixa para comparar com `diff`, a conferência é feita lendo as regras na própria
saída. Nesta execução:

- `Iron Will`, `Sky Diver`, `Cartographer` e `Hidden Path Finder` estão nos quatro jogadores, e
  são as quatro comuns;
- `Trap Master` está no Bob e em mais ninguém, e é o único elemento de `Only Bob has`;
- `Silent Step`, `Archivist` e `Strategist` não foram sorteadas para ninguém: não estão em
  `All distinct achievements` e estão em todos os "missing";
- `All distinct achievements` tem 57 conquistas; com as 3 que ninguém tem, são 60, o tamanho da
  lista;
- para cada jogador, as conquistas dele mais as que faltam somam 60: a Alice tem 33 e faltam 27.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3
.venv/bin/mypy --disallow-untyped-defs ex3
```

```text
Success: no issues found in 1 source file
```
