---
sidebar_position: 5
title: Glossário
---

# Glossário

## As coleções

| Termo | Significado |
|---|---|
| **coleção** | um valor que guarda vários outros dentro dele. [Veja](../02-colecoes/01-o-que-e-uma-colecao.md) |
| **elemento** | cada valor guardado numa coleção. [Veja](../02-colecoes/01-o-que-e-uma-colecao.md) |
| **iterável** | o que pode ser percorrido com `for`: listas, tuplas, sets, dicionários, textos, generators. [Veja](../02-colecoes/01-o-que-e-uma-colecao.md) |
| **lista** (`list`) | coleção entre colchetes, em ordem, com acesso pela posição, que aceita repetidos e pode mudar. [Veja](../02-colecoes/02-as-quatro-colecoes.md) |
| **tupla** (`tuple`) | coleção entre parênteses, em ordem, com acesso pela posição, que não muda depois de criada. [Veja](../05-ex2/02-tuplas.md) |
| **set** | coleção entre chaves de valores únicos, sem ordem; o vazio é `set()`. [Veja](../06-ex3/02-sets.md) |
| **dicionário** (`dict`) | coleção de pares `chave: valor`, com acesso pela chave, na ordem em que as chaves entraram. [Veja](../07-ex4/02-dicionarios.md) |
| **chave** e **valor** | as duas partes de cada par de um dicionário: a chave é única e dá acesso ao valor. [Veja](../07-ex4/02-dicionarios.md) |
| **mutável** | que pode mudar depois de criado: lista, set e dicionário. [Veja](../02-colecoes/02-as-quatro-colecoes.md) |
| **imutável** | que nunca muda: tupla, `int`, `float` e `str`. [Veja](../02-colecoes/02-as-quatro-colecoes.md) |
| **hash** | número inteiro calculado a partir do conteúdo de um valor, que o set e o dicionário usam para achá-lo direto. [Veja](../02-colecoes/03-a-estrutura-e-o-algoritmo.md) |
| **hashable** | valor que tem hash e por isso pode ser elemento de set ou chave de dicionário: `int`, `float`, `str` e tuplas só com elementos hashable. [Veja](../02-colecoes/03-a-estrutura-e-o-algoritmo.md) |
| **tempo linear** | tempo que cresce na mesma proporção do tamanho da coleção (o dobro de elementos, o dobro do tempo), como o de procurar um valor numa lista. [Veja](../02-colecoes/03-a-estrutura-e-o-algoritmo.md) |
| **índice** | a posição de um elemento numa lista ou tupla, contando de 0; negativo conta do fim. [Veja](../03-ex0/03-indices-e-fatias.md) |
| **fatia** (*slice*) | lista nova com um pedaço de outra: `lista[a:b]` vai do índice `a` até antes do `b`. [Veja](../03-ex0/03-indices-e-fatias.md) |
| **desempacotamento** (*unpacking*) | dar um nome a cada elemento de uma tupla de uma vez: `x, y, z = position`. [Veja](../05-ex2/02-tuplas.md) |
| **união**, **interseção**, **diferença** | o que está em um ou outro set, o que está nos dois, o que está no primeiro e não no segundo. [Veja](../06-ex3/03-uniao-intersecao-diferenca.md) |
| **visão** (*view*) | o que `keys()` e `values()` devolvem: um objeto que percorre as chaves ou os valores do dicionário, sem ser uma lista. [Veja](../07-ex4/02-dicionarios.md) |
| **generator** | objeto que produz valores um de cada vez, criado por uma função com `yield`. [Veja](../08-ex5/02-generators.md) |
| **`yield`** | entrega um valor e pausa a função geradora até o próximo pedido. [Veja](../08-ex5/02-generators.md) |
| **`next()`** | pede o próximo valor a um generator. [Veja](../08-ex5/02-generators.md) |
| **`StopIteration`** | o sinal de que um generator acabou; o `for` o trata sozinho. [Veja](../08-ex5/02-generators.md) |
| **comprehension** | uma lista, dicionário ou set construído numa linha a partir de outra coleção: `[n * n for n in numbers]`. [Veja](../09-ex6/02-list-comprehension.md) |

## O Python

