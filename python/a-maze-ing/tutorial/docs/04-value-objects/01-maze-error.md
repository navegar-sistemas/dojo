---
sidebar_position: 1
title: MazeError
---

# `MazeError`

O gerador precisa avisar quem o chamou quando algo dá errado: uma largura 0, por exemplo, não
dá labirinto nenhum. Em Python, esse aviso é uma **exceção**: um objeto de erro. O código
**levanta (lança)** uma exceção com `raise` (em inglês, "levantar"): a execução para naquele
ponto, e quem chamou pode capturar o erro com `try`/`except`. Esta página cria o tipo de exceção
do gerador, `MazeError`, a primeira peça do pacote `mazegen`.

## Quando ela aparece

`MazeError` é a única exceção que o `mazegen` levanta. Ela sai em três situações:

| Quem levanta | Quando | Exemplo de mensagem |
|---|---|---|
| a criação do `MazeGenerator` (a classe principal do gerador, [parte 9](../09-gerador/01-a-fachada.md)) | um parâmetro impossível | `width must be between 1 and 100, got 0` |
| `MazeGenerator.generate()` | o modo Pac-Man não deu certo em 20 tentativas seguidas | `could not build a Pac-Man board after 20 attempts` |
| o `Maze`, a grade de paredes ([parte 5](../05-maze/01-a-grade-de-paredes.md)) | o próprio gerador tentou abrir uma parede proibida | `internal: cannot change a border or "42" wall` |

O limite de 1 a 100 da primeira mensagem é uma escolha do projeto, não do enunciado
([explicada na parte 3](../03-ambiente/06-config-txt.md)).

A segunda linha vem do modo Pac-Man. Ele abre paredes sorteadas, e às vezes o sorteio deixa
becos sem saída demais ou rotas alternativas de menos. O gerador então descarta o labirinto e
tenta de novo, com um novo sorteio. Se 20 tentativas seguidas falharem, ele desiste com esse
erro. O número 20 e o motivo das tentativas estão na
[parte 9](../09-gerador/03-generate.md).

`MazeError` vem primeiro porque não depende de nada, e todas as outras peças podem levantá-la.

## Por que uma exceção própria

Quem reutiliza o `mazegen` num outro projeto precisa saber **o que capturar**. Com uma classe
só, a resposta cabe numa linha:

```python
try:
    gen = MazeGenerator(width=0, height=15)
except MazeError as error:
    print("Error:", error)
```

O `except MazeError as error` captura só erros do tipo `MazeError`, e `error` é o objeto do erro;
`print` o mostra pela mensagem.

A alternativa seria levantar `ValueError`, a exceção que o Python já usa para "valor inválido". Mas
um `except ValueError` também capturaria erros que não têm nada a ver com o labirinto, como um
`int("abc")` esquecido em outro ponto do programa, e o problema verdadeiro ficaria escondido. Um
tipo próprio diz de onde o erro veio.

O `a_maze_ing.py` ([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)) captura `MazeError` e
os erros da aplicação no mesmo lugar e imprime `Error: <mensagem>`, sem o *traceback* (a
listagem de erro que o Python mostra quando ninguém captura a exceção).

## Por que o corpo vazio basta

```python
class MazeError(Exception):
    """Impossible parameter or broken invariant inside the maze generator.

    Messages that start with ``internal:`` point to a bug, not to a user
    error.
    """
```

`class MazeError(Exception)` cria uma classe que **herda** de `Exception`: um `MazeError` é um
tipo particular de `Exception`, e ganha de graça tudo o que ela faz. E ela já faz o necessário:
guarda a mensagem passada na criação e a devolve em `str(error)`.

A classe nova não precisa de atributo nem de método. O que importa é o **nome**: é ele que o
`except` usa para escolher o que capturar.

Toda classe Python precisa de pelo menos uma instrução no corpo; a linha `class ...:` sozinha
dá erro de sintaxe. A docstring (o texto entre `"""` que documenta a classe) conta como
instrução, então ela basta, sem `pass`.

## O prefixo `internal:`

Há dois tipos de erro bem diferentes:

- **erro de quem usa**: um parâmetro impossível (`width=0`). A mensagem cita o parâmetro, e quem
  chamou corrige a chamada.
- **erro do próprio gerador**: uma regra que deveria valer sempre foi quebrada por dentro. Por
  exemplo, um algoritmo tentando abrir uma parede da borda do labirinto, que o enunciado manda
  ficar sempre fechada. Isso nunca acontece com o código correto; se acontecer, é um defeito
  (*bug*).

As mensagens do segundo tipo começam com `internal:`. É uma convenção do projeto: quem lê
`Error: internal: ...` sabe que não adianta mudar o config, porque o defeito está no código. A
docstring da classe registra essa convenção para quem abrir o arquivo.

## O arquivo completo

```python title="mazegen/errors.py"
"""Exception raised by the maze generator."""


class MazeError(Exception):
    """Impossible parameter or broken invariant inside the maze generator.

    Messages that start with ``internal:`` point to a bug, not to a user
    error.
    """
```

## Experimente

Com o arquivo acima gravado em `mazegen/errors.py`, rode na raiz do projeto (a página
[Como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos) explica
o formato: tudo entre a primeira linha e o `EOF` vai para o Python do ambiente virtual):

```bash
.venv/bin/python - <<'EOF'
from mazegen.errors import MazeError

try:
    raise MazeError("width must be between 1 and 100, got 0")
except MazeError as error:
    print("Error:", error)
print(issubclass(MazeError, Exception))
EOF
```

```text
Error: width must be between 1 and 100, got 0
True
```

O `raise` levanta o erro, o `except` o captura, e o `print` mostra a mensagem.
`issubclass(MazeError, Exception)` confirma que `MazeError` é um tipo de `Exception`.
