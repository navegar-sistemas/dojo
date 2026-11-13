---
sidebar_position: 5
title: Booleanos
---

# Booleanos

`PERFECT=True` escolhe o tipo de labirinto (perfeito ou tabuleiro de Pac-Man) e chega ao
programa como texto. Ele precisa virar o booleano `True` ou `False`, o tipo do Python que só
tem esses dois valores. Esta página mostra o conversor `to_bool` do `ValueParser`, a classe de
conversores começada na [página 3](./02-inteiros-sem-surpresa.md).

## A armadilha do `bool()`

O jeito óbvio não funciona:

```bash
.venv/bin/python -c 'print(bool("False"))'
```

```text
True
```

Para o Python, todo texto **não vazio** é verdadeiro, inclusive o texto `"False"`. `bool()` só
diz se o texto tem algum caractere. É o erro clássico de converter booleano a partir de texto.

## `to_bool`: comparar com as duas palavras

```python
lowered = value.lower()
if lowered == "true":
    return True
if lowered == "false":
    return False
raise ValueError(value)
```

- `value.lower()` passa o texto para minúsculas: `True`, `TRUE` e `true` viram todos `true`.
- Duas comparações decidem; qualquer outro texto levanta `ValueError`, como no `to_int`.

O enunciado escreve `PERFECT=True`. Aceitar qualquer caixa (maiúsculas ou minúsculas) é escolha
do projeto, porque é natural alguém escrever `true`.

O que **não** é aceito: `yes`, `1`, `sim`, `on`. Cada um é a convenção de outro programa; aceitar
uns e recusar outros seria arbitrário, e aceitar todos não teria fim. `True` e `False` são as
palavras do enunciado e do próprio Python.

O último conversor, o de coordenadas, e o arquivo completo do `ValueParser` estão na
[próxima página](./03-booleanos-e-coordenadas.md).
