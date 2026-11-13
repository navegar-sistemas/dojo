---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

O enunciado pede domínio de funções, classes, exceções e estruturas de dados básicas. Os
exercícios usam este básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float`, `str` e `bool` | `power = 50`, `average = 72.33`, `name = "Alex"`, `valid = True` |
| `if`, `elif`, `else`, `not`, `and`, `or` | `if not mages:` |
| laço `for` sobre uma lista | `for spell in spells:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"{name} has {power} power"` vira `Alex has 50 power` |
| listas, tuplas e dicionários | `[1, 2]`, `("a", "b")`, `{"name": "Alex", "power": 50}` |
| ler uma chave de um dicionário | `mage["power"]` dá `50` |
| desempacotar uma tupla ou lista em variáveis | `first, second = ["a", "b"]` |
| fatia de lista: `[:2]` são os dois primeiros itens | `[5, 6, 7][:2]` dá `[5, 6]` |
| juntar textos de uma lista com um separador | `", ".join(["a", "b"])` dá `"a, b"` |

## Compreensão de lista

Uma **compreensão de lista** monta uma lista nova a partir de outra, numa linha:

```python
numbers = [1, 2, 3]
doubles = [number * 2 for number in numbers]
```

`doubles` vale `[2, 4, 6]`: para cada `number` de `numbers`, a expressão `number * 2` entra na
lista nova. É o mesmo que um `for` com `append`, escrito de forma mais curta.

## Classes, em resumo

Uma **classe** é o molde de um tipo de objeto. Um **objeto** (ou **instância**) é um valor
criado a partir do molde, chamando a classe como uma função:

```python
class Mage:
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self) -> str:
        return f"I am {self.name}"


mage = Mage("Alex")
print(mage.greet())
```

```text
I am Alex
```

- `__init__` é o **construtor**: roda sozinho quando o objeto é criado, com `Mage("Alex")`;
- `self` é o próprio objeto. `self.name` é um **atributo**: uma variável guardada dentro do
  objeto;
- `greet` é um **método**: uma função definida dentro da classe, chamada com ponto
  (`mage.greet()`). O Python passa o objeto como `self` sozinho.

## Exceções, em resumo

Quando algo dá errado, o Python cria uma **exceção**: um objeto que descreve o erro, com um
**tipo** (como `TypeError`) e uma **mensagem**. Se nenhum `except` a captura, o programa para e
imprime um relatório de erro chamado **traceback**. Um bloco `try` com `except` captura a
exceção, e o programa continua:

```python
try:
    number = int("abc")
except ValueError as error:
    print(f"Caught: {error}")
```

```text
Caught: invalid literal for int() with base 10: 'abc'
```

`as error` guarda a exceção na variável `error`, e `{error}` imprime a mensagem dela.

O próprio código também pode **lançar** uma exceção, com `raise`, quando recebe algo que não
aceita:

```python
def half(number: int) -> int:
    if number % 2 != 0:
        raise ValueError("Odd number")
    return number // 2
```

`half(3)` interrompe a função na linha do `raise`, e a exceção `ValueError` com a mensagem
`Odd number` sobe para quem chamou. Os tipos mais usados no projeto são `ValueError` (o valor é
do tipo certo, mas não serve, como uma operação desconhecida) e `TypeError` (o valor é do
**tipo** errado, como um texto onde se esperava uma função).

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
e listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos
funcionam no terminal do Linux e do macOS.
