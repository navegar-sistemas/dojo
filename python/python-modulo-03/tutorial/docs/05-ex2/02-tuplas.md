---
sidebar_position: 2
title: Tuplas
---

# Tuplas

Uma posição tem sempre três números, nessa ordem, e não faz sentido trocar só o `y` de uma
posição: um jogador que se move está numa posição **nova**. A coleção feita para isso é a
**tupla** (`tuple`): uma sequência ordenada, como a lista, mas que não muda depois de criada. O
enunciado a descreve como "dados gravados em pedra".

```python title="experimentos/tuplas.py"
position = (1.0, 2.5, 3.0)
print(position)
print(position[0], position[-1], len(position))
x, y, z = position
print(f"X={x}, Y={y}, Z={z}")
try:
    position[0] = 9.0
except TypeError as error:
    print(f"TypeError: {error}")
```

```bash
python3 experimentos/tuplas.py
```

```text
(1.0, 2.5, 3.0)
1.0 3.0 3
X=1.0, Y=2.5, Z=3.0
TypeError: 'tuple' object does not support item assignment
```

- os parênteses com valores separados por vírgula criam a tupla, e `print` a mostra do mesmo
  jeito;
- índices e `len()` funcionam como na lista;
- `x, y, z = position` é o **desempacotamento** (*unpacking*): cada variável da esquerda recebe
  um elemento, na ordem. O número de variáveis tem de ser igual ao de elementos; com dois nomes
  para três valores, o Python lança `ValueError`. O desempacotamento funciona com qualquer
  sequência, inclusive listas, e o exercício usa esse erro para conferir se a posição digitada
  tem três partes ([get_player_pos](./04-get-player-pos.md));
- tentar trocar um elemento lança `TypeError`: "objeto tupla não aceita atribuição a item". Não
  há `append` nem nenhum outro método que mude a tupla.

## Tupla ou lista?

| | tupla | lista |
|---|---|---|
| tamanho | fixo | cresce e diminui |
| muda depois de criada | não | sim |
| pode ser elemento de set ou chave de dicionário | sim, se os elementos dela também forem hashable | não |
| uso típico | um registro com partes de significado fixo: `(x, y, z)`, `(nome, ação)` | vários valores do mesmo tipo: pontuações, argumentos |

Uma posição é um registro: a primeira parte é sempre o `x`. Por isso ela é uma tupla. A
anotação de tipo diz o tipo de cada posição: `tuple[float, float, float]` é uma tupla de
exatamente três floats.
