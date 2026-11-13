---
sidebar_position: 3
title: União, interseção e diferença
---

# União, interseção e diferença

As quatro perguntas do exercício (o que existe no total, o que todos têm, o que só um tem, o que
falta) se respondem com as três operações clássicas entre conjuntos. Com dois sets, `a` e `b`:

![Três pares de círculos sobrepostos, a à esquerda e b à direita, com 1 e 2 só em a, 3 e 4 nos dois e 5 só em b. Na união, os dois círculos inteiros estão pintados, e o resultado de a.union(b) é {1, 2, 3, 4, 5}. Na interseção, só a parte em que os círculos se sobrepõem: a.intersection(b) é {3, 4}. Na diferença, só a parte de a que fica fora de b: a.difference(b) é {1, 2}](/img/ex3/operacoes.svg)

| Operação | Método | Resultado | Pergunta do exercício |
|---|---|---|---|
| **união** | `a.union(b)` | tudo o que está em `a` **ou** em `b` | conquistas distintas de todos |
| **interseção** | `a.intersection(b)` | só o que está em `a` **e** em `b` | conquistas comuns a todos |
| **diferença** | `a.difference(b)` | o que está em `a` e **não** em `b` | o que só um tem; o que falta a um |

```python title="experimentos/operacoes.py"
a = {1, 2, 3, 4}
b = {3, 4, 5}
c = {4, 6}
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))
print(b.difference(a))
print(a.union(b, c))
print(a.intersection(b, c))
print(a)
```

```bash
python3 experimentos/operacoes.py
```

```text
{1, 2, 3, 4, 5}
{3, 4}
{1, 2}
{5}
{1, 2, 3, 4, 5, 6}
{4}
{1, 2, 3, 4}
```

- a diferença depende da ordem: `a.difference(b)` é `{1, 2}`, e `b.difference(a)` é `{5}`;
- os três métodos aceitam vários sets de uma vez: `a.union(b, c)` junta os três;
- nenhum dos três muda `a`: cada um devolve um set **novo**, e `a` continua `{1, 2, 3, 4}`.

O Python também escreve essas operações com símbolos: `a | b` (união), `a & b` (interseção) e
`a - b` (diferença). O enunciado autoriza os métodos pelo nome, e o exercício usa os nomes.

## Juntar muitos sets, um de cada vez

Os jogadores ficam numa lista, e a quantidade pode crescer. Para juntar as conquistas de todos,
um laço acumula a união, começando de um set vazio:

```python
distinct: set[str] = set()
for achievements in [{"Legend", "Survivor"}, {"Survivor"}, {"Pacifist"}]:
    distinct = distinct.union(achievements)
```

Depois do laço, `distinct` é `{"Legend", "Survivor", "Pacifist"}`, numa ordem qualquer. Como
`union` devolve um set novo, o resultado é guardado de volta em `distinct` a cada volta.

A interseção não pode começar de um set vazio: a interseção de qualquer coisa com o vazio é
vazia. Ela começa com o primeiro set, e o laço vai cortando o que não se repete nos outros.
