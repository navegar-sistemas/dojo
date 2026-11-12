---
sidebar_position: 6
title: O desenho e o menu
---

# O desenho e o menu

## Desenhar com cores de fundo

O labirinto é desenhado no terminal com **cores de fundo ANSI**: cada posição do desenho são
dois espaços pintados de uma cor. Dois espaços porque um caractere de terminal é mais alto do que
largo, e dois juntos formam um quadrado.

Uma grade `W x H` vira um desenho de `2W + 1` colunas por `2H + 1` linhas, porque entre duas
células sempre existe uma posição de parede, e entre quatro paredes sempre existe um canto. Para
uma grade 3x2, são 7 por 5 posições:

![As posições do desenho de uma grade 3 por 2](/img/problema/posicoes.svg)

| Posição | Representa |
|---|---|
| `(2x + 1, 2y + 1)` | a célula `(x, y)` |
| `(2x + 1, 2y)` | a parede Norte da célula `(x, y)` |
| `(2x, 2y + 1)` | a parede Oeste da célula `(x, y)` |
| `(2x, 2y)` | o canto entre quatro paredes |

O labirinto 3x2 da página do arquivo de saída fica assim no terminal, com as paredes brancas:

![Desenho do labirinto 3 por 2 com o caminho oculto](/img/problema/desenho-3x2.svg)

![Desenho do labirinto 3 por 2 com o caminho em ciano](/img/problema/desenho-3x2-caminho.svg)

## As cores

| O quê | Cor |
|---|---|
| paredes e cantos | branco, amarelo, verde ou azul (troca pelo menu) |
| célula do "42" | cinza |
| entrada | magenta |
| saída | vermelho |
| caminho mais curto, quando visível | ciano |
| corredor | fundo padrão do terminal |

## O menu

Depois de cada desenho:

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

| Escolha | Efeito | Desenha de novo |
|---|---|---|
| `1` | gera outro labirinto e regrava o arquivo | sim |
| `2` | mostra ou esconde o caminho | sim |
| `3` | avança a cor das paredes | sim |
| `4` | sai com código 0 | não |
| outra coisa | imprime `Invalid choice` e pergunta de novo | não |

O caminho começa oculto e as paredes começam brancas. Regenerar troca só o labirinto: o caminho
continua visível ou oculto, e a cor continua a escolhida.

## Sair sem susto

Ctrl+C ou o fim da entrada (Ctrl+D) encerram o programa com uma linha vazia e código 0, sem
traceback.

## Por que não uma janela gráfica

O subject oferece a MiniLibX para desenhar numa janela, mas o pacote fornecido é um binário de
Linux. O desenho no terminal funciona em qualquer máquina e também é aceito pelo subject.
