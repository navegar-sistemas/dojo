---
sidebar_position: 4
title: Os papéis das classes
---

# Os papéis das classes

Cada classe do projeto tem um **papel**, e o papel decide a pasta onde ela mora e as regras que
segue.

## Value object

Um **valor**: imutável e comparado pelo conteúdo, como um número ou uma string. Duas células
`(3, 4)` são iguais mesmo sendo objetos diferentes.

- Feito com `@dataclass(frozen=True)`, ou `Enum` quando os valores são um conjunto fechado.
- Quando há regra para criar, usa um método de fábrica que valida (`create`, `for_size`).
- Exemplos: `Cell`, `Direction`, `Pattern42`, `MazeConfig`, `GeneratedMaze`.

## Entidade

Um objeto com **estado que muda**, e que protege as próprias regras.

- Os métodos nunca deixam o estado inválido.
- Exemplos: `Maze` (as paredes mudam enquanto o labirinto é cavado, mas a coerência nunca
  quebra) e `ViewState` (caminho visível ou não, cor atual).

## Service

Uma **operação** sem estado: recebe o que precisa por parâmetro, faz o trabalho e devolve.

- Exemplos: `Carver` (cava), `Braider` (trança), `Solver` (resolve), `RenderService` (desenha
  em texto).

## Use case

**Uma operação da aplicação**, num único método `execute`.

- Depende de portas, não de implementações concretas.
- Exemplo: `GenerateMaze` (gerar, montar o retrato, gravar).

## Port

Um contrato: a assinatura que o use case precisa, escrita como `typing.Protocol`.

- Exemplo: `MazeRepository`, com `save(path, maze)`.

## Repository

A **única** camada que abre arquivos. Converte erros do sistema operacional em erros da
aplicação, com mensagem clara.

- Exemplos: `FileConfigRepository` (lê o config), `FileMazeRepository` (grava a saída).

## UI

A única camada, junto com o `main`, que usa `print` e `input`.

- Exemplo: `Menu`.

## Utilitária

Funções puras agrupadas numa classe, só com `@staticmethod` e constantes.

- Exemplos: `ValueParser` (converte texto em número, booleano, coordenada) e `Ansi` (códigos de
  cor).

## Composition root

O lugar que cria as classes concretas e as liga: `a_maze_ing.py`.

## Resumo

| Papel | Pasta | Muda de estado? | Faz I/O? |
|---|---|---|---|
| Value object | `value_objects/` | não | não |
| Entidade | `entities/` | sim | não |
| Service | `services/` | não | não |
| Use case | `use_cases/` | não | só pelas portas |
| Repository | `repositories/` | não | **arquivos** |
| UI | `ui/` | não | **terminal** |
| Utilitária | `utils/` | não | não |
