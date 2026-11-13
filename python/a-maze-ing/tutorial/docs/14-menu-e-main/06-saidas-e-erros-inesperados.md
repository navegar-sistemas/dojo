---
sidebar_position: 9
title: Saídas do usuário e erros inesperados
---

# Saídas do usuário e erros inesperados

A barreira de erros do `main` ([página 7](./05-a-barreira-de-erros.md)) transforma os
erros conhecidos, de configuração, de gravação e do gerador, em uma linha `Error: ...` e
código 1. Sobram dois casos: o usuário que quer sair no meio (Ctrl+C, Ctrl+D) e o erro que
ninguém previu, um defeito do código. Os dois também não podem terminar num traceback.
Esta página mostra os dois `except` que cuidam deles e por que a ordem dos `except` importa.

```python
    except (KeyboardInterrupt, EOFError):
        # Keeps the shell prompt off the "Choice? (1-4): " line.
        print()
        return EXIT_OK
    except Exception as error:
        print(f"Error: unexpected: {type(error).__name__}: {error}",
              file=sys.stderr)
        return EXIT_ERROR
```

## Saída do usuário: Ctrl+C e Ctrl+D

Apertar **Ctrl+C** no terminal pede ao sistema que interrompa o programa. O Python transforma
esse pedido na exceção `KeyboardInterrupt`, levantada no ponto onde o programa estiver (quase
sempre parado no `input` do menu). **Ctrl+D**, num terminal de Linux ou macOS, avisa que a
entrada acabou; o `input` levanta `EOFError`. O mesmo acontece quando o texto de um pipe acaba.

Nenhum dos dois é erro: o usuário quis sair. O projeto escolheu terminar com código 0, sem nada
na stderr, como na opção `4`. Muitos programas terminam com o código 130 no Ctrl+C: é a
convenção dos terminais do Linux e do macOS para "interrompido", 128 mais o número do sinal que
o Ctrl+C envia ao programa (um **sinal** é um aviso que o sistema manda a um programa em
execução, identificado por um número; o do Ctrl+C é o `SIGINT`, sinal 2). Aqui, sair pelo Ctrl+C
é tratado como sair
pela opção `4`.

O `print()` imprime só uma quebra de linha. O usuário estava parado em `Choice? (1-4): `, sem
quebra no fim; sem o `print()`, o prompt do terminal apareceria colado na pergunta do menu. É o
que diz o comentário em inglês acima dele: "mantém o prompt do shell fora da linha
`Choice? (1-4): `".

O Experimente no fim da página mostra isso com `< /dev/null`, que liga a entrada do programa a
um arquivo vazio: o primeiro `input` já encontra o fim da entrada.

## A rede de segurança: `Exception`

Qualquer outra exceção é um defeito: algo que nenhuma camada previu. Ela também vira uma linha
só, com o tipo e a mensagem, e código 1. Um `KeyError` com a mensagem `'x'` (simulado no
"Experimente" abaixo) sai assim:

```text
Error: unexpected: KeyError: 'x'
```

`type(error).__name__` é o nome da classe da exceção (`KeyError`), a pista mais útil para quem
vai consertar. O `unexpected:` ("inesperado") avisa que não é um erro de uso: o arquivo de
configuração não tem culpa.

## A ordem dos `except` importa

O Python testa os `except` de cima para baixo e usa o **primeiro** que combina. Um `except` de
uma classe também pega as subclasses dela. As exceções do Python formam uma árvore: no topo está
`BaseException`; abaixo dela, `Exception`, a base dos erros comuns; e, ao lado de `Exception`,
direto sob `BaseException`, algumas exceções que não são erros, como `KeyboardInterrupt`.

- `EOFError` é subclasse de `Exception`. Se o `except Exception` viesse antes, o Ctrl+D virava
  `Error: unexpected: EOFError` com código 1.
- `AppError` e `MazeError` também são subclasses de `Exception`. Pelo mesmo motivo, ficam acima
  dele, ou todo erro de configuração sairia como `unexpected`.
- `KeyboardInterrupt` **não** é subclasse de `Exception`: herda direto de `BaseException`, de
  propósito, para que um `except Exception` qualquer não engula um Ctrl+C. Por isso ele precisa
  estar listado pelo nome.

A ordem fica: erros conhecidos, saídas do usuário e, por último, o genérico.

## O que fica fora do `try`

A conferência dos argumentos fica antes do `try` porque não levanta nada: é um `if` que imprime a
linha de uso e devolve 1.

