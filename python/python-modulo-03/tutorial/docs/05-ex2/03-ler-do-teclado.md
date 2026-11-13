---
sidebar_position: 3
title: Ler do teclado
---

# Ler do teclado

As posições são digitadas pelo usuário enquanto o programa roda. A função `input()` mostra uma
pergunta, espera o usuário digitar e apertar Enter, e devolve o texto digitado:

```python
text = input("Enter new coordinates as floats in format 'x,y,z': ")
```

O texto da pergunta aparece sem quebra de linha no fim, então o que o usuário digita fica na
mesma linha, como no enunciado. O texto devolvido não inclui o Enter.

Daí em diante, o trabalho é transformar um texto como `"1.0 , 2.5, 3.0"` em três floats. O
experimento usa textos fixos no lugar do `input()`, para rodar sem precisar digitar:

```python title="experimentos/partes.py"
for text in ["1.0 , 2.5, 3.0", "hello world", "4,abc,5"]:
    print(text.split(","))
print("'" + " 2.5".strip() + "'")
print(float(" 2.5"), float("4"), float("-7"))
try:
    float("abc")
except ValueError as error:
    print(f"ValueError: {error}")
```

```bash
python3 experimentos/partes.py
```

```text
['1.0 ', ' 2.5', ' 3.0']
['hello world']
['4', 'abc', '5']
'2.5'
2.5 4.0 -7.0
ValueError: could not convert string to float: 'abc'
```

## split: cortar nas vírgulas

`text.split(",")` corta o texto em cada vírgula e devolve a **lista** dos pedaços. Os espaços
ficam nos pedaços: `"1.0 , 2.5, 3.0"` vira `['1.0 ', ' 2.5', ' 3.0']`. Um texto sem vírgula vira
uma lista de um pedaço só, o texto inteiro.

O número de pedaços decide o primeiro erro: diferente de três, a entrada não tem o formato
`x,y,z`, e a resposta é `Invalid syntax`. `len()` não está autorizada neste exercício, e a
conferência é feita sem contar os pedaços ([get_player_pos](./04-get-player-pos.md)).

## strip: tirar os espaços das pontas

`" 2.5".strip()` devolve o texto sem os espaços do começo e do fim: `"2.5"`. As aspas em volta da
saída do experimento mostram que os espaços sumiram.

O `float()` já ignora esses espaços sozinho, mas a mensagem de erro do enunciado mostra a parte
que falhou: `Error on parameter 'abc'`. Com `strip`, a parte sai limpa na mensagem, sem os
espaços que estavam em volta da vírgula.

## float: converter

`float(texto)` converte o texto num número com parte decimal (escrita com **ponto**, como `2.5`),
e lança `ValueError` quando o texto não é um número. A mensagem do erro,
`could not convert string to float: 'abc'` ("não foi possível converter o texto em float"), é a
que o enunciado repete depois de `Error on parameter 'abc': `. Inteiros como `"4"` viram `4.0`.

O `float()` também aceita textos que não são posições de verdade:

```python title="experimentos/especiais.py"
print(float("inf"), float("nan"), float("1e200"))
try:
    print(1e200 ** 2)
except OverflowError:
    print("OverflowError")
```

```bash
python3 experimentos/especiais.py
```

```text
inf nan 1e+200
OverflowError
```

- `"inf"` vira o infinito, e `"nan"` (*not a number*, "não é um número") um valor especial que
  representa um resultado indefinido. Com eles, a distância sairia `inf` ou `nan`, que não é uma
  distância;
- `"1e200"` é a **notação científica**: 1 × 10²⁰⁰. É um float comum, mas o seu quadrado passa do
  maior float, cerca de 1.8 × 10³⁰⁸, e `** 2` lança `OverflowError` ("erro de estouro"). Sem
  tratamento, a conta da distância travaria o programa.

O programa recusa os três casos, com uma faixa de valores aceitos
([get_player_pos](./04-get-player-pos.md#a-faixa-de-valores)).

Os métodos `split` e `strip` são do tipo `str`, e `float()` é o construtor do tipo `float`: os
três vêm da regra geral que libera esses tipos em todos os exercícios.
