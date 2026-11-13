---
sidebar_position: 3
title: Converter e descartar
---

# Converter e descartar

Cada argumento é um texto. `int(texto)` o converte num inteiro, e lança `ValueError` quando o
texto não é um número inteiro. O experimento mostra o que passa e o que não passa:

```python title="experimentos/converter.py"
for text in ["1500", "-30", " 42 ", "1_000", "٣", "ab", "4.5"]:
    try:
        print(f"'{text}' -> {int(text)}")
    except ValueError as error:
        print(f"'{text}' -> ValueError: {error}")
```

```bash
python3 experimentos/converter.py
```

```text
'1500' -> 1500
'-30' -> -30
' 42 ' -> 42
'1_000' -> 1000
'٣' -> 3
'ab' -> ValueError: invalid literal for int() with base 10: 'ab'
'4.5' -> ValueError: invalid literal for int() with base 10: '4.5'
```

`int()` aceita sinal, ignora espaços nas pontas, aceita o `_` como separador de milhares e
reconhece dígitos de outras escritas, como o `٣` (3, em algarismo arábico-índico). Recusa letras
e números com parte decimal. As pontuações do enunciado são todas inteiras, então `4.5` é
inválido; números negativos continuam sendo inteiros e são aceitos.

## Um limite para as pontuações

`int()` aceita inteiros de até 4300 dígitos (acima disso, lança `ValueError`), mas a média é uma
divisão `/`, e o resultado de `/` é um `float`. Um `float` não guarda números maiores que cerca de
1.8 × 10³⁰⁸, e acima de 2⁵³ ele já começa a perder as unidades:

```python title="experimentos/limite.py"
print(2 ** 53)
print(float(2 ** 53) == 2 ** 53, float(2 ** 53 + 1) == 2 ** 53 + 1)
try:
    print(10 ** 400 / 2)
except OverflowError as error:
    print(f"OverflowError: {error}")
```

```bash
python3 experimentos/limite.py
```

```text
9007199254740992
True False
OverflowError: integer division result too large for a float
```

- 2⁵³ = 9007199254740992 é o ponto a partir do qual o `float` deixa de guardar todos os
  inteiros: até 2⁵³ todos são exatos, e `2 ** 53 + 1` vira `2 ** 53` ao passar para `float`;
- um inteiro de 400 dígitos dividido por 2 não cabe num `float`, e o Python lança
  `OverflowError` ("erro de estouro"). Sem tratamento, uma pontuação assim travaria o programa no
  cálculo da média.

O programa aceita pontuações de −2⁵³ a 2⁵³ e trata o resto como argumento inválido. O limite fica
numa constante:

```python
MAX_SCORE = 2 ** 53
```

Com esse limite, cada pontuação vira `float` sem perder nada, e a média, que fica entre a menor e
a maior pontuação, nunca passa de 2⁵³: a divisão nunca estoura. O total é um inteiro e pode passar
de 2⁵³ sem problema, porque é impresso como inteiro; a média, nesse caso, pode perder a última
casa.

## A função que separa

```python
def parse_scores(arguments: list[str]) -> list[int]:
    """Convert the arguments to scores, reporting and skipping bad ones."""
    scores: list[int] = []
    for argument in arguments:
        try:
            score = int(argument)
        except ValueError:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        if not -MAX_SCORE <= score <= MAX_SCORE:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        scores.append(score)
    return scores
```

- `scores` começa vazia;
- para cada argumento, o `try` tenta converter. Se `int()` lançar `ValueError`, o `except` avisa o
  argumento inválido, entre aspas simples, como no enunciado, e o `continue` passa para o próximo;
- `-MAX_SCORE <= score <= MAX_SCORE` confere as duas pontas de uma vez: o Python lê como
  `-MAX_SCORE <= score and score <= MAX_SCORE`. Fora da faixa, o argumento recebe o mesmo aviso;
- só um argumento que passou pelas duas conferências chega ao `append`;
- o `try` fica **dentro** do `for`: um argumento inválido é avisado e o laço segue, sem perder os
  que vêm depois;
- no fim, a função devolve a lista só com os válidos. Se nenhum era válido, devolve `[]`.

Aqui o `except` não usa `as error`, porque a mensagem impressa não inclui o texto do erro.

O argumento vai para a mensagem passando por `printable`, a função do
[exercício 0](../03-ex0/05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido) que troca um
texto com bytes inválidos por `<not valid UTF-8>`.

Com os argumentos `1500 ab 2300`, a função imprime `Invalid parameter: 'ab'` e devolve
`[1500, 2300]`.
