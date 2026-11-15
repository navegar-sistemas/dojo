---
sidebar_position: 9
title: O desenho e o menu
---

# O desenho e o menu

O enunciado exige que o programa **mostre** o labirinto, com as paredes, a entrada, a saída e o
caminho mais curto bem visíveis, e que o usuário possa interagir com ele enquanto o programa
roda. Esta página mostra como o labirinto aparece no terminal e o que o menu oferece.

## Terminal ou janela

O enunciado aceita duas formas de mostrar o labirinto: desenhado no **terminal**, com
caracteres, ou numa **janela gráfica** com a biblioteca MiniLibX. Desenhar no terminal é
escolha do projeto: a MiniLibX que vem com o enunciado só funciona em Linux, e o terminal
funciona em qualquer máquina.

## Linhas e fundos coloridos

O desenho é feito de **texto**: cada ponto dele é um caractere do terminal. As paredes são
**caracteres de caixa**, caracteres como `━`, `┃` e `┏`, feitos para desenhar molduras: os
traços deles encostam nas bordas do caractere e se emendam com os do vizinho, formando linhas
contínuas. Eles são explicados na [parte 10](../10-utilitarios/09-caracteres-de-caixa.md).

Cada caractere do terminal tem duas cores: a do **texto** (o traço) e a do **fundo** (o
retângulo atrás do traço). O desenho usa as duas: as paredes e o caminho mais curto são linhas
coloridas no texto; o fundo é branco em todo o desenho, e cinza, magenta ou vermelho onde ficam
o "42", a entrada e a saída. As cores são ligadas e desligadas por sequências especiais de
caracteres, as **sequências ANSI**, que o terminal entende e não mostra. Elas são explicadas na
[parte 10](../10-utilitarios/08-sequencias-ansi.md).

## Onde cada pedaço fica

Um caractere de terminal é mais ou menos duas vezes mais alto do que largo. Para uma célula sair
quase quadrada, ela ocupa **4 colunas** de caracteres por **2 linhas**: uma coluna para a parede
da esquerda e três para o interior; uma linha para a parede de cima e uma para o interior. Uma
grade de `WIDTH` colunas vira um desenho de `4 × WIDTH + 1` caracteres de largura (o `+ 1` é a
borda da direita) e `2 × HEIGHT + 1` linhas de altura (o `+ 1` é a borda de baixo).

Para uma grade 3x2, o desenho tem 5 linhas de 13 caracteres, numeradas a partir de 0:

![A grade de caracteres de um labirinto 3 por 2: 5 linhas por 13 colunas, com cantos, lugares de parede e o interior de cada célula](/img/problema/grade-3x2.svg)

- **amarelo**: o interior das células, três caracteres cada; o do meio, mais forte, é o
  **centro** da célula;
- **azul**: os lugares de parede, entre duas células e na borda; cada um vira linha ou espaço,
  conforme a parede esteja fechada ou aberta;
- **escuro**: os cantos, onde até quatro paredes se encontram.

A célula `x,y` fica na linha `2y + 1`, colunas `4x + 1` a `4x + 3`, com o centro na coluna
`4x + 2`. A parede Norte dela são os três caracteres logo acima, na linha `2y`; a Oeste é o
caractere logo à esquerda, na coluna `4x`. Na figura, a célula `1,0` tem o centro na coluna 6
da linha 1; a parede Norte dela (N) ocupa as colunas 5 a 7 da linha 0; e a Oeste (O), a coluna 4
da linha 1.

O labirinto 3x2 do [arquivo de saída](./04-o-arquivo-de-saida.md) (`d53`/`d56`) fica assim no
terminal. A moldura escura é o terminal em volta; o desenho tem fundo branco e paredes grafite:

![Desenho do labirinto 3 por 2 no terminal, com o caminho oculto](/img/problema/desenho-3x2.svg)

E com o caminho mais curto à mostra, como uma linha ciano que passa pelo centro das células:

![Desenho do labirinto 3 por 2 no terminal, com o caminho em ciano](/img/problema/desenho-3x2-caminho.svg)

## As cores

| O quê | Cor | Onde |
|---|---|---|
| paredes e cantos | grafite, laranja, verde ou azul (troca pelo menu) | texto |
| caminho mais curto, quando visível | ciano | texto |
| células do "42" | cinza | fundo |
| entrada | magenta | fundo |
| saída | vermelho | fundo |
| todo o resto | branco | fundo |

As cores são escolha do projeto; o enunciado só pede que as paredes, a entrada, a saída e o
caminho sejam distinguíveis e que a cor das paredes possa mudar.

## O menu

Depois de cada desenho, o programa mostra um menu e espera o usuário digitar um número e
apertar Enter. Ler a linha inteira, com Enter, é escolha do projeto: funciona igual em qualquer
terminal, sem configurar o teclado para ler uma tecla por vez.

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

As três primeiras opções são as interações que o enunciado exige (gerar outro labirinto,
mostrar ou esconder o caminho, trocar a cor das paredes); a quarta é a saída do programa. Os
textos do menu, em inglês como todo o programa, são escolha do projeto.

| Escolha | Efeito | Desenha de novo |
|---|---|---|
| `1` | gera outro labirinto e regrava o arquivo de saída | sim |
| `2` | mostra o caminho mais curto, ou esconde se já estava à mostra | sim |
| `3` | passa as paredes para a próxima cor: grafite, laranja, verde, azul e volta ao grafite | sim |
| `4` | encerra o programa | não |
| qualquer outra coisa | imprime `Invalid choice` e pergunta de novo | não |

O caminho começa escondido e as paredes começam grafite. Gerar outro labirinto troca só o
labirinto: se o caminho estava à mostra, continua à mostra, e a cor continua a escolhida.

## Sair a qualquer momento

Além da opção `4`, o usuário pode encerrar com **Ctrl+C** (interromper) ou **Ctrl+D** (fim da
entrada). Nos dois casos o programa pula uma linha e termina sem mostrar traceback (a listagem de
erro do Python). O enunciado só proíbe que o programa quebre; terminar com código de saída 0,
como na opção `4`, é escolha do projeto, porque sair assim é um pedido do usuário, não um erro.
