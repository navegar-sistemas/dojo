---
sidebar_position: 1
title: O formato dos erros
---

# O formato dos erros

Muita coisa pode dar errado por causa do que o usuário escreveu: o arquivo de configuração não
existe, a largura é `abc`, o arquivo de saída aponta para uma pasta que não existe. O enunciado
do projeto exige que, nesses casos, o programa **nunca quebre**: ele precisa terminar com uma
mensagem de erro clara. Esta página define como o programa mostra todo erro e por que ele precisa
de exceções próprias; a [próxima](./05-a-hierarquia-app-error.md) cria essas exceções.

## Onde esta parte se encaixa

O projeto tem dois pacotes Python ([parte 2](../02-arquitetura/02-dois-pacotes.md)):

- `mazegen`, o gerador de labirintos reutilizável, construído nas partes 4 a 9;
- `amazeing`, a aplicação em volta dele: lê o arquivo de configuração, grava o arquivo de saída,
  desenha no terminal e mostra o menu.

As partes 10 a 14 constroem o `amazeing`. Esta parte começa pelas peças pequenas que todas as
outras usam: as exceções, os conversores de texto e as cores do terminal.

## Exceção em poucas palavras

Quando o Python encontra um problema que não sabe resolver, ele **levanta** (lança) uma exceção
(em inglês, *raise*): um objeto que interrompe a função atual e sobe pelas funções que a chamaram.
Se nenhuma delas a **captura** com `try`/`except`, o programa para e imprime um **traceback**, a
listagem de linhas de código que levou ao erro:

```bash
.venv/bin/python -c 'int("abc")'
```

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    int("abc")
    ~~~^^^^^^^
ValueError: invalid literal for int() with base 10: 'abc'
```

As duas linhas do meio (o código e os sinais `~~~^^^^^^^` que apontam o trecho do erro) só
aparecem a partir do Python 3.13; no 3.10 ao 3.12, a listagem vai direto do `File ...` para o
`ValueError`. Nos dois casos, é exatamente o que o enunciado proíbe: quem usa o programa não deve ver isso.

## O plano: um único lugar imprime os erros

Este projeto escolheu um formato para todo erro de configuração ou de execução: **uma** linha
começando com `Error: `, impressa em **stderr**, e o programa termina com **código de saída 1**.
(A linha de uso, impressa quando o programa recebe zero ou mais de um argumento, é a exceção:
começa com `Usage:`; a [parte 14](../14-menu-e-main/04-o-composition-root.md) explica por quê.)

- **stderr** é a saída de erros do programa, separada da saída normal (stdout). No terminal as
  duas aparecem juntas, mas um script consegue separá-las.
- O **código de saída** é o número que o programa devolve ao terminar: 0 quer dizer sucesso e
  qualquer outro valor quer dizer erro. O terminal mostra o último com `echo $?`.

O enunciado só exige uma mensagem clara; o formato é escolha do projeto. Uma linha com prefixo
fixo é fácil de reconhecer, e stderr com código 1 deixa um script perceber que houve erro.

Quem imprime é a função `main` do `a_maze_ing.py`, o arquivo principal
([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)), num único `except`:

```python
except (AppError, MazeError) as error:
    print(f"Error: {error}", file=sys.stderr)
    return EXIT_ERROR
```

- `except (AppError, MazeError) as error:` captura uma exceção de qualquer uma das classes entre
  parênteses. Os parênteses formam uma **tupla** de classes, e o `except` aceita a exceção se ela
  for de qualquer uma delas. `AppError` é a exceção da aplicação, criada na
  [próxima página](./05-a-hierarquia-app-error.md); `MazeError` é a do gerador
  ([parte 4](../04-value-objects/01-maze-error.md)). O `as error` dá o nome `error` à exceção
  capturada.
- `print(..., file=sys.stderr)` escreve em stderr em vez de stdout.
- `f"Error: {error}"` é uma *f-string*: o `{error}` é trocado pelo texto da exceção.
- `return EXIT_ERROR` faz o `main` devolver 1 (o valor da constante `EXIT_ERROR`). A última linha
  do `a_maze_ing.py`, `sys.exit(main(sys.argv[1:]))`, entrega o número que o `main` devolveu ao
  sistema operacional: é ele que vira o código de saída do programa
  ([parte 14](../14-menu-e-main/05-a-barreira-de-erros.md)).

Há uma única linha `Error: ` que não passa por esse `except`: o aviso
`Error: maze too small for the "42" pattern`, que o menu imprime quando o "42" não cabe na grade
([O padrão "42"](../01-o-problema/06-o-padrao-42.md)). Ele não encerra o programa, porque o
labirinto foi gerado e funciona; por isso não é uma exceção, e sim um aviso que o próprio menu
escreve antes de cada desenho ([parte 14](../14-menu-e-main/03-mostrar-o-labirinto.md)).

Para isso funcionar, a **mensagem** da exceção já precisa ser a frase final, pronta para vir
depois de `Error: `. Quem levanta o erro é quem sabe o que deu errado, então é ele quem monta a
frase:

```text
Error: config.txt: WIDTH must be an integer, got 'abc'
Error: cannot write output file 'nao_existe/maze.txt': No such file or directory
```

As mensagens estão em inglês porque todos os textos do projeto estão.

## Por que exceções próprias

O `main` poderia capturar as exceções do próprio Python, como `ValueError` ou `OSError`. O
problema: elas também aparecem quando o **código** tem um bug. Um `except ValueError` no `main`
mostraria um bug como se fosse culpa do arquivo do usuário, com uma mensagem sem sentido.

Uma classe própria resolve: ela só é levantada de propósito, por quem detectou um erro do
usuário e já escreveu a mensagem. Capturar essa classe quer dizer "erro esperado, mensagem
pronta". A [próxima página](./05-a-hierarquia-app-error.md) cria essa classe e as suas filhas.
