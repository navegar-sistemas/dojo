---
sidebar_position: 6
title: O padrão "42"
---

# O padrão "42"

O enunciado exige que todo labirinto mostre o número **42** (o nome da escola) desenhado por
células com as quatro paredes fechadas. Essas células valem 15, ou `f` no arquivo de saída, e
aparecem em cinza no desenho. Esta página define a forma do desenho, onde ele fica e o que
acontece quando não cabe.

## A forma

O enunciado não descreve a forma em palavras, mas o exemplo de arquivo de saída que ele mostra
tem um "42" feito de `f`. Este projeto copia exatamente aquela forma: cada dígito ocupa 3
colunas por 5 linhas, com uma coluna livre entre os dois, num bloco de 7 colunas por 5 linhas.
As células cinza são do "42"; as brancas são células comuns do labirinto:

![O desenho do 42 num bloco de 7 por 5](/img/problema/glifo-42.svg)

São 18 células cinza. O "4" é aberto em cima, como no exemplo do enunciado.

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

## Onde ele fica: no centro

O bloco de 7x5 fica centralizado na grade. Para centralizar, sobra o mesmo espaço dos dois
lados: a largura que sobra é `WIDTH − 7`, e metade dela fica à esquerda do bloco. O mesmo vale
na vertical. O canto de cima à esquerda do bloco fica em:

```python
x0 = (WIDTH - 7) // 2
y0 = (HEIGHT - 5) // 2
```

O `//` é a divisão inteira do Python: divide e joga fora a parte quebrada (`13 // 2` dá `6`).
Quando a sobra é ímpar, o bloco fica uma célula mais perto da esquerda (ou de cima).

Cada `X` da linha `dy` e da coluna `dx` do desenho (contando de 0) vira a célula
`x0 + dx, y0 + dy` da grade.

Exemplo, numa grade 20x15: `x0 = (20 − 7) // 2 = 6` e `y0 = (15 − 5) // 2 = 5`. O "4" ocupa as
colunas 6 a 8, o "2" as colunas 10 a 12, e os dois as linhas 5 a 9:

![Labirinto 20 por 15 com o 42 em cinza no centro](/img/problema/labirinto-20x15.svg)

## Regras

- As células do "42" ficam com as quatro paredes fechadas e **fora do labirinto**: o gerador
  nunca abre passagem para elas. Por isso o enunciado faz a exceção "toda célula é alcançável,
  menos as do 42".
- A entrada e a saída não podem cair numa célula do "42". O programa recusa:

  ```text
  Error: config.txt: ENTRY=6,5 lies on the "42" pattern
  ```

- O mesmo tamanho de grade dá sempre as mesmas células do "42", nos dois tipos de labirinto e em
  toda regeneração.

## Quando não cabe

Para o desenho ficar legível, o bloco precisa de pelo menos uma célula de corredor entre ele e
cada borda: são 7 + 2 = 9 colunas e 5 + 2 = 7 linhas. Com `WIDTH` menor que 9 ou `HEIGHT` menor
que 7, o "42" não cabe.

O enunciado diz o que fazer nesse caso: gerar o labirinto **sem** o "42" e mostrar uma mensagem
de erro no terminal. O programa imprime:

```text
Error: maze too small for the "42" pattern
```

e continua normalmente, mostrando o labirinto e o menu. Terminar com código de saída 0 nesse caso
é uma escolha do projeto: o labirinto foi gerado e funciona, só falta o desenho.

## Duas células presas

As células brancas dentro do bloco são comuns e fazem parte do labirinto. Duas delas ficam
dentro das curvas do "2", na coluna 5 do desenho: uma na linha 1 e outra na linha 3. Cada uma
está cercada por células do "42" por três lados e só tem uma vizinha livre. Elas viram sempre becos sem saída, e não há como abrir outra passagem,
porque os outros lados dão para o "42". Esses becos são chamados de **becos cercados** e não
contam na regra do Pac-Man de "no máximo dois becos".
