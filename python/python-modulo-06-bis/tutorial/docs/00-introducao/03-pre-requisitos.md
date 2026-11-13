---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float` e `str` | `count = 3`, `price = 2.5`, `name = "foo"` |
| `if`, `elif`, `not`, `and`, `or` | `if not data:` |
| laço `for` sobre uma lista | `for item in items:` |
| laço `for` que só repete: `range(3)` dá 0, 1 e 2, e `_` é o nome de costume para a variável que não é usada | `for _ in range(3):` |
| laço `while`, que repete enquanto a condição for verdadeira | `while len(data) < 3:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"total {count} items"` vira `total 3 items` |
| listas, tuplas e dicionários | `[1, 2]`, `(0, "a")`, `{"log_level": "INFO"}` |
| desempacotar uma tupla em duas variáveis | `rank, value = (0, "a")` |

## Classes, em resumo

Uma **classe** é o molde de um tipo de objeto. Um **objeto** (ou **instância**) é um valor
criado a partir do molde, chamando a classe como uma função:

```python
class Counter:
    def __init__(self) -> None:
        self.count = 0

    def add(self) -> None:
        self.count += 1


counter = Counter()
counter.add()
counter.add()
print(counter.count)
```

```text
2
```

- `__init__` é o **construtor**: roda sozinho quando o objeto é criado, com `Counter()`;
- `self` é o próprio objeto. `self.count` é um **atributo**: uma variável guardada dentro do
  objeto, que dura enquanto ele existir;
- `add` é um **método**: uma função definida dentro da classe, chamada com ponto
  (`counter.add()`). O Python passa o objeto como `self` sozinho.

Um atributo cujo nome começa com `_`, como `self._items`, é **interno** por costume: só o código
da própria classe (e das filhas) deve mexer nele. O Python não impede o acesso de fora; o `_` é
um aviso para quem lê.

Um atributo também pode ser criado direto no corpo da classe, fora de qualquer método:
`name = "Counter"`. Esse é um **atributo de classe**: o mesmo valor para todos os objetos,
lido como `counter.name`.

## Herança, em resumo

Uma classe pode **herdar** de outra: escreve-se a classe mãe entre parênteses. A classe filha
ganha todos os métodos e atributos da mãe e pode acrescentar os seus:

```python
class LoudCounter(Counter):
    def shout(self) -> None:
        print(f"COUNT IS {self.count}!")


loud = LoudCounter()
loud.add()
loud.shout()
```

```text
COUNT IS 1!
```

`LoudCounter` não tem `__init__` nem `add`: usa os de `Counter`. A parte
[Classes abstratas e polimorfismo](../02-conceitos/01-sobrescrever-um-metodo.md) parte daqui.

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
`Odd number` sobe para quem chamou, como qualquer outra exceção. `TypeError` é o tipo de exceção
que o Python usa quando um valor é do **tipo** errado, como em `"abc" + 1`.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
e listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos
funcionam no terminal do Linux e do macOS.
