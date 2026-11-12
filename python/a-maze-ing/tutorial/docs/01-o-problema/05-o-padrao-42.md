---
sidebar_position: 5
title: O padrão "42"
---

# O padrão "42"

O subject pede que o labirinto mostre um **"42"** desenhado por células totalmente fechadas
(valor `15`, dígito `f` no arquivo).

## O desenho

Dois dígitos de 3 colunas por 5 linhas, com uma coluna livre entre eles. As células cinza são
do "42"; as brancas são células comuns:

![O desenho do 42 num bloco de 7 por 5](/img/problema/glifo-42.svg)

No código, o desenho é guardado como texto, uma string por linha, com `X` para célula do "42" e
`.` para célula comum:

```python
GLYPHS = (
    "X...XXX",
    "X.....X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
)
```

## Onde ele fica

Centralizado na grade. O canto de cima à esquerda do bloco 7x5 fica em:

```text
x0 = (WIDTH  − 7) // 2
y0 = (HEIGHT − 5) // 2
```

e cada `X` da linha `dy`, coluna `dx` do desenho vira a célula `(x0 + dx, y0 + dy)`.

Para 20x15: `x0 = 13 // 2 = 6` e `y0 = 10 // 2 = 5`. O "4" ocupa as colunas 6 a 8, o "2" as
colunas 10 a 12, e os dois as linhas 5 a 9:

![Labirinto 20 por 15 com o 42 em cinza no centro](/img/problema/labirinto-20x15.svg)

## Regras

- As células do "42" valem `15` e **nenhuma passagem as toca**. Elas ficam fora do labirinto: o
  gerador nunca entra nelas.
- `ENTRY` e `EXIT` não podem cair num `X`:

  ```text
  Error: config.txt: ENTRY=6,5 lies on the "42" pattern
  ```

- O mesmo tamanho de grade dá sempre as mesmas células, nos dois modos e em toda regeneração.

## Quando não cabe

O bloco precisa de pelo menos uma célula de corredor entre ele e cada borda: `WIDTH >= 9` e
`HEIGHT >= 7`. Numa grade menor, o labirinto é gerado **sem** o "42", e o programa avisa em
stderr, sem tratar isso como falha (código de saída 0):

```text
Error: maze too small for the "42" pattern
```

## Duas células especiais

As células `.` dentro do bloco são comuns e alcançáveis. Duas delas, à direita do "4" (linhas 1
e 3 do desenho), só têm uma vizinha fora do "42". Por isso viram sempre becos sem saída
**cercados**, e não contam como becos reais na regra do Pac-Man.
