---
sidebar_position: 2
title: Lambda
---

# Lambda

Funções como `sorted`, `max` e `map` recebem uma função pequena que diz **como** tratar cada
item: por qual campo ordenar, o que comparar, como transformar. Escrever um `def` com nome só para
isso, usado uma única vez, põe a regra numa função à parte, longe do lugar onde ela é usada. A
**lambda** resolve: é uma função sem nome, escrita no próprio lugar onde é usada.

```python
lambda potion: potion["price"]
```

- `lambda` abre a função;
- antes dos dois-pontos, os parâmetros (aqui, um: `potion`);
- depois dos dois-pontos, **uma expressão só**, cujo valor é devolvido. Não há `return`, nem
  vários comandos, nem `if` de bloco (só a expressão condicional `a if condição else b`).

Essa lambda faz o mesmo que:

```python
def price(potion: dict) -> int:
    return potion["price"]
```

Uma lambda não aceita type hints nos parâmetros. O mypy deduz o tipo de cada parâmetro pelo lugar
onde a lambda é usada e confere o corpo com esse tipo: com `words: list[str]`, a linha
`sorted(words, key=lambda word: word + 1)` dá o erro
`Unsupported operand types for + ("str" and "int")`, porque `word` é um `str`. O
`--disallow-untyped-defs` não reclama da falta de anotação, porque ele só vale para funções
escritas com `def`.

## O experimento

Crie `experimentos/lambdas.py`:

```python title="experimentos/lambdas.py"
potions: list[dict] = [
    {"name": "Mana", "price": 30},
    {"name": "Health", "price": 50},
    {"name": "Speed", "price": 20},
]

names = map(lambda potion: potion["name"], potions)
print(type(names))
print(list(names))
print(list(names))
print(list(filter(lambda potion: potion["price"] < 40, potions)))
print(sorted(potions, key=lambda potion: potion["price"]))
print(sorted(potions, key=lambda potion: potion["price"], reverse=True))
print(max(potions, key=lambda potion: potion["price"]))
print(min(potions, key=lambda potion: potion["price"]))
print(sum(map(lambda potion: potion["price"], potions)))
print(round(100 / 3, 2))
print((lambda a, b: a + b)(2, 3))
```

A anotação `list[dict]` em `potions` é necessária. Sem ela, o mypy deduz o tipo pelos valores:
cada dicionário mistura `str` (`"Mana"`) e `int` (`30`), e ele conclui `dict[str, object]`, em que
`object` quer dizer "um valor qualquer, sem operação garantida". Aí ele recusa comparar e somar
preços (`<`, `sorted`, `max`, `min`, `sum`), porque um `object` não garante nenhuma das duas
operações. Com `dict` sem colchetes, o mypy aceita qualquer chave e qualquer valor, e confia no
código, inclusive dentro das lambdas.

```bash
python3 experimentos/lambdas.py
```

```text
<class 'map'>
['Mana', 'Health', 'Speed']
[]
[{'name': 'Mana', 'price': 30}, {'name': 'Speed', 'price': 20}]
[{'name': 'Speed', 'price': 20}, {'name': 'Mana', 'price': 30}, {'name': 'Health', 'price': 50}]
[{'name': 'Health', 'price': 50}, {'name': 'Mana', 'price': 30}, {'name': 'Speed', 'price': 20}]
{'name': 'Health', 'price': 50}
{'name': 'Speed', 'price': 20}
100
33.33
5
```

## O que aconteceu

| Linha | Função | O que a lambda diz | Resultado |
|---|---|---|---|
| `map(lambda potion: potion["name"], potions)` | `map` aplica a função a cada item | "de cada poção, pegue o nome" | os nomes |
| `filter(lambda potion: potion["price"] < 40, potions)` | `filter` fica com os itens em que a função dá verdadeiro | "o preço é menor que 40?" | Mana e Speed |
| `sorted(potions, key=...)` | `sorted` devolve uma lista **nova**, ordenada pelo valor que a função `key` dá a cada item | "ordene pelo preço" | do mais barato ao mais caro |
| `sorted(..., reverse=True)` | `reverse=True` inverte a ordem | | do mais caro ao mais barato |
| `max(potions, key=...)` e `min(...)` | devolvem o **item** com o maior ou o menor valor de `key` | "compare pelo preço" | a poção inteira, não só o preço |
| `sum(map(...))` | `sum` soma os números | "de cada poção, pegue o preço" | 100 |

E mais três detalhes:

- **`map` e `filter` são preguiçosos.** Eles não devolvem uma lista, e sim um **iterador**
  (`type(valor)` dá a classe de um valor, e a de `names` é `<class 'map'>`): um objeto que entrega
  os itens um por um, só quando alguém pede, e uma única vez. O primeiro `list(names)` pediu
  todos os itens; o segundo não recebeu nenhum (`[]`). Por isso o código do projeto embrulha `map` e `filter` em `list(...)` quando precisa devolver uma lista;
- **`round(valor, 2)`** arredonda para duas casas decimais: `100 / 3` é `33.333...`, e vira
  `33.33`;
- **uma lambda pode ser chamada no lugar**: `(lambda a, b: a + b)(2, 3)` cria a função e a chama
  com 2 e 3. Ela pode ter vários parâmetros, separados por vírgula.

`sorted` não muda a lista original: `potions` continua na ordem em que foi escrita. Quando dois
itens têm o mesmo valor de `key`, eles ficam na ordem em que estavam (a ordenação do Python é
**estável**).

## Lambda com nome: use def

Uma lambda também pode ser guardada numa variável. Crie `experimentos/nome_lambda.py`:

```python title="experimentos/nome_lambda.py"
price = lambda potion: potion["price"]
print(price({"name": "Mana", "price": 30}))
```

```bash
python3 experimentos/nome_lambda.py
.venv/bin/flake8 experimentos/nome_lambda.py
```

```text
30
experimentos/nome_lambda.py:1:1: E731 do not assign a lambda expression, use a def
```

O programa funciona, mas o flake8 recusa: "não atribua uma expressão lambda, use um def". Uma
lambda guardada num nome é uma função com nome escrita do jeito mais limitado (sem type hints,
sem vários comandos, e com `__name__` igual a `<lambda>`, o que atrapalha mensagens de erro). A
regra prática: **lambda para uma função curta usada uma vez, no lugar em que é passada; `def` para
uma função que precisa de nome.** Corrija o arquivo:

```python title="experimentos/nome_lambda.py"
def price(potion: dict) -> int:
    return potion["price"]


print(price({"name": "Mana", "price": 30}))
```

```bash
python3 experimentos/nome_lambda.py
.venv/bin/flake8 experimentos/nome_lambda.py
```

```text
30
```

O exercício 0 segue essa regra: toda função que ordena, filtra, transforma ou compara é uma lambda
passada direto para `sorted`, `filter`, `map`, `max` ou `min`
([O problema do exercício 0](../03-ex0/01-o-problema.md)).
