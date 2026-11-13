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
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **Tipos e funções embutidos liberados, menos `eval` e `exec`.** Todos os tipos padrão (`int`,
  `str`, `list`, `dict`, `tuple`...) com todos os seus métodos, e todas as funções que o Python
  oferece sem `import` (`print`, `len`, `isinstance`, `range`...), exceto `eval()` e `exec()`,
  que rodam um texto como se fosse código. Um **método** é uma função que pertence a um valor e é
  chamada com ponto: `"abc".upper()` chama o método `upper` do texto `"abc"` e devolve `"ABC"`.
- **Exceções tratadas, nenhum programa quebra.** Uma **exceção** é o objeto que o Python cria
  quando algo dá errado; se ninguém a trata, o programa para com uma mensagem de erro
  ([Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo)). Nenhum programa do projeto pode
  terminar assim. A única exceção que o projeto prevê é a da estratégia inválida no exercício 2,
  e o torneio a trata ([A função battle](../05-ex2/05-a-funcao-battle.md)).
- **Nenhuma biblioteca externa.** Só o que vem com o Python. Em cada exercício, os únicos
  `import` da biblioteca do Python são `abc` e `typing`, dois **módulos** (arquivos de código que
  vêm com o Python): `abc` traz o que é preciso para criar classes abstratas
  ([Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md)), e `typing` traz type
  hints especiais. Além deles, cada exercício importa o próprio código do projeto: o `ex1` usa o
  `ex0`, e o `ex2` usa os dois.
- **Um `__init__.py` em cada pasta de exercício.** É o arquivo que transforma a pasta num
  **pacote**, uma pasta de código que se importa pelo nome
  ([Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md)).
- **Os programas de teste ficam na raiz.** A **raiz** do repositório é a pasta principal, a que
  contém as pastas `ex0/`, `ex1/` e `ex2/`. Os três programas de teste (`battle.py`,
  `capacitor.py` e `tournament.py`) ficam nela, fora dos pacotes.

## Os três exercícios

| Exercício | O que precisa ser feito |
|---|---|
| 0 | no pacote `ex0`: a classe abstrata `Creature` (nome, tipo, `attack` abstrato e `describe` comum), as criaturas `Flameling`, `Pyrodon`, `Aquabub` e `Torragon`, a classe abstrata `CreatureFactory` (com `create_base` e `create_evolved`) e as fábricas `FlameFactory` e `AquaFactory`. Na raiz, `battle.py` testa cada fábrica e faz duas criaturas lutarem ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | no pacote `ex1`: as classes abstratas `HealCapability` (com `heal`) e `TransformCapability` (com `transform` e `revert`), as criaturas `Sproutling` e `Bloomelle` (que curam), `Shiftling` e `Morphagon` (que se transformam) e as fábricas `HealingCreatureFactory` e `TransformCreatureFactory`. Na raiz, `capacitor.py` testa as duas famílias ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | no pacote `ex2`: a classe abstrata `BattleStrategy` (com `act` e `is_valid`), as estratégias `NormalStrategy`, `AggressiveStrategy` e `DefensiveStrategy` e uma exceção própria para combinações inválidas. Na raiz, `tournament.py` organiza três torneios com uma única função `battle` ([Exercício 2](../05-ex2/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída completa do programa de teste. A página
[O resultado final](./04-o-resultado-final.md) reúne as três.

## Os pacotes só expõem fábricas

Os pacotes `ex0` e `ex1` **não podem expor as criaturas concretas**: quem usa o pacote recebe
as fábricas, e só por meio delas obtém criaturas. "Expor" é oferecer um nome a quem importa o
pacote: `from ex0 import FlameFactory` precisa funcionar, e `from ex0 import Flameling` não pode
([O `__init__.py` do pacote](../03-ex0/06-o-init-do-pacote.md)).

## Entrega

Os três programas de teste e as três pastas de pacote, num repositório Git. Na avaliação, quem
avalia pode pedir que você explique os padrões de projeto usados
([As perguntas do enunciado](../06-fechamento/03-as-perguntas-do-enunciado.md)).

## O que o enunciado cita sem explicar

- **Creature** ("criatura"): cada carta do jogo. Tem um nome, um tipo (como `Fire`, "fogo") e um
  ataque.
- **Família, base e evoluída:** as criaturas vêm em famílias de duas: a forma **base** e a forma
  **evoluída**, mais forte. `Flameling` é a base da família do fogo, e `Pyrodon`, a evoluída.
- **Factory** ("fábrica"): objeto cujo trabalho é criar outros objetos
  ([O padrão fábrica abstrata](../03-ex0/02-o-padrao-fabrica-abstrata.md)).
- **Capability** ("capacidade"): uma habilidade extra, descrita numa classe abstrata separada de
  `Creature` ([As capacidades](../04-ex1/02-as-capacidades.md)).
- **Strategy** ("estratégia"): o jeito de agir numa luta, guardado num objeto que se pode trocar
  ([O padrão estratégia](../05-ex2/02-o-padrao-estrategia.md)).
- **Deck Architect, DataDeck, *Gotta catch 'em all*:** só o cenário de ficção do projeto, um jogo
  de colecionar monstros.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
