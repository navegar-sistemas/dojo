---
sidebar_position: 8
title: O padrão "42"
---

# O padrão "42"

O enunciado exige que o labirinto mostre o número **42** desenhado por
células com as quatro paredes fechadas, sempre que houver espaço para ele. Essas células valem
15, ou `f` no arquivo de saída, e aparecem em cinza no desenho. Esta página define a forma do
desenho, onde ele fica e o que acontece quando não cabe.

## A forma

O enunciado não descreve a forma em palavras, mas o exemplo de arquivo de saída que ele mostra
tem um "42" feito de `f`. Este projeto copia exatamente aquela forma: cada dígito ocupa 3
colunas por 5 linhas, com uma coluna livre entre os dois, num bloco de 7 colunas por 5 linhas.
As colunas e as linhas do bloco aparecem numeradas na figura, contando de 0:

![O desenho do 42 num bloco de 7 por 5, com as 18 células do 42 em cinza](/img/problema/glifo-42.svg)

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

O enunciado não diz onde o "42" fica. Pôr no centro é escolha do projeto, por dois motivos: é
onde ele fica mais visível, e a coluna livre entre o "4" e o "2" cai bem no meio da grade, o que
deixa o centro livre para o jogador começar no modo Pac-Man
([Labirinto perfeito e tabuleiro Pac-Man](./05-perfeito-e-pac-man.md)).

Para centralizar, sobra o mesmo espaço dos dois lados: a largura que sobra é `WIDTH − 7`, e
metade dela fica à esquerda do bloco. O mesmo vale na vertical. O canto de cima à esquerda do
bloco fica na coluna `x0` e na linha `y0`:

```python
x0 = (WIDTH - 7) // 2
y0 = (HEIGHT - 5) // 2
```

O `//` é a divisão inteira do Python: divide e joga fora a parte quebrada (`13 // 2` dá `6`).
Quando a sobra é ímpar, o bloco fica uma célula mais perto da esquerda (ou de cima).

Cada `X` da coluna `dx` e da linha `dy` do bloco (contando de 0) vira a célula
`x0 + dx, y0 + dy` da grade. O `d` vem de **deslocamento**: `dx` é quantas colunas o `X` está à
direita do canto do bloco, e `dy` quantas linhas abaixo.

Exemplo, numa grade 20x15: `x0 = (20 − 7) // 2 = 6` e `y0 = (15 − 5) // 2 = 5`. O "4" ocupa as
colunas 6 a 8, o "2" as colunas 10 a 12, e os dois as linhas 5 a 9. O `X` do canto do bloco
(`dx = 0`, `dy = 0`) vira a célula `6,5`:

![Labirinto 20 por 15 com o 42 em cinza no centro, a entrada em magenta e a saída em vermelho](/img/problema/labirinto-20x15.svg)

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

O enunciado só diz que o "42" pode ficar de fora quando o labirinto é pequeno demais, sem dizer
o tamanho. O mínimo de 9 colunas por 7 linhas é escolha do projeto: o bloco tem 7x5, e o projeto
exige pelo menos uma célula de corredor entre ele e cada borda, o que dá 7 + 2 = 9 colunas e
5 + 2 = 7 linhas. Essa folga deixa o desenho legível, sem colar na borda, e garante que os quatro
cantos nunca são células do "42", como pede o modo Pac-Man. Com `WIDTH` menor que 9 ou `HEIGHT`
menor que 7, o "42" não cabe.

O enunciado diz o que fazer nesse caso: gerar o labirinto **sem** o "42" e mostrar uma mensagem
de erro no terminal. O programa imprime:

```text
Error: maze too small for the "42" pattern
```

e continua normalmente, mostrando o labirinto e o menu. A mensagem volta a aparecer a cada vez
que o labirinto é desenhado de novo.

Esta é a única mensagem com `Error: ` que não encerra o programa. Os outros erros (os do
[arquivo de configuração](./03-o-arquivo-de-configuracao.md), por exemplo) impedem que exista um
labirinto, e o programa termina com código de saída 1. Aqui o labirinto foi gerado e funciona,
só falta o desenho: o texto começa com `Error: ` porque o enunciado chama esse aviso de "mensagem
de erro", mas o programa segue e, quando o usuário sai, termina com código 0. Seguir em frente
com código 0 é escolha do projeto.

## Duas células presas: os becos cercados

As células brancas dentro do bloco são comuns e fazem parte do labirinto. Duas delas ficam
dentro das curvas do "2", na coluna 5 do bloco: uma na linha 1 e outra na linha 3. Na grade
20x15, são as células `11,6` e `11,8`.

![O bloco do 42 com as duas células presas em amarelo, na coluna 5, linhas 1 e 3](/img/problema/glifo-42-cercados.svg)

Cada uma está cercada por células do "42" em três lados e só tem uma vizinha livre: a da linha 1
tem a vizinha livre à esquerda, e a da linha 3, à direita. Elas viram sempre becos sem saída, e
não há como abrir outra passagem, porque os outros lados dão para o "42".

Um beco assim, em que todas as paredes fechadas dão para a borda da grade ou para o "42", se
chama **beco cercado**: não há parede que dê para abrir. Os dois de dentro do "2" são os becos
cercados que todo "42" cria. Becos cercados não contam na regra do Pac-Man de "no máximo dois
becos"; os outros becos, que dá para abrir, são os **becos reais**.
