---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([Ambiente](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha comprida demais, falta de linha em branco entre funções,
  variável criada e nunca usada. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todas as funções e métodos, conferidos pelo mypy.** Um *type hint* é a anotação
  do tipo de cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o
  programa que confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **Um arquivo por exercício**, cada um na sua pasta (`ex0/` a `ex4/`).
- **O programa nunca pode travar.** "Travar" (*crash*) aqui quer dizer parar no meio com uma
  mensagem de erro do Python. Todo erro que os programas provocam de propósito precisa ser
  capturado.
- **Usar as exceções que já vêm com o Python** (as *embutidas*) do jeito certo: cada erro com o
  tipo que combina com ele ([Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md)).
- **Mostrar os dois lados:** os programas demonstram operações que dão certo e operações que
  dão errado. A saída de exemplo do exercício 3 só tem erros, e o programa segue o exemplo
  ([Exercício 3](../06-ex3/01-o-problema.md)).
- **Tratar os erros com `try` e `except`**, em todos os exercícios
  ([try e except](../02-excecoes/03-try-e-except.md)).
- **Qualquer exceção embutida pode ser usada**, como `ValueError`, `TypeError`,
  `ZeroDivisionError`, `FileNotFoundError`, `KeyError`, `IndexError`, `AttributeError` e
  `Exception`, a classe de que todas elas derivam; alguns exercícios indicam as mais adequadas
  ([Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md)).
- **Soluções simples**, focadas em mostrar o tratamento de erros.

O enunciado também diz que as palavras `try`, `except`, `finally` e `raise` podem ser usadas à
vontade, mesmo sem aparecer nas listas abaixo, porque são parte da linguagem e não funções.

## Funções autorizadas

Cada exercício tem uma lista de **funções autorizadas**: as únicas funções prontas do Python que o
código pode chamar. Funções e classes que você mesmo escreve no arquivo podem ser chamadas sempre.

| Exercício | Funções autorizadas |
|---|---|
| 0 e 1 | `int()`, `print()` |
| 2 | `print()`, `open()`, `int()` |
| 3 | `print()` |
| 4 | `print()`, `str.capitalize()` |

A lista do exercício 3 tem só `print()`. Isso muda a forma de escrever as classes de erro, como
mostra a página [O método `__str__`](../06-ex3/04-o-metodo-str.md).

## Os cinco exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | uma função `input_temperature(temp_str)` que converte um texto em número inteiro, e uma função `test_temperature()` que a testa com `"25"` (dá certo) e `"abc"` (dá errado), mostra o erro e segue em frente ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | a mesma `input_temperature`, agora **lançando** uma exceção quando a temperatura está fora da faixa de 0 a 40 graus Celsius (0 e 40 são aceitos); os testes ganham `"100"` e `"-50"`, e o **main** do arquivo (o trecho que ele executa quando é rodado, explicado em [O main](../03-ex0/04-o-main.md)) chama `test_temperature()` ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | uma função `garden_operations(operation_number)` que provoca um tipo de erro diferente para cada número de 0 a 3 (`ValueError`, `ZeroDivisionError`, `FileNotFoundError` e `TypeError`) e não faz nada com os outros, e uma função `test_error_types()` que mostra cada erro acontecendo, o captura e explica o que deu errado, continua depois de cada um e mostra como capturar vários tipos com um único `try`, sem usar `type()` ([Exercício 2](../05-ex2/01-o-problema.md)) |
| 3 | três tipos de erro novos: `GardenError` e, herdando dele, `PlantError` e `WaterError`, cada um com uma mensagem padrão; funções que os lançam em situações diferentes, mostram como capturar cada tipo específico e mostram que capturar `GardenError` pega todos os erros do jardim, inclusive os das duas filhas ([Exercício 3](../06-ex3/01-o-problema.md)) |
| 4 | uma função `water_plant(plant_name)` que rega uma planta e recusa nomes que não estão **capitalizados** (primeira letra maiúscula e as outras minúsculas, como `Tomato`), lançando o `PlantError` do exercício 3 nesse caso e imprimindo uma mensagem quando rega; e uma função `test_watering_system()` que "abre" o sistema de irrigação, rega várias plantas, trata o erro de um nome inválido interrompendo o teste e voltando imediatamente para o main, e "fecha" o sistema sempre, com erro ou sem erro, num bloco `finally` ([Exercício 4](../07-ex4/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída exata do programa. A página
[O resultado final](./04-o-resultado-final.md) reúne as cinco.

## Entrega

Só os cinco arquivos `.py` (`ex0/ft_first_exception.py`, `ex1/ft_raise_exception.py`,
`ex2/ft_different_errors.py`, `ex3/ft_custom_errors.py` e `ex4/ft_finally_block.py`), com esses
nomes e nessas pastas, num repositório Git ([Entregar](../08-fechamento/02-entregar.md)).

## O que o enunciado cita sem explicar

- **"Module 00" e "Module 01"** (módulos 00 e 01): o básico de Python e as classes, que o enunciado supõe
  conhecidos. Tudo o que este tutorial usa deles está nos
  [pré-requisitos](./03-pre-requisitos.md).
- **"You have already encountered open() in C"** (você já encontrou o `open()` em C): a linguagem C também tem uma função `open` para abrir
  arquivos. Não é preciso saber C; o `open()` do Python é explicado no
  [exercício 2](../05-ex2/02-garden-operations.md).
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo, conferido e testado antes de ser usado.
