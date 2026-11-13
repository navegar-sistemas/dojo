---
sidebar_position: 6
title: Gravando o arquivo de saída
---

# Gravando o arquivo de saída

Com o texto montado ([página anterior](./04-o-texto-do-arquivo.md)), falta escrevê-lo no
arquivo indicado pela opção `OUTPUT_FILE` da configuração. Escrever pode falhar: a pasta pode
não existir, ou o usuário pode não ter permissão para gravar ali. Esta página grava o arquivo e
transforma essas falhas numa mensagem clara.

## O método `save`

```python
def save(self, path: str, maze: GeneratedMaze) -> None:
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(self.to_text(maze))
    except OSError as error:
        raise OutputError(f"cannot write output file '{path}': "
                          f"{error.strerror}") from None
```

É este `save` que cumpre a porta `MazeRepository`
([página 3](./03-a-porta-maze-repository.md)): mesmo nome, mesmos parâmetros, mesmo retorno.
Por isso o `GenerateMaze` consegue usá-lo sem conhecer a classe.

`file.write(self.to_text(maze))` monta o texto e o escreve de uma vez. Os três argumentos do
`open` são explicados a seguir.

### `"w"`: substituir o arquivo inteiro

O modo `"w"` (*write*, escrever) cria o arquivo se ele não existe e **apaga** o conteúdo se ele
já existe. Cada geração substitui o arquivo inteiro: depois de três labirintos novos pedidos
pelo menu, o arquivo contém só o terceiro, o que está na tela.

### `encoding="utf-8"`

O texto só tem dígitos, vírgulas e as letras `NESW`, que têm os mesmos bytes em qualquer
codificação comum. Mesmo assim, o projeto sempre diz a codificação, para nunca depender da
configuração do computador ([parte 11](../11-configuracao/05-abrindo-o-arquivo.md)).

### `newline="\n"`: o mesmo fim de linha em qualquer sistema

Ao **gravar** em modo texto, o Python troca cada `\n` pelo fim de linha do sistema: no Linux e no
macOS, `\n` continua `\n`; no Windows, vira `\r\n`. O enunciado pede `\n` no fim de cada linha.

`newline="\n"` desliga essa troca: o que o `to_text` montou é exatamente o que vai para o disco.

| `newline` | Linux e macOS | Windows |
|---|---|---|
| omitido | `\n` | `\r\n` |
| `"\n"` | `\n` | `\n` |

## O erro de gravação

Toda falha do sistema ao abrir ou escrever um arquivo é um `OSError`, a exceção do Python para
erros do sistema operacional. O `save` captura e levanta no lugar um `OutputError`, a exceção da
aplicação para o arquivo de saída ([parte 10](../10-utilitarios/05-a-hierarquia-app-error.md)):

| `OUTPUT_FILE` | Situação | Mensagem |
|---|---|---|
| `nao_existe/maze.txt` | a pasta não existe | `cannot write output file 'nao_existe/maze.txt': No such file or directory` |
| `trancado/maze.txt` | a pasta não permite gravar | `cannot write output file 'trancado/maze.txt': Permission denied` |
| `pasta_saida` | o caminho é uma pasta | `cannot write output file 'pasta_saida': Is a directory` |

É o mesmo padrão da leitura da configuração
([parte 11, "As falhas da leitura"](../11-configuracao/10-as-falhas-da-leitura.md)):

- `error.strerror` é só a frase do sistema operacional, sem o número interno do erro;
- `from None` descarta a exceção original, que a nova mensagem já resume;
- o `main` imprime a mensagem depois de `Error: ` e termina com código 1.

O caminho vai entre aspas simples na mensagem, para um nome com espaços continuar legível.

O programa **não cria pastas**. Se `nao_existe/` não existe, o mais provável é que o caminho
esteja errado; criar a pasta em silêncio esconderia o erro de digitação. Essa é uma escolha do
projeto.

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

## Experimente

Os exemplos rodam na raiz do projeto, com o labirinto 3x2 da [página 2](./02-o-caminho-em-celulas.md)
escrito à mão. O primeiro mostra o texto que o `to_text` monta, sem gravar nada:

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

O `repr` mostra cada `\n` escrito por extenso: um depois de cada linha da grade, o par `\n\n` da
linha vazia, e o `\n` final depois do caminho.

O segundo cria uma pasta comum e uma sem permissão de gravar, grava o mesmo labirinto em quatro
caminhos, três deles impossíveis, e no fim apaga tudo o que criou:

```bash
mkdir pasta_saida trancado
chmod 555 trancado
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from amazeing.errors import OutputError
from amazeing.repositories.maze_repository import FileMazeRepository

maze = GeneratedMaze(((9, 1, 3), (12, 4, 6)), (0, 0), (2, 1), "EES",
                     frozenset())
for path in ["saida_3x2.txt", "nao_existe/maze.txt", "trancado/maze.txt",
             "pasta_saida"]:
    try:
        FileMazeRepository().save(path, maze)
        print("ok:", path)
    except OutputError as error:
        print(error)
'
cat saida_3x2.txt
chmod 755 trancado
rm -r saida_3x2.txt pasta_saida trancado
```

```text
ok: saida_3x2.txt
cannot write output file 'nao_existe/maze.txt': No such file or directory
cannot write output file 'trancado/maze.txt': Permission denied
cannot write output file 'pasta_saida': Is a directory
913
c46

0,0
2,1
EES
```

`chmod 555 trancado` tira a permissão de gravar na pasta (deixa só ler e entrar); o `cat` mostra
o arquivo gravado; `chmod 755 trancado` devolve a permissão, sem a qual o `rm -r` não apagaria a
pasta.
