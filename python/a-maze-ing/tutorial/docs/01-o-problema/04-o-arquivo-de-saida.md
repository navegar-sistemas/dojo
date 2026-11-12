---
sidebar_position: 4
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
   mostrado na [página anterior](./02-paredes-em-bits.md).
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

Decifrando a primeira linha, `d53`, com a tabela da página anterior:

| Célula | Caractere | Valor | Soma | Paredes |
|---|---|---|---|---|
| `0,0` | `d` | 13 | 8 + 4 + 1 | Oeste, Sul e Norte |
| `1,0` | `5` | 5 | 4 + 1 | Sul e Norte |
| `2,0` | `3` | 3 | 2 + 1 | Leste e Norte |

A célula `0,0` não tem parede no Leste, a `1,0` não tem no Leste nem no Oeste, e a `2,0` não
tem no Oeste nem no Sul: a linha de cima é um corredor que termina descendo pela direita.

Depois da linha vazia vêm a entrada (`0,0`), a saída (`0,1`) e o caminho `EESWW`: dois passos
para a direita, um para baixo e dois para a esquerda.

![O caminho EESWW no labirinto 3 por 2](/img/problema/exemplo-3x2-caminho.svg)

## Regras do formato

- As letras do hexadecimal saem em **minúsculas** (`a` a `f`). O enunciado aceita as duas
  formas; minúsculas é a escolha do projeto, igual ao exemplo do enunciado.
- A linha `y` do arquivo é a linha `y` da grade, e o caractere de número `x` dessa linha (contando
  de 0) é a célula `x,y`.
- Toda linha termina com uma quebra de linha (`\n`), inclusive a última.
- Nada de espaços, comentários ou linhas a mais. O exemplo do enunciado mostra `# entry (x,y)`
  ao lado das coordenadas, mas é só uma anotação da figura: com ela no arquivo, o verificador
  do enunciado não consegue ler a entrada.

## Quando o arquivo é gravado

Na primeira geração e toda vez que o usuário pede um labirinto novo pelo menu. Cada gravação
substitui o arquivo inteiro: no fim, ele contém o último labirinto mostrado.

A gravação acontece **antes** do desenho. Se ela falha (por exemplo, a pasta não existe), o
programa mostra só o erro e termina, sem desenhar um labirinto que não está no arquivo:

```text
Error: cannot write output file 'nao_existe/maze.txt': No such file or directory
```

## O verificador do enunciado

O enunciado vem com um programa pronto, o `maze_analyzer.py`, que lê o arquivo de saída e
confere:

- se as paredes são coerentes (duas vizinhas concordam sobre a parede que dividem);
- se toda célula é alcançável a partir da entrada;
- se o labirinto é **perfeito** ou um **tabuleiro de Pac-Man**, conforme pedido no
  arquivo de configuração.

Para este projeto, um arquivo está certo quando esse verificador o aceita.
