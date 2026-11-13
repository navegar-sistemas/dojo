---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__all__`** | lista, num `__init__.py`, dos nomes que o pacote oferece a quem o importa | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#o-aviso-do-flake8-no-__init__py) |
| **`__init__`** | o construtor: método que roda sozinho quando o objeto é criado | [Pré-requisitos](./03-pre-requisitos.md) |
| **`__init__.py`** | arquivo que transforma uma pasta num pacote; roda quando o pacote é importado | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#pacote) |
| **`__mro__`** | a ordem de busca de métodos de uma classe | [Herança múltipla](../02-conceitos/03-heranca-multipla.md#a-ordem-de-busca) |
| **`__name__`** | variável que vale `"__main__"` no arquivo rodado com `python3` | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#o-experimento) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um módulo; não é entregue | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#o-__pycache__) |
| **ABC** | classe do módulo `abc` da qual uma classe herda para virar abstrata | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **`@abstractmethod`** | decorador que marca um método como obrigatório nas classes filhas | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **atributo** | variável guardada dentro de um objeto, como `self.name` | [Pré-requisitos](./03-pre-requisitos.md) |
| **`AttributeError`** | exceção de quando um objeto não tem o atributo ou método pedido | [Herança múltipla](../02-conceitos/03-heranca-multipla.md) |
| **capacidade (*capability*)** | classe abstrata com uma habilidade extra, separada de `Creature`, herdada junto com ela | [As capacidades](../04-ex1/02-as-capacidades.md) |
| **classe** | o molde de um tipo de objeto | [Pré-requisitos](./03-pre-requisitos.md) |
| **classe abstrata** | classe que só serve de molde: não pode ser instanciada e lista os métodos que as filhas escrevem | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **classe concreta** | classe que escreveu todos os métodos abstratos e pode ser instanciada | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Conferir tudo](../06-fechamento/01-conferir-tudo.md) |
| **decorador** | linha com `@` em cima de um `def` que modifica o método | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **`diff`** | comando que compara dois textos linha a linha e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/09-rodar-e-conferir.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **estratégia (*strategy*)** | objeto que guarda um jeito de fazer uma tarefa; aqui, o jeito de lutar | [O padrão estratégia](../05-ex2/02-o-padrao-estrategia.md) |
| **estreitar o tipo** | o mypy tratar um valor como de um tipo mais específico dentro de um `if isinstance(...)` | [isinstance e o mypy](../02-conceitos/04-isinstance-e-o-mypy.md#isinstance-direto-no-if) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **exceção dedicada** | classe de exceção própria do projeto, filha de `Exception`, como `InvalidStrategyError` | [A exceção dedicada](../05-ex2/03-a-excecao-dedicada.md) |
| **expor** | um pacote oferecer um nome a quem o importa, pelo `__init__.py` | [O `__init__.py` do pacote](../03-ex0/06-o-init-do-pacote.md) |
| **fábrica (*factory*)** | objeto cujo trabalho é criar outros objetos | [O padrão fábrica abstrata](../03-ex0/02-o-padrao-fabrica-abstrata.md) |
| **fábrica abstrata** | classe abstrata que declara o que toda fábrica cria; cada família tem uma fábrica concreta | [O padrão fábrica abstrata](../03-ex0/02-o-padrao-fabrica-abstrata.md) |
| **família** | as duas formas de uma criatura: a base e a evoluída | [O problema do exercício 0](../03-ex0/01-o-problema.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`hasattr`** | função que responde se um objeto tem um atributo com o nome dado | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#o-experimento) |
| **herança** | uma classe filha recebe os métodos e atributos da classe mãe | [Pré-requisitos](./03-pre-requisitos.md) |
| **herança múltipla** | uma classe com mais de uma classe mãe | [Herança múltipla](../02-conceitos/03-heranca-multipla.md) |
| **import relativo** | import com ponto, como `from .creature import Creature`: um módulo do mesmo pacote | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#o-experimento) |
| **`ImportError`** | exceção de um import que não acha o nome pedido | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#um-arquivo-de-pacote-não-é-rodado-sozinho) |
| **instância (objeto)** | valor criado a partir de uma classe, como `FlameFactory()` | [Pré-requisitos](./03-pre-requisitos.md) |
| **`isinstance`** | função que responde se um valor é de uma classe (ou de uma filha dela) | [isinstance e o mypy](../02-conceitos/04-isinstance-e-o-mypy.md) |
| **método** | função que pertence a um objeto e é chamada com ponto | [Pré-requisitos](./03-pre-requisitos.md) |
| **método abstrato** | método marcado com `@abstractmethod`, que toda filha precisa escrever | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md) |
| **mixin** | classe feita para ser herdada junto com outra e acrescentar uma habilidade; as capacidades são mixins | [As capacidades](../04-ex1/02-as-capacidades.md) |
| **módulo** | arquivo `.py` que entra no programa com `import` | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md) |
| **`ModuleNotFoundError`** | exceção de um import que não acha o módulo | [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`MYPYPATH`** | variável que diz ao mypy em que pastas procurar os módulos importados | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#a-classe-abstrata-não-é-instanciada) |
| **ordem de busca (MRO)** | a sequência de classes em que o Python procura um método; `super()` vai para a próxima dela | [Herança múltipla](../02-conceitos/03-heranca-multipla.md#a-ordem-de-busca) |
| **pacote** | pasta com `__init__.py`, importada pelo nome da pasta | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#pacote) |
| **padrão de projeto (*design pattern*)** | solução conhecida, com nome, para um problema que se repete na organização de programas | [O que vamos construir](./01-o-que-vamos-construir.md) |
| **polimorfismo** | o mesmo código, escrito para a classe mãe, funcionar com qualquer filha, cada uma do seu jeito | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#polimorfismo) |
| **`PYTHONPATH`** | variável que acrescenta pastas à lista onde o Python procura módulos | [Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#onde-o-python-procura) |
| **raiz** | a pasta principal do projeto, que contém `ex0/`, `ex1/`, `ex2/` e os programas de teste | [A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md) |
| **`self`** | o próprio objeto, recebido como primeiro parâmetro de cada método | [Pré-requisitos](./03-pre-requisitos.md) |
| **sobrescrever (*override*)** | a filha definir um método com o mesmo nome de um método da mãe, que passa a valer para os objetos dela | [Pré-requisitos](./03-pre-requisitos.md#herança-em-resumo) |
| **`super()`** | acesso aos métodos da próxima classe da ordem de busca; numa herança simples, a mãe | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#super-o-construtor-da-mãe) |
| **todos contra todos** | cada oponente luta uma vez contra cada um dos outros | [A função battle](../05-ex2/05-a-funcao-battle.md#todos-contra-todos) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `name: str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`TypeError`** | exceção para valor do tipo errado; também lançada ao instanciar uma classe abstrata | [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md#a-classe-abstrata-não-é-instanciada) |
