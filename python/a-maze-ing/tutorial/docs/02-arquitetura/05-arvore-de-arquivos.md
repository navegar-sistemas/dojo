---
sidebar_position: 7
title: A árvore de arquivos
---

# A árvore de arquivos

Com as camadas e os papéis definidos, falta decidir onde cada classe mora no disco. Esta página
mostra a estrutura completa de pastas e arquivos que o tutorial constrói, e a ordem em que cada
peça é escrita.

## Uma classe por arquivo

Cada arquivo `.py` contém uma classe, e o nome do arquivo vem do nome da classe escrito em
**snake_case** (palavras em minúsculas separadas por `_`): `ViewState` fica em `view_state.py`,
`GenerateMaze` em `generate_maze.py`. Quando a pasta já diz o contexto, o nome encurta:
`MazeGenerator` fica em `mazegen/generator.py`, e `FileConfigRepository` em
`repositories/config_repository.py`.

A pasta de cada arquivo é a do seu papel: as entidades em `entities/`, os value objects em
`value_objects/`, e assim por diante. Os dois pacotes repetem alguns desses nomes: há uma pasta
`services/` dentro de `mazegen/` (com `Carver`, `Braider` e `Solver`, parte do gerador, no anel
central das camadas) e outra dentro de `amazeing/` (com `RenderService`, a camada `services` do
anel de fora).

```text
a_maze_ing.py                              ponto de entrada e barreira de erros
mazegen/                                   o gerador (vai para o pacote)
    __init__.py                            documentação; exporta MazeGenerator e MazeError
    py.typed                               marca o pacote como tipado
    errors.py                              MazeError
    generator.py                           MazeGenerator
    entities/
        maze.py                            Maze
    value_objects/
        cell.py                            Cell
        direction.py                       Direction
        pattern42.py                       Pattern42
    services/
        carver.py                          Carver
        braider.py                         Braider
        solver.py                          Solver
amazeing/                                  a aplicação
    errors.py                              AppError, ConfigError, OutputError
    domain/
        entities/
            view_state.py                  ViewState
        value_objects/
            maze_config.py                 MazeConfig
            generated_maze.py              GeneratedMaze
    use_cases/
        ports.py                           MazeRepository
        generate_maze.py                   GenerateMaze
    repositories/
        config_repository.py               FileConfigRepository
        maze_repository.py                 FileMazeRepository
    services/
        render_service.py                  RenderService
    ui/
        menu.py                            Menu
    utils/
        value_parser.py                    ValueParser
        ansi.py                            Ansi
```

Três tipos de arquivo fogem da regra "uma classe por arquivo". Os dois primeiros são explicados
na [parte 3](../03-ambiente/07-pacotes-do-mazegen.md):

- **`__init__.py`**: o arquivo que transforma uma pasta em pacote Python. Toda pasta da árvore
  tem um, mesmo que não apareça acima. O de `mazegen/` também guarda a documentação de uso do
  gerador.
- **`py.typed`**: um arquivo vazio que avisa às ferramentas de verificação de tipos que o pacote
  `mazegen` tem anotações de tipo (o `-> int`, o `: str` das funções).

O terceiro são os `errors.py`, que guardam os tipos de erro de cada pacote: `MazeError` para o
gerador e, para a aplicação, `AppError` junto com as suas variações `ConfigError` e
`OutputError`, três classes pequenas no mesmo arquivo.

## A ordem de construção

O tutorial constrói primeiro o que não depende de nada e por último o que liga tudo. Assim,
toda peça nova só importa peças que já existem e já funcionam:

| Parte | Constrói |
|---|---|
| [3](../03-ambiente/01-o-ambiente-virtual.md) | o ambiente: `Makefile`, `pyproject.toml`, configuração do lint, pastas vazias |
| [4](../04-value-objects/01-maze-error.md) | os value objects `Direction`, `Cell` e `Pattern42`, e antes deles o `MazeError` (uma exceção, não um value object: vem primeiro porque não depende de nada e todas as outras peças podem levantá-lo) |
| [5](../05-maze/01-a-grade-de-paredes.md) | `Maze` |
| [6](../06-carver/01-labirinto-perfeito.md) | `Carver` |
| [7](../07-solver/01-busca-em-largura.md) | `Solver` |
| [8](../08-braider/01-becos-sem-saida.md) | `Braider` |
| [9](../09-gerador/01-a-fachada.md) | `MazeGenerator`, a documentação e o pacote |
| [10](../10-utilitarios/01-excecoes-da-aplicacao.md) | `AppError`, `ValueParser`, `Ansi` |
| [11](../11-configuracao/01-o-value-object-maze-config.md) | `MazeConfig`, `FileConfigRepository` |
| [12](../12-geracao-e-saida/01-o-retrato-generated-maze.md) | `GeneratedMaze`, `MazeRepository`, `FileMazeRepository`, `GenerateMaze` |
| [13](../13-tela/01-o-estado-da-tela.md) | `ViewState`, `RenderService` |
| [14](../14-menu-e-main/01-o-laco-do-menu.md) | `Menu`, `a_maze_ing.py` |
| [15](../15-fechamento/01-o-que-o-readme-precisa-ter.md) | o `README.md` e o pacote final |
| [16](../16-bonus/01-o-tabuleiro-sem-becos.md) | o bônus |

Os dois pacotes são construídos em sequência: as partes 4 a 9 fazem o `mazegen` inteiro, e só
depois as partes 10 a 14 fazem a aplicação que o usa.
