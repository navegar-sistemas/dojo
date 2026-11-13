---
sidebar_position: 4
title: A mensagem do erro
---

# A mensagem do erro

Os programas do projeto precisam **mostrar** o erro capturado: por exemplo,
`Caught input_temperature error: invalid literal for int() with base 10: 'abc'`. Para isso, o
bloco `except` precisa de acesso à exceção. É o que faz o `as` da
[página anterior](./03-try-e-except.md):

```python
except ValueError as error:
    print(f"Caught: {error}")
```

- `as error` guarda o objeto da exceção na variável `error`. O nome é livre; `error` é só uma
  escolha clara;
- dentro de uma f-string, `{error}` vira o **texto** da exceção, que é a mensagem:
  `invalid literal for int() with base 10: 'abc'`.

O texto da exceção é só a mensagem, sem o tipo. É por isso que a saída do projeto escreve o nome
do tipo à mão quando quer mostrá-lo, como em `print(f"Caught ValueError: {error}")` no
[exercício 2](../05-ex2/04-varios-except.md).

A variável `error` só existe dentro do bloco `except`. Depois dele, o Python a apaga.
