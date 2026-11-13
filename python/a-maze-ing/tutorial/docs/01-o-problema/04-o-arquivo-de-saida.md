---
sidebar_position: 5
title: O arquivo de saída
---

# O arquivo de saída

Além de desenhar o labirinto na tela, o programa precisa **gravá-lo num arquivo de texto**, no
formato que o enunciado define. É esse arquivo que outro programa (ou um avaliador) lê para
conferir se o labirinto está certo. O nome do arquivo vem da opção `OUTPUT_FILE` do arquivo de
configuração.

## As partes do arquivo

1. A **grade**: uma linha do arquivo para cada linha do labirinto, e um caractere para cada
   célula. O caractere é o número das paredes da célula em hexadecimal, de `0` a `f`, como
   mostrado em [As paredes de uma célula em um número](./02-paredes-em-bits.md).
2. Uma **linha vazia**.
3. A **entrada**, como `x,y`.
4. A **saída**, como `x,y`.
5. O **caminho mais curto** da entrada até a saída, uma letra por passo: `N` (um passo para
   cima), `E` (para a direita), `S` (para baixo) ou `W` (para a esquerda).

## Um exemplo pequeno

Um labirinto de 3 colunas por 2 linhas, com a entrada em `0,0` e a saída em `0,1`:

```text
d53
d56

0,0
0,1
EESWW
```

As duas primeiras linhas são a grade. Cada caractere vira as paredes da célula na mesma
posição:

![Labirinto 3 por 2 com o caractere de cada célula](/img/problema/exemplo-3x2.svg)

Decifrando as duas linhas com a [tabela de exemplos](./02-paredes-em-bits.md#tabela-de-exemplos)
(em `x,y`, o `x` é a coluna e o `y` a linha, contando de 0):

| Célula | Caractere | Valor | Soma | Paredes fechadas | Passagens |
|---|---|---|---|---|---|
| `0,0` | `d` | 13 | 8 + 4 + 1 | Oeste, Sul e Norte | Leste |
| `1,0` | `5` | 5 | 4 + 1 | Sul e Norte | Oeste e Leste |
| `2,0` | `3` | 3 | 2 + 1 | Leste e Norte | Oeste e Sul |
| `0,1` | `d` | 13 | 8 + 4 + 1 | Oeste, Sul e Norte | Leste |
| `1,1` | `5` | 5 | 4 + 1 | Sul e Norte | Oeste e Leste |
| `2,1` | `6` | 6 | 4 + 2 | Sul e Leste | Oeste e Norte |

A linha de cima (`d53`) é um corredor que vai da esquerda para a direita e desce pela célula
`2,0`, que não tem parede no Sul. A linha de baixo (`d56`) é outro corredor, que recebe essa
descida pela `2,1` (sem parede no Norte) e volta para a esquerda até a `0,1`.

Depois da linha vazia vêm a entrada (`0,0`), a saída (`0,1`) e o caminho `EESWW`: dois passos
para a direita, um para baixo e dois para a esquerda.

![O caminho EESWW no labirinto 3 por 2](/img/problema/exemplo-3x2-caminho.svg)

## Regras do formato

- As letras do hexadecimal saem em **minúsculas** (`a` a `f`). O enunciado não diz se as letras
  são maiúsculas ou minúsculas. O texto dele escreve o valor 10 como `A`, maiúsculo, num
  exemplo ("`A` (binário `1010`) significa que as paredes leste e oeste estão fechadas"). O
  arquivo de exemplo que ele mostra usa minúsculas: as duas primeiras linhas são
  `9139551111555515515395153` e `ac2a9102829113855692c3a92`. O verificador que acompanha o
  enunciado aceita as duas formas. O projeto usa minúsculas, como o arquivo de exemplo.
- A linha `y` do arquivo é a linha `y` da grade, e o caractere de número `x` dessa linha (contando
  de 0) é a célula `x,y`.
- Toda linha termina com uma quebra de linha (`\n`), inclusive a última.
- Nada de espaços, comentários ou linhas a mais. O fim do arquivo de exemplo do enunciado
  aparece assim:

  ```text
  1,1        # entry  (x,y)
  19,14      # exit   (x,y)
  ESEENEEESSSEESESSESESSSSEEEEEESES
  ```

  O `# entry (x,y)` e o `# exit (x,y)` ao lado das coordenadas são só anotações que o enunciado
  pôs no exemplo para explicar ao leitor o que cada linha é. Com eles no arquivo, o verificador do enunciado
  não consegue ler a entrada. O arquivo que o projeto grava traz só as coordenadas, como
  `0,0` e `19,14`.

## Quando o arquivo é gravado

Na primeira geração e toda vez que o usuário pede um labirinto novo pelo menu. Cada gravação
substitui o arquivo inteiro: no fim, ele contém o último labirinto mostrado.

A gravação acontece **antes** do desenho, por escolha do projeto: assim, o que aparece na tela
está sempre no arquivo. Se a gravação falha (por exemplo, a pasta não existe), o programa mostra
só o erro e termina com código 1, sem desenhar um labirinto que não está no arquivo:

```text
Error: cannot write output file 'nao_existe/maze.txt': No such file or directory
```

## O verificador do enunciado

O enunciado vem com um programa pronto, o `maze_analyzer.py`, que lê o arquivo de saída e
confere:

- se as paredes são coerentes (duas vizinhas concordam sobre a parede que dividem);
- se toda célula é alcançável a partir da entrada;
- se o labirinto é **perfeito** ou um **tabuleiro de Pac-Man** utilizável. Ele só recebe o
  arquivo de saída, então não sabe o que o arquivo de configuração pediu: quem roda o
  verificador compara a resposta dele com o `PERFECT` que usou.

Para este projeto, um arquivo está certo quando esse verificador o aceita.
