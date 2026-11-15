---
sidebar_position: 1
title: O menu e os seus textos
---

# O menu e os seus textos

Depois de desenhar o labirinto, o programa não pode simplesmente terminar. O enunciado exige que,
**com o programa rodando**, o usuário consiga gerar outro labirinto, mostrar ou esconder o
caminho mais curto e trocar a cor das paredes. O programa precisa repetir sempre o mesmo ciclo:
desenhar, perguntar o que o usuário quer, reagir, e voltar a desenhar, até o usuário pedir para
sair. A classe `Menu` (`amazeing/ui/menu.py`) faz esse ciclo. Esta página mostra os textos que
ela imprime, por que ela lê o teclado com `input()` e as peças que ela recebe; o laço em si está
na [próxima página](./07-o-laco-do-run.md).

Na tela, depois de cada desenho, aparece isto ([parte 1](../01-o-problema/07-o-desenho-e-o-menu.md)):

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

O `Menu` é a camada de **interface**: junto com o `main` do `a_maze_ing.py`, é o único lugar do
projeto que usa `print` e `input`, isto é, que conversa com o usuário.

## Os textos do menu

```python
MENU = ("=== A-Maze-ing ===", "1. Re-generate a new maze",
        "2. Show / Hide the shortest path", "3. Rotate the wall colours",
        "4. Quit")
PROMPT = "Choice? (1-4): "
PATTERN_MISSING = 'Error: maze too small for the "42" pattern'
CHOICES = ("1", "2", "3", "4")
```

- `MENU`: as cinco linhas do menu, uma por item da tupla.
- `PROMPT`: a pergunta que fica esperando a resposta. Termina com um espaço e sem quebra de
  linha, então o cursor fica na mesma linha, logo depois dos dois-pontos.
- `PATTERN_MISSING`: o aviso para quando o "42" não coube no labirinto
  ([página 4](./03-mostrar-o-labirinto.md)). Ele começa com `Error:` como os erros do programa,
  mas é o único que não encerra a execução: o labirinto sem o "42" continua válido, e o menu
  segue. Por isso o próprio `Menu` o imprime, em vez de deixá-lo subir até o `main` do
  `a_maze_ing.py`, que só imprime os erros que terminam o programa
  ([página 7](./05-a-barreira-de-erros.md)).
- `CHOICES`: as quatro respostas válidas, como texto.

Os textos ficam em constantes no topo do arquivo, e não espalhados pelos métodos: são o que o
usuário vê do programa, e mudar um deles é mudar uma linha só. Os textos em inglês e as quatro
opções são escolha do projeto; o enunciado pede no mínimo as três interações (gerar de novo,
mostrar ou esconder o caminho, trocar a cor das paredes), e a opção `4` é a saída.

## Por que `input()`

`input(texto)` mostra o texto, espera o usuário digitar uma linha e apertar Enter, e devolve o
que foi digitado, sem o Enter. O menu lê a escolha assim: o usuário digita `2` e confirma com
Enter.

A alternativa seria reagir a cada tecla, sem Enter, pondo o terminal num modo especial (o modo
*raw*, "cru"). O projeto escolheu `input()` porque o modo raw:

- depende do sistema: no Linux e no macOS é um módulo do Python (`termios`), no Windows é outro;
- não funciona quando a entrada vem de um **pipe** (abaixo);
- deixa o terminal desconfigurado, sem mostrar o que se digita, se o programa morrer antes de
  restaurá-lo.

Um **pipe** é o `|` do terminal: ele entrega a saída de um comando como entrada de outro, como se
alguém digitasse. Neste comando, o `printf` escreve `2`, Enter, `4`, Enter, e o programa lê essas
duas respostas como se o usuário as tivesse digitado: mostra o caminho e sai.

```bash
printf '2\n4\n' | .venv/bin/python a_maze_ing.py config.txt
```

O comando roda o programa com o Python do ambiente virtual (`.venv/bin/python`); é o mesmo que o
`python3 a_maze_ing.py config.txt` do enunciado. Ele só funciona no fim desta parte, quando o
`a_maze_ing.py` estiver completo; a [página 10](./09-o-programa-rodando.md) o roda de verdade.

Com `input()`, o menu funciona igual num terminal e num pipe, e é assim que se pode rodar o
programa sem ninguém no teclado.

## Os colaboradores

```python
    def __init__(self, generate: GenerateMaze, renderer: RenderService,
                 state: ViewState) -> None:
        """Keep the collaborators of the menu.

        Args:
            generate: Use case that builds and stores a maze.
            renderer: Service that draws a maze.
            state: Path visibility and wall colour of the session.
        """
        self._generate = generate
        self._renderer = renderer
        self._state = state
```

O `Menu` recebe três objetos prontos, e só os guarda:

| Parâmetro | O que é |
|---|---|
| `generate` | o `GenerateMaze`, a operação que gera um labirinto, grava o arquivo de saída e devolve o retrato `GeneratedMaze` ([parte 12](../12-geracao-e-saida/06-o-caso-de-uso-generate-maze.md)) |
| `renderer` | o `RenderService`, que transforma o labirinto em linhas coloridas ([parte 13](../13-tela/02-a-grade-de-caracteres.md)) |
| `state` | o `ViewState`, com o caminho visível ou não e a cor das paredes ([parte 13](../13-tela/01-o-estado-da-tela.md)) |

O `_` no começo de `self._generate` é uma convenção do Python: avisa que o atributo é de uso
interno da classe.

O `Menu` não cria nada disso. Quem cria e liga as peças é o `main`
([página 6](./08-montar-as-pecas.md)). Por isso o menu não sabe que existe um arquivo de
configuração, nem qual arquivo de saída é gravado: ele só pede "gere outro" ao `GenerateMaze`.
