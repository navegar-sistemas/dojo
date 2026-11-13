---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__init__`** | o construtor: método que roda sozinho quando o objeto é criado | [Pré-requisitos](./03-pre-requisitos.md) |
| **`__name__`** | variável que vale `"__main__"` no arquivo rodado com `python3` | [A demonstração do exercício 0](../03-ex0/07-a-demonstracao.md) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um arquivo; não é entregue | [Rodar e conferir do exercício 0](../03-ex0/09-rodar-e-conferir.md) |
| **ABC** | classe do módulo `abc` da qual uma classe herda para virar abstrata | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **`@abstractmethod`** | decorador que marca um método como obrigatório nas classes filhas | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **`Any`** | type hint de `typing` que quer dizer "qualquer tipo" | [Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md) |
| **assinatura** | a linha do `def`: nome, parâmetros com tipos e tipo do retorno | [O problema do exercício 0](../03-ex0/01-o-problema.md) |
| **atributo** | variável guardada dentro de um objeto, como `self._items` | [Pré-requisitos](./03-pre-requisitos.md) |
| **atributo de classe** | atributo escrito no corpo da classe, igual para todos os objetos, como `name` | [Nome e contadores](../04-ex1/02-nome-e-contadores.md) |
| **`Callable`** | type hint de `typing` para uma função: `Callable[[Any], bool]` recebe um argumento e devolve `bool` | [Numeric Processor](../03-ex0/03-numeric-processor.md) |
| **classe** | o molde de um tipo de objeto | [Pré-requisitos](./03-pre-requisitos.md) |
| **classe abstrata** | classe que só serve de molde: não pode ser instanciada e lista os métodos que as filhas escrevem | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Conferir tudo](../06-fechamento/01-conferir-tudo.md) |
| **CSV** | formato de texto para tabelas: campos separados por vírgula | [O plugin CSV](../05-ex2/04-o-plugin-csv.md) |
| **decorador** | linha com `@` em cima de um `def` que modifica o método | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **`diff`** | comando que compara duas listas de linhas e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/09-rodar-e-conferir.md) |
| **duck typing** | julgar um objeto pelos métodos que ele tem, e não pela classe de que herda | [Protocol e duck typing](../05-ex2/02-protocol-e-duck-typing.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **escape** | escrever um caractere especial com um código, como `\"` no JSON | [O plugin JSON](../05-ex2/05-o-plugin-json.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **expressão condicional** | `a if condição else b`: vale `a` se a condição é verdadeira, e `b` se não | [Numeric Processor](../03-ex0/03-numeric-processor.md) |
| **fila (FIFO)** | estrutura em que o primeiro a entrar é o primeiro a sair | [A fila](../02-conceitos/05-a-fila.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **fluxo (*stream*)** | sequência de dados que chega para ser processada; aqui, uma lista | [O problema do exercício 1](../04-ex1/01-o-problema.md) |
| **herança** | uma classe filha recebe os métodos e atributos da classe mãe | [Pré-requisitos](./03-pre-requisitos.md) |
| **`IndexError`** | exceção de `pop(0)` numa lista vazia | [A fila](../02-conceitos/05-a-fila.md) |
| **instância (objeto)** | valor criado a partir de uma classe, como `NumericProcessor()` | [Pré-requisitos](./03-pre-requisitos.md) |
| **invariante** | regra do mypy para listas: `list[int]` não é aceita onde se pede `list[int \| float]` | [Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md#lista-invariante) |
| **`isinstance`** | função que responde se um valor é de um tipo (ou de um tipo filho dele) | [Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md) |
| **JSON** | formato de texto para dados estruturados: pares `"chave": valor` entre chaves | [O plugin JSON](../05-ex2/05-o-plugin-json.md) |
| **lote (*batch*)** | uma lista de elementos enviada de uma vez ao fluxo | [O problema do exercício 1](../04-ex1/01-o-problema.md) |
| **log** | registro de algo que aconteceu num sistema, com nível e mensagem | [Log Processor](../03-ex0/05-log-processor.md) |
| **método** | função que pertence a um objeto e é chamada com ponto | [Pré-requisitos](./03-pre-requisitos.md) |
| **método abstrato** | método marcado com `@abstractmethod`, que toda filha precisa escrever | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **módulo** | arquivo de código que entra no programa com `import`, como `abc` e `typing` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`MYPYPATH`** | variável que diz ao mypy em que pasta procurar os módulos importados | [Rodar e conferir do exercício 2](../05-ex2/08-rodar-e-conferir.md) |
| **`None`** | o valor que quer dizer "nada" | [Registrar e rotear](../04-ex1/03-registrar-e-rotear.md) |
| **pipeline** | o caminho completo do dado: entrada no fluxo, fila do processador, exportação | [output_pipeline](../05-ex2/03-output-pipeline.md) |
| **plugin** | objeto que se encaixa no programa sem que o programa mude; aqui, um exportador | [O problema do exercício 2](../05-ex2/01-o-problema.md) |
| **polimorfismo** | chamar o mesmo método em objetos de classes diferentes e cada um responder do seu jeito | [Polimorfismo](../02-conceitos/04-polimorfismo.md) |
| **processador** | objeto de uma filha de `DataProcessor`: confere, guarda e devolve um tipo de dado | [O problema do exercício 0](../03-ex0/01-o-problema.md) |
| **`Protocol`** | classe de `typing` que descreve os métodos que um objeto precisa ter, sem exigir herança | [Protocol e duck typing](../05-ex2/02-protocol-e-duck-typing.md) |
| **`raise`** | instrução que lança uma exceção | [Pré-requisitos](./03-pre-requisitos.md) |
| **rank** | número de ordem de chegada de um item no processador, começando em 0 | [A fila](../02-conceitos/05-a-fila.md) |
| **rotear** | escolher para onde vai cada dado | [Registrar e rotear](../04-ex1/03-registrar-e-rotear.md) |
| **`self`** | o próprio objeto, recebido como primeiro parâmetro de cada método | [Pré-requisitos](./03-pre-requisitos.md) |
| **sobrescrever (*override*)** | a filha definir um método com o mesmo nome de um método da mãe, que passa a valer para os objetos dela | [Sobrescrever um método](../02-conceitos/01-sobrescrever-um-metodo.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `data: Any` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`TypeError`** | exceção para valor do tipo errado; também lançada ao instanciar uma classe abstrata | [A classe abstrata](../02-conceitos/02-a-classe-abstrata.md) |
| **união** | `int \| float`: um tipo ou outro | [Any, união e isinstance](../02-conceitos/03-any-uniao-e-isinstance.md) |
