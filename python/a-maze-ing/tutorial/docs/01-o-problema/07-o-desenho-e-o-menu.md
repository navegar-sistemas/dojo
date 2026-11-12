---
sidebar_position: 7
title: O desenho e o menu
---

# O desenho e o menu

O enunciado exige que o programa **mostre** o labirinto, com as paredes, a entrada, a saída e o
caminho mais curto bem visíveis, e que o usuário possa interagir com ele enquanto o programa
roda. Esta página mostra como o labirinto aparece no terminal e o que o menu oferece.

## Terminal ou janela

O enunciado aceita duas formas de mostrar o labirinto: desenhado no **terminal**, com
caracteres, ou numa **janela gráfica** com a biblioteca MiniLibX. A MiniLibX que vem com o
enunciado só funciona em Linux, então este projeto desenha no terminal, o que funciona em
qualquer máquina.

## Quadrados coloridos

Um terminal consegue pintar o **fundo** de cada caractere com uma cor. O desenho usa só isso:
cada pedaço do labirinto vira **dois espaços** com o fundo pintado. São dois espaços porque um
caractere de terminal é mais alto do que largo, e dois lado a lado formam quase um quadrado.

As cores são ligadas e desligadas por sequências especiais de caracteres, as **sequências
ANSI**, que o terminal entende e não mostra. Elas são explicadas na
[parte 10](../10-utilitarios/04-cores-ansi.md).

## As posições do desenho

O desenho não tem só células: entre duas células existe a parede (ou a passagem) que as separa,
e ela também precisa de um quadrado. Por isso, uma grade de `WIDTH` colunas vira um desenho de
`2 × WIDTH + 1` quadrados de largura: uma posição para cada célula, uma para cada parede entre
células, e mais uma para a borda. O mesmo vale na altura.

Para uma grade 3x2, são 7 por 5 posições:

![As posições do desenho de uma grade 3 por 2](/img/problema/posicoes.svg)

- **amarelo**: as células;
- **azul**: as paredes, ou passagens, entre duas células e na borda;
- **escuro**: os cantos, onde quatro paredes se encontram.

Contando as posições a partir de 0, a célula `x,y` fica na coluna `2x + 1` e na linha `2y + 1`
do desenho; a parede Norte dela fica logo acima, e a Oeste logo à esquerda.

O labirinto 3x2 do [arquivo de saída](./04-o-arquivo-de-saida.md) (`d53`/`d56`) fica assim no
terminal, com as paredes brancas e o fundo escuro do terminal nos corredores:

![Desenho do labirinto 3 por 2 com o caminho oculto](/img/problema/desenho-3x2.svg)

E com o caminho mais curto à mostra:

![Desenho do labirinto 3 por 2 com o caminho em ciano](/img/problema/desenho-3x2-caminho.svg)

## As cores

| O quê | Cor |
|---|---|
| paredes e cantos | branco, amarelo, verde ou azul (troca pelo menu) |
| células do "42" | cinza |
| entrada | magenta |
| saída | vermelho |
| caminho mais curto, quando visível | ciano |
| corredor | o fundo normal do terminal |

As cores são escolha do projeto; o enunciado só pede que as paredes, a entrada, a saída e o
caminho sejam distinguíveis e que a cor das paredes possa mudar.

## O menu

Depois de cada desenho, o programa mostra um menu e espera o usuário digitar um número e
apertar Enter:

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

As três primeiras opções são as interações que o enunciado exige; a quarta é a saída do
programa.

| Escolha | Efeito | Desenha de novo |
|---|---|---|
| `1` | gera outro labirinto e regrava o arquivo de saída | sim |
| `2` | mostra o caminho mais curto, ou esconde se já estava à mostra | sim |
| `3` | passa as paredes para a próxima cor: branco, amarelo, verde, azul e volta ao branco | sim |
| `4` | encerra o programa | não |
| qualquer outra coisa | imprime `Invalid choice` e pergunta de novo | não |

O caminho começa escondido e as paredes começam brancas. Gerar outro labirinto troca só o
labirinto: se o caminho estava à mostra, continua à mostra, e a cor continua a escolhida.

## Sair a qualquer momento

Além da opção `4`, o usuário pode encerrar com **Ctrl+C** (interromper) ou **Ctrl+D** (fim da
entrada). Nos dois casos o programa pula uma linha e termina normalmente, sem mostrar
traceback.
