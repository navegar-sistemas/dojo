---
sidebar_position: 4
title: O texto do arquivo de saída
---

# O texto do arquivo de saída

O `FileMazeRepository` (`amazeing/repositories/maze_repository.py`) grava o retrato no
`OUTPUT_FILE`. O trabalho se divide em dois métodos: `to_text`, que monta o conteúdo, e `save`,
que grava (próxima página).

## O formato

O formato vem do subject (parte 1): uma linha de dígitos hexadecimais por linha da grade, uma
linha vazia, a entrada, a saída e o caminho. Para um labirinto 11x9 com `seed=3`:

![Labirinto 11 por 9 com o dígito hexadecimal de cada célula](/img/geracao/arquivo-11x9.svg)

```text
95395391553
a968546c552
aafa93fff96
86fc6857fc3
c3fffafff92
9693fafd52a
a92afafffaa
aa829451542
c6c44554556

0,0
10,8
SSSSESWSSSENNESESEEEEEEE
```

Cada dígito do arquivo é o número escrito na célula da figura: a linha `y` do arquivo é a linha
`y` da grade, e o caractere `x` é a coluna `x`. Os `f` do meio são o "42".

## A grade em hexadecimal

```python
lines = ["".join(format(cell, "x") for cell in row)
         for row in maze.grid]
```

Para cada linha da grade, cada célula vira um dígito, e os dígitos são colados sem separador.

`format(cell, "x")` escreve o número em hexadecimal, em **minúsculas** e sem prefixo:

| Valor | `format(v, "x")` | `hex(v)` | `format(v, "X")` |
|---|---|---|---|
| 0 | `0` | `0x0` | `0` |
| 9 | `9` | `0x9` | `9` |
| 10 | `a` | `0xa` | `A` |
| 15 | `f` | `0xf` | `F` |

- `hex()` põe o prefixo `0x`, que teria de ser cortado.
- `"X"` dá maiúsculas. O `maze_analyzer.py` aceita as duas, mas o exemplo do subject usa
  minúsculas, e o projeto segue o exemplo.

Como o valor de uma célula vai de 0 a 15, o resultado é sempre **um** dígito: nunca é preciso
completar com zero à esquerda.

## O rodapé

```python
ex, ey = maze.entry
sx, sy = maze.exit
lines += ["", f"{ex},{ey}", f"{sx},{sy}", maze.solution]
```

- `""` é a linha vazia que separa a grade do rodapé.
- A entrada e a saída saem como `x,y`, sem espaço e sem parênteses: o mesmo formato do config.
  Escrever `str(maze.entry)` daria `(0, 0)`, que o `maze_analyzer.py` não lê.
- O caminho é o `solution`, as mesmas letras que o desenho pinta de ciano.

O exemplo do subject tem anotações como `# entry (x,y)` ao lado do rodapé. Elas fazem parte da
**figura**, não do arquivo: com elas, o `maze_analyzer.py` não acha a entrada.

## Juntar com `\n`

```python
return "\n".join(lines) + "\n"
```

`"\n".join(lines)` põe uma quebra **entre** as linhas, mas não depois da última. O `+ "\n"` final
faz toda linha terminar em quebra, inclusive a do caminho: é o que um arquivo de texto bem formado
tem, e o que o formato pede.

## Por que `to_text` é separado e estático

Montar o texto não precisa de arquivo nem de estado: recebe um retrato, devolve uma string. Fica
num método à parte, `@staticmethod`, por dois motivos:

- `save` fica curto: abrir, escrever, tratar o erro;
- dá para ver o conteúdo exato sem gravar nada, como no exemplo abaixo.

## Experimente

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.repositories.maze_repository import FileMazeRepository

maze = GeneratedMaze(((9, 1, 3), (12, 4, 6)), (0, 0), (2, 1), "EES",
                     frozenset())
print(repr(FileMazeRepository.to_text(maze)))
'
```

```text
'913\nc46\n\n0,0\n2,1\nEES\n'
```

O `repr` mostra cada `\n`: um depois de cada linha da grade, o par `\n\n` da linha vazia, e o
`\n` final depois do caminho.
