---
sidebar_position: 5
title: Glossário
---

# Glossário

## O programa

| Termo | Significado |
|---|---|
| **script** | um arquivo `.py` rodado diretamente com `python3 arquivo.py`. [Veja](../02-ex0/03-o-ponto-de-partida.md) |
| **módulo** | um arquivo `.py` cujo código outro arquivo pode usar. [Veja](../02-ex0/03-o-ponto-de-partida.md) |
| **import** | o comando que carrega um módulo para usar o código dele em outro arquivo. [Veja](../02-ex0/03-o-ponto-de-partida.md) |
| **`__name__`** | variável que o Python cria em todo arquivo: vale `"__main__"` no arquivo rodado diretamente e, num arquivo importado, o nome usado no `import`. [Veja](../02-ex0/03-o-ponto-de-partida.md) |
| **bloco main** | o código dentro de `if __name__ == "__main__":`, que só roda quando o arquivo é o script principal. [Veja](../02-ex0/03-o-ponto-de-partida.md) |
| **shebang** | a primeira linha `#!/usr/bin/env python3`, que diz ao sistema qual programa roda o arquivo, permitindo `./arquivo.py`. [Veja](../02-ex0/06-o-shebang.md) |
| **permissão de execução** | a marca, dada com `chmod +x`, que deixa o sistema rodar um arquivo como programa. [Veja](../02-ex0/06-o-shebang.md) |
| **type hint** | a anotação do tipo de uma variável, de um parâmetro ou do retorno: `height: int`, `-> None`. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`float`** | o tipo dos números com casas decimais (`25.0`, `0.8`); guarda a maioria dos decimais só de forma aproximada. [Veja](../04-ex2/03-o-float-e-o-round.md) |

## Classes e objetos

| Termo | Significado |
|---|---|
| **classe** | um molde que descreve que dados e que ações todas as coisas de um tipo têm; `Plant` é a classe das plantas. [Veja](../03-ex1/02-classe-e-objeto.md) |
| **objeto (instância)** | uma coisa criada a partir de uma classe, com os seus próprios valores; a rosa é uma instância de `Plant`. [Veja](../03-ex1/02-classe-e-objeto.md) |
| **instanciar** | criar um objeto chamando a classe como uma função: `Plant()`. [Veja](../03-ex1/02-classe-e-objeto.md) |
| **atributo** | uma variável que pertence a um objeto, acessada com ponto: `rose.name`. [Veja](../03-ex1/03-os-atributos.md) |
| **método** | uma função que pertence a uma classe e age sobre um objeto: `rose.show()`. [Veja](../03-ex1/04-o-metodo-show.md) |
| **`self`** | o primeiro parâmetro de todo método comum: o objeto sobre o qual o método foi chamado. [Veja](../03-ex1/04-o-metodo-show.md) |
| **estado** | os valores dos atributos de um objeto num dado momento; métodos como `grow()` mudam o estado. [Veja](../04-ex2/02-grow-e-age.md) |
| **construtor (`__init__`)** | o método que o Python chama sozinho ao criar o objeto, para já preenchê-lo com os seus dados. [Veja](../05-ex3/02-o-construtor.md) |

## Proteger os dados

| Termo | Significado |
|---|---|
| **encapsulamento** | esconder os dados de um objeto e só deixar mexer neles por métodos que a classe controla. [Veja](../06-ex4/02-encapsulamento.md) |
| **convenção protected** | começar o nome de um atributo com um `_` (`_height`) para avisar que ele é interno da classe e das classes filhas. [Veja](../06-ex4/02-encapsulamento.md) |
| **name mangling** | o que o Python faz com atributos que começam com `__`: troca o nome por dentro, para dificultar o acesso de fora; o projeto não o usa, porque o enunciado pede a convenção protected no lugar dele. [Veja](../06-ex4/02-encapsulamento.md) |
| **getter** | método que devolve o valor de um atributo protegido: `get_height()`. [Veja](../06-ex4/03-getters.md) |
| **setter** | método que muda o valor de um atributo protegido, depois de conferir se o valor serve: `set_height()`. [Veja](../06-ex4/04-setters-que-validam.md) |
| **validação** | a conferência de que um valor serve antes de guardá-lo. [Veja](../06-ex4/04-setters-que-validam.md) |

## Herança

| Termo | Significado |
|---|---|
| **herança** | criar uma classe a partir de outra, recebendo tudo o que ela tem: `class Flower(Plant):`. [Veja](../07-ex5/02-heranca.md) |
| **classe pai (base)** | a classe de onde outra herda; `Plant` é a classe pai de `Flower`. [Veja](../07-ex5/02-heranca.md) |
| **classe filha** | a classe que herda; `Flower` é filha de `Plant`. [Veja](../07-ex5/02-heranca.md) |
| **sobrescrever (override)** | escrever na classe filha um método com o mesmo nome de um método da classe pai, que passa a valer no lugar dele. [Veja](../07-ex5/02-heranca.md) |
| **`super()`** | dá acesso, de dentro da classe filha, aos métodos da classe pai: `super().show()`. [Veja](../07-ex5/03-super.md) |
| **cadeia de herança** | uma classe que herda de outra que herda de uma terceira: `Seed` → `Flower` → `Plant`. [Veja](../08-ex6/06-seed.md) |
| **polimorfismo** | o mesmo código chamando um método que cada tipo de objeto implementa do seu jeito: `display_stats` funciona com qualquer planta. [Veja](../08-ex6/07-a-funcao-de-estatisticas.md) |

## Métodos especiais e classes aninhadas

| Termo | Significado |
|---|---|
| **decorador** | uma linha `@nome` logo antes de um `def`: passa a função definida para `nome` e guarda o resultado no lugar dela; `@staticmethod` transforma o método em método estático. [Veja](../08-ex6/02-o-metodo-estatico.md) |
| **método estático** | método que não recebe o objeto nem a classe; é uma função comum guardada dentro da classe. [Veja](../08-ex6/02-o-metodo-estatico.md) |
| **método de classe** | método que recebe a classe (`cls`) em vez do objeto; serve para criar objetos de um jeito especial. [Veja](../08-ex6/03-o-metodo-de-classe.md) |
| **classe aninhada** | uma classe escrita dentro de outra: `Plant.Stats`. [Veja](../08-ex6/04-a-classe-aninhada.md) |

## As ferramentas

| Termo | Significado |
|---|---|
| **terminal** | a janela onde se digitam comandos. [Veja](./03-pre-requisitos.md) |
| **ambiente virtual (venv)** | uma pasta que aponta para o Python instalado e guarda as bibliotecas do projeto, como as ferramentas de conferência. [Veja](../01-ambiente/03-o-ambiente-virtual.md) |
| **flake8** | o programa que confere o estilo do código. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **mypy** | o programa que confere os type hints. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`diff`** | o comando que compara dois textos e imprime só as diferenças. [Veja](../02-ex0/05-rodar-e-conferir.md) |
| **código de saída** | o número que um programa devolve ao sistema ao terminar: `0` quando termina bem, outro número quando para com erro. [Veja](../09-fechamento/01-conferir-tudo.md) |
