---
sidebar_position: 1
title: O primeiro modelo
---

# O primeiro modelo

Um **modelo** do Pydantic é uma classe que descreve um tipo de dado: quais campos ele tem e de
que tipo é cada um. A classe herda de **`BaseModel`**, a classe base do Pydantic, e lista os
campos como linhas `nome: tipo` no corpo da classe, sem `__init__`. O `BaseModel` cria o
construtor sozinho, a partir dessa lista, e esse construtor confere cada valor recebido.

## O experimento

Crie `experimentos/modelo.py`:

```python title="experimentos/modelo.py"
from pydantic import BaseModel


class Planet(BaseModel):
    name: str
    moons: int
    has_rings: bool = False


earth = Planet(name="Earth", moons=1)
saturn = Planet(name="Saturn", moons=274, has_rings=True)
print(earth)
print(repr(saturn))
print(f"{saturn.name} has {saturn.moons} moons")
```

- `from pydantic import BaseModel` traz a classe `BaseModel` da biblioteca;
- `class Planet(BaseModel)` cria o modelo. Cada linha `nome: tipo` do corpo é um **campo**;
- `has_rings: bool = False` tem um **valor padrão**: quem cria o objeto pode deixar esse campo de
  fora, e ele vale `False`. `name` e `moons` não têm padrão: são **obrigatórios**;
- o objeto é criado chamando a classe com os campos **pelo nome** (`name="Earth"`). O
  construtor do `BaseModel` não aceita valores sem nome, como `Planet("Earth", 1)`;
- cada campo vira um atributo do objeto: `saturn.name`, `saturn.moons`.

```bash
.venv/bin/python experimentos/modelo.py
```

```text
name='Earth' moons=1 has_rings=False
Planet(name='Saturn', moons=274, has_rings=True)
Saturn has 274 moons
```

- `print(earth)` mostra os campos e os valores, separados por espaço; o `has_rings`, que não foi
  passado, aparece com o valor padrão;
- `repr(saturn)` dá a forma completa, com o nome da classe na frente. `repr` é a função embutida
  que devolve um valor escrito do jeito que ele seria escrito no código; com ela, um texto aparece
  entre aspas.

## O que o modelo garante

Um objeto `Planet` só existe se cada campo passou na conferência: `name` é um `str`, `moons` é um
`int`, `has_rings` é um `bool`. Quando um valor não serve, o construtor não devolve objeto
nenhum: lança uma exceção, a **`ValidationError`**
([próxima página](./02-validationerror.md)). Por isso o resto do programa pode usar `saturn.moons`
como inteiro sem conferir de novo.

O mypy também conhece o modelo. Ele confere, sem rodar o programa, que cada argumento passado ao
construtor tem o tipo do campo e que nenhum campo obrigatório ficou de fora
([E pelo construtor?](./04-conversao-de-tipos.md#e-pelo-construtor)).

```bash
.venv/bin/flake8 experimentos/modelo.py
.venv/bin/mypy --disallow-untyped-defs experimentos/modelo.py
```

```text
Success: no issues found in 1 source file
```
