---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([O Python](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha com mais de 79 caracteres, falta de linha em branco entre
  funções, `import` que não é usado. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todas as funções.** Um *type hint* é a anotação do tipo de cada parâmetro e do
  retorno, como em `def double(n: int) -> int:`. O enunciado pede type hints em todas as
  assinaturas (a linha do `def`). O tutorial confere isso com o **mypy**, um programa que acusa
  funções sem anotação e tipos que não batem
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **O tratamento de exceções protege os dados.** A frase do enunciado é "o tratamento de
  exceções deve proteger os fluxos de dados contra corrupção" (*Exception handling should protect
  the data streams from corruption*). O tutorial a concretiza assim (escolha do tutorial): uma
  entrada inválida não pode deixar o programa num estado errado nem produzir um resultado sem
  sentido, e a função recusa a entrada com uma **exceção** (o objeto de erro do Python) e uma
  mensagem clara.
- **Padrões funcionais à mostra.** O código deve deixar claro o assunto de cada exercício, sem
  complicação além do necessário.
- **Cada exercício no seu arquivo**, com o nome exato que o enunciado dá.

## O que pode ser importado

Um **módulo** é um arquivo de código que entra no programa com `import`. O enunciado libera:

- o módulo `typing`, para type hints especiais, como `Any` ("qualquer tipo");
- `Callable`, o type hint de "uma função", importado de `collections.abc` (e não de `typing`);
- o módulo `itertools`, de ferramentas para percorrer sequências (os exercícios do tutorial não
  precisam dele);
- `functools` e `operator`, só nos exercícios que os liberam (o 3 libera os dois, o 4 libera
  `functools.wraps`);
- todas as classes e coleções padrão (`int`, `str`, `list`, `dict`...) com os seus métodos, e
  todas as funções embutidas (as que existem sem `import`, como `print` e `len`), **menos
  `eval()` e `exec()`**, duas funções que executam texto como se fosse código;
- outros módulos da biblioteca padrão (os que vêm com o Python) quando o exercício precisa. O
  exercício 4 usa o `time`, para medir tempo, que o próprio enunciado sugere.

## O que é proibido

- **Bibliotecas externas**: nada instalado com `pip install` no código entregue.
- **Ler ou escrever arquivos**: tudo acontece na memória.
- **Algoritmos complexos**: o foco é o padrão funcional, não a esperteza do algoritmo.
- **`eval()` e `exec()`**.
- **Variáveis globais**: uma variável global é a que fica no nível de cima do arquivo, fora de
  qualquer função. O motivo da proibição está em
  [Escopo e closures](../02-conceitos/04-escopo-e-closures.md); na prática, todo o código de
  demonstração de cada exercício fica dentro de uma função `main`.

## As saídas

Cada exercício mostra um exemplo de saída do programa. O enunciado diz que esse é o formato
**sugerido**: a estrutura precisa ser mantida, e as mensagens podem ser adaptadas, desde que a
informação essencial continue lá. O tutorial reproduz cada exemplo exatamente, letra por letra,
para que a comparação com o enunciado seja automática (escolha do tutorial). No exercício 1, o
exemplo é curto e o enunciado pede a demonstração de todas as funções: lá, o exemplo é o começo
da saída, e o resto demonstra as funções que ele não mostra.

## Os cinco exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | `artifact_sorter` ordena artefatos do mais forte para o mais fraco com `sorted`; `power_filter` escolhe os magos com poder mínimo com `filter`; `spell_transformer` enfeita nomes de feitiços com `map`; `mage_stats` calcula o maior, o menor e a média dos poderes com `max`, `min`, `sum` e `round`. Toda transformação com **lambda** ([Exercício 0](../03-ex0/01-o-problema.md)) |
| 1 | `spell_combiner` junta dois feitiços num só; `power_amplifier` cria um feitiço com o poder multiplicado; `conditional_caster` cria um feitiço que só funciona se uma condição for verdadeira; `spell_sequence` cria um feitiço que lança uma lista de feitiços em ordem ([Exercício 1](../04-ex1/01-o-problema.md)) |
| 2 | `mage_counter` cria um contador de chamadas; `spell_accumulator` cria um acumulador de poder; `enchantment_factory` cria funções que encantam itens; `memory_vault` cria um par de funções que guardam e recuperam memórias. Tudo com **closures**, e `nonlocal` liberado ([Exercício 2](../05-ex2/01-o-problema.md)) |
| 3 | `spell_reducer` combina uma lista de poderes com `functools.reduce`; `partial_enchanter` cria três encantamentos pré-preenchidos com `functools.partial`; `memoized_fibonacci` calcula a sequência de Fibonacci com cache, com `functools.lru_cache`; `spell_dispatcher` escolhe o comportamento pelo tipo do argumento com `functools.singledispatch` ([Exercício 3](../06-ex3/01-o-problema.md)) |
| 4 | os decoradores `spell_timer` (mede o tempo), `power_validator` (recusa poder baixo) e `retry_spell` (tenta de novo quando falha), e a classe `MageGuild`, com um `@staticmethod` ([Exercício 4](../07-ex4/01-o-problema.md)) |

A página [O resultado final](./04-o-resultado-final.md) reúne a saída dos cinco programas.

## O gerador de dados

O enunciado vem com um anexo, `generator.tar.gz`, que contém o programa `data_generator.py`: ele
sorteia dados de teste para cada exercício (magos, artefatos, feitiços, poderes). O enunciado
sugere usá-lo para testar o código
([O gerador de dados](../01-ambiente/05-o-gerador-de-dados.md)).

## Entrega

Só os cinco arquivos `.py`, com esses nomes e nessas pastas, num repositório Git
([Entregar](../08-fechamento/02-entregar.md)). Cada exercício do enunciado termina com perguntas
sobre os conceitos que ele usa; as respostas estão em
[Perguntas de revisão](../08-fechamento/03-perguntas-de-revisao.md).

## O que o enunciado cita sem explicar

- **Cidadão de primeira classe** (*first-class citizen*): um valor que pode ser guardado numa
  variável, passado como argumento e devolvido por uma função. No Python, as funções são
  ([Funções são valores](../02-conceitos/01-funcoes-sao-valores.md)).
- **Função anônima**: função sem nome, a lambda ([Lambda](../02-conceitos/02-lambda.md)).
- **Escopo léxico** (*lexical scoping*): a regra de que uma função enxerga as variáveis do lugar
  onde foi **escrita** ([Escopo e closures](../02-conceitos/04-escopo-e-closures.md)).
- **Memoização** (*memoization*): guardar o resultado de uma chamada para não recalcular quando
  a mesma chamada se repete ([memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md)).
- **Aplicação parcial**: criar uma função nova a partir de outra, com alguns argumentos já
  preenchidos ([partial_enchanter](../06-ex3/03-partial-enchanter.md)).
- **Despacho único** (*single dispatch*): escolher qual versão de uma função roda pelo tipo do
  primeiro argumento ([spell_dispatcher](../06-ex3/05-spell-dispatcher.md)).
- **Fibonacci**: a sequência 0, 1, 1, 2, 3, 5, 8..., em que cada número é a soma dos dois
  anteriores.
- **Ano 2142, magos, Sage Lambda, Grandmaster Decorator...**: só o cenário de ficção do projeto.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que só se use código vindo de uma
  ferramenta de IA depois de entendê-lo por completo, conferi-lo e testá-lo.
