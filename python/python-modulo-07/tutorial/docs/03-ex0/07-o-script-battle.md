---
sidebar_position: 7
title: O script battle
---

# O script battle

O pacote está pronto, mas nada o usa. O `battle.py`, na raiz do projeto, fora da pasta `ex0`,
testa as fábricas e imprime a saída do enunciado. Ele só importa o que o pacote expõe.

Crie `battle.py` na pasta `datadeck`, começando pelo import:

```python
from ex0 import AquaFactory, CreatureFactory, FlameFactory
```

## A função que testa uma fábrica

```python
def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    for creature in [base, evolved]:
        print(creature.describe())
        print(creature.attack())
```

É a função **única** que o enunciado pede: recebe uma fábrica qualquer (o type hint é a classe
abstrata `CreatureFactory`), cria a criatura base e a evoluída, e faz cada uma se descrever e
atacar. A mesma função serve para o fogo e para a água, porque só usa os métodos que a classe
abstrata garante. O mypy deduz que `base` e `evolved` são `Creature`, pelo tipo de retorno de
`create_base` e `create_evolved`, e confere que `describe` e `attack` existem nesse tipo.

## A função da luta

```python
def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    one = first.create_base()
    two = second.create_base()
    print(one.describe())
    print(" vs.")
    print(two.describe())
    print(" fight!")
    print(one.attack())
    print(two.attack())
```

Recebe as duas fábricas, cria a criatura base de cada uma, apresenta as duas e faz cada uma atacar
uma vez. As linhas ` vs.` e ` fight!` têm o espaço no começo dentro do próprio texto, como na
saída do enunciado. A luta é só a troca de ataques: o enunciado não tem pontos de vida nem
vencedor.

## O main

```python
def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    test_factory(flame)
    print()
    test_factory(aqua)
    print()
    test_battle(flame, aqua)


if __name__ == "__main__":
    main()
```

- as duas fábricas são criadas uma vez e usadas nos três testes;
- `print()` sem argumento imprime a linha vazia que separa os blocos da saída;
- o `if __name__ == "__main__":` roda o `main` só quando o arquivo é executado com `python3`
  ([Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#o-experimento)).

`battle.py` não menciona nenhuma criatura concreta: os nomes `Flameling` e `Aquabub` só
aparecem na saída, vindos dos objetos criados pelas fábricas.
