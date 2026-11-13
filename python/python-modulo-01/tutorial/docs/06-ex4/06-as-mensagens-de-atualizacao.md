---
sidebar_position: 6
title: As mensagens de atualização
---

# As mensagens de atualização

A saída mostra, depois de cada tentativa de mudança, uma linha com o resultado:
`Height updated: 25cm` quando a mudança é aceita, `Height update rejected` quando é recusada. Duas
funções do programa, fora da classe, fazem a tentativa e imprimem o resultado a partir do `bool`
que o setter devolve:

```python
def update_height(plant: Plant, height: float) -> None:
    if plant.set_height(height):
        print(f"Height updated: {round(plant.get_height())}cm")
    else:
        print("Height update rejected")


def update_age(plant: Plant, age_days: int) -> None:
    if plant.set_age(age_days):
        print(f"Age updated: {plant.get_age()} days")
    else:
        print("Age update rejected")
```

- `plant: Plant`: o type hint de um parâmetro pode ser uma classe, e diz que ali chega um objeto
  dela;
- o `if` chama o setter e já usa a resposta: `True` imprime a confirmação, `False` imprime a
  recusa. A mensagem de erro, essa, já foi impressa de dentro da classe;
- a leitura usa os getters, nunca `plant._height`: as funções estão fora da classe;
- `round(plant.get_height())`, **sem** o número de casas, devolve um inteiro, e a linha sai
  `25cm`, sem casa decimal, como no enunciado
  ([O float e o round](../04-ex2/03-o-float-e-o-round.md)).

## A divisão entre classe e programa

Esta é uma escolha do projeto. A classe imprime o **erro**, porque o enunciado exige; o programa
imprime o **resultado** da tentativa, porque é ele quem a pediu. Assim os setters ficam
silenciosos quando aceitam um valor, e o construtor pode usá-los sem imprimir "updated" ao criar
uma planta.

Outra opção seria os setters imprimirem também as confirmações e recusas. Nesse caso o construtor
não poderia chamá-los (a criação imprimiria `Height updated: 15cm`) e teria de repetir a
validação, e a regra deixaria de estar num lugar só.
