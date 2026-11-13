---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `float`, `str` e `bool` | `crew = 6`, `power = 85.5`, `name = "ISS"`, `ok = True` |
| `if`, `elif`, `not`, `and`, `or` | `if not ok:` |
| laço `for` sobre uma lista | `for member in crew:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"Crew: {crew} people"` vira `Crew: 6 people` |
| listas e dicionários | `[1, 2]`, `{"name": "ISS", "crew": 6}` |
| `None`, o valor que quer dizer "nada" | `notes = None` |
| repetir um texto com `*` | `"=" * 5` vira `=====` |

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

`LoudCounter` não tem `__init__` nem `add`: usa os de `Counter`. Todo modelo do Pydantic é uma
classe filha de `BaseModel`, e herda dela o construtor que confere os dados
([O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md)).

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
`Odd number` sobe para quem chamou, como qualquer outra exceção. O Pydantic usa exceções do mesmo
jeito: quando um dado não passa, ele lança uma exceção própria, a `ValidationError`.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
e listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos
funcionam no terminal do Linux e do macOS.
