---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo** ([O Python](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha com mais de 79 caracteres, falta de linha em branco entre
  funções, `import` que não é usado. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todo o código, conferidos pelo mypy.** Um *type hint* é a anotação do tipo de
  cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o programa que
  confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **O tratamento de exceções protege os dados.** Um dado inválido não pode virar objeto nem
  derrubar o programa: o erro de validação é capturado e mostrado
  ([ValidationError](../02-conceitos/02-validationerror.md)).
- **Tipos e funções embutidos liberados.** Todos os tipos padrão (`int`, `str`, `list`, `dict`...)
  com todos os seus métodos, e todas as funções que o Python oferece sem `import` (`print`, `len`,
  `isinstance`...).
- **pip e ambiente virtual obrigatórios.** O Pydantic não vem com o Python: é instalado com o
  `pip`, o instalador de bibliotecas do Python, dentro de um **ambiente virtual**, uma pasta com
  as bibliotecas só deste projeto ([O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md)).
- **Pydantic 2.x em todos os exercícios.** A versão 2 do Pydantic mudou muitos nomes da versão 1.
  O enunciado pede a sintaxe da versão 2: manda evitar o `@validator`, obsoleto, e usar o
  `@model_validator` ([model_validator](../02-conceitos/06-model-validator.md)). Um **decorador**
  é a linha com `@` escrita em cima de um `def`, que modifica a função logo abaixo.

## Os `import` permitidos

O enunciado diz que os módulos permitidos além do Pydantic aparecem no quadro de cada exercício,
e os três quadros dizem `Authorized: None` ("autorizado: nenhum"). Mas o mesmo enunciado, na seção
sobre as ferramentas de dados, diz que os módulos da **biblioteca padrão** (os que vêm com o
Python, como `json`, `csv` e `datetime`) são permitidos. Um **módulo** é um arquivo de código que
entra no programa com `import`.

Os três exercícios precisam de dois módulos da biblioteca padrão: `datetime`, porque todos têm um
campo de data e hora, e `enum`, porque os exercícios 1 e 2 pedem um *Enum* (uma lista fechada de
valores, [Enum](../02-conceitos/05-enum.md)). Escolha do tutorial: `None` quer dizer "nenhuma
biblioteca de fora além do Pydantic", e a biblioteca padrão vale pela regra das ferramentas. Os
arquivos entregues importam só `pydantic`, `datetime` e `enum`.

## Os três exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | criar o modelo `SpaceStation`, de uma estação espacial, com oito campos e os limites de cada um (identificador de 3 a 10 caracteres, tripulação de 1 a 20 pessoas, energia e oxigênio de 0 a 100%...). O `main()` cria uma estação válida, mostra os dados dela e tenta criar uma estação com 25 tripulantes ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | criar o Enum `ContactType` com os tipos de contato `radio`, `visual`, `physical` e `telepathic`, e o modelo `AlienContact`, de um relato de contato com alienígenas, com nove campos e quatro regras de negócio num `@model_validator` ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | criar o Enum `Rank` com as patentes, o modelo `CrewMember`, de um tripulante, e o modelo `SpaceMission`, de uma missão com uma lista de tripulantes, com quatro regras de segurança ([Exercício 2](../05-ex2/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída do programa. A página
[O resultado final](./04-o-resultado-final.md) reúne as três.

## As ferramentas de dados

O enunciado vem com duas ferramentas escritas em Python, `data_generator.py` e
`data_exporter.py`, que geram dados de teste para os três modelos e os gravam numa pasta
`generated_data/`. Elas não fazem parte da entrega; servem para testar os modelos com muitos
dados ([Os dados do gerador](../06-dados-do-gerador/01-as-ferramentas.md)).

## Entrega

Só os três arquivos `.py`, com esses nomes e nessas pastas, num repositório Git. O enunciado
também pede que o código mostre que os conceitos foram entendidos, com comentários claros e nomes
de variáveis que digam o que guardam ([Entregar](../07-fechamento/02-entregar.md)).

## O que o enunciado cita sem explicar

- **Modelo** e **`BaseModel`**: um modelo é uma classe que herda de `BaseModel`, do Pydantic, e
  descreve os campos de um tipo de dado ([O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md)).
- **`Field`**: a função do Pydantic que põe limites e valores padrão num campo
  ([Field e restrições](../02-conceitos/03-field-e-restricoes.md)).
- **Validação embutida** e **conversão automática de tipos**: o que o Pydantic confere e
  converte sozinho, só pelos tipos e limites declarados
  ([Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md)).
- **Decorador**: a linha com `@` em cima de um `def`, como `@model_validator(...)`, que modifica
  a função logo abaixo ([Decorador](../02-conceitos/06-model-validator.md#decorador)).
- **`@model_validator(mode='after')`**: o decorador das regras que vão além do limite de cada
  campo, rodadas depois que cada campo passou na sua conferência
  ([model_validator](../02-conceitos/06-model-validator.md)).
- **Enum**: uma lista fechada de valores com nome ([Enum](../02-conceitos/05-enum.md)).
- **DateTime**: o tipo `datetime`, uma data com hora ([Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md)).
- **Optional string** ("string opcional"): um campo que pode ser um texto ou `None`, o valor
  que quer dizer "nada" ([Field e restrições](../02-conceitos/03-field-e-restricoes.md)).
- **Modelos aninhados** (*nested models*): um modelo cujo campo guarda outros modelos, como a
  missão que guarda tripulantes ([Modelos aninhados](../02-conceitos/07-modelos-aninhados.md)).
- **JSON e CSV**: dois formatos de texto para dados, usados pelas ferramentas de dados
  ([As ferramentas](../06-dados-do-gerador/01-as-ferramentas.md#data_exporterpy)).
- **Cosmic Data Observatory, "junior Data Engineer"**: só o cenário de ficção do projeto.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
