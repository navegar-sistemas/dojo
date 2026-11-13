---
sidebar_position: 4
title: O método __str__
---

# O método `__str__`

A [página anterior](./03-a-mensagem-padrao.md) terminou com um problema: `PlantError()` guarda
`"Unknown plant error"` em `self.message`, mas o texto da exceção sai vazio, porque vem do
`args`. A solução é fazer o texto vir de `self.message`.

Quem transforma um objeto em texto é o método **`__str__`**. Toda vez que o objeto aparece num
`print`, ou dentro de `{}` numa f-string, o Python chama o `__str__` dele.

Uma classe filha recebe os métodos da mãe que ela não reescreve (a página
[A família de erros do jardim](./05-heranca.md) volta a isso). Assim, toda exceção já tem um
`__str__` pronto, definido em `BaseException`, a base de todas, e é ele que monta o texto a
partir do `args`. Uma classe que escreve o
seu próprio `__str__` substitui o herdado; basta escrevê-lo para devolver a mensagem guardada:

```python
class PlantError(Exception):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message
```

Crie `experimentos/comstr.py` com esta classe e as duas linhas de `print` do experimento
`semstr.py` da [página anterior](./03-a-mensagem-padrao.md):

```python
class PlantError(Exception):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


print(f"[{PlantError('The tomato plant is wilting!')}]")
print(f"[{PlantError()}]")
```

```bash
python3 experimentos/comstr.py
```

```text
[The tomato plant is wilting!]
[Unknown plant error]
```

## Por que não `super()`

Muitos exemplos de Python escrevem esse `__init__` com `super().__init__(message)`, que entrega a
mensagem para o `__init__` de `Exception` e dispensa o `__str__`. Mas `super()` é uma
**função embutida** do Python, e a lista de funções autorizadas do exercício 3 tem só `print()`.
Guardar a mensagem em `self.message` e devolvê-la no `__str__` chega ao mesmo resultado sem
chamar nenhuma função fora da lista.
