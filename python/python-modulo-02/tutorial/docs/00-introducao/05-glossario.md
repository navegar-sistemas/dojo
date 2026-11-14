---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__init__`** | o método que o Python roda ao criar um objeto; recebe os valores iniciais | [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
| **`__name__`** | variável que vale `"__main__"` quando o arquivo é rodado e o nome do arquivo sem o `.py` quando ele é importado | [O main](../03-ex0/04-o-main.md) |
| **`__str__`** | o método que transforma um objeto em texto, chamado pelo `print` e pelo `{}` das f-strings | [O método `__str__`](../06-ex3/04-o-metodo-str.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **`args`** | atributo de toda exceção com os argumentos passados sem nome na criação | [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
| **`as`** | em `except Tipo as error`, guarda a exceção capturada na variável `error` | [A mensagem do erro](../02-excecoes/04-a-mensagem-do-erro.md) |
| **atributo** | variável guardada dentro de um objeto e lida com ponto, como `self.message` | [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
| **capitalizado** | texto com a primeira letra maiúscula e as outras minúsculas, como `Tomato` | [str.capitalize](../07-ex4/03-capitalize.md) |
| **capturar** | tratar uma exceção num bloco `except`, impedindo que ela trave o programa | [try e except](../02-excecoes/03-try-e-except.md) |
| **classe base, classe filha** | numa herança, a classe de onde se herda (base, mãe) e a que herda (filha) | [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md#os-tipos-formam-uma-árvore); nas classes próprias, em [A família de erros do jardim](../06-ex3/05-heranca.md) |
| **código de saída** | número que um programa devolve ao terminal ao terminar: `0` é sucesso, outro número é erro; `echo $?` mostra o do último programa | [O programa que trava](../02-excecoes/01-o-programa-que-trava.md) |
| **commit (registro)** | um registro dos arquivos marcados no histórico do repositório; é o que o `git push` envia | [Entregar](../08-fechamento/02-entregar.md) |
| **constante** | valor que o programa nunca muda; por costume, com nome em maiúsculas | [Os limites](../04-ex1/03-os-limites.md) |
| **`diff`** | comando que compara dois textos e imprime só as diferenças; nada impresso quer dizer iguais | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O que vamos construir](./01-o-que-vamos-construir.md#o-enunciado) |
| **exceção** | o objeto que descreve um erro, com um tipo e uma mensagem; é lançado e pode ser capturado | [Lendo o traceback](../02-excecoes/02-lendo-o-traceback.md) |
| **exceção embutida (*built-in*)** | tipo de exceção que já vem com o Python, como `ValueError` | [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md) |
| **`except`** | bloco que roda quando o `try` lança uma exceção do tipo indicado | [try e except](../02-excecoes/03-try-e-except.md) |
| **f-string** | texto com `f` na frente, em que `{expressão}` é trocado pelo valor | [Pré-requisitos](./03-pre-requisitos.md) |
| **`finally`** | bloco que roda sempre que o `try` termina, com erro ou sem erro | [finally](../07-ex4/02-finally.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **funções autorizadas** | as únicas funções prontas do Python que cada exercício pode chamar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **herança** | uma classe ser um caso particular de outra e receber os métodos dela | [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md#os-tipos-formam-uma-árvore); nas classes próprias, em [A família de erros do jardim](../06-ex3/05-heranca.md) |
| **importar** | carregar um arquivo `.py` dentro de outro código para usar as funções dele, com `import` | [O main](../03-ex0/04-o-main.md) |
| **lançar** | criar uma exceção e interromper o código com ela; no seu código, com `raise` | [Lendo o traceback](../02-excecoes/02-lendo-o-traceback.md); com `raise`, em [raise](../04-ex1/02-raise.md) |
| **main** | o trecho que o arquivo executa quando é rodado, dentro de `if __name__ == "__main__":` | [O main](../03-ex0/04-o-main.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`pass`** | instrução que não faz nada, usada onde a linguagem exige um corpo | [A menor exceção](../06-ex3/02-a-menor-excecao.md) |
| **PEP 8** | o guia de estilo padrão do Python, que o flake8 confere | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **pip** | o instalador de bibliotecas do Python | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **`raise`** | a palavra que lança uma exceção | [raise](../04-ex1/02-raise.md) |
| **ramo (*branch*)** | linha de histórico de um repositório; o ramo padrão se chama `main` ou `master` | [Entregar](../08-fechamento/02-entregar.md) |
| **recurso** | algo que se abre e precisa ser fechado ou devolvido, como um arquivo | [O problema do exercício 4](../07-ex4/01-o-problema.md) |
| **repositório** | pasta acompanhada pelo git, com o histórico dos arquivos; a entrega do projeto é feita num deles | [Entregar](../08-fechamento/02-entregar.md) |
| **`self`** | dentro de um método, o próprio objeto | [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
| **traceback** | o relatório que o Python imprime quando uma exceção não é capturada | [Lendo o traceback](../02-excecoes/02-lendo-o-traceback.md) |
| **travar (*crash*)** | o programa parar no meio por causa de uma exceção que ninguém capturou | [O programa que trava](../02-excecoes/01-o-programa-que-trava.md) |
| **`try`** | bloco com o código que pode lançar uma exceção | [try e except](../02-excecoes/03-try-e-except.md) |
| **tupla** | sequência de valores separados por vírgula, em geral entre parênteses, como `("25", "abc")`; com um item só, leva uma vírgula no fim: `("25",)` | [Pré-requisitos](./03-pre-requisitos.md); a de um item, em [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
| **type hint** | anotação do tipo de um parâmetro ou do retorno, como `temp_str: str` e `-> int` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **valor padrão** | valor que um parâmetro recebe quando quem chama não passa nada | [A mensagem padrão](../06-ex3/03-a-mensagem-padrao.md) |
