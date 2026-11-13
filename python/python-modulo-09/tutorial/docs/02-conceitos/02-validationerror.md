---
sidebar_position: 2
title: ValidationError
---

# ValidationError

Dados que vêm de fora do programa (de um arquivo JSON, de outro sistema) chegam como
**dicionários**, com nomes de campo como chaves: `{"name": "Mars", "moons": 2}`. Ninguém garante
que esses dicionários estão certos. Quando um valor não serve, o Pydantic lança a exceção
**`ValidationError`**, que diz quais campos falharam e por quê.

## model_validate

Para criar um objeto a partir de um dicionário, todo modelo tem o método **`model_validate`**:
`Planet.model_validate({"name": "Mars", "moons": 2})` confere o dicionário e devolve um `Planet`,
como o construtor faria com `Planet(name="Mars", moons=2)`. É o jeito de receber dados de fora.

## O experimento

Crie `experimentos/erros.py`. O segundo dicionário tem dois problemas: falta o `name`, e o
`moons` é um texto que não é número:

```python title="experimentos/erros.py"
from pydantic import BaseModel, ValidationError


class Planet(BaseModel):
    name: str
    moons: int
    has_rings: bool = False


mars = Planet.model_validate({"name": "Mars", "moons": 2})
print(repr(mars))
try:
    Planet.model_validate({"moons": "two"})
except ValidationError as error:
    print(error)
    print("---")
    print(error.error_count())
    for detail in error.errors():
        print(detail["loc"], detail["type"], detail["msg"])
```

`ValidationError` também vem de `pydantic`. O `try`/`except` captura o erro, e o programa
continua ([Exceções, em resumo](../00-introducao/03-pre-requisitos.md#exceções-em-resumo)).

```bash
.venv/bin/python experimentos/erros.py
```

```text
Planet(name='Mars', moons=2, has_rings=False)
2 validation errors for Planet
name
  Field required [type=missing, input_value={'moons': 'two'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing
moons
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='two', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/int_parsing
---
2
('name',) missing Field required
('moons',) int_parsing Input should be a valid integer, unable to parse string as an integer
```

## O que a ValidationError traz

O Pydantic confere **todos** os campos antes de desistir, e junta todos os problemas numa
exceção só. `print(error)` mostra o relatório completo:

- a primeira linha conta os erros e diz o modelo: `2 validation errors for Planet`;
- para cada erro, o nome do campo e, na linha de baixo, a **mensagem**: `Field required` ("campo
  obrigatório"); `Input should be a valid integer, unable to parse string as an integer` ("a
  entrada deveria ser um inteiro válido; não foi possível ler o texto como inteiro");
- entre colchetes, o **tipo** do erro (`missing`, `int_parsing`), o valor recebido e o tipo
  dele;
- um endereço com a explicação daquele tipo de erro. O `2.14` no meio do endereço é a versão do
  Pydantic instalada, e muda com ela.

O relatório é bom para quem lê, mas um programa precisa das partes separadas. Dois métodos da
exceção as dão:

- `error.error_count()` devolve quantos erros há;
- `error.errors()` devolve uma lista com um **dicionário por erro**. As chaves mais usadas são
  `loc`, `type` e `msg`.

| Chave | O que guarda | No primeiro erro |
|---|---|---|
| `loc` | onde está o erro: uma tupla com o caminho até o campo | `('name',)` |
| `type` | o tipo do erro, um nome curto e fixo | `'missing'` |
| `msg` | a mensagem, em inglês | `'Field required'` |
| `input` | o valor que foi recusado | o dicionário inteiro, porque o campo nem existia |

O `loc` é uma tupla porque, em modelos dentro de modelos, o caminho tem vários passos
([Modelos aninhados](./07-modelos-aninhados.md)). A vírgula em `('name',)` é a forma do Python
escrever uma tupla de um item só.

## No projeto

A saída do exercício 0 termina com a mensagem do primeiro erro:

```text
Expected validation error:
Input should be less than or equal to 20
```

Essa linha é o `msg` de `error.errors()[0]`: o primeiro dicionário da lista
([A demonstração do exercício 0](../03-ex0/03-a-demonstracao.md)).

```bash
.venv/bin/flake8 experimentos/erros.py
.venv/bin/mypy --disallow-untyped-defs experimentos/erros.py
```

```text
Success: no issues found in 1 source file
```
