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
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)). O mypy acusa
  um único erro em todo o projeto, no exercício 0: o enunciado pede um teste que o provoca e
  avisa que ele fica de propósito
  ([O erro proposital do mypy](../03-ex0/07-o-erro-proposital-do-mypy.md)).
- **O tratamento de exceções protege os fluxos de dados contra corrupção.** No tutorial, isso
  quer dizer que um dado inválido não estraga o que já estava guardado: ou ele entra inteiro, ou
  não entra nada
  ([Numeric Processor](../03-ex0/03-numeric-processor.md#por-que-validar-a-lista-inteira-antes-de-guardar)).
- **Só dois `import` da biblioteca do Python: `abc` e `typing`.** São dois **módulos**
  (arquivos de código que vêm com o Python): `abc` traz o que é preciso para criar classes
  abstratas ([A classe abstrata](../02-conceitos/02-a-classe-abstrata.md)), e `typing` traz type
  hints especiais, como `Any` e `Protocol`
  ([Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md)). Bibliotecas
  externas (as que se instalam à parte, com `pip`) são proibidas. Os arquivos do próprio projeto
  importam uns aos outros: o exercício 4 usa as criaturas do exercício 3, e isso é pedido pelo
  enunciado.
- **Tipos e funções embutidos liberados, menos `eval` e `exec`.** Todos os tipos padrão (`int`,
  `str`, `list`, `dict`, `tuple`...) com todos os seus métodos, e todas as funções que o Python
  oferece sem `import` (`print`, `len`, `isinstance`, `range`, `str`...), exceto `eval()` e
  `exec()`, que rodam um texto como se fosse código Python. Um **método** é uma função que
  pertence a um valor e é chamada com ponto: `"abc".upper()` chama o método `upper` do texto
  `"abc"` e devolve `"ABC"`.

## Onde fica cada arquivo

Tudo fica na **raiz do repositório** (a pasta principal da entrega, sem subpasta por exercício),
menos os dois pacotes:

- os exercícios 0, 1 e 2 são arquivos soltos na raiz: `data_processor.py`, `data_stream.py` e
  `data_pipeline.py`;
- os exercícios 3 e 4 são **pacotes**, as pastas `ex3/` e `ex4/`. Cada uma tem obrigatoriamente
  um arquivo `__init__.py`, o arquivo que transforma uma pasta em pacote
  ([O pacote](../06-pacotes/01-o-pacote.md));
- os **scripts de teste** dos exercícios 3 e 4 (`battle.py`, `capacitor.py` e `tournament.py`)
  ficam na raiz, ao lado dos pacotes, e importam o que precisam deles.

O enunciado avisa que os pacotes e o `__init__.py` são pré-requisito: a parte
[Pacotes e herança múltipla](../06-pacotes/01-o-pacote.md) explica o necessário antes do
exercício 3.

## Os cinco exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | criar a classe abstrata `DataProcessor` com os métodos `validate` (o dado serve?), `ingest` (guarda o dado) e `output` (devolve o item mais antigo, com o seu número de ordem), e três classes filhas: `NumericProcessor` (números), `TextProcessor` (textos) e `LogProcessor` (registros de log). Depois, testar cada uma ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | partir do exercício 0 e criar a classe `DataStream`, que recebe processadores com `register_processor`, distribui uma lista de dados misturados entre eles com `process_stream` e mostra quantos itens cada um recebeu com `print_processors_stats` ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | partir do exercício 1, criar a regra `ExportPlugin` para os plugins de exportação, o método `output_pipeline` em `DataStream`, e dois plugins: um que escreve os dados em CSV e outro em JSON ([Exercício 2](../05-ex2/01-o-problema.md)) |
| 3 | no pacote `ex3`, criar a classe abstrata `Creature`, duas criaturas comuns (`Flameling` e `Pyrodon`), a capacidade abstrata `TransformCapability`, duas criaturas que se transformam (`Shiftling` e `Morphagon`) e as fábricas que as criam (`CreatureFactory`, `FlameFactory` e `TransformCreatureFactory`). O pacote só oferece as fábricas. Testar com `battle.py` e `capacitor.py` ([Exercício 3](../07-ex3/01-o-problema.md)) |
| 4 | no pacote `ex4`, criar a estratégia abstrata `BattleStrategy` e duas estratégias, `NormalStrategy` e `AggressiveStrategy`; em `tournament.py`, uma função `battle` que põe criaturas para lutar, cada uma com a sua estratégia ([Exercício 4](../08-ex4/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída completa do programa. A página
[O resultado final](./04-o-resultado-final.md) reúne todas.

## Entrega

Só os arquivos pedidos, com esses nomes e nesses lugares, num repositório Git. Na avaliação, quem
avalia pode pedir que você explique o polimorfismo, mostre a sobrescrita de métodos, acrescente
ao sistema um tipo de dado novo, uma família de criaturas nova ou uma estratégia nova, ou mude o
jeito de processar um dado, e que explique para que serve cada padrão de projeto
([As perguntas do enunciado](../09-fechamento/03-as-perguntas-do-enunciado.md)).

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
- **Duck typing** ("tipagem de pato") e **tipagem estrutural**: aceitar qualquer objeto que tenha
  os métodos certos, sem exigir que ele herde de uma classe
  ([Protocol e duck typing](../05-ex2/02-protocol-e-duck-typing.md)).
- **CSV e JSON**: dois formatos de texto para dados, explicados em
  [O plugin CSV](../05-ex2/04-o-plugin-csv.md) e [O plugin JSON](../05-ex2/05-o-plugin-json.md).
- **Package** ("pacote") e **`__init__.py`**: a pasta de módulos e o arquivo que diz o que ela
  oferece a quem a importa ([O pacote](../06-pacotes/01-o-pacote.md)).
- **Abstract factory** ("fábrica abstrata"): o padrão em que um objeto, a fábrica, cria os
  objetos de uma família, e quem pede não sabe qual classe recebe
  ([A fábrica abstrata](../07-ex3/06-a-fabrica-abstrata.md)).
- **Capability** ("capacidade"): uma habilidade descrita numa classe abstrata separada, que só
  as classes que têm a habilidade herdam ([A capacidade](../07-ex3/04-a-capacidade.md)).
- **Abstract strategy** ("estratégia abstrata"): o padrão em que o jeito de agir fica num objeto
  à parte, trocável, e quem usa só chama um método dele
  ([A estratégia abstrata](../08-ex4/03-a-estrategia-abstrata.md)).
- **Neo-Tokyo, 2087, "Stream Engineer", "combat sandbox"**: só o cenário de ficção do projeto.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