| Termo | Significado |
|---|---|
| **módulo** | código que vem com o Python e reúne funções de um assunto, carregado com `import`: `sys`, `math`, `random`, `typing`. [Veja](./02-o-enunciado-em-linguagem-simples.md#o-que-pode-ser-usado) |
| **método** | função que pertence a um tipo e é chamada com ponto: `scores.append(1500)`. [Veja](./02-o-enunciado-em-linguagem-simples.md#o-que-pode-ser-usado) |
| **construtor** | a chamada pelo nome do tipo que cria um valor dele: `int("42")`, `set()`. [Veja](./02-o-enunciado-em-linguagem-simples.md#o-que-pode-ser-usado) |
| **linha de comando** | o texto digitado no terminal para rodar um programa. [Veja](../03-ex0/02-a-linha-de-comando.md) |
| **shell** | o programa que roda dentro do terminal, lê cada comando, corta os argumentos e inicia os programas (no Linux, normalmente o `bash`). [Veja](../03-ex0/02-a-linha-de-comando.md) |
| **UTF-8** e **locale** | UTF-8 é a forma padrão de escrever texto em bytes; o locale é a configuração de idioma do sistema, que, junto com a versão do Python, decide o que o `print` faz com bytes inválidos. [Veja](../03-ex0/05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido) |
| **traceback** | o relatório de erro que o Python imprime quando um erro não é capturado e o programa trava. [Veja](../03-ex0/05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido) |
| **pipe** (`\|`) | a barra vertical que liga a saída de um comando à entrada do seguinte. [Veja](../05-ex2/07-rodar-e-conferir.md#rodar-com-as-respostas-prontas) |
| **argumento** | cada pedaço da linha de comando depois do nome do programa. [Veja](../03-ex0/02-a-linha-de-comando.md) |
| **`sys.argv`** | a lista com o nome do programa e os argumentos, todos como texto. [Veja](../03-ex0/02-a-linha-de-comando.md) |
| **main** | a função que faz o trabalho do programa, chamada pelo bloco `if __name__ == "__main__":`. [Veja](../03-ex0/05-o-arquivo-completo.md#o-main) |
| **constante** | variável criada fora das funções, com nome em maiúsculas, que por costume nunca muda. [Veja](../04-ex1/03-converter-e-descartar.md#um-limite-para-as-pontuações) |
| **regra dos tipos** | a regra do enunciado que libera `str`, `int` e `float`, com todos os seus métodos e construtores, em qualquer exercício. [Veja](./02-o-enunciado-em-linguagem-simples.md#o-que-pode-ser-usado) |
| **apelido de tipo** (*type alias*) | um nome para um tipo comprido: `Event = tuple[str, str]`. [Veja](../08-ex5/03-o-gerador-sem-fim.md) |
| **`EOFError`** | o erro do `input()` quando a entrada acabou, por Ctrl-D ou porque o texto preparado terminou. [Veja](../05-ex2/06-o-arquivo-completo.md#quando-o-usuário-desiste) |
| **`KeyboardInterrupt`** | o erro lançado quando o usuário aperta Ctrl-C. [Veja](../05-ex2/06-o-arquivo-completo.md#quando-o-usuário-desiste) |
| **`OverflowError`** | o erro de estouro: um resultado grande demais para caber num `float`, maior que cerca de 1.8 × 10³⁰⁸. [Veja](../04-ex1/03-converter-e-descartar.md#um-limite-para-as-pontuações) |
| **`inf`** e **`nan`** | valores especiais do `float`: o infinito e o "não é um número", resultado de uma conta indefinida. [Veja](../05-ex2/03-ler-do-teclado.md#float-converter) |
| **notação científica** | a escrita `1e200` para 1 × 10²⁰⁰, que o `float()` aceita. [Veja](../05-ex2/03-ler-do-teclado.md#float-converter) |
| **código de saída** | o número que um programa devolve ao shell ao terminar: 0 é sucesso; um programa que trava devolve outro número. [Veja](../03-ex0/06-rodar-e-conferir.md#um-argumento-que-não-é-utf-8) |

## As ferramentas

| Termo | Significado |
|---|---|
| **type hint** | a anotação do tipo de um parâmetro, variável ou retorno: `def double(number: int) -> int:`. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **docstring** | texto entre três aspas na primeira linha de uma função, que diz o que ela faz. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md#docstrings) |
| **flake8** | programa que confere o estilo do código. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **mypy** | programa que confere os type hints. [Veja](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **ambiente virtual** (venv) | pasta com um Python próprio do projeto e as bibliotecas dele. [Veja](../01-ambiente/03-o-ambiente-virtual.md) |
| **`diff`** | comando que compara dois textos e imprime só as diferenças. [Veja](../03-ex0/06-rodar-e-conferir.md) |

## As contas

| Termo | Significado |
|---|---|
| **média** | a soma dividida pela quantidade; com `/`, é sempre um `float`. [Veja](../04-ex1/04-as-estatisticas.md) |
| **amplitude** (*range*) | o maior valor menos o menor. [Veja](../04-ex1/04-as-estatisticas.md) |
| **distância euclidiana** | o comprimento da linha reta entre dois pontos, pelo teorema de Pitágoras. [Veja](../05-ex2/05-a-distancia.md) |
