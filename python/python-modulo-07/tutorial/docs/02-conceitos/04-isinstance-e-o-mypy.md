---
sidebar_position: 4
title: isinstance e o mypy
---

# isinstance e o mypy

Uma fábrica do projeto devolve uma `Creature`. Algumas criaturas sabem curar, mas o tipo
`Creature` não tem o método `heal`: para o mypy, chamar `heal` numa `Creature` é um erro, mesmo
quando o objeto de verdade sabe curar. O código precisa **conferir** a capacidade antes de usá-la,
e o mypy precisa enxergar essa conferência.

## isinstance

`isinstance(valor, Classe)` devolve `True` se o valor é um objeto daquela classe ou de uma filha
dela, e `False` se não é. Com herança múltipla, um objeto é instância de todas as mães
([Herança múltipla](./03-heranca-multipla.md#a-ordem-de-busca)).

## O experimento

Crie `experimentos/estreitar.py`. Todo animal tem nome; nadar é uma capacidade à parte, que o pato
tem e o gato não:

```python title="experimentos/estreitar.py"
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Swimmer:
    def swim(self) -> str:
        return "splash"


class Duck(Animal, Swimmer):
    pass


class Cat(Animal):
    pass


def show(animal: Animal) -> None:
    print(f"{animal.name}: {animal.swim()}")


show(Duck("Ducky"))
show(Cat("Kitty"))
```

`Duck` não escreve nada: herda o `__init__` de `Animal` e o `swim` de `Swimmer`.

```bash
python3 experimentos/estreitar.py
```

A saída começa com:

```text
Ducky: splash
```

E a última linha é:

```text
AttributeError: 'Cat' object has no attribute 'swim'
```

O pato nadou; o gato quebrou o programa. O mypy acha o problema sem rodar nada:

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/estreitar.py
```

```text
experimentos/estreitar.py:20: error: "Animal" has no attribute "swim"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

O parâmetro é um `Animal`, e `Animal` não tem `swim`. O mypy só conhece o tipo anotado, não o
objeto que vai chegar.

## Uma função que confere não basta

Uma tentativa natural é escrever uma função que confere e usá-la no `if`:

```python title="experimentos/estreitar.py"
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Swimmer:
    def swim(self) -> str:
        return "splash"


class Duck(Animal, Swimmer):
    pass


class Cat(Animal):
    pass


def can_swim(animal: Animal) -> bool:
    return isinstance(animal, Swimmer)


def show(animal: Animal) -> None:
    if can_swim(animal):
        print(f"{animal.name}: {animal.swim()}")
    else:
        print(f"{animal.name} cannot swim")


show(Duck("Ducky"))
show(Cat("Kitty"))
```

```bash
python3 experimentos/estreitar.py
.venv/bin/mypy --disallow-untyped-defs experimentos/estreitar.py
```

```text
Ducky: splash
Kitty cannot swim
experimentos/estreitar.py:25: error: "Animal" has no attribute "swim"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
```

O programa agora funciona, mas o mypy continua reclamando. Para ele, `can_swim` é uma função que
devolve um `bool` qualquer: ele não olha dentro dela para concluir que, no `True`, o animal sabe
nadar.

## isinstance direto no if

Quando a condição do `if` é o próprio `isinstance`, o mypy entende: dentro do bloco, o valor é
daquela classe. Isso se chama **estreitar o tipo** (*type narrowing*): o tipo `Animal` fica mais
estreito, "um `Animal` que também é `Swimmer`". Escreva a versão final:

```python title="experimentos/estreitar.py"
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Swimmer:
    def swim(self) -> str:
        return "splash"


class Duck(Animal, Swimmer):
    pass


class Cat(Animal):
    pass


def show(animal: Animal) -> None:
    if isinstance(animal, Swimmer):
        print(f"{animal.name}: {animal.swim()}")
    else:
        print(f"{animal.name} cannot swim")


def force_swim(animal: Animal) -> str:
    if not isinstance(animal, Swimmer):
        raise TypeError(f"{animal.name} cannot swim")
    return f"{animal.name}: {animal.swim()}"


show(Duck("Ducky"))
show(Cat("Kitty"))
print(force_swim(Duck("Ducky")))
try:
    force_swim(Cat("Kitty"))
except TypeError as error:
    print(f"Error: {error}")
```

- em `show`, dentro do `if isinstance(animal, Swimmer):`, o mypy aceita `animal.name` (é um
  `Animal`) e `animal.swim()` (é um `Swimmer`);
- em `force_swim`, o `if not isinstance(...)` lança uma exceção quando o animal não nada. Como o
  `raise` interrompe a função, o mypy sabe que, depois do `if`, o animal **é** um `Swimmer`. É o
  jeito de conferir uma vez, no começo, e usar a capacidade no resto da função. `TypeError` é o
  tipo de exceção que o Python usa para "valor do tipo errado".

```bash
python3 experimentos/estreitar.py
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Ducky: splash
Kitty cannot swim
Ducky: splash
Error: Kitty cannot swim
Success: no issues found in 7 source files
```

## No projeto

O `capacitor.py` do exercício 1 recebe criaturas como `Creature` e usa
`if isinstance(creature, HealCapability):` antes de chamar `heal`
([O script capacitor](../04-ex1/06-o-script-capacitor.md)). As estratégias do exercício 2 usam o
`if not isinstance(...): raise` para recusar uma criatura sem a capacidade certa
([As três estratégias](../05-ex2/04-as-tres-estrategias.md)).
