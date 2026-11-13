---
sidebar_position: 2
title: Sets
---

# Sets

As conquistas de um jogador não têm ordem nem repetição: ou ele tem "Boss Slayer", ou não tem. A
coleção feita para isso é o **set** ("conjunto", no sentido da matemática): um grupo de valores
**únicos**, sem ordem.

```python title="experimentos/sets.py"
levels = {30, 10, 20, 10}
print(levels, len(levels))
levels.add(40)
levels.add(10)
print(levels)
print(20 in levels, 99 in levels)
levels.discard(30)
print(levels)
print(set([5, 5, 6]))
empty = set()
print(empty, len(empty))
print(type({}))
try:
    print(levels[0])
except TypeError as error:
    print(f"TypeError: {error}")
```

```bash
python3 experimentos/sets.py
```

```text
{10, 20, 30} 3
{40, 10, 20, 30}
True False
{40, 10, 20}
{5, 6}
set() 0
<class 'dict'>
TypeError: 'set' object is not subscriptable
```

- `{30, 10, 20, 10}` cria um set. O segundo `10` é ignorado: o set tem três elementos;
- `add` acrescenta um elemento. Acrescentar um que já existe (`10`) não muda nada;
- `in` responde se o valor está no set, com a busca rápida pelo hash
  ([A estrutura e o algoritmo](../02-colecoes/03-a-estrutura-e-o-algoritmo.md));
- `discard` tira um elemento, se ele estiver lá;
- `set([5, 5, 6])` cria um set a partir de uma lista, descartando as repetições;
- `set()` cria um set vazio;
- `{}` **não** é um set vazio: `type({})` mostra que é um dicionário;
- um set não tem índices: `levels[0]` lança `TypeError`, "o objeto set não aceita índice".

## A ordem não é a da escrita

O `40` foi acrescentado por último e aparece primeiro. Um set guarda cada elemento na gaveta que
o hash dele indica, e imprime os elementos na ordem das gavetas, não na ordem em que entraram.
Com números pequenos essa ordem se repete a cada execução. Com textos, o hash é sorteado de novo
cada vez que o Python começa, e o mesmo set de conquistas sai numa ordem diferente a cada
execução. O programa não deve depender da ordem de um set.

## Como um set vazio é impresso

O enunciado pergunta como o Python imprime um set vazio, e por quê. A resposta está no
experimento: `set()`. Um set com elementos é impresso entre chaves, mas as chaves vazias, `{}`,
já significam o dicionário vazio. Para que a impressão de um set vazio não seja confundida com um
dicionário, o Python a escreve como a chamada que cria um set vazio: `set()`. No exemplo do
enunciado, `Only Alice has: set()` quer dizer "nenhuma conquista só da Alice".
