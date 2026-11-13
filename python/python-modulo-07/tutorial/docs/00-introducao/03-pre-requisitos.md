---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `bool` e `str` | `count = 3`, `ready = True`, `name = "foo"` |
| `if`, `else`, `not` | `if not ready:` |
| laço `for` sobre uma lista | `for item in items:` |
| `range(a, b)`: os números de `a` até `b - 1` (com um número só, `range(b)` começa em 0) | `range(1, 4)` dá 1, 2 e 3 |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"{count} opponents"` vira `3 opponents` |
| listas e tuplas | `[1, 2]`, `("Flameling", "Fire")` |
| desempacotar uma tupla em duas variáveis, inclusive no `for` | `name, kind = ("Flameling", "Fire")` e `for name, kind in pairs:` |

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

`LoudCounter` não tem `__init__` nem `add`: usa os de `Counter`. Quando a filha define um método
com o **mesmo nome** de um método da mãe, o dela passa a valer para os objetos dela: a filha
**sobrescreve** (*override*) o método.

## Exceções, em resumo

Quando algo dá errado, o Python cria uma **exceção**: um objeto que descreve o erro, com um
**tipo** (como `ValueError`) e uma **mensagem**. Se nenhum `except` a captura, o programa para e
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
`Odd number` sobe para quem chamou, como qualquer outra exceção. Ela continua subindo, função
por função, até encontrar um `try` cujo `except` a capture.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
e listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos
funcionam no terminal do Linux e do macOS.
