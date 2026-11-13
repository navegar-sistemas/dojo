---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`*args`** | parâmetro que recolhe os argumentos posicionais numa tupla; na chamada, `*` espalha uma tupla em argumentos | [\*args e \*\*kwargs](../02-conceitos/05-args-e-kwargs.md) |
| **`**kwargs`** | parâmetro que recolhe os argumentos nomeados num dicionário; na chamada, `**` espalha um dicionário | [\*args e \*\*kwargs](../02-conceitos/05-args-e-kwargs.md) |
| **`__closure__`** | atributo de uma função com as células das variáveis livres dela | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal) |
| **`__name__`** (de uma função) | o nome com que a função foi criada no `def` | [Funções são valores](../02-conceitos/01-funcoes-sao-valores.md) |
| **`__name__`** (do arquivo) | variável que vale `"__main__"` no arquivo rodado com `python3` | [A demonstração do exercício 0](../03-ex0/05-a-demonstracao.md) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um arquivo; não é entregue | [Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md#as-outras-duas-funções) |
| **`all`** | função embutida que responde se todos os valores são verdadeiros | [spell_sequence](../04-ex1/06-spell-sequence.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **aplicação parcial** | criar uma função nova a partir de outra, com alguns argumentos já preenchidos | [partial_enchanter](../06-ex3/03-partial-enchanter.md) |
| **argumento nomeado** | argumento passado com o nome do parâmetro, como `power=10` | [\*args e \*\*kwargs](../02-conceitos/05-args-e-kwargs.md) |
| **argumento posicional** | argumento que vai para o parâmetro da mesma posição | [\*args e \*\*kwargs](../02-conceitos/05-args-e-kwargs.md) |
| **assinatura** | a linha do `def`: nome, parâmetros com tipos e tipo do retorno | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **cache** | memória de resultados já calculados | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md) |
| **`cache_info()`** | método que o `lru_cache` acrescenta: mostra acertos, faltas e tamanho do cache | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md) |
| **`Callable`** | type hint de "algo que pode ser chamado", importado de `collections.abc` | [Funções são valores](../02-conceitos/01-funcoes-sao-valores.md#o-type-hint-callable) |
| **`callable()`** | função embutida que responde se um valor pode ser chamado com parênteses | [Funções são valores](../02-conceitos/01-funcoes-sao-valores.md#callable) |
| **célula** | onde a closure guarda cada variável livre; `cell_contents` é o valor atual | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal) |
| **cidadão de primeira classe** | valor que pode ser guardado, passado e devolvido; as funções do Python são | [Funções são valores](../02-conceitos/01-funcoes-sao-valores.md) |
| **closure** | função mais as variáveis do escopo envolvente que ela usa, que sobrevivem depois que a função de fora termina | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Conferir tudo](../08-fechamento/01-conferir-tudo.md) |
| **composição** | encaixar funções umas nas outras, porque seguem o mesmo contrato | [power_amplifier](../04-ex1/04-power-amplifier.md) |
| **compreensão de lista** | `[expressão for item in lista]`: monta uma lista nova numa linha | [Pré-requisitos](./03-pre-requisitos.md#compreensão-de-lista) |
| **decorador** | função que recebe uma função e devolve outra, que faz algo a mais e chama a original; aplicado com `@` | [Decoradores](../02-conceitos/06-decoradores.md) |
| **despacho único (*single dispatch*)** | escolher qual versão de uma função roda pelo tipo do primeiro argumento | [spell_dispatcher](../06-ex3/05-spell-dispatcher.md) |
| **`diff`** | comando que compara duas listas de linhas e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md) |
| **docstring** | texto entre aspas triplas logo abaixo do `def`, guardado em `__doc__` | [Decoradores](../02-conceitos/06-decoradores.md#o-nome-perdido) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **escopo** | a parte do código em que um nome existe; procurado na ordem LEGB | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md) |
| **escopo léxico** | regra de que uma função enxerga as variáveis do lugar onde foi escrita | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **expressão geradora** | uma compreensão sem colchetes, que entrega os valores um a um, como dentro de `all(...)` | [spell_sequence](../04-ex1/06-spell-sequence.md) |
| **expressão regular** | padrão de texto, como `[0-9]{3}` (três algarismos), usado pelo `grep -E` | [Rodar e conferir do exercício 4](../07-ex4/08-rodar-e-conferir.md#a-linha-do-tempo) |
| **fábrica de decoradores** | função que recebe um parâmetro e devolve um decorador, como `power_validator(10)` | [Decoradores com parâmetros](../02-conceitos/07-decoradores-com-parametros.md) |
| **fábrica de funções** | função que monta e devolve uma função nova | [Funções que devolvem funções](../02-conceitos/03-funcoes-que-devolvem-funcoes.md) |
| **Fibonacci** | a sequência 0, 1, 1, 2, 3, 5, 8..., cada número é a soma dos dois anteriores | [O problema do exercício 3](../06-ex3/01-o-problema.md) |
| **`filter`** | função embutida que fica com os itens em que a função dá verdadeiro | [Lambda](../02-conceitos/02-lambda.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **função de ordem superior** | função que recebe ou devolve outra função | [Funções são valores](../02-conceitos/01-funcoes-sao-valores.md) |
| **`functools`** | módulo da biblioteca padrão com ferramentas para funções: `reduce`, `partial`, `lru_cache`, `singledispatch`, `wraps` | [O problema do exercício 3](../06-ex3/01-o-problema.md) |
| **gerador de dados** | o `data_generator.py`, anexo do enunciado que sorteia dados de teste | [O gerador de dados](../01-ambiente/05-o-gerador-de-dados.md) |
| **`global`** | instrução que faz uma função atribuir a uma variável do nível de cima do arquivo | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#global-e-nonlocal) |
| **iterador** | objeto que entrega itens um por um, uma vez só, como o que `map` e `filter` devolvem | [Lambda](../02-conceitos/02-lambda.md#o-que-aconteceu) |
| **lambda** | função sem nome, de uma expressão só, escrita no lugar onde é usada | [Lambda](../02-conceitos/02-lambda.md) |
| **LEGB** | a ordem em que o Python procura um nome: local, envolvente, global, embutido | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md) |
| **`lru_cache`** | decorador do `functools` que guarda os resultados de uma função | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md) |
| **`map`** | função embutida que aplica uma função a cada item | [Lambda](../02-conceitos/02-lambda.md) |
| **memoização** | guardar o resultado de uma chamada para não recalcular quando ela se repete | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md) |
| **método estático** | método marcado com `@staticmethod`, que não recebe `self` | [MageGuild](../07-ex4/05-mage-guild.md) |
| **módulo** | arquivo de código que entra no programa com `import` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **mypy** | ferramenta que confere os type hints do código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`nonlocal`** | instrução que faz as atribuições de uma função mudarem a variável da função envolvente | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal) |
| **`operator`** | módulo com os operadores em forma de função, como `operator.add` e `operator.mul` | [spell_reducer](../06-ex3/02-spell-reducer.md) |
| **`partial`** | ferramenta do `functools` que cria uma função com argumentos pré-preenchidos | [partial_enchanter](../06-ex3/03-partial-enchanter.md) |
| **`perf_counter`** | função do módulo `time` que dá um instante para medir intervalos | [spell_timer](../07-ex4/02-spell-timer.md) |
| **`PYTHONPATH`** | variável que diz ao Python em que pasta procurar os módulos importados | [Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md#as-outras-duas-funções) |
| **`RecursionError`** | exceção lançada quando as chamadas recursivas passam do limite da pilha | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md#o-limite-da-recursão) |
| **recursiva** | função que chama a si mesma | [memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md) |
| **`reduce`** | ferramenta do `functools` que combina uma lista inteira com uma função de dois argumentos | [spell_reducer](../06-ex3/02-spell-reducer.md) |
| **`singledispatch`** | decorador do `functools` que escolhe a versão da função pelo tipo do argumento | [spell_dispatcher](../06-ex3/05-spell-dispatcher.md) |
| **`sorted`** | função embutida que devolve uma lista nova, ordenada; a ordenação é estável | [Lambda](../02-conceitos/02-lambda.md) |
| **`@staticmethod`** | decorador que faz um método não receber `self` | [MageGuild](../07-ex4/05-mage-guild.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md#exceções-em-resumo) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `power: int` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`UnboundLocalError`** | exceção de ler uma variável local antes de ela receber valor | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#um-contador-que-não-funciona) |
| **variável global** | variável do nível de cima do arquivo, fora de qualquer função; proibida no projeto | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md) |
| **variável livre** | nome que uma função usa e que pertence a um escopo envolvente | [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal) |
| **`wraps`** | decorador do `functools` que copia nome e docstring da função original para o embrulho | [Decoradores](../02-conceitos/06-decoradores.md#functoolswraps) |
| **`zip`** | função embutida que anda em duas listas ao mesmo tempo, em pares, e para na mais curta | [Rodar e conferir do exercício 1](../04-ex1/09-rodar-e-conferir.md#com-dados-do-gerador) |
