---
sidebar_position: 1
title: Funções são valores
---

# Funções são valores

Todos os exercícios do projeto tratam funções como dados: guardam funções em variáveis e em
dicionários, passam funções para outras funções e devolvem funções. Isso é possível porque, no
Python, as funções são **cidadãs de primeira classe** (*first-class citizens*): valem tanto
quanto um número ou um texto, e podem ir para qualquer lugar onde um valor pode ir.

Os experimentos desta parte não são entregues. Para ficarem curtos, deixam o código solto no
arquivo, fora de funções. Nos exercícios, isso criaria variáveis globais, proibidas pelo
enunciado ([Escopo e closures](./04-escopo-e-closures.md)), e lá o código fica dentro de uma
função `main`.

## O experimento

Crie `experimentos/valores.py`:

```python title="experimentos/valores.py"
from collections.abc import Callable


def shout(text: str) -> str:
    return text.upper() + "!"


def whisper(text: str) -> str:
    return text.lower() + "..."


def cast(spell: Callable[[str], str], text: str) -> str:
    return spell(text)


speak = shout
print(speak("hello"))
print(speak is shout, speak.__name__)
print(cast(whisper, "HELLO"))
voices = {"loud": shout, "soft": whisper}
for name, voice in voices.items():
    print(f"{name}: {voice('Magic')}")
print(callable(shout), callable("shout"), callable(len), callable(int))
```

```bash
python3 experimentos/valores.py
```

```text
HELLO!
True shout
hello...
loud: MAGIC!
soft: magic...
True False True True
```

## O que aconteceu

**Guardar numa variável.** `speak = shout` não chama `shout`: não há parênteses. A variável
`speak` passa a apontar para a **mesma** função, e `speak("hello")` a chama. `speak is shout` dá
`True` (`is` pergunta se os dois nomes apontam para o mesmo objeto), e `speak.__name__` mostra o
nome com que a função foi criada no `def`: `shout`. Todo objeto função guarda o próprio nome no
atributo `__name__`.

**Passar como argumento.** `cast(whisper, "HELLO")` entrega a função `whisper` (de novo, sem
parênteses) para `cast`, que a chama lá dentro, com `spell(text)`. `cast` não sabe qual função vai
receber: é quem chama que decide. Uma função que recebe ou devolve outra função se chama
**função de ordem superior** (*higher-order function*).

**Guardar numa estrutura de dados.** O dicionário `voices` tem funções como valores. O `for`
percorre os pares `(nome, função)` de `voices.items()` e chama cada função com `voice('Magic')`.

## O type hint Callable

`Callable` é o type hint de "algo que pode ser chamado", como uma função. O enunciado manda
importá-lo de `collections.abc` (o módulo `typing` também tem um `Callable`, mas ele é só um
apelido antigo do de `collections.abc`).

| Type hint | Quer dizer |
|---|---|
| `Callable[[str], str]` | uma função que recebe um `str` e devolve um `str` |
| `Callable[[str, int], str]` | recebe um `str` e um `int`, devolve um `str` |
| `Callable[[], int]` | não recebe nada e devolve um `int` |
| `Callable` | qualquer coisa que possa ser chamada, sem dizer o que recebe nem o que devolve |

Entre os primeiros colchetes ficam os tipos dos argumentos; depois, o tipo do retorno. As
assinaturas do enunciado usam a forma curta, `Callable`, sem colchetes; o mypy aceita, e a
função recebida pode ser chamada com qualquer argumento. O tutorial copia essas assinaturas como
estão.

## callable()

`callable(valor)` é uma função embutida que responde se o valor pode ser chamado com
parênteses: `True` para funções (`shout`, `len`) e também para classes (`int`, porque `int("5")`
cria um número); `False` para o texto `"shout"`, que é só um nome escrito entre aspas. Ela serve
para conferir, antes de usar, se um argumento que deveria ser uma função é mesmo uma função
([spell_combiner](../04-ex1/03-spell-combiner.md)).
