---
sidebar_position: 3
title: Transformar o texto
---

# Transformar o texto

Cada linha do texto ganha um `#` no fim, antes da quebra de linha.

![Antes: as três linhas do fragmento, cada uma terminada por um \n. Depois de transform(): as mesmas linhas, cada uma com um # destacado em vermelho antes do \n](/img/ex1/transformacao.svg)

```python
def transform(content: str) -> str:
    result = ""
    for line in content.splitlines():
        result += line + "#\n"
    return result
```

## splitlines

`content.splitlines()` é um método de `str` que divide o texto nas quebras de linha e devolve uma
lista com as linhas, **sem** os `\n`:

```python
"one\ntwo\n".splitlines()
```

```text
['one', 'two']
```

## Montar o texto novo

`result` começa vazio. Para cada linha, `result += line + "#\n"` acrescenta a linha, o `#` e uma
quebra de linha nova (`a += b` é o mesmo que `a = a + b`). No fim, o texto tem as mesmas linhas de
antes, cada uma terminada em `#` e `\n`.

Como o texto novo também termina com `\n`, o `display` o mostra com a mesma linha vazia antes do
`---` final ([read e o texto](../02-arquivos/03-read-e-o-texto.md)).

## Por que não trocar \n por #\n

`content.replace("\n", "#\n")` daria o mesmo resultado para o `ancient_fragment.txt`. Num arquivo
cuja última linha não termina com `\n`, porém, a última linha ficaria sem `#`. Com `splitlines()`,
toda linha ganha o `#`, termine ela com `\n` ou não.
