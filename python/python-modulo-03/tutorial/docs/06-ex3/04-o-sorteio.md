---
sidebar_position: 4
title: O sorteio
---

# O sorteio

`gen_player_achievements()` sorteia duas coisas: quantas conquistas o jogador tem e quais são.
O módulo `random` ("aleatório"), que vem com o Python, faz os dois sorteios.

```python title="experimentos/sorteio.py"
import random

names = ["Boss Slayer", "Survivor", "Legend", "Strategist", "Pacifist"]
for _ in range(3):
    count = random.randint(2, 4)
    picked = random.sample(names, count)
    print(count, picked)
```

```bash
python3 experimentos/sorteio.py
```

```text
4 ['Survivor', 'Legend', 'Strategist', 'Pacifist']
2 ['Boss Slayer', 'Strategist']
4 ['Pacifist', 'Strategist', 'Boss Slayer', 'Legend']
```

A saída muda a cada execução. O que não muda:

- `random.randint(2, 4)` sorteia um inteiro de 2 a 4, **incluindo** as duas pontas;
- `random.sample(names, count)` sorteia `count` elementos **diferentes** da lista e os devolve
  numa lista nova (*sample* é "amostra"). Um mesmo elemento nunca sai duas vezes na mesma
  amostra. `count` maior que o tamanho da lista lança `ValueError`.

## A função

```python
def gen_player_achievements() -> set[str]:
    """Pick a random number of distinct achievements for one player."""
    count = random.randint(27, 33)
    return set(random.sample(ACHIEVEMENTS, count))
```

`ACHIEVEMENTS` é a lista fixa de conquistas, uma constante no topo do arquivo, e `set(...)`
transforma a amostra num set. Como a amostra já não tem repetidos, o set tem exatamente `count`
elementos. O tipo de retorno `set[str]` diz que a função devolve um set de textos.

## Quantas conquistas na lista, quantas por jogador

O enunciado pede para ajustar os dois números de modo que todos os resultados pedidos tenham boa
chance de não sair vazios. São cinco resultados que podem sair `set()`: as conquistas comuns e as
exclusivas de cada um dos quatro jogadores. Duas perguntas puxam para lados opostos:

- para uma conquista ser **comum**, os quatro jogadores precisam tê-la: isso fica mais provável
  quando cada um tem muitas;
- para uma conquista ser **só de um**, os outros três precisam não tê-la: isso fica mais provável
  quando cada um tem poucas.

O equilíbrio é cada jogador ter mais ou menos **metade** da lista. Aí, cada conquista tem chance
de ½ de estar com um jogador, e:

- a chance de estar com os quatro é ½ × ½ × ½ × ½ = 1/16;
- a chance de estar só com um certo jogador (com ele, e não com os outros três) também é
  ½ × ½ × ½ × ½ = 1/16;
- numa lista de 60 conquistas, isso dá, em média, 60 × 1/16 = 3.75 comuns e 3.75 exclusivas por
  jogador;
- tratando cada conquista como uma moeda independente, a chance de nenhuma das 60 ser comum
  seria (15/16)⁶⁰ ≈ 0.02. Como cada jogador tem um número fixo de conquistas, sorteadas sem
  repetição, a chance real é um pouco menor: cerca de 1.3% para as comuns, e o mesmo para as
  exclusivas de cada jogador.

Numa simulação de 100 000 execuções do programa, algum dos cinco resultados sai `set()` em cerca
de 6.5% das vezes, uma execução a cada quinze. Com uma lista de 30 conquistas e de 12 a 18 por
jogador, a mesma simulação dá cerca de 50%: uma execução a cada duas mostra alguma linha
vazia.

Por isso o exercício usa uma lista de **60** conquistas e sorteia de **27 a 33** para cada
jogador. A lista do exemplo do enunciado tem só 14, e lá três dos quatro "só ele tem" saíram
vazios. A lista maior deixa as linhas da saída mais compridas.

```python
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
```

As 14 primeiras são as do exemplo do enunciado. Uma lista pode ocupar várias linhas: enquanto o
colchete não fecha, o Python continua lendo. A vírgula depois do último elemento é opcional, e o
costume é deixá-la quando cada linha termina com vírgula.
