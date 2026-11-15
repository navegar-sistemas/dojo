---
sidebar_position: 5
title: O composition root
---

# O composition root

O programa é feito de muitas classes, separadas em camadas, e cada uma recebe prontos, no
construtor, os objetos de que precisa: o `Menu` recebe o `GenerateMaze`, o `GenerateMaze` recebe
o `MazeGenerator` e o repositório que grava o arquivo, e assim por diante. Alguém precisa criar
todos esses objetos, na ordem certa, e ligá-los uns aos outros. Esse lugar se chama
***composition root*** ("raiz de composição"). Aqui, é a função `main` do `a_maze_ing.py`.

O `a_maze_ing.py` é o arquivo que o enunciado manda executar, com esse nome obrigatório:

```bash
python3 a_maze_ing.py config.txt
```

Ele não tem nenhuma regra do labirinto. Faz três coisas: **confere** os argumentos da linha de
comando (nesta página), **monta** as peças ([próxima página](./08-montar-as-pecas.md)) e
**trata** todo erro que chegar até ele ([página 7](./05-a-barreira-de-erros.md)).

## Por que só ele conhece todas as classes

O projeto segue uma **regra de dependência**: cada camada só importa as camadas mais internas
([parte 2](../02-arquitetura/03-regra-de-dependencia.md)). O `Menu`, por exemplo, não importa o
`FileMazeRepository`, a classe que grava o arquivo de saída: ele recebe pronto um `GenerateMaze`
que já sabe gravar.

Se cada classe criasse os próprios colaboradores, o `Menu` teria de importar o repositório, o
gerador e a leitura da configuração, e a interface passaria a depender de como os arquivos são
lidos e gravados. Com o *composition root*, as classes só declaram **do que** precisam, e um
único ponto, fora de todas as camadas, decide **quem** fornece. Trocar uma peça (um repositório
que grava em memória em vez de em disco, por exemplo) muda uma linha aqui e nenhuma em outro
lugar.

## Os imports

```python
import sys

from amazeing.domain.entities.view_state import ViewState
from amazeing.errors import AppError
from amazeing.repositories.config_repository import FileConfigRepository
from amazeing.repositories.maze_repository import FileMazeRepository
from amazeing.services.render_service import RenderService
from amazeing.ui.menu import Menu
from amazeing.use_cases.generate_maze import GenerateMaze
from mazegen import MazeError, MazeGenerator
```

O script importa de todas as camadas. Ele pode, porque é o anel mais externo do desenho de
camadas da [parte 2](../02-arquitetura/01-por-que-camadas.md): depende de tudo, e nada depende
dele.

| Nome | O que é | Explicado na |
|---|---|---|
| `ViewState` | o caminho visível ou não e a cor das paredes | [parte 13](../13-tela/01-o-estado-da-tela.md) |
| `AppError` | a base dos erros da aplicação (config ruim, saída que não grava) | [parte 10](../10-utilitarios/05-a-hierarquia-app-error.md) |
| `FileConfigRepository` | lê o arquivo de configuração e devolve um `MazeConfig` | [parte 11](../11-configuracao/05-abrindo-o-arquivo.md) |
| `FileMazeRepository` | grava o arquivo de saída | [parte 12](../12-geracao-e-saida/05-gravando-o-arquivo.md) |
| `RenderService` | transforma o labirinto em linhas coloridas | [parte 13](../13-tela/02-a-grade-de-caracteres.md) |
| `Menu` | o laço que desenha, pergunta e reage | [páginas 1 a 4](./01-o-laco-do-menu.md) |
| `GenerateMaze` | gera um labirinto, grava o arquivo e devolve o retrato | [parte 12](../12-geracao-e-saida/06-o-caso-de-uso-generate-maze.md) |
| `MazeGenerator` | o gerador do pacote reutilizável `mazegen` | [parte 9](../09-gerador/01-a-fachada.md) |
| `MazeError` | o erro do gerador, para parâmetros impossíveis | [parte 4](../04-value-objects/01-maze-error.md) |

Do `mazegen` vêm só os dois nomes que o pacote oferece ao mundo de fora, `MazeGenerator` e
`MazeError`.

## As constantes

```python
USAGE = "Usage: python3 a_maze_ing.py <config_file>"
EXIT_OK = 0
EXIT_ERROR = 1
```

`EXIT_OK` e `EXIT_ERROR` dão nome aos **códigos de saída** (o número que o programa entrega ao
sistema quando termina: 0 = "terminou bem", outro = "deu erro";
[página 2](./07-o-laco-do-run.md)). `return EXIT_ERROR` diz o que significa; `return 1`
obrigaria o leitor a conhecer a convenção.

## A linha de comando

```python
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
```

`argv` é a lista das palavras escritas depois do nome do script. Para
`python3 a_maze_ing.py config.txt`, ela é `["config.txt"]`.

O `main` **recebe** essa lista e **devolve** o código de saída, em vez de ler os argumentos e
encerrar o programa por conta própria. Assim, outro código Python pode chamá-lo com qualquer
lista e decidir o que fazer com o código devolvido.

O enunciado diz que o programa recebe um único argumento: o arquivo de configuração. Com zero
argumentos, ou com dois ou mais, o `main` imprime a linha de uso na saída de erros (*stderr*,
[página 4](./03-mostrar-o-labirinto.md)) e devolve 1, antes de tentar abrir qualquer arquivo. O
texto da mensagem é escolha do projeto: ele mostra o comando inteiro, pronto para copiar, e o
`<config_file>` entre sinais de menor e maior é a convenção para "ponha aqui o nome do arquivo".

A linha de uso é a única mensagem de falha que **não** começa com `Error:`. Os erros de
configuração e de execução começam todos com esse prefixo
([parte 10](../10-utilitarios/01-excecoes-da-aplicacao.md)); a linha de uso segue outro formato,
o tradicional dos programas de terminal para dizer "como usar": a palavra `Usage:` seguida do
comando. Quem a recebe não precisa saber o que deu errado, e sim como chamar o programa, e ela
diz isso. O código de saída continua 1, como em qualquer falha.

Com o programa pronto (os dois rodam na [página 10](./09-o-programa-rodando.md)), estes
dois comandos imprimem a mesma linha de uso e terminam com código 1:

```bash
.venv/bin/python a_maze_ing.py
.venv/bin/python a_maze_ing.py config.txt outro.txt
```

```text
Usage: python3 a_maze_ing.py <config_file>
Usage: python3 a_maze_ing.py <config_file>
```

A mensagem cita `python3`, o comando do enunciado; aqui o programa roda com o Python do ambiente
virtual, `.venv/bin/python`, que dá no mesmo.

Com os argumentos conferidos, o `main` monta as peças, na
[próxima página](./08-montar-as-pecas.md).
