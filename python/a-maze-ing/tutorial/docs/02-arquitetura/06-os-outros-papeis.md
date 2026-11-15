---
sidebar_position: 6
title: Os outros papéis
---

# Os outros papéis

A [página anterior](./04-papeis-das-classes.md) apresentou os papéis do miolo do programa: value
object (um valor que não muda), entidade (um objeto que muda, mas protege as próprias regras),
service (uma operação sem estado), use case (uma operação completa da aplicação) e port (a
descrição do que um use case precisa). Faltam os papéis das pontas: a classe que quem reutiliza
o gerador enxerga, os tipos de erro, quem abre arquivos, quem fala com o usuário e quem liga
tudo. Esta página apresenta cada um, com um exemplo do projeto.

Relembrando duas palavras da página anterior: **estado** são os dados que um objeto guarda e que
podem mudar; **I/O** (entrada e saída) é tudo o que fala com fora do programa, como abrir um
arquivo ou imprimir na tela.

## Fachada

Uma classe que esconde várias outras atrás de uma porta de entrada simples. Quem a usa não
precisa saber quais peças trabalham por trás.

- Exemplo: `MazeGenerator`. Quem reutiliza o gerador cria um `MazeGenerator` com o tamanho e as
  opções, chama `generate()` e lê o resultado. Não precisa conhecer `Maze`, `Carver`, `Braider`
  nem `Solver`, que o `MazeGenerator` usa por dentro
  ([parte 9](../09-gerador/01-a-fachada.md)).

## Exceção

Um tipo de erro. **Levantar (lançar) uma exceção** (em inglês, *raise*) é interromper o código
com um objeto de erro; quem chamou pode capturá-lo com `try`/`except` e decidir o que fazer.
Cada pacote tem os seus tipos de erro, num arquivo `errors.py`, e não guarda estado nenhum além
da mensagem.

- Exemplos: `MazeError`, o único erro que o gerador levanta
  ([parte 4](../04-value-objects/01-maze-error.md)), e `AppError`, com as variações
  `ConfigError` (problema no arquivo de opções) e `OutputError` (problema ao gravar a saída)
  ([parte 10](../10-utilitarios/05-a-hierarquia-app-error.md)).

## Repository

A **única** camada que abre arquivos. Quando o sistema operacional reclama (arquivo que não
existe, pasta sem permissão), o repository transforma esse erro numa mensagem clara do programa.

- Exemplos: `FileConfigRepository` (lê o config) e `FileMazeRepository` (grava a saída).

## UI

A camada de interface com o usuário (*user interface*): a única que usa `input` (lê o teclado).
Ela também usa `print` para mostrar o labirinto e o menu; fora dela, só o `a_maze_ing.py` usa
`print`, para mostrar a mensagem de erro final.

- Exemplo: `Menu`.

## Utilitária

Funções pequenas e independentes, agrupadas numa classe só para ficarem juntas. Cada uma é um
`@staticmethod`: um método que não usa o objeto nem a classe, e por isso é chamado direto pelo
nome da classe.

```python
ValueParser.to_coordinate("19,14")   # (19, 14)
```

- Exemplos: `ValueParser` (converte texto em número, booleano ou coordenada), `Ansi` (as cores
  do terminal) e `Box` (os caracteres de caixa que desenham as paredes).

## Composition root

O lugar que cria as classes concretas e as liga umas às outras. No projeto é a função `main` do
`a_maze_ing.py`, construída na [parte 14](../14-menu-e-main/04-o-composition-root.md). Estas
quatro linhas dela são o coração da ligação:

```python
        config = FileConfigRepository().load(argv[0])
        generator = MazeGenerator(config.width, config.height, config.entry,
                                  config.exit, config.perfect, config.seed)
        generate = GenerateMaze(generator, FileMazeRepository(), config)
        return Menu(generate, RenderService(), ViewState()).run()
```

1. Lê o config. `argv` é a lista de argumentos da linha de comando **sem** o nome do programa
   (o `main` recebe `sys.argv[1:]`). Em `python3 a_maze_ing.py config.txt`, `argv` é
   `["config.txt"]`, e `argv[0]` é o nome do arquivo de opções.
2. Cria o gerador com as opções lidas.
3. Cria o use case, entregando o repository que grava o arquivo.
4. Entrega tudo ao menu e roda o menu. O `run()` só termina quando o usuário sai, e devolve o
   **código de saída** do programa: o número que ele entrega ao terminal ao terminar, 0 para
   sucesso. O `return` repassa esse número para quem chamou o `main`.

## Resumo

Alguns papéis aparecem nos dois pacotes, cada um na sua pasta: o `mazegen` tem as suas
subpastas (no anel central das camadas) e o `amazeing` tem as dele. A coluna "Pasta" traz o
caminho completo.

| Papel | Pasta | Exemplo | Estado muda? | Faz I/O? |
|---|---|---|---|---|
| Value object | `mazegen/value_objects/` e `amazeing/domain/value_objects/` | `Cell` (em `mazegen/value_objects/`) | não | não |
| Entidade | `mazegen/entities/` e `amazeing/domain/entities/` | `Maze` (em `mazegen/entities/`) | sim | não |
| Service | `mazegen/services/` e `amazeing/services/` | `Carver` (em `mazegen/services/`) e `RenderService` (em `amazeing/services/`) | não | não |
| Use case | `amazeing/use_cases/` | `GenerateMaze` | não | só pela porta |
| Port | `amazeing/use_cases/ports.py` | `MazeRepository` | não | não |
| Fachada | `mazegen/generator.py` | `MazeGenerator` | sim: guarda o último labirinto gerado | não |
| Exceção | `mazegen/errors.py` e `amazeing/errors.py` | `MazeError` (em `mazegen/errors.py`) | não | não |
| Repository | `amazeing/repositories/` | `FileMazeRepository` | não | **arquivos** |
| UI | `amazeing/ui/` | `Menu` | não | **terminal** |
| Utilitária | `amazeing/utils/` | `ValueParser` | não | não |
| Composition root | `a_maze_ing.py` | a função `main` | não | **terminal**: imprime a mensagem de erro final |
