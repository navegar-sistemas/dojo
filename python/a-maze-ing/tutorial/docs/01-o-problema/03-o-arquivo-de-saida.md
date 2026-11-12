---
sidebar_position: 3
title: O arquivo de saída
---

# O arquivo de saída

O labirinto gerado é gravado no `OUTPUT_FILE` do config, num formato fixo:

```text
<HEIGHT linhas, cada uma com WIDTH dígitos hexadecimais>
<linha vazia>
<x,y da entrada>
<x,y da saída>
<caminho mais curto>
```

## Exemplo mínimo

Um labirinto 3x2, entrada `0,0`, saída `0,1`:

```text
d53
d56

0,0
0,1
EESWW
```

Decifrando a primeira linha com a tabela de bits da página anterior:

| Célula | Dígito | Soma | Fechadas |
|---|---|---|---|
| `(0, 0)` | `d` | 1 + 4 + 8 | Norte, Sul e Oeste |
| `(1, 0)` | `5` | 1 + 4 | Norte e Sul |
| `(2, 0)` | `3` | 1 + 2 | Norte e Leste |

Desenhando cada célula com o seu dígito:

![Labirinto 3 por 2 com o dígito de cada célula](/img/problema/exemplo-3x2.svg)

O caminho `EESWW` sai da entrada, vai duas vezes a Leste, desce uma vez (Sul) e volta duas vezes
a Oeste até a saída:

![O caminho EESWW no labirinto 3 por 2](/img/problema/exemplo-3x2-caminho.svg)

## Regras do formato

- Um dígito por célula, em **minúsculas** (`0-9a-f`).
- A linha `y` do arquivo é a linha `y` da grade; o caractere `x` dessa linha é a célula `(x, y)`.
- Depois da grade, uma linha vazia e três linhas de rodapé:
  1. a entrada, `x,y`;
  2. a saída, `x,y`;
  3. o caminho mais curto, uma letra `N`, `E`, `S` ou `W` por passo.
- Toda linha termina em `\n`, inclusive a última. Nada de espaços extras nem `\r`.

## Quando o arquivo é gravado

Na primeira geração e a cada regeneração pelo menu. Cada gravação substitui o arquivo inteiro, e
sempre acontece **antes** do desenho: se a gravação falha, o usuário vê só o erro, nunca um
labirinto que não está no arquivo.

```text
Error: cannot write output file 'nao_existe/maze.txt': No such file or directory
```

## Um verificador pronto

O subject vem com um `maze_analyzer.py`, que lê o arquivo de saída e confere a coerência das
paredes, a conectividade e o tipo do labirinto. Ele é a régua do que o arquivo precisa conter.
