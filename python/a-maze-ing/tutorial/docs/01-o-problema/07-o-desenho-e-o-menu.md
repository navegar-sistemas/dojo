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

## Quadrados coloridos

Um terminal consegue pintar o **fundo** de cada caractere com uma cor. O desenho usa só isso:
cada pedaço do labirinto vira **dois espaços** com o fundo pintado. São dois espaços porque um
caractere de terminal é mais alto do que largo, e dois lado a lado formam quase um quadrado.

As cores são ligadas e desligadas por sequências especiais de caracteres, as **sequências
ANSI**, que o terminal entende e não mostra. Elas são explicadas na
[parte 10](../10-utilitarios/08-sequencias-ansi.md).

## As posições do desenho

O desenho não tem só células: entre duas células existe a parede (ou a passagem) que as separa,
e ela também precisa de um quadrado. Por isso, uma grade de `WIDTH` colunas vira um desenho de
`2 × WIDTH + 1` quadrados de largura: uma posição para cada célula, uma para cada parede entre
células, e mais uma para a borda. O mesmo vale na altura. O tutorial chama essa tabela de
posições de **quadro**.

Para uma grade 3x2, o quadro tem 7 colunas por 5 linhas, numeradas a partir de 0:

![O quadro de uma grade 3 por 2: 7 colunas por 5 linhas de posições numeradas](/img/problema/posicoes.svg)

- **amarelo**: as células;
- **azul**: as posições de parede entre duas células e na borda; cada uma vira parede ou
  passagem, conforme o labirinto;
- **escuro**: os cantos, onde quatro paredes se encontram.

A célula `x,y` fica na coluna `2x + 1` e na linha `2y + 1` do quadro. A parede Norte dela fica
logo acima, na linha `2y`, e a Oeste logo à esquerda, na coluna `2x`. Na figura, a célula `1,0`
está na coluna 3, linha 1; a parede Norte dela (N) na coluna 3, linha 0; e a Oeste (O) na
coluna 2, linha 1.

O labirinto 3x2 do [arquivo de saída](./04-o-arquivo-de-saida.md) (`d53`/`d56`) fica assim no
terminal. A moldura escura é o fundo do terminal; as paredes são brancas, e os corredores ficam
com o fundo escuro, sem cor:

![Desenho do labirinto 3 por 2 no fundo escuro do terminal, com o caminho oculto](/img/problema/desenho-3x2.svg)

E com o caminho mais curto à mostra, em ciano:

![Desenho do labirinto 3 por 2 no fundo escuro do terminal, com o caminho em ciano](/img/problema/desenho-3x2-caminho.svg)

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
| `3` | passa as paredes para a próxima cor: branco, amarelo, verde, azul e volta ao branco | sim |
| `4` | encerra o programa | não |
| qualquer outra coisa | imprime `Invalid choice` e pergunta de novo | não |

O caminho começa escondido e as paredes começam brancas. Gerar outro labirinto troca só o
labirinto: se o caminho estava à mostra, continua à mostra, e a cor continua a escolhida.

## Sair a qualquer momento

Além da opção `4`, o usuário pode encerrar com **Ctrl+C** (interromper) ou **Ctrl+D** (fim da
entrada). Nos dois casos o programa pula uma linha e termina sem mostrar traceback (a listagem de
erro do Python). O enunciado só proíbe que o programa quebre; terminar com código de saída 0,
como na opção `4`, é escolha do projeto, porque sair assim é um pedido do usuário, não um erro.
