---
sidebar_position: 3
title: super()
---

# super()

Sobrescrever um método troca o método da classe pai pelo da filha. Muitas vezes a filha não quer
**trocar**, e sim **completar**: o `show()` da flor deve imprimir a linha de planta **e** a cor.
Copiar o `print` de `Plant` para dentro de `Flower` duplicaria código. O `super()` resolve:
dentro de um método da filha, `super()` dá acesso aos métodos da classe pai, e `super().show()`
roda o `show()` de `Plant`.

## Um experimento

```python title="experimentos/super.py"
class Plant:
    def __init__(self, name: str) -> None:
        self._name = name

    def show(self) -> None:
        print(f"Plant: {self._name}")


class Flower(Plant):
    def __init__(self, name: str, color: str) -> None:
        super().__init__(name)
        self._color = color

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")


rose = Flower("Rose", "red")
rose.show()
```

```bash
python3 experimentos/super.py
```

```text
Plant: Rose
 Color: red
```

- o construtor da flor recebe o que a planta precisa (`name`) e o que é só da flor (`color`).
  `super().__init__(name)` passa o nome para o construtor de `Plant`, que o guarda em
  `self._name`; depois, a flor guarda a cor. A flor não repete nada do que a planta já sabe
  fazer;
- o `show()` da flor chama `super().show()`, que imprime a linha de planta, e acrescenta a linha
  da cor;
- `super()` está na lista de funções autorizadas deste exercício.

Quando a filha escreve o seu próprio `__init__`, ele **sobrescreve** o de `Plant`: ao criar uma
flor, o Python chama só o `__init__` da flor. Por isso esse construtor **precisa** chamar
`super().__init__`: sem essa chamada, o `__init__` de `Plant` não roda, e a flor ficaria sem
`_name`. No experimento de [Herança](./02-heranca.md), a `Flower` não tinha `__init__` próprio, e
o de `Plant` era usado direto.

## O padrão dos três tipos

Os três tipos do exercício seguem o mesmo molde:

1. o `__init__` recebe os dados de planta mais os do tipo, passa os de planta para
   `super().__init__` e guarda os do tipo em atributos protegidos;
2. o `show()` chama `super().show()` e imprime as linhas extras, começando com um espaço;
3. cada tipo acrescenta os métodos que só ele tem.
