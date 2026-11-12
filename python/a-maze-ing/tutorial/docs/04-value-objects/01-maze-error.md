---
sidebar_position: 1
title: MazeError
---

# `MazeError`

## O que é

A única exceção que o `mazegen` levanta. Ela sai em três situações:

| Quem levanta | Quando | Exemplo de mensagem |
|---|---|---|
| construtor do `MazeGenerator` | parâmetro impossível | `width must be between 1 and 100, got 0` |
| `MazeGenerator.generate()` | o modo Pac-Man falhou 20 vezes seguidas | `could not build a Pac-Man board after 20 attempts` |
| `Maze` | o próprio gerador tentou quebrar uma regra da grade | `internal: cannot change a border or "42" wall` |

É a primeira peça do gerador porque não depende de nada, e todas as outras podem levantá-la.

## Por que uma exceção própria

Quem reutiliza o `mazegen` num outro projeto precisa saber **o que capturar**. Com uma classe
só, a resposta é uma linha:

```python
try:
    gen = MazeGenerator(width=0, height=15)
except MazeError as error:
    print("Error:", error)
```

A alternativa seria levantar `ValueError`. Mas um `except ValueError` também captura erros que
não têm nada a ver com o labirinto, como um `int("abc")` esquecido em outro ponto do programa. Um
tipo próprio diz de onde o erro veio.

O `a_maze_ing.py` (parte 14) captura `MazeError` e os erros da aplicação no mesmo lugar e imprime
`Error: <mensagem>`, sem traceback.

## Por que o corpo vazio basta

```python
class MazeError(Exception):
```

`Exception` já faz tudo o que é preciso: guarda a mensagem passada ao construtor e a devolve em
`str(error)`. A classe nova não precisa de atributo nem de método; o que importa é o **nome**,
que o `except` usa para escolher o que capturar.

Uma classe Python precisa de pelo menos uma instrução no corpo. A docstring conta como
instrução, então ela basta, sem `pass`.

## O prefixo `internal:`

Há dois tipos de erro bem diferentes:

- **erro do usuário**: um parâmetro impossível (`width=0`). A mensagem cita o parâmetro, e quem
  chamou corrige a chamada.
- **erro do programa**: um invariante quebrado, por exemplo um algoritmo tentando abrir uma
  parede da borda. Isso nunca acontece com o código correto; se acontecer, é bug.

As mensagens do segundo tipo começam com `internal:`. Quem lê `Error: internal: ...` sabe que
não adianta mudar o config: é um defeito a relatar. A docstring da classe registra essa
convenção para quem abrir o arquivo.

## Experimente

```python
from mazegen.errors import MazeError

try:
    raise MazeError("width must be between 1 and 100, got 0")
except MazeError as error:
    print("Error:", error)
print(issubclass(MazeError, Exception))
```

```text
Error: width must be between 1 and 100, got 0
True
```

## O arquivo completo

```python title="mazegen/errors.py"
"""Exception raised by the maze generator."""


class MazeError(Exception):
    """Impossible parameter or broken invariant inside the maze generator.

    Messages that start with ``internal:`` point to a bug, not to a user
    error.
    """
```
