---
sidebar_position: 1
title: O retrato GeneratedMaze
---

# O retrato `GeneratedMaze`

Depois de cada `generate()`, o `MazeGenerator` guarda o labirinto em três atributos públicos:
`grid`, `solution` e `pattern`. Duas peças da aplicação precisam desse resultado: o repositório,
que grava o arquivo de saída, e o `RenderService` (parte 13), que desenha. O `GeneratedMaze`
(`amazeing/domain/value_objects/generated_maze.py`) é um **retrato** desse resultado: uma cópia
imutável, tirada logo depois da geração.

## Por que não ler direto do gerador

O desenho e o arquivo têm de mostrar **o mesmo** labirinto: as mesmas paredes, a mesma entrada e
saída, o mesmo caminho. Se os dois lessem os atributos do gerador:

- `grid` é uma lista de listas, mutável: qualquer código com acesso a ela pode alterar uma parede
  por engano, e o desenho deixaria de bater com o arquivo;
- cada `generate()` troca `grid` e `solution`: quem guardasse o gerador para desenhar depois
  veria o labirinto **atual**, não o que foi gravado;
- o gerador não expõe a entrada e a saída, que o arquivo e o desenho também precisam.

O retrato resolve as três: congela o resultado de **uma** geração, junto com a entrada e a saída,
num objeto que ninguém consegue mudar. O arquivo e a tela partem do mesmo retrato, então não têm
como discordar.

## Os campos

```python
@dataclass(frozen=True)
class GeneratedMaze:
    grid: tuple[tuple[int, ...], ...]
    entry: tuple[int, int]
    exit: tuple[int, int]
    solution: str
    pattern: frozenset[tuple[int, int]]
```

| Campo | Tipo | Conteúdo |
|---|---|---|
| `grid` | tupla de tuplas | `grid[y][x]` = paredes fechadas da célula `(x, y)` |
| `entry`, `exit` | `(x, y)` | as células do config |
| `solution` | `str` | o caminho mais curto, uma letra `N`, `E`, `S` ou `W` por passo |
| `pattern` | `frozenset` | as células `(x, y)` do "42"; vazio quando ele não coube |

Cada tipo é a versão **imutável** do que o gerador usa: `tuple` no lugar de `list`, `frozenset`
no lugar de `set`. `frozen=True` impede trocar um campo inteiro (`maze.grid = ...` levanta
`FrozenInstanceError`); os tipos imutáveis impedem mexer **dentro** do campo
(`maze.grid[0][0] = 15` levanta `TypeError`). As duas coisas juntas tornam o retrato realmente
imutável.

O `tuple[int, ...]` com reticências quer dizer "tupla de inteiros de qualquer tamanho", porque
o número de colunas varia com o config.

## `from_generator`: tirar o retrato

```python
@classmethod
def from_generator(cls, generator: MazeGenerator, entry: tuple[int, int],
                   exit: tuple[int, int]) -> "GeneratedMaze":
    return cls(tuple(tuple(row) for row in generator.grid), entry, exit,
               generator.solution, frozenset(generator.pattern))
```

- `tuple(tuple(row) for row in generator.grid)` copia linha por linha. Só `tuple(generator.grid)`
  não bastaria: a tupla de fora seria nova, mas as linhas dentro dela continuariam sendo as
  listas do gerador.
- `solution` é uma `str`, que já é imutável em Python; pode ser usada como está.
- `entry` e `exit` vêm de fora (do config), porque o gerador não os expõe.

O método é de **classe** (`@classmethod`) porque cria um objeto novo: é uma fábrica, como o
`MazeConfig.create`.

## Experimente

O retrato não muda quando o gerador gera de novo, e não aceita alteração:

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from mazegen import MazeGenerator

generator = MazeGenerator(6, 4, seed=1)
generator.generate()
maze = GeneratedMaze.from_generator(generator, (0, 0), (5, 3))
print(maze.solution)
generator.generate()
print(generator.solution)
print(maze.solution)
try:
    maze.grid[0][0] = 15
except TypeError as error:
    print(error)
'
```

```text
EESEEESS
EEEEESSS
EESEEESS
'tuple' object does not support item assignment
```

A segunda geração trocou o caminho do gerador; o retrato continua com o da primeira.
