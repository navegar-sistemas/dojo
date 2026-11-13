---
sidebar_position: 4
title: A mensagem do erro
---

# A mensagem do erro

O exercício 0 imprimia o `msg` do primeiro erro. Aqui isso não serve: quando o erro vem de um
`ValueError` lançado numa regra, o Pydantic escreve `Value error, ` na frente da mensagem, e a
saída do enunciado mostra a mensagem sem esse acréscimo
([A mensagem da regra](../02-conceitos/06-model-validator.md#a-mensagem-da-regra)):

| | Texto |
|---|---|
| `msg` do erro | `Value error, Telepathic contact requires at least 3 witnesses` |
| saída do enunciado | `Telepathic contact requires at least 3 witnesses` |

Uma função escolhe o texto certo para cada tipo de erro. Ela entra no arquivo depois da classe
`AlienContact`:

```python
def validation_message(error: ValidationError) -> str:
    detail = error.errors()[0]
    # A ValueError raised by a validator shows up in msg as
    # "Value error, <text>"; ctx keeps the original exception.
    if detail["type"] == "value_error":
        return str(detail["ctx"]["error"])
    return detail["msg"]
```

- `detail` é o dicionário do primeiro erro;
- se o erro é de uma regra (`type` igual a `"value_error"`), a função devolve o `ValueError`
  original, guardado em `ctx["error"]`, convertido em texto com `str`: só a mensagem que a regra
  escreveu;
- qualquer outro erro, como um limite de campo, já tem no `msg` a mensagem do Pydantic, sem
  acréscimo, e a função a devolve como está.

Com essa função, a demonstração imprime a mensagem certa nos dois casos: uma regra quebrada mostra
`Telepathic contact requires at least 3 witnesses`, e um campo fora do limite mostra, por exemplo,
`Input should be less than or equal to 1440`.

## Outros caminhos

Tirar o `Value error, ` do começo do `msg` com uma operação de texto daria o mesmo resultado
neste caso, mas dependeria da forma exata como o Pydantic escreve a mensagem. Lançar a exceção
própria do `pydantic_core` (a biblioteca que o Pydantic instala junto) também deixaria o `msg`
sem acréscimo, mas acrescentaria um `import` de outra biblioteca. O `ctx["error"]` usa só o que
a `ValidationError` já entrega.
