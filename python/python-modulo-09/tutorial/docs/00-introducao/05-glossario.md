---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__name__`** | variável que vale `"__main__"` no arquivo rodado direto | [A demonstração do exercício 0](../03-ex0/03-a-demonstracao.md#o-if-do-fim) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um arquivo; não é entregue | [Rodar e conferir do exercício 0](../03-ex0/05-rodar-e-conferir.md#testar-cada-limite) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o Pydantic, o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **`Any`** | type hint de `typing` que quer dizer "qualquer tipo" | [Field e restrições](../02-conceitos/03-field-e-restricoes.md#o-experimento) |
| **atributo** | variável guardada dentro de um objeto; num modelo, cada campo vira um atributo | [Pré-requisitos](./03-pre-requisitos.md) |
| **`BaseModel`** | a classe base do Pydantic: todo modelo herda dela | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
| **biblioteca** | código pronto, instalado à parte, que o programa usa com `import` | [O que vamos construir](./01-o-que-vamos-construir.md) |
| **biblioteca padrão** | os módulos que vêm com o Python, como `datetime`, `enum` e `json` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md#os-import-permitidos) |
| **campo** | cada linha `nome: tipo` de um modelo | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
| **campo obrigatório** | campo sem valor padrão; se faltar, o erro é `Field required` | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
| **campo opcional** | campo `str \| None` com padrão `None`: aceita um texto ou nada | [Field e restrições](../02-conceitos/03-field-e-restricoes.md#campo-opcional) |
| **classe** | o molde de um tipo de objeto | [Pré-requisitos](./03-pre-requisitos.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Conferir tudo](../07-fechamento/01-conferir-tudo.md#nenhum-programa-trava) |
| **construtor** | o método que cria o objeto; num modelo, recebe os campos pelo nome e os confere | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
| **CSV** | formato de texto para tabelas: uma linha por registro, campos separados por vírgula | [As ferramentas](../06-dados-do-gerador/01-as-ferramentas.md#data_exporterpy) |
| **`ctx`** | chave do erro com o contexto; num `value_error`, guarda o `ValueError` original | [model_validator](../02-conceitos/06-model-validator.md#a-mensagem-da-regra) |
| **`datetime`** | o tipo de data e hora do Python, do módulo `datetime` | [Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md#datetime) |
| **decorador** | linha com `@` em cima de um `def` que modifica a função | [model_validator](../02-conceitos/06-model-validator.md#decorador) |
| **`diff`** | comando que compara dois textos linha a linha e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/05-rodar-e-conferir.md) |
| **Enum** | classe com uma lista fechada de valores, os membros | [Enum](../02-conceitos/05-enum.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`error_count()`** | método da `ValidationError` que devolve quantos erros há | [ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz) |
| **`errors()`** | método da `ValidationError` que devolve a lista de erros, um dicionário por erro | [ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **`Field`** | função do Pydantic que põe restrições e valor padrão num campo | [Field e restrições](../02-conceitos/03-field-e-restricoes.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`ge`, `le`, `gt`, `lt`** | restrições de número: maior ou igual, menor ou igual, maior, menor | [Field e restrições](../02-conceitos/03-field-e-restricoes.md) |
| **herança** | uma classe filha recebe os métodos e atributos da classe mãe | [Pré-requisitos](./03-pre-requisitos.md#herança-em-resumo) |
| **ISO 8601** | o formato padrão de data e hora em texto: `2024-01-15T10:30:00` | [Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md#datetime) |
| **JSON** | formato de texto para dados: listas, dicionários, textos, números, `true`, `false` e `null` | [As ferramentas](../06-dados-do-gerador/01-as-ferramentas.md#data_exporterpy) |
| **`loc`** | chave do erro com o caminho até o campo, como `('crew', 1, 'age')` | [ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz) |
| **membro** | cada valor de um Enum, com nome (`RADIO`) e valor (`"radio"`) | [Enum](../02-conceitos/05-enum.md) |
| **`min_length`, `max_length`** | restrições de tamanho: caracteres de um texto ou itens de uma lista | [Field e restrições](../02-conceitos/03-field-e-restricoes.md) |
| **modelo** | classe que herda de `BaseModel` e descreve os campos de um tipo de dado | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
| **modelo aninhado** | modelo usado como tipo de um campo de outro modelo | [Modelos aninhados](../02-conceitos/07-modelos-aninhados.md) |
| **modo leniente (*lax mode*)** | o padrão do Pydantic: converte valores quando a conversão não perde nada | [Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md#o-que-aconteceu) |
| **`model_validate`** | método de todo modelo que cria o objeto a partir de um dicionário | [ValidationError](../02-conceitos/02-validationerror.md#model_validate) |
| **`model_validator`** | decorador de um método com regras que envolvem vários campos | [model_validator](../02-conceitos/06-model-validator.md) |
| **módulo** | arquivo de código que entra no programa com `import` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md#os-import-permitidos) |
| **`msg`** | chave do erro com a mensagem, em inglês | [ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`MYPYPATH`** | variável que diz ao mypy em que pastas procurar os módulos importados | [Rodar e conferir do exercício 0](../03-ex0/05-rodar-e-conferir.md#testar-cada-limite) |
| **`None`** | o valor que quer dizer "nada" | [Pré-requisitos](./03-pre-requisitos.md) |
| **pip** | o instalador de bibliotecas do Python | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **Pydantic** | biblioteca que confere e converte dados a partir de classes com campos tipados | [O que vamos construir](./01-o-que-vamos-construir.md) |
| **`PYTHONPATH`** | variável que acrescenta pastas à procura de módulos do Python | [Rodar e conferir do exercício 0](../03-ex0/05-rodar-e-conferir.md#testar-cada-limite) |
| **regra de negócio** | regra do assunto tratado que vai além do limite de cada campo, muitas vezes comparando campos entre si | [O problema do exercício 1](../04-ex1/01-o-problema.md) |
| **restrição** | limite de um campo além do tipo, como `le=20` | [Field e restrições](../02-conceitos/03-field-e-restricoes.md) |
| **semente (*seed*)** | o ponto de partida do sorteio do `random`; a mesma semente dá os mesmos números | [As ferramentas](../06-dados-do-gerador/01-as-ferramentas.md#data_generatorpy) |
| **`self`** | o próprio objeto, recebido como primeiro parâmetro de cada método | [Pré-requisitos](./03-pre-requisitos.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **type hint** | anotação do tipo de um parâmetro, variável, retorno ou campo, como `crew_size: int` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **união** | `str \| None`: um tipo ou outro | [Field e restrições](../02-conceitos/03-field-e-restricoes.md#campo-opcional) |
| **validação** | conferir se os dados seguem os tipos e as regras antes de usá-los | [O que vamos construir](./01-o-que-vamos-construir.md) |
| **`ValidationError`** | a exceção do Pydantic com todos os erros de validação | [ValidationError](../02-conceitos/02-validationerror.md) |
| **`value_error`** | tipo de erro de um `ValueError` lançado numa regra; o `msg` começa com `Value error, ` | [model_validator](../02-conceitos/06-model-validator.md#a-mensagem-da-regra) |
| **`ValueError`** | exceção do Python para valor inválido; as regras a lançam | [model_validator](../02-conceitos/06-model-validator.md) |
| **valor padrão** | valor que um campo recebe quando fica de fora | [O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md) |
