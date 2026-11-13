---
sidebar_position: 2
title: Protocol e duck typing
---

# Protocol e duck typing

Os processadores do exercício 0 seguem uma regra por **herança**: para ser um `DataProcessor`, a
classe precisa herdar dele. Os plugins do exercício 2 seguem a regra de outro jeito: um objeto
serve como plugin se **tem** o método `process_output` com a assinatura certa, seja qual for a
classe dele.

## Duck typing

O nome vem do ditado "se anda como um pato e grasna como um pato, então é um pato". **Duck
typing** é julgar um objeto pelo que ele sabe fazer (os métodos que tem), e não pela classe de que
ele herda.

O Python sempre funcionou assim ao rodar: `objeto.metodo()` só precisa que o objeto tenha um
`metodo`. O que falta é o mypy conseguir conferir isso antes de o programa rodar. Para isso
existe o **`Protocol`**, do módulo `typing`: uma classe que herda de `Protocol` descreve os
métodos que um objeto precisa ter, e o mypy aceita qualquer objeto que os tenha, sem exigir
herança.

## O experimento

Crie `experimentos/protocolo.py`:

```python title="experimentos/protocolo.py"
from typing import Protocol


class Speaker(Protocol):
    def speak(self, words: str) -> None:
        ...


class Robot:
    def speak(self, words: str) -> None:
        print(f"BEEP {words} BEEP")


class Parrot:
    def speak(self, words: str) -> None:
        print(f"{words}! {words}!")


def greet(speaker: Speaker) -> None:
    speaker.speak("hello")


greet(Robot())
greet(Parrot())
```

- `Speaker` herda de `Protocol` e descreve um método, `speak`. O corpo `...` (três pontos) é um
  valor do Python que não faz nada, usado aqui como corpo vazio: um `Protocol` só descreve,
  ninguém executa o método dele;
- `Robot` e `Parrot` **não herdam** de `Speaker`: só têm um `speak` com a mesma assinatura;
- `greet` recebe um `Speaker`, e o mypy aceita os dois.

```bash
python3 experimentos/protocolo.py
.venv/bin/mypy --disallow-untyped-defs experimentos/protocolo.py
```

```text
BEEP hello BEEP
hello! hello!
Success: no issues found in 1 source file
```

## Um objeto que não serve

Acrescente uma classe sem `speak` e mais uma chamada. O arquivo fica assim:

```python title="experimentos/protocolo.py"
from typing import Protocol


class Speaker(Protocol):
    def speak(self, words: str) -> None:
        ...


class Robot:
    def speak(self, words: str) -> None:
        print(f"BEEP {words} BEEP")


class Parrot:
    def speak(self, words: str) -> None:
        print(f"{words}! {words}!")


def greet(speaker: Speaker) -> None:
    speaker.speak("hello")


class Rock:
    def fall(self) -> None:
        print("thud")


greet(Robot())
greet(Parrot())
greet(Rock())
```

O mypy acusa a última linha sem rodar o programa:

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/protocolo.py
```

```text
experimentos/protocolo.py:30: error: Argument 1 to "greet" has incompatible type "Rock"; expected "Speaker"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

Rodando, as duas primeiras chamadas funcionam e a terceira para o programa. A última linha do
traceback é:

```text
AttributeError: 'Rock' object has no attribute 'speak'
```

("o objeto `Rock` não tem o atributo `speak`"). O `Protocol` não muda nada no programa rodando:
ele só deixa o mypy achar o erro antes.

## Herança ou Protocol

| | Classe abstrata (`ABC`) | `Protocol` |
|---|---|---|
| como uma classe entra na regra | herdando da classe abstrata | tendo os métodos com a assinatura certa |
| quem confere | o Python, ao criar o objeto (`TypeError`), e o mypy | só o mypy, antes de rodar |
| herda código pronto | sim: os métodos comuns, como `output` | não |
| no projeto | `DataProcessor` e os processadores | `ExportPlugin` e os plugins |

Os processadores herdam porque compartilham código (a fila, o `output`, os contadores). Os
plugins não compartilham nada além do nome de um método, e qualquer classe, até uma escrita sem
conhecer o projeto, pode virar plugin. O enunciado fecha o exercício 2 perguntando qual é a
diferença real entre os dois e por que um sistema de plugins prefere o `Protocol`; a resposta
completa está em
[Perguntas de revisão](../09-fechamento/03-perguntas-de-revisao.md#abc-ou-protocol).

## O ExportPlugin

```python
class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
```

A assinatura é a do enunciado. `ExportPlugin` entra no arquivo logo antes de `DataStream`, que
usa o nome dele no type hint de `output_pipeline` ([output_pipeline](./03-output-pipeline.md)).
No `import` de `typing`, acrescente `Protocol`: `from typing import Any, Callable, Protocol`.

Aqui o `...` é código de verdade, e fica no arquivo: é o corpo vazio do método do `Protocol`.