Os `import` do topo também ficam fora. Se a pasta `amazeing/` não estiver ao lado do script, o
Python falha com `ModuleNotFoundError` antes de o `main` existir. Isso só acontece com uma
instalação incompleta, e a [parte 15](../15-fechamento/08-o-roteiro-da-avaliacao.md) mostra por
que a pasta `amazeing/` precisa ir junto com o script.

## O arquivo completo

```python title="a_maze_ing.py"
"""Entry point of A-Maze-ing: wire the layers and report every error."""

import sys

from amazeing.domain.entities.view_state import ViewState
from amazeing.errors import AppError
from amazeing.repositories.config_repository import FileConfigRepository
from amazeing.repositories.maze_repository import FileMazeRepository
from amazeing.services.render_service import RenderService
from amazeing.ui.menu import Menu
from amazeing.use_cases.generate_maze import GenerateMaze
from mazegen import MazeError, MazeGenerator

USAGE = "Usage: python3 a_maze_ing.py <config_file>"
EXIT_OK = 0
EXIT_ERROR = 1


def main(argv: list[str]) -> int:
    """Read the configuration, generate the maze and run the menu.

    Args:
        argv: Command-line arguments without the script name.

    Returns:
        0 on Quit, end of input or Ctrl+C; 1 on any error.
    """
    if len(argv) != 1:
        print(USAGE, file=sys.stderr)
        return EXIT_ERROR
    try:
        config = FileConfigRepository().load(argv[0])
        generator = MazeGenerator(config.width, config.height, config.entry,
                                  config.exit, config.perfect, config.seed)
        generate = GenerateMaze(generator, FileMazeRepository(), config)
        return Menu(generate, RenderService(), ViewState()).run()
    except (AppError, MazeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_ERROR
    except (KeyboardInterrupt, EOFError):
        # Keeps the shell prompt off the "Choice? (1-4): " line.
        print()
        return EXIT_OK
    except Exception as error:
        print(f"Error: unexpected: {type(error).__name__}: {error}",
              file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Experimente

Com o `a_maze_ing.py` completo, os exemplos rodam na raiz do projeto. Cada um grava o
`maze.txt`, o arquivo de saída do `config.txt`, que o `.gitignore` deixa fora do repositório.

Fim da entrada logo no primeiro `input`: o `< /dev/null` liga a entrada do programa a um arquivo
vazio. O primeiro comando mostra a última linha da saída com `cat -e`, que marca com `$` o fim
de cada linha; o segundo descarta a saída e mostra o código de saída:

```bash
.venv/bin/python a_maze_ing.py config.txt < /dev/null | tail -n 1 | cat -e
.venv/bin/python a_maze_ing.py config.txt < /dev/null > /dev/null; echo "exit=$?"
```

```text
Choice? (1-4): $
exit=0
```

A pergunta do menu termina com a quebra de linha do `print()` (o `$`), e o código é 0.

Um erro inesperado, simulado: o trecho troca o método `load` do `FileConfigRepository` por uma
função que levanta `KeyError`, como se o código tivesse um defeito, e chama o `main`. O
`echo "exit=$?"` mostra o código de saída.

```bash
.venv/bin/python -c 'import sys, a_maze_ing
from amazeing.repositories.config_repository import FileConfigRepository
def boom(self, path): raise KeyError("x")
FileConfigRepository.load = boom
sys.exit(a_maze_ing.main(["config.txt"]))'; echo "exit=$?"
```

```text
Error: unexpected: KeyError: 'x'
exit=1
```

Linha a linha:

- `import sys, a_maze_ing` importa o programa como um módulo. Importar não roda o `main`: o
  `if __name__ == "__main__":` do fim do arquivo só é verdadeiro quando o arquivo é executado
  diretamente ([página 6](./08-montar-as-pecas.md)).
- `def boom(self, path): raise KeyError("x")` cria uma função com os mesmos parâmetros do
  `load` que só levanta o erro.
- `FileConfigRepository.load = boom` troca o método **na classe**. Todo objeto
  `FileConfigRepository`, inclusive o que o `main` cria lá dentro, passa a usar o `boom` no
  lugar do `load` verdadeiro. A troca só vale enquanto esse comando roda; o arquivo
  `config_repository.py` não muda.
- `sys.exit(a_maze_ing.main(["config.txt"]))` chama o `main` como se a linha de comando fosse
  `config.txt` e encerra com o código que ele devolve.

O `import a_maze_ing` deixa na raiz uma pasta `__pycache__/`, com a versão já traduzida do
arquivo que o Python guarda para ir mais rápido; o `.gitignore` também a deixa de fora.
