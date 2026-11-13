---
sidebar_position: 3
title: A estrutura e o algoritmo
---

# A estrutura e o algoritmo

O prefácio do enunciado conta um caso do Twitter: o código guardava dados em listas e perguntava
"este valor já está aqui?" milhões de vezes por segundo. Com poucos usuários, a resposta vinha em
microssegundos; com milhões, a mesma pergunta virou o gargalo do sistema. A correção foi trocar
as listas por estruturas "baseadas em hash", como o set. O código continuou fazendo a mesma
coisa, só que muito mais rápido. A frase final do prefácio resume: em escala, a sua estrutura de
dados é o seu algoritmo.

## Procurar numa lista

Para responder `"Untouchable" in achievements` numa lista, o Python compara o valor procurado com
o primeiro elemento, depois com o segundo, e assim por diante, até achar ou até a lista acabar.
Numa lista de oito elementos, procurar o último custa oito comparações; numa de um milhão, um
milhão de comparações. O tempo cresce na mesma proporção da lista (o dobro de elementos, o dobro
do tempo): é o que o prefácio chama de **tempo linear**.

## Procurar num set

O set guarda os elementos numa tabela interna com muitas gavetas. Para decidir a gaveta de um
valor, ele calcula o **hash** do valor: um número inteiro obtido a partir do conteúdo, sempre o
mesmo para valores iguais. Procurar um valor é calcular o hash dele e abrir a gaveta
correspondente. Às vezes dois valores caem na mesma gaveta (uma **colisão**), e o set olha mais
uma ou duas. Mesmo assim, não importa se o set tem oito ou um milhão de elementos: a busca olha
uma gaveta, ou poucas.

![À esquerda, uma lista de oito conquistas: procurar "Untouchable" compara com cada elemento, da posição 0 à 7, e só acha na oitava comparação. À direita, um set com as mesmas conquistas em doze gavetas numeradas: o hash de "Untouchable" aponta direto para a gaveta 2, onde ela está, numa comparação só](/img/colecoes/busca-lista-vs-set.svg)

O dicionário usa a mesma tabela para as chaves: achar `inventory["sword"]` também é calcular um
hash e abrir uma gaveta.

## Medir

```python title="experimentos/velocidade.py"
import time

numbers_list = list(range(1_000_000))
numbers_set = set(numbers_list)

start = time.perf_counter()
for _ in range(100):
    found = 999_999 in numbers_list
list_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(100):
    found = 999_999 in numbers_set
set_time = time.perf_counter() - start

print(f"list: {round(list_time * 1000, 3)} ms")
print(f"set:  {round(set_time * 1000, 3)} ms")
```

- `list(range(1_000_000))` cria uma lista com os inteiros de 0 a 999 999 (o `_` dentro do número
  só separa os milhares para facilitar a leitura); `set(numbers_list)` cria um set com os mesmos
  valores;
- `time.perf_counter()` devolve um relógio em segundos; a diferença entre duas leituras é o tempo
  que passou;
- cada laço procura 100 vezes o último número. A variável `_` é o nome costumeiro para uma
  variável de laço que não é usada;
- o tempo é multiplicado por 1000 para sair em milissegundos (`ms`) e arredondado em três casas.

```bash
python3 experimentos/velocidade.py
```

```text
list: 571.515 ms
set:  0.007 ms
```

Os números mudam de máquina para máquina e de execução para execução, mas a diferença fica: a
lista leva centenas de milissegundos, e o set, uma fração de milissegundo. Este experimento usa o
módulo `time`, que nenhum exercício autoriza, e `range` e `round`, que só alguns autorizam. Ele
serve só para ver a diferença e não vai na entrega.

## Por que o set não aceita listas

O hash é calculado a partir do conteúdo. Se um elemento mudasse depois de guardado, o hash dele
mudaria, e o set passaria a procurá-lo na gaveta errada. Por isso, o Python não calcula o hash das
coleções mutáveis (lista, set e dicionário), e elas não podem ser elemento de set nem chave de
dicionário:

```python title="experimentos/hash.py"
print(hash(42))
print(hash((1.0, 2.5)) == hash((1.0, 2.5)))
try:
    hash([1, 2])
except TypeError as error:
    print(f"TypeError: {error}")
```

```bash
python3 experimentos/hash.py
```

```text
42
True
TypeError: unhashable type: 'list'
```

- o hash de um inteiro positivo pequeno é o próprio número;
- duas tuplas iguais têm o mesmo hash;
- uma lista não tem hash: o Python lança `TypeError`, o erro de operação feita com o tipo errado,
  com a mensagem "tipo sem hash: lista".

Um valor que tem hash se chama **hashable**. Inteiros, floats e textos são hashable; listas, sets
e dicionários não são. Uma tupla é hashable quando todos os elementos dela também são:
`(1.0, 2.5)` é, e uma tupla que guarda um set, como `("Alice", {"Legend", "Survivor"})`, não é.
É por isso que o enunciado descreve as tuplas como "ordenadas, imutáveis, hashable" ("ordenadas"
no sentido de guardar a ordem em que os elementos foram escritos, sem classificá-los): com
elementos imutáveis, ela pode ser elemento de um set ou chave de um dicionário, e a lista não
pode.

## O hash dos textos muda a cada execução

O hash de um texto é sorteado de novo cada vez que o Python começa, uma proteção contra quem
tenta montar textos que caiam todos na mesma gaveta para deixar o programa lento. Rode duas vezes:

```bash
python3 -c 'print(hash("Alice"))'
python3 -c 'print(hash("Alice"))'
```

```text
2790973624702019832
3846300548131226830
```

(`python3 -c` roda o código escrito entre aspas, sem precisar de arquivo.) Os dois números são
diferentes, e serão outros na sua máquina. Dentro de uma mesma execução, o hash de `"Alice"` é
sempre o mesmo, e o set funciona. Mas a gaveta de cada texto muda de uma execução para outra, e é
por isso que um set de textos é impresso numa ordem diferente a cada vez que o programa roda, como
no [exercício 3](../06-ex3/02-sets.md).
