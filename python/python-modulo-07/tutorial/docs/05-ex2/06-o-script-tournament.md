---
sidebar_position: 6
title: O script tournament
---

# O script tournament

Com a função `battle` pronta, falta o cenário: criar as fábricas e as estratégias e rodar os
três torneios do enunciado. Acrescente o `main` no fim de `tournament.py`, com duas linhas em
branco antes do `def`:

```python
def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame, normal), (healing, defensive)])

    print()
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame, aggressive), (healing, defensive)])

    print()
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), "
          "(Transform+Aggressive) ]")
    battle([(aqua, normal), (healing, defensive), (transform, aggressive)])


if __name__ == "__main__":
    main()
```

## As peças

- quatro fábricas (duas do `ex0`, duas do `ex1`) e as três estratégias, criadas uma vez cada. Uma
  estratégia não guarda estado, então o mesmo objeto serve para vários oponentes e vários
  torneios;
- cada torneio é uma chamada a `battle`, com a lista de tuplas `(fábrica, estratégia)`. O mypy
  confere cada tupla contra o type hint `list[tuple[CreatureFactory, BattleStrategy]]`;
- antes de cada chamada, o título e a lista de oponentes. Escolha do tutorial: textos fixos,
  copiados do enunciado, porque a saída do enunciado não segue regra (`Flameling` é nome de
  criatura, `Healing` é parte do nome da fábrica)
  ([O que a saída revela](./01-o-problema.md#o-que-a-saída-revela)). A lista do torneio 2 passa
  dos 79 caracteres e foi dividida em dois textos seguidos;
- `print()` imprime a linha vazia entre os torneios. Dentro do `main`, as linhas em branco entre
  os grupos de comandos só separam os torneios para quem lê; elas não aparecem na saída.

## Os três torneios

| Torneio | Oponentes | O que mostra |
|---|---|---|
| 0 (basic) | fogo com a normal, cura com a defensiva | uma luta, duas estratégias válidas |
| 1 (error) | fogo com a **agressiva**, cura com a defensiva | `Flameling` não se transforma: o `act` da agressiva lança a exceção, e o torneio é abortado |
| 2 (multiple) | água com a normal, cura com a defensiva, transformação com a agressiva | três oponentes, três lutas, as três estratégias |

O torneio 1 termina com a mensagem de erro, e o programa continua: o torneio 2 roda inteiro. É o
que pedem as regras gerais do enunciado: "tratar exceções de forma adequada, para evitar que o
programa quebre".
