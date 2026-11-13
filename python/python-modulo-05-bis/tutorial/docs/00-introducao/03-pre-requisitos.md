---
sidebar_position: 3
title: Pré-requisitos
---

# Pré-requisitos

Os exercícios usam o básico de Python sem explicação longa:

| Assunto | Exemplo |
|---|---|
| variáveis, `int`, `str` e `bool` | `count = 3`, `name = "fire"`, `ready = True` |
| `if`, `elif`, `else`, `not`, `and`, `or`, `in` | `if name in names:` |
| laço `for` sobre uma lista | `for name in names:` |
| funções com `def` e `return` | `def double(n: int) -> int: return n * 2` |
| f-strings: texto com valores dentro de `{}` | `f"total {count} items"` vira `total 3 items` |
| listas, tuplas e dicionários | `["earth", "air"]`, `("pandas", "Data")`, `{"LOG_LEVEL": "DEBUG"}` |
| desempacotar uma tupla em duas variáveis no `for` | `for name, purpose in pairs:` |
| métodos de texto | `"Fire".lower()` dá `"fire"`; `"a,b".split(",")` dá `["a", "b"]`; `", ".join(["a", "b"])` dá `"a, b"` |
| `None`, o valor que quer dizer "nada" | `return None` |

Um **método** é uma função que pertence a um valor e é chamada com ponto: `"Fire".lower()` chama o
método `lower` do texto `"Fire"`.

## O programa que roda e o programa que é importado

Todo arquivo `.py` pode ser rodado com `python3 arquivo.py` ou importado por outro arquivo com
`import`. A linha

```python
if __name__ == "__main__":
```

separa as duas situações: o bloco dentro dela só roda quando o arquivo é o programa principal.
`__name__` é uma variável que o Python preenche sozinho: vale `"__main__"` no arquivo rodado com
`python3`, e o nome do módulo (como `"elements"`) num arquivo importado. A parte
[Módulos e pacotes](../04-conceitos/01-modulo-e-import.md) volta a isso.

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

Um traceback se lê de baixo para cima: a última linha é o tipo e a mensagem da exceção, e as
linhas de cima mostram o caminho que o programa percorreu até ela, um par de linhas por arquivo
(`File "...", line N` e a linha de código naquele ponto). Os exercícios 2 e 4 terminam com um
traceback de propósito.

## Ler um arquivo

`open(caminho)` abre um arquivo de texto, e `.read()` devolve o conteúdo inteiro como um `str`:

```python
with open("notes.txt") as file:
    text = file.read()
```

O `with` fecha o arquivo sozinho no fim do bloco, mesmo se acontecer um erro dentro dele.

## O terminal

O **terminal** é a janela onde se digitam comandos. É preciso saber andar entre pastas com `cd`
e listar arquivos com `ls`; os outros comandos são explicados onde aparecem. Os comandos
funcionam no terminal do Linux e do macOS.

Um comando roda numa pasta, a **pasta atual**, e os caminhos sem `/` no começo, como
`ex0/construct.py`, são **relativos** a ela: `ex0/construct.py` é "o arquivo `construct.py` dentro
da pasta `ex0` da pasta atual". Um caminho que começa com `/`, como `/tmp`, é **absoluto**: vale
de qualquer pasta. O comando `pwd` mostra o caminho absoluto da pasta atual.
