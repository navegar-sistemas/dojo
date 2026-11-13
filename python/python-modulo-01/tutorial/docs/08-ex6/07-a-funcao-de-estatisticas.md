---
sidebar_position: 7
title: A função de estatísticas
---

# A função de estatísticas

O enunciado pede uma **única** função, fora de qualquer classe, que exiba as estatísticas de
qualquer tipo de planta:

```python
def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()
```

- o parâmetro é anotado como `Plant`, e aceita qualquer filha: uma `Flower`, uma `Tree` ou uma
  `Seed` **é uma** `Plant`, e o mypy aceita todas;
- a função fica fora da classe, então lê o nome e as estatísticas pelos getters;
- `plant.get_stats().display()` pede o objeto de estatísticas e manda ele se exibir.

## Uma chamada, comportamentos diferentes

A função não sabe que tipo de planta recebeu, e não precisa saber. Numa rosa, `get_stats()`
devolve um `Plant.Stats`, e `display()` imprime uma linha. Num carvalho, devolve um `Tree.Stats`,
e o `display()` sobrescrito imprime as duas:

```text
[statistics for Oak]
Stats: 0 grow, 0 age, 1 show
 0 shade
```

O mesmo código chamando um método que cada tipo implementa do seu jeito é o que a orientação a
objetos chama de **polimorfismo** ("muitas formas"). Um tipo novo de planta, com estatísticas
próprias, funcionaria com `display_stats` sem mexer nela.

![Quatro plantas e os seus objetos de estatísticas no fim do programa: a rosa com 1 grow, 0 age e 2 show; o carvalho, com um Tree.Stats, 0 grow, 0 age, 1 show e 1 shade; o girassol com 1 grow, 1 age e 2 show; a planta anônima com 0 grow, 0 age e 1 show](/img/ex6/estatisticas.svg)
