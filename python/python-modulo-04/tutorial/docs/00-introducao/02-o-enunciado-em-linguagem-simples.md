---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([Ambiente](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que foge
  do estilo padrão do Python: linha com mais de 79 caracteres, falta de linha em branco entre
  funções, variável criada e nunca usada. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todas as funções e métodos, conferidos pelo mypy.** Um *type hint* é a anotação do
  tipo de cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o programa que
  confere se esses tipos batem com o uso ([Type hints, flake8 e
  mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **O programa nunca pode travar.** "Travar" (*crash*) aqui quer dizer parar no meio com a mensagem
  de erro do próprio Python. Toda falha previsível (arquivo inexistente, sem permissão, conteúdo que
  não é texto) precisa ser tratada com `try` e `except`.
- **A instrução `with` só pode aparecer no exercício 3.** Os exercícios 0, 1 e 2 fecham os arquivos
  à mão ([O with](../06-ex3/02-o-with.md)).
- **Tipos permitidos:** `str`, `int`, `float`, `list`, `dict`, `set` e `tuple`, com todos os seus
  métodos e construtores. Um **método** é uma função que pertence a um valor e é chamada com ponto:
  `"abc".upper()` chama o método `upper` do texto `"abc"` e devolve `"ABC"`. Um **construtor** é o
  próprio tipo chamado como função para criar um valor dele: `str(25)` dá `"25"`, `int("25")` dá
  `25`.
- **As mensagens podem variar**, desde que a estrutura da saída e a informação essencial sejam as
  dos exemplos.

## Funções autorizadas

Cada exercício tem uma lista de **funções autorizadas**: as únicas funções prontas do Python que o
código pode chamar. Funções que você mesmo escreve no arquivo, os métodos e os construtores dos
tipos permitidos podem ser chamados sempre. `try`, `except`, `finally`, `if`, `for`, `return` e
`import` são palavras da linguagem, não funções.

| Exercício | Autorizado |
|---|---|
| 0 | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `read()`, `close()`, `print()` |
| 1 | o mesmo do exercício 0, mais `write()` e `input()` |
| 2 | o mesmo do exercício 1, **menos** `input()`, mais `sys.stdin`, `sys.stdout`, `sys.stderr`, `readline()` e `flush()` |
| 3 | `open()`, `read()`, `write()`, `print()` |

O enunciado escreve `io.read()`, `io.close()` e assim por diante: são os métodos do objeto que
`open()` devolve, explicados em [open e o objeto
arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md). `sys` e `typing` são **módulos**: arquivos
de código que vêm com o Python e entram no programa com `import` ([Os argumentos do
terminal](../02-arquivos/06-os-argumentos-do-terminal.md)).

## Os quatro exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | receber o nome de um arquivo no terminal, mostrar o conteúdo dele entre um cabeçalho e um rodapé, e tratar as falhas: arquivo inexistente, sem permissão e outras ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | partir do exercício 0, acrescentar um `#` no fim de cada linha, mostrar o texto novo, perguntar um nome de arquivo e gravar nele o texto novo; resposta vazia não grava nada ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | partir do exercício 1, mandar as mensagens de erro para a **saída de erro**, com o prefixo `[STDERR]`, e ler o nome do arquivo sem usar `input()` ([Exercício 2](../05-ex2/01-o-problema.md)) |
| 3 | escrever uma função `secure_archive()` que lê ou grava um arquivo usando `with` e devolve uma tupla `(True ou False, texto)`, e uma demonstração com quatro chamadas ([Exercício 3](../06-ex3/01-o-problema.md)) |

Para cada exercício, o enunciado mostra exemplos da saída. A página [O resultado
final](./04-o-resultado-final.md) reúne todos.

## Entrega

Só os quatro arquivos `.py`, com esses nomes e nessas pastas, num repositório Git. Na avaliação,
quem avalia pode pedir que você explique as operações com arquivos, mostre o tratamento de erros e
explique como o `with` funciona ([Entregar](../07-fechamento/02-entregar.md)).

## O que o enunciado cita sem explicar

- **`cat`**: o comando do terminal que imprime o conteúdo de um arquivo. `cat ancient_fragment.txt`
  mostra o texto do arquivo, sem mais nada.
- **`/etc/master.passwd`**: um arquivo do macOS que só o administrador pode ler; o enunciado o usa
  como exemplo de "arquivo inacessível". No Linux ele não existe. O tutorial usa `/etc/sudoers`,
  protegido do mesmo jeito e presente nos dois sistemas ([Quando o open
  falha](../02-arquivos/05-quando-o-open-falha.md)).
- **"Compatível com 2087"**: só a justificativa de brincadeira para o `#` no fim das linhas.
- **"Três canais de dados mais antigos que a Internet"**: a entrada padrão, a saída padrão e a saída
  de erro, que existem desde os primeiros sistemas Unix ([Os três
  fluxos](../05-ex2/02-os-tres-fluxos.md)).
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
