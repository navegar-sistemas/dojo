---
sidebar_position: 3
title: Perguntas de revisão
---

# Perguntas de revisão

Os conceitos por trás do código, em forma de pergunta e resposta. Várias das perguntas vêm do
próprio enunciado, que as deixa ao longo dos exercícios.

## Por que usar `if __name__ == "__main__":`?

Porque um arquivo `.py` pode ser rodado diretamente ou importado por outro arquivo. O Python põe
`"__main__"` na variável `__name__` só do arquivo rodado diretamente; num arquivo importado, ela
vale o nome usado no `import`. O `if` faz a demonstração rodar só no primeiro caso, e o arquivo
pode ser importado para usar as classes dele sem imprimir nada
([O ponto de partida](../02-ex0/03-o-ponto-de-partida.md)). É o que permite importar a `Plant` do
exercício 4 num teste rápido ([Rodar e conferir](../06-ex4/08-rodar-e-conferir.md)) sem rodar a demonstração.

## O que faz a linha shebang?

`#!/usr/bin/env python3`, como primeira linha, diz ao sistema que programa deve ler o arquivo.
Com ela e com a permissão de execução (`chmod +x`), o arquivo roda como um programa comum,
`./ex0/ft_garden_intro.py`, sem digitar `python3`. O `env` procura o `python3` nas pastas de
programas do sistema (o `PATH`), e por isso a linha funciona em máquinas com o Python instalado
em lugares diferentes ([O shebang](../02-ex0/06-o-shebang.md)).

## Como guardar os dados das plantas, e o que muda com mais plantas?

Variáveis soltas (`rose_name`, `rose_height`) multiplicam-se com cada planta e não dizem quais
dados andam juntos. Uma classe descreve uma vez o que toda planta tem e sabe fazer, e cada
planta vira um objeto com os seus valores ([Classe e objeto](../03-ex1/02-classe-e-objeto.md)).
Com mais plantas, os objetos cabem numa lista e são percorridos num laço
([Cinco plantas](../05-ex3/03-cinco-plantas.md)).

## Como a planta muda com o tempo, e como plantas diferentes evoluem de jeitos diferentes?

`grow()` e `age()` são métodos que mudam o estado da planta: a altura e a idade guardadas nela.
Cada planta guarda a sua taxa de crescimento, e `grow()` usa a taxa da própria planta: a rosa
cresce 0,8 cm por chamada, o girassol do exercício 6, 30 cm
([grow e age](../04-ex2/02-grow-e-age.md)). Um tipo de planta também pode mudar o que esses
métodos fazem, sobrescrevendo-os: a hortaliça cresce como qualquer planta e ainda ganha valor
nutricional ([Vegetable](../07-ex5/06-vegetable.md)).

## Para que serve o construtor?

Para que a planta nasça completa: os dados entram na mesma linha que cria o objeto, e não existe
um momento em que a planta está pela metade ([O construtor](../05-ex3/02-o-construtor.md)).

## Como usar o show() sem mudança para imprimir "Created: ..."?

O prefixo é impresso antes, com `print("Created: ", end="")`, que não quebra a linha, e o
`show()` completa a mesma linha ([O prefixo Created](../05-ex3/04-o-prefixo-created.md)).

## Por que a convenção protected, e não o name mangling?

Um `_` na frente do nome (`_height`) avisa que o atributo é interno da classe **e das filhas**, e
as filhas (`Flower`, `Tree`) usam `self._height` normalmente. Dois `_` (`__height`) fazem o
Python trocar o nome por dentro para `_Plant__height`, e então nem as filhas enxergam o atributo
pelo nome escrito ([Encapsulamento](../06-ex4/02-encapsulamento.md)).

## Como proteger os dados?

Escondendo os atributos atrás de métodos. Os getters devolvem os valores; os setters validam
antes de guardar e recusam valores inválidos, com uma mensagem de erro, deixando o valor antigo.
Todo caminho que muda altura ou idade (o construtor, `grow()`, `age()`) passa pelos setters, e a
regra fica escrita num lugar só ([Setters que validam](../06-ex4/04-setters-que-validam.md)).

## Como lidar com as características comuns aos tipos de planta?

Com herança. `Plant` tem o que é comum (nome, altura, idade, validação, crescer, envelhecer,
mostrar), e `Flower`, `Tree` e `Vegetable` herdam tudo isso e só escrevem o que é delas. Com
`super()`, cada filha completa os métodos da classe pai em vez de copiá-los
([Herança](../07-ex5/02-heranca.md) e [super()](../07-ex5/03-super.md)).

## Qual a diferença entre um método estático e um método de classe?

Um método comum recebe o objeto (`self`). Um método **estático** não recebe nada além dos seus
parâmetros: é uma função guardada na classe porque o assunto é dela, como "esta idade passa de
um ano?". Um método **de classe** recebe a classe (`cls`) e serve, tipicamente, para criar
objetos de um jeito especial, como a planta anônima
([O método estático](../08-ex6/02-o-metodo-estatico.md) e
[O método de classe](../08-ex6/03-o-metodo-de-classe.md)).

## Por que uma classe aninhada para as estatísticas?

Porque as estatísticas são um conjunto de dados com comportamento próprio (contar, exibir) que só
existe como parte de uma planta. Dentro de `Plant`, a classe `Stats` fica junto de quem a usa, e
os contadores ficam protegidos dentro dela. A árvore estende as estatísticas por herança, com
`Tree.Stats` ([A classe aninhada](../08-ex6/04-a-classe-aninhada.md) e
[A estatística da árvore](../08-ex6/05-a-estatistica-da-arvore.md)).

## Como uma única função exibe as estatísticas de qualquer planta?

`display_stats` recebe uma `Plant`, e toda filha é uma `Plant`. Ela só pede o objeto de
estatísticas e manda que ele se exiba; cada tipo de estatística sabe se exibir do seu jeito. O
mesmo código com comportamentos diferentes conforme o objeto é o **polimorfismo**
([A função de estatísticas](../08-ex6/07-a-funcao-de-estatisticas.md)).
