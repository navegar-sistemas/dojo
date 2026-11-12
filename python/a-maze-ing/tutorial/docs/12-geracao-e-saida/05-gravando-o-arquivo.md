---
sidebar_position: 5
title: Gravando o arquivo de saída
---

# Gravando o arquivo de saída

Com o texto pronto, `save` grava. É o `save` que cumpre a porta `MazeRepository`: mesmo nome,
mesmos parâmetros, mesmo retorno.

## O método

```python
def save(self, path: str, maze: GeneratedMaze) -> None:
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(self.to_text(maze))
    except OSError as error:
        raise OutputError(f"cannot write output file '{path}': "
                          f"{error.strerror}") from None
```

### `"w"`: substituir o arquivo inteiro

O modo `"w"` cria o arquivo se ele não existe e **apaga** o conteúdo se ele existe. Cada geração
substitui o arquivo inteiro: depois de três regenerações pelo menu, o arquivo contém só o
terceiro labirinto, o que está na tela.

### `encoding="utf-8"`

O conteúdo é todo ASCII (dígitos, vírgulas, letras `NESW`), e em ASCII o UTF-8 é igual byte a
byte. O `encoding` explícito segue a regra do projeto: nunca depender da codificação padrão da
máquina.

### `newline="\n"`

No modo texto, o Python **traduz** o `\n` escrito para o fim de linha do sistema. No Linux e no
macOS, `\n` continua `\n`; no Windows, vira `\r\n`. O formato pede `\n` e nada de `\r`, em
qualquer máquina.

`newline="\n"` desliga a tradução: o que `to_text` montou é exatamente o que vai para o disco.

| `newline` | Linux e macOS | Windows |
|---|---|---|
| omitido | `\n` | `\r\n` |
| `"\n"` | `\n` | `\n` |

## O erro de gravação

Gravar pode falhar: a pasta do `OUTPUT_FILE` não existe, não há permissão de escrita, o caminho
é uma pasta. Todos são `OSError`, e todos viram `OutputError`:

| `OUTPUT_FILE` | Mensagem |
|---|---|
| `nao_existe/maze.txt` | `cannot write output file 'nao_existe/maze.txt': No such file or directory` |
| `trancado/maze.txt` | `cannot write output file 'trancado/maze.txt': Permission denied` |
| `pasta` | `cannot write output file 'pasta': Is a directory` |

O mesmo padrão do repositório de config (parte 11): a única camada que abre arquivos converte o
erro do sistema num erro da aplicação, com `strerror` e `from None`, para o `main` imprimir uma
linha limpa.

O programa **não cria pastas**. Se `nao_existe/` não existe, é mais provável que o caminho
esteja errado do que o usuário queira uma pasta nova; criar em silêncio esconderia o erro de
digitação.

O caminho vai entre aspas simples na mensagem: um `OUTPUT_FILE` com espaços no nome fica legível.

## Experimente

```bash
mkdir -p pasta
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.errors import OutputError
from amazeing.repositories.maze_repository import FileMazeRepository

maze = GeneratedMaze(((9, 1, 3), (12, 4, 6)), (0, 0), (2, 1), "EES",
                     frozenset())
for path in ["small.txt", "nao_existe/maze.txt", "pasta"]:
    try:
        FileMazeRepository().save(path, maze)
        print("ok:", path)
    except OutputError as error:
        print(error)
'
cat small.txt
```

```text
ok: small.txt
cannot write output file 'nao_existe/maze.txt': No such file or directory
cannot write output file 'pasta': Is a directory
913
c46

0,0
2,1
EES
```

## O arquivo completo

```python title="amazeing/repositories/maze_repository.py"
"""Writing of the output file."""

from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.errors import OutputError


class FileMazeRepository:
    """Store a maze in the hexadecimal format of the subject."""

    def save(self, path: str, maze: GeneratedMaze) -> None:
        """Write the maze, replacing the whole file.

        Args:
            path: OUTPUT_FILE of the configuration.
            maze: Maze to write.

        Raises:
            OutputError: The file cannot be written.
        """
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as file:
                file.write(self.to_text(maze))
        except OSError as error:
            raise OutputError(f"cannot write output file '{path}': "
                              f"{error.strerror}") from None

    @staticmethod
    def to_text(maze: GeneratedMaze) -> str:
        """Build the content of the output file.

        Args:
            maze: Maze to serialise.

        Returns:
            One hexadecimal digit per cell, a blank line, the entry, the
            exit and the shortest path, every line ending in a newline.
        """
        ex, ey = maze.entry
        sx, sy = maze.exit
        lines = ["".join(format(cell, "x") for cell in row)
                 for row in maze.grid]
        lines += ["", f"{ex},{ey}", f"{sx},{sy}", maze.solution]
        return "\n".join(lines) + "\n"
```

A classe não herda de `MazeRepository` nem importa `ports.py`: tem o `save` com a assinatura
certa, e isso basta.
