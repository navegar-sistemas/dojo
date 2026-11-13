---
sidebar_position: 3
title: Os atributos
---

# Os atributos

Um **atributo** é uma variável que pertence a um objeto. Ele é lido e escrito com um ponto entre
o objeto e o nome do atributo: `rose.name` é o atributo `name` do objeto `rose`.

## Um experimento

Crie `experimentos/atributos.py`:

```python title="experimentos/atributos.py"
class Plant:
    pass


rose = Plant()
rose.name = "Rose"
rose.height = 25

oak = Plant()
oak.name = "Oak"
oak.height = 200

print(rose.name, rose.height)
print(oak.name, oak.height)
```

```bash
python3 experimentos/atributos.py
```

```text
Rose 25
Oak 200
```

- `rose.name = "Rose"` cria o atributo `name` dentro do objeto `rose` e guarda nele o texto;
- cada objeto tem os seus atributos: mudar `oak.name` não mexe em `rose.name`;
- `print()` com vários valores separados por vírgula imprime todos na mesma linha, com um espaço
  entre eles.

## O que o mypy acha disso

O Python aceitou, mas o mypy não:

```bash
.venv/bin/mypy --strict experimentos/atributos.py
```

```text
experimentos/atributos.py:6: error: "Plant" has no attribute "name"  [attr-defined]
experimentos/atributos.py:7: error: "Plant" has no attribute "height"  [attr-defined]
experimentos/atributos.py:10: error: "Plant" has no attribute "name"  [attr-defined]
experimentos/atributos.py:11: error: "Plant" has no attribute "height"  [attr-defined]
experimentos/atributos.py:13: error: "Plant" has no attribute "name"  [attr-defined]
experimentos/atributos.py:13: error: "Plant" has no attribute "height"  [attr-defined]
experimentos/atributos.py:14: error: "Plant" has no attribute "name"  [attr-defined]
experimentos/atributos.py:14: error: "Plant" has no attribute "height"  [attr-defined]
Found 8 errors in 1 file (checked 1 source file)
```

O mypy confere o código lendo a classe, e a classe `Plant` não diz em lugar nenhum que uma planta
tem `name` e `height`. Para ele, `rose.name` é tão suspeito quanto `rose.nmae`, um erro de
digitação que o Python aceitaria calado, criando um atributo novo com o nome errado.

## Declarar os atributos na classe

A correção é dizer, no corpo da classe, que atributos toda planta tem e de que tipo, com type
hints sem valor:

```python title="experimentos/atributos.py"
class Plant:
    name: str
    height: int


rose = Plant()
rose.name = "Rose"
rose.height = 25

oak = Plant()
oak.name = "Oak"
oak.height = 200

print(rose.name, rose.height)
print(oak.name, oak.height)
```

```bash
.venv/bin/mypy --strict experimentos/atributos.py
```

```text
Success: no issues found in 1 source file
```

As linhas `name: str` e `height: int` não guardam valor nenhum: só **declaram** que toda planta
tem esses atributos, com esses tipos. O valor de cada um continua sendo dado objeto por objeto,
depois de instanciar, que é o jeito que o enunciado pede neste exercício.

## Os três atributos da planta

A planta do exercício tem nome, altura e idade:

```python
class Plant:
    name: str
    height: int
    age_days: int
```

A idade se chama `age_days` ("idade em dias") e não `age` porque, no exercício 2, a planta ganha
uma ação chamada `age()` ("envelhecer"). Um objeto não deve ter um atributo e uma ação com o
mesmo nome: o atributo do objeto esconderia o método, e `rose.age()` tentaria chamar um número.
Escolher `age_days` desde já evita renomear depois.
