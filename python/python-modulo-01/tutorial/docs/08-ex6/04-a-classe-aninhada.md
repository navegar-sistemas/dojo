---
sidebar_position: 4
title: A classe aninhada
---

# A classe aninhada

Cada planta precisa contar quantas vezes `grow()`, `age()` e `show()` foram chamados nela, e
mostrar esses números. São três contadores e as ações sobre eles: um conjunto de dados com
comportamento próprio, ou seja, uma classe. Ela só faz sentido como parte de uma planta, e por
isso é escrita **dentro** da classe `Plant`, como uma **classe aninhada**.

## A classe Stats

```python
class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def count_grow(self) -> None:
            self._grow_calls += 1

        def count_age(self) -> None:
            self._age_calls += 1

        def count_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(
                f"Stats: {self._grow_calls} grow, "
                f"{self._age_calls} age, {self._show_calls} show"
            )
```

- a classe fica recuada dentro de `Plant`, e o nome completo dela é `Plant.Stats`;
- os três contadores começam em 0 e são **protegidos** (`_grow_calls`): o encapsulamento que o
  enunciado exige. A única mudança que a classe oferece é aumentar de um em um, pelos métodos
  `count_*`; escrever um número direto num contador (`_grow_calls = 99`) funcionaria, mas
  quebraria o combinado do `_`;
- `display()` é a função de exibição que o enunciado pede, e imprime a linha `Stats: ...` da
  saída.

## Cada planta com as suas estatísticas

O construtor de `Plant` cria um objeto `Stats` e o guarda num atributo protegido:

```python
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self._name = name
        self._height = 0.0
        self._age_days = 0
        self._stats = Plant.Stats()
        self.set_height(height)
        self.set_age(age_days)
```

Cada planta tem o seu próprio `_stats`, e por isso os números da rosa não se misturam com os do
carvalho. O `_stats` é criado antes dos setters por costume de deixar os atributos prontos
primeiro; os setters não contam nada.

## Contar as chamadas

Os três métodos contados avisam o `_stats` logo no começo:

```python
    def show(self) -> None:
        self._stats.count_show()
        print(
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._age_days} days old"
        )

    def grow(self, centimeters: float) -> None:
        self._stats.count_grow()
        self.set_height(self._height + centimeters)

    def age(self, days: int) -> None:
        self._stats.count_age()
        self.set_age(self._age_days + days)
```

As classes filhas não precisam contar `grow`, `age` nem `show`: `Flower.show()` chama
`super().show()`, que é este
`show()`, e a contagem acontece aqui, uma vez por chamada.

## Ler as estatísticas de fora

Um getter devolve o objeto de estatísticas e outro o nome da planta, para a
[função de estatísticas](./07-a-funcao-de-estatisticas.md), que fica fora da classe e não usa
atributos protegidos:

```python
    def get_name(self) -> str:
        return self._name

    def get_stats(self) -> "Plant.Stats":
        return self._stats
```

Quem recebe o objeto `Stats` pode chamar `display()` e também os `count_*`: nada impede um
`plant.get_stats().count_grow()` de fora da classe. O que fica protegido são os números, que só
mudam de um em um. O programa só usa `display()` de fora.

Devolver o objeto `Stats` é escolha do projeto: com isso, a função de fora não precisa de nenhum
método novo em `Plant`. A alternativa seria um método `Plant.show_stats()` que chama
`self._stats.display()` sem expor os `count_*`; a função de fora só repassaria a chamada.

O tipo de retorno de `get_stats`, `"Plant.Stats"`, vai entre aspas pelo mesmo motivo do
[método de classe](./03-o-metodo-de-classe.md#por-que-plant-entre-aspas): até o Python 3.13, a
anotação é lida no momento do `def`, quando o nome `Plant` ainda não existe. O `Plant.Stats()`
dentro do `__init__` dispensa as aspas: o corpo de um método só roda quando o método é chamado
(aqui, quando uma planta é criada), e nessa hora a classe `Plant` já está pronta.
