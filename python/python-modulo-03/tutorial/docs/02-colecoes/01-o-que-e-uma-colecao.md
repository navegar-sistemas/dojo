---
sidebar_position: 1
title: O que é uma coleção
---

# O que é uma coleção

Cinco jogadores terminaram uma partida, e o programa precisa da pontuação de cada um. Com uma
variável por valor, o código fica assim:

```python
score1 = 1500
score2 = 2300
score3 = 1800
score4 = 2100
score5 = 1950
```

Somar, achar a maior ou imprimir todas exige escrever as cinco variáveis de novo, e um sexto
jogador obriga a mudar o código inteiro. Uma **coleção** resolve isso: é **um** valor que guarda
vários outros dentro dele. Os valores guardados se chamam **elementos**.

```python
scores = [1500, 2300, 1800, 2100, 1950]
```

`scores` é uma coleção do tipo **lista**, com cinco elementos. Seis jogadores seriam seis
elementos, sem mudar mais nada.

## O que toda coleção sabe fazer

O Python tem quatro coleções principais ([As quatro coleções](./02-as-quatro-colecoes.md)). Três
operações funcionam em todas elas:

```python title="experimentos/colecao.py"
scores = [1500, 2300, 1800, 2100, 1950]
print(len(scores))
print(2300 in scores)
print(999 in scores)
for score in scores:
    print(score)
```

```bash
python3 experimentos/colecao.py
```

```text
5
True
False
1500
2300
1800
2100
1950
```

- `len(scores)` devolve quantos elementos a coleção tem (de *length*, "comprimento");
- `2300 in scores` pergunta se o valor está na coleção e devolve `True` (verdadeiro) ou `False`
  (falso). `not in` pergunta o contrário;
- `for score in scores:` percorre a coleção: o corpo do laço roda uma vez para cada elemento, com
  `score` valendo esse elemento.

Uma coleção que pode ser percorrida com `for` também se chama **iterável** (*iterable*), de
"iterar", repetir passo a passo. O mesmo `for` serve para textos: `for letter in "abc":` percorre
as letras.
