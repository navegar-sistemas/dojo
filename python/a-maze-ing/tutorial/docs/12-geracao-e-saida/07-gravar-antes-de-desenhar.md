---
sidebar_position: 8
title: Gravar antes de desenhar
---

# Gravar antes de desenhar

O `execute` do `GenerateMaze` ([página anterior](./06-o-caso-de-uso-generate-maze.md)) grava o
arquivo de saída antes de devolver o retrato a quem vai desenhá-lo. A ordem importa quando a
gravação falha: o usuário não pode ver na tela um labirinto diferente do que está no arquivo.
Esta página explica essa ordem, as exceções que o `execute` deixa passar e mostra o arquivo
completo.

## Quando a gravação falha

O desenho só acontece **depois** que o `execute` devolve o retrato. Se a gravação falha, o
`save` levanta `OutputError`, o `execute` não chega ao `return`, e a exceção sobe até o `main`
do `a_maze_ing.py` ([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)). Quando o programa
estiver pronto, ele imprime o erro e termina com código 1:

```text
Error: cannot write output file 'nao_existe/maze.txt': No such file or directory
```

Assim, o usuário nunca vê na tela um labirinto que não está no arquivo. Na ordem inversa,
desenhar e depois gravar, uma falha deixaria na tela um labirinto que o arquivo não tem. O
arquivo ficaria com o labirinto anterior, se a falha acontecesse ao abrir (a pasta não existe,
falta permissão), ou vazio ou pela metade, se acontecesse durante a escrita (o disco encheu): o
modo `"w"` apaga o conteúdo antigo assim que abre o arquivo. Essa ordem é escolha do projeto.

Vale também na regeneração: se o disco encher entre uma geração e outra, a opção `1` termina
no mesmo formato, `Error: cannot write output file ...`, com a frase do sistema para o disco
cheio (`No space left on device`), e o mesmo código 1 da primeira geração.

## Um caminho só para todas as gerações

A tela e o arquivo vêm do **mesmo** retrato, criado uma vez por chamada: o objeto que o `save`
gravou é o mesmo que o `execute` devolve para desenhar.

E a primeira geração e as regenerações passam pelo mesmo `execute`. Se a regeneração fosse um
código à parte no menu, bastaria esquecer o `save` ali para o arquivo ficar com o labirinto
antigo.

## As exceções

O `execute` não captura nada: as duas falhas possíveis já chegam com a mensagem pronta para o
usuário.

| Exceção | De onde | Quando |
|---|---|---|
| `MazeError` | `generate()` | o gerador não conseguiu montar um tabuleiro de Pac-Man em 20 tentativas |
| `OutputError` | `save()` | o `OUTPUT_FILE` não pode ser gravado |

O `main` captura as duas na mesma linha, `except (AppError, MazeError)`
([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)).

## O arquivo completo

```python title="amazeing/use_cases/generate_maze.py"
"""Use case that generates, stores and returns one maze."""

from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.use_cases.ports import MazeRepository
from mazegen import MazeGenerator


class GenerateMaze:
    """One generation: generate, snapshot, store, return.

    The first maze and every regeneration go through execute, so the file
    always holds the maze that the screen shows next.
    """

    def __init__(self, generator: MazeGenerator, repository: MazeRepository,
                 config: MazeConfig) -> None:
        """Keep the collaborators of the use case.

        Args:
            generator: Generator built from the configuration.
            repository: Storage of the output file.
            config: Validated configuration.
        """
        self._generator = generator
        self._repository = repository
        self._config = config

    def execute(self) -> GeneratedMaze:
        """Generate a new maze and store it before anyone draws it.

        Returns:
            The stored maze.

        Raises:
            MazeError: The generator could not build the maze.
            OutputError: The output file cannot be written.
        """
        self._generator.generate()
        maze = GeneratedMaze.from_generator(
            self._generator, self._config.entry, self._config.exit)
        self._repository.save(self._config.output_file, maze)
        return maze
```

## Experimente

Qualquer objeto com um `save` serve de repositório. O `Memory` abaixo não grava nada: só anota
numa lista o caminho e o `solution` de cada labirinto que receberia:

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.maze_config import MazeConfig
from amazeing.use_cases.generate_maze import GenerateMaze
from mazegen import MazeGenerator


class Memory:
    def __init__(self):
        self.saved = []

    def save(self, path, maze):
        self.saved.append((path, maze.solution))


config = MazeConfig.create({"WIDTH": "6", "HEIGHT": "4", "ENTRY": "0,0",
                            "EXIT": "5,3", "OUTPUT_FILE": "maze.txt",
                            "PERFECT": "False", "SEED": "1"})
generator = MazeGenerator(config.width, config.height, config.entry,
                          config.exit, config.perfect, config.seed)
memory = Memory()
use_case = GenerateMaze(generator, memory, config)
first = use_case.execute()
second = use_case.execute()
print(memory.saved)
print(first.solution, second.solution)
'
```

```text
[('maze.txt', 'EESEEESS'), ('maze.txt', 'EEEEESSS')]
EESEEESS EEEEESSS
```

Duas chamadas, dois labirintos, duas gravações no mesmo caminho, cada uma com o retrato que o
`execute` devolveu. O `Memory` não herda de nada e não importa nada: é a porta `MazeRepository`
funcionando. Com `FileMazeRepository()` no lugar de `memory`, o `maze.txt` fica com o segundo
labirinto, o último devolvido.
