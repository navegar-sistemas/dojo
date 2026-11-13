---
sidebar_position: 2
title: input_temperature
---

# input_temperature

A função recebe o texto lido do sensor e devolve a temperatura como inteiro. O `int()` já faz
exatamente isso:

```python
def input_temperature(temp_str: str) -> int:
    return int(temp_str)
```

- `temp_str: str`: o parâmetro é um texto (`str`); o nome `temp_str` é o que o enunciado usa;
- `-> int`: a função devolve um inteiro;
- `int(temp_str)`: converte. `int("25")` devolve `25`; `int("-50")` devolve `-50`.

## E quando o texto não é um número?

`int("abc")` lança um `ValueError`, como mostrou a página
[O programa que trava](../02-excecoes/01-o-programa-que-trava.md). A função **não** captura esse
erro: ela não saberia o que devolver no lugar de uma temperatura que não existe. A exceção sobe
para quem chamou `input_temperature`, e é ali, na função de teste, que o erro é tratado (a
página [A exceção sobe](../02-excecoes/05-a-excecao-sobe.md) mostra esse caminho).

Essa divisão de trabalho é a ideia central do exercício: **quem faz o trabalho lança o erro;
quem sabe o que fazer com ele, captura.**
