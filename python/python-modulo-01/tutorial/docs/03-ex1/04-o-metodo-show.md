---
sidebar_position: 4
title: O método show
---

# O método show

Um **método** é uma função escrita dentro de uma classe. Ele é chamado com um ponto depois do
objeto, como os atributos, e age sobre aquele objeto: `rose.show()` mostra a rosa,
`sunflower.show()` mostra o girassol.

## O método

```python
class Plant:
    name: str
    height: int
    age_days: int

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age_days} days old")
```

- o `def` fica recuado dentro da classe; é isso que faz de `show` um método de `Plant`;
- entre os atributos e o `def` há uma linha em branco: o flake8 exige uma linha em branco antes
  de um método que vem depois de outra linha da classe (sem ela, o aviso seria
  `E301 expected 1 blank line, found 0`). Um método escrito logo abaixo da linha `class Plant:`
  dispensa essa linha, como o `__init__` do [exercício 3](../05-ex3/02-o-construtor.md);
- `-> None`: o método não devolve nada, só imprime.

## O self

Todo método comum recebe, como **primeiro parâmetro**, o objeto sobre o qual foi chamado. O
costume do Python é chamar esse parâmetro de `self` ("o próprio"). Em `rose.show()`, o `self` é a
`rose`, e `self.name` é `rose.name`; em `sunflower.show()`, o `self` é o `sunflower`.

O Python passa esse objeto sozinho: `rose.show()` é um atalho para `Plant.show(rose)`. Um
experimento mostra as duas formas:

```python title="experimentos/self.py"
class Plant:
    name: str

    def show(self) -> None:
        print(f"Plant: {self.name}")


rose = Plant()
rose.name = "Rose"
oak = Plant()
oak.name = "Oak"

rose.show()
oak.show()
Plant.show(rose)
```

```bash
python3 experimentos/self.py
```

```text
Plant: Rose
Plant: Oak
Plant: Rose
```

O mesmo método, escrito uma vez, mostrou objetos diferentes, porque o `self` muda a cada
chamada. O `self` não leva type hint: o mypy já sabe que ele é um objeto da própria classe.

## A linha impressa

`f"{self.name}: {self.height}cm, {self.age_days} days old"` monta a linha da saída: o nome,
dois-pontos e espaço, a altura colada em `cm`, vírgula e espaço, a idade e `days old`. Para a
rosa, `Rose: 25cm, 30 days old`.
