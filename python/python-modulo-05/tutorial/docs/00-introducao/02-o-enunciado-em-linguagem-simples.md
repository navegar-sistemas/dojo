---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([O Python](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha com mais de 79 caracteres, falta de linha em branco entre
  funções, `import` que não é usado. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todo o código, conferidos pelo mypy.** Um *type hint* é a anotação do tipo de
  cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o programa que
  confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)). Há uma única
  reclamação do mypy que o enunciado pede de propósito, no exercício 0
  ([O erro proposital do mypy](../03-ex0/06-o-erro-proposital-do-mypy.md)).
- **O tratamento de exceções protege os dados.** Um dado inválido não pode estragar o que já
  estava guardado: ou ele entra inteiro, ou não entra nada
  ([Numeric Processor](../03-ex0/03-numeric-processor.md)).
- **Só dois `import`: `abc` e `typing`.** São dois **módulos** (arquivos de código que vêm com o
  Python): `abc` traz o que é preciso para criar classes abstratas
  ([A classe abstrata](../02-conceitos/02-a-classe-abstrata.md)), e `typing` traz type hints
  especiais, como `Any` e `Protocol`
  ([Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md)).
- **Tipos e funções embutidos liberados.** Todos os tipos padrão (`int`, `str`, `list`, `dict`,
  `tuple`...) com todos os seus métodos, e todas as funções que o Python oferece sem `import`
  (`print`, `len`, `isinstance`, `range`, `str`...). Um **método** é uma função que pertence a um
  valor e é chamada com ponto: `"abc".upper()` chama o método `upper` do texto `"abc"` e devolve
  `"ABC"`.

## Os três exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | criar a classe abstrata `DataProcessor` com os métodos `validate` (o dado serve?), `ingest` (guarda o dado) e `output` (devolve o item mais antigo, com o seu número de ordem), e três classes filhas: `NumericProcessor` (números), `TextProcessor` (textos) e `LogProcessor` (registros de log). Depois, testar cada uma ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | partir do exercício 0 e criar a classe `DataStream`, que recebe processadores com `register_processor`, distribui uma lista de dados misturados entre eles com `process_stream` e mostra quantos itens cada um recebeu com `print_processors_stats` ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | partir do exercício 1, criar a regra `ExportPlugin` para os plugins de exportação, o método `output_pipeline` em `DataStream`, e dois plugins: um que escreve os dados em CSV e outro em JSON ([Exercício 2](../05-ex2/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída completa do programa. A página
[O resultado final](./04-o-resultado-final.md) reúne as três.

## Entrega

Só os três arquivos `.py`, com esses nomes e nessas pastas, num repositório Git. Na avaliação,
quem avalia pode pedir que você explique o polimorfismo, mostre a sobrescrita de métodos,
acrescente um tipo de dado novo ao sistema ou mude o jeito de processar um dado
([As perguntas do enunciado](../06-fechamento/03-as-perguntas-do-enunciado.md)).

## O que o enunciado cita sem explicar

- **ABC** (*Abstract Base Class*, "classe base abstrata"): a classe do módulo `abc` da qual uma
  classe herda para virar abstrata ([A classe abstrata](../02-conceitos/02-a-classe-abstrata.md)).
- **Stream** ("fluxo", "correnteza"): uma sequência de dados que chega para ser processada; aqui,
  uma lista do Python ([Registrar e rotear](../04-ex1/03-registrar-e-rotear.md)).
- **Rank** ("posição", "ordem"): o número de ordem de cada item dentro do processador: o primeiro
  item guardado tem rank 0, o segundo 1, e assim por diante ([A fila](../02-conceitos/05-a-fila.md)).
- **Pipeline** ("encanamento", "linha de montagem"): o caminho completo do dado, da entrada no
  fluxo até a saída exportada ([output_pipeline](../05-ex2/03-output-pipeline.md)).
- **Plugin**: uma peça que se encaixa no programa sem que o programa precise ser alterado; aqui,
  um objeto que sabe exportar dados num formato.
- **Duck typing** ("tipagem de pato"): aceitar qualquer objeto que tenha os métodos certos, sem
  exigir que ele herde de uma classe ([Protocol e duck typing](../05-ex2/02-protocol-e-duck-typing.md)).
- **CSV e JSON**: dois formatos de texto para dados, explicados em
  [O plugin CSV](../05-ex2/04-o-plugin-csv.md) e [O plugin JSON](../05-ex2/05-o-plugin-json.md).
- **Neo-Tokyo, 2087, "Stream Engineer"**: só o cenário de ficção do projeto.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
