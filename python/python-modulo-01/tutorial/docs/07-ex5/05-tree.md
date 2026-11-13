---
sidebar_position: 5
title: Tree
---

# Tree

A árvore tem um tronco, com um diâmetro em centímetros, e faz sombra.

```python
class Tree(Plant):
    def __init__(
        self, name: str, height: float, age_days: int,
        trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age_days)
        self._trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{round(self._height, 1)}cm long and "
            f"{round(self._trunk_diameter, 1)}cm wide."
        )

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {round(self._trunk_diameter, 1)}cm")
```

- o diâmetro é um `float`, mostrado com uma casa decimal como a altura (`5.0cm`);
- `produce_shade()` imprime a sombra que a árvore faz. O enunciado não diz como ela é calculada;
  a saída (`200.0cm long and 5.0cm wide` num carvalho de 200 cm com tronco de 5 cm) bate com
  comprimento igual à altura e largura igual ao diâmetro do tronco, e é essa a leitura que o
  projeto adota. A frase usa `self._height`, o atributo protegido herdado de `Plant`;
- `_trunk_diameter` é o atributo `trunk_diameter` pedido, com a marca protected
  ([color ou _color](./04-flower.md#color-ou-_color));
- o `show()` acrescenta a linha do diâmetro.

![Vista de cima da sombra do carvalho: um retângulo de 200,0 cm de comprimento por 5,0 cm de largura, partindo do tronco, desenhado na proporção real entre as duas medidas](/img/ex5/sombra.svg)

Na saída:

```text
Oak: 200.0cm, 365 days old
 Trunk diameter: 5.0cm
[asking the oak to produce shade]
Tree Oak now produces a shade of 200.0cm long and 5.0cm wide.
```
