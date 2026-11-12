---
sidebar_position: 5
title: A árvore de arquivos
---

# A árvore de arquivos

Esta é a estrutura completa que o tutorial constrói. Cada arquivo `.py` contém uma classe, e o
nome do arquivo é o nome da classe em `snake_case` (`FileConfigRepository` →
`config_repository.py`).

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

Toda pasta também tem um `__init__.py`, que a transforma em pacote Python.

## A ordem de construção

O tutorial segue a regra de dependência: primeiro o que não depende de nada, por último o que
liga tudo.

| Parte | Constrói |
|---|---|
| 3 | ambiente: `Makefile`, `pyproject.toml`, lint, pastas vazias |
| 4 | `MazeError`, `Direction`, `Cell`, `Pattern42` |
| 5 | `Maze` |
| 6 | `Carver` |
| 7 | `Solver` |
| 8 | `Braider` |
| 9 | `MazeGenerator`, documentação e pacote |
| 10 | `AppError`, `ValueParser`, `Ansi` |
| 11 | `MazeConfig`, `FileConfigRepository` |
| 12 | `GeneratedMaze`, `MazeRepository`, `FileMazeRepository`, `GenerateMaze` |
| 13 | `ViewState`, `RenderService` |
| 14 | `Menu`, `a_maze_ing.py` |
| 15 | `README.md` e pacote final |
| 16 | bônus |

Cada peça só usa as que vieram antes dela.
