---
sidebar_position: 5
title: A estatística da árvore
---

# A estatística da árvore

As árvores contam uma coisa a mais: as chamadas a `produce_shade()`. As estatísticas de uma
árvore são as de qualquer planta mais um contador, e isso é exatamente uma herança: uma classe de
estatísticas de árvore que herda de `Plant.Stats`.

## Tree.Stats

```python
class Tree(Plant):
    class Stats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls = 0

        def count_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> None:
            super().display()
            print(f" {self._shade_calls} shade")
```

- `Tree.Stats` é uma classe aninhada em `Tree`, filha de `Plant.Stats`. As duas se chamam
  `Stats`, cada uma dentro da sua classe, e o nome completo as distingue;
- o construtor chama `super().__init__()`, que cria os três contadores comuns, e acrescenta o
  quarto;
- `display()` imprime a linha comum (`super().display()`) e a linha da sombra, começando com um
  espaço: ` 0 shade`.

## A árvore usa as estatísticas de árvore

```python
    _stats: "Tree.Stats"

    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float,
        trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
        self._trunk_diameter = trunk_diameter
        self._stats = Tree.Stats()

    def produce_shade(self) -> None:
        self._stats.count_shade()
        print(
            f"Tree {self._name} now produces a shade of "
            f"{round(self._height, 1)}cm long and "
            f"{round(self._trunk_diameter, 1)}cm wide."
        )
```

- o construtor de `Plant`, chamado pelo `super().__init__`, cria um `Plant.Stats`; logo depois,
  a árvore o troca por um `Tree.Stats`, novo, com os quatro contadores zerados. Nada foi contado
  entre as duas linhas. Trocar o objeto ali é escolha do projeto, por ser o caminho mais curto
  (uma linha, sem mexer em `Plant`); outra opção seria o construtor de `Plant` criar
  `self.Stats()`, que numa árvore já acharia o `Tree.Stats`;
- `produce_shade()` conta a sombra e imprime a frase do exercício 5;
- `grow()`, `age()` e `show()` continuam vindo de `Plant` e contam no mesmo `self._stats`, que
  agora é o de árvore.

## A declaração `_stats: "Tree.Stats"`

Para o mypy, o atributo `_stats` é um `Plant.Stats`, porque foi assim que o construtor de `Plant`
o criou, e um `Plant.Stats` não tem `count_shade()`. A linha `_stats: "Tree.Stats"`, no corpo de
`Tree`, declara que, nas árvores, `_stats` é sempre um `Tree.Stats`; com ela, o mypy aceita
`self._stats.count_shade()`. É a mesma declaração de atributo sem valor do
[exercício 1](../03-ex1/03-os-atributos.md), agora dando um tipo mais específico a um atributo
herdado.

Do Python 3.10 ao 3.13, as aspas são necessárias pelo mesmo motivo do
[método de classe](./03-o-metodo-de-classe.md#por-que-plant-entre-aspas): uma anotação escrita
direto no corpo da classe é lida no momento em que o Python passa por ela, e nessa hora a classe
`Tree` ainda está sendo montada; o nome `Tree` ainda não existe. A partir do 3.14, a anotação só
é lida quando alguém a pede, e o código funciona com ou sem as aspas. O `Tree.Stats()` do `__init__`
dispensa as aspas em todas as versões: o corpo de um método só roda quando o método é chamado, e
então a classe `Tree` já existe.
