---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

Cada exercício termina com perguntas para a avaliação, e o capítulo de entrega avisa que pode ser
pedido que você explique conceitos de programação funcional, demonstre como as closures funcionam
ou mostre como os decoradores transformam funções. A introdução do enunciado também pede que se
entenda **por que** esses padrões são poderosos, e não só **como** escrevê-los. As respostas
abaixo seguem a ordem dos exercícios.

## Exercício 0

### Como as lambdas deixam o código mais conciso?

A regra fica escrita no lugar onde é usada. `sorted(artifacts, key=lambda artifact:
artifact["power"], reverse=True)` diz numa linha o que ordenar, por qual campo e em que sentido;
com `def`, seria uma função de duas linhas com nome, escrita longe da chamada, para ser usada uma
vez só ([Lambda](../02-conceitos/02-lambda.md)).

### Quando usar lambda e quando usar def?

- **lambda:** uma expressão curta, usada uma vez, passada direto para outra função (`key=` de
  `sorted`, `max` e `min`, ou `map` e `filter`);
- **def:** tudo que precisa de nome, de type hints, de mais de uma expressão, de docstring, ou
  que é usado em mais de um lugar. Guardar uma lambda num nome é justamente o caso em que o flake8
  manda usar `def` (aviso `E731`, em [Lambda com nome: use def](../02-conceitos/02-lambda.md#lambda-com-nome-use-def)).

## Exercício 1

### Como as funções de ordem superior permitem reaproveitar e compor código?

Cada uma resolve um problema uma vez, para qualquer feitiço: `power_amplifier` amplifica qualquer
feitiço, existente ou futuro, sem que nenhum seja reescrito. E como todas recebem e devolvem
feitiços com o mesmo contrato, `(target, power) -> resultado`, elas se encaixam umas nas outras:
um feitiço amplificado pode entrar numa sequência, uma sequência pode ser condicional, um
amplificado pode ser amplificado de novo
([Com dados do gerador](../04-ex1/09-rodar-e-conferir.md#com-dados-do-gerador)). Peças pequenas e
combináveis substituem uma coleção de variações escritas à mão.

### O que faz das funções "cidadãs de primeira classe" no Python?

Uma função é um objeto como outro qualquer: pode ser guardada numa variável (`speak = shout`),
numa lista ou num dicionário (`memory_vault` devolve um dicionário de funções), passada como
argumento (`spell_combiner(fireball, heal)`) e devolvida por outra função (todas as funções dos
exercícios 1 e 2). E carrega atributos, como `__name__`
([Funções são valores](../02-conceitos/01-funcoes-sao-valores.md)).

### De qual pacote é recomendado importar Callable?

De `collections.abc`, como o próprio enunciado manda: `from collections.abc import Callable`. O
`Callable` de `typing` é só um apelido antigo, mantido por compatibilidade.

### Para que serve callable()?

Para perguntar, enquanto o programa roda, se um valor pode ser chamado com parênteses: funções,
métodos, classes e objetos com o método especial `__call__` dão `True`. No exercício 1, ele
recusa na hora um argumento que não é função, com um `TypeError` claro, em vez de deixar o erro
para o momento do lançamento ([spell_combiner](../04-ex1/03-spell-combiner.md)). O type hint
`Callable` faz a conferência equivalente antes de rodar, pelo mypy.

## Exercício 2

### Como as closures permitem que uma função "lembre" o ambiente onde foi criada?

Quando uma função de dentro usa uma variável da função de fora, o Python guarda essa variável
numa **célula**, presa à função de dentro (`__closure__`). A função de fora termina, mas a célula
continua viva enquanto a função de dentro existir. Cada chamada da função de fora cria células
novas: por isso `counter_a` e `counter_b` contam separado
([Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal)). Para mostrar na avaliação:
`counter.__code__.co_freevars` lista os nomes lembrados, e
`counter.__closure__[0].cell_contents` mostra o valor atual
([Estado independente e privado](../05-ex2/08-rodar-e-conferir.md#estado-independente-e-privado)).

### Quais são os benefícios do escopo léxico na programação funcional?

- **previsível:** o que uma função enxerga depende só de onde ela foi escrita, e dá para saber
  lendo o código, sem rodar;
- **estado privado:** a variável de uma closure só é alcançada pelas funções criadas junto com
  ela, como a memória de `memory_vault`;
- **funções configuráveis:** uma fábrica cria funções especializadas que levam a configuração
  junto (`enchantment_factory("Flaming")`), sem classes e sem variáveis globais.

### Por que global é proibido e nonlocal é permitido? Quais as diferenças?

`global` faz a função mudar uma variável do nível de cima do arquivo: existe uma só para o
programa inteiro, qualquer linha pode mudá-la, e o resultado de uma função passa a depender de
algo fora dela. `nonlocal` faz a função mudar uma variável da função envolvente: existe uma por
chamada da função de fora, e só as funções criadas naquela chamada a alcançam. Com `global`, dois
contadores dividiriam a mesma contagem; com `nonlocal`, cada um tem a sua
([global e nonlocal](../02-conceitos/04-escopo-e-closures.md#global-e-nonlocal)).

## Exercício 3

### Como functools.reduce permite agregações poderosas?

`reduce` transforma qualquer operação de **dois** valores numa operação sobre uma lista
**inteira**: soma, produto, maior e menor são o mesmo `reduce` com funções diferentes, e
qualquer outra função de dois argumentos (juntar dicionários, achar o mago mais forte) vira uma
agregação sem escrever um laço ([spell_reducer](../06-ex3/02-spell-reducer.md)).

### Quais são os ganhos de desempenho da memoização com lru_cache?

Cada resultado é calculado uma única vez; as repetições custam só uma consulta ao cache. No
Fibonacci recursivo, isso troca um número de chamadas que explode (21891 para `Fib(20)`) por um
cálculo por valor (21 para `Fib(20)`), e chamadas repetidas não calculam nada
([memoized_fibonacci](../06-ex3/04-memoized-fibonacci.md)). O custo é a memória do cache, que o
`maxsize` pode limitar.

## Exercício 4

### Como os decoradores permitem a separação de responsabilidades?

O código de cada função cuida só do trabalho dela; os comportamentos que valem para muitas
funções (medir tempo, validar poder, tentar de novo) ficam cada um num decorador, escrito uma vez
e aplicado com uma linha `@`. `cast_spell` só monta a mensagem de sucesso; a recusa por poder
baixo é do `power_validator` ([MageGuild](../07-ex4/05-mage-guild.md)). Trocar a regra de
validação muda um lugar só, e tirar o comportamento é apagar uma linha.

### Qual a diferença entre @staticmethod e um método de instância comum?

Um método de instância recebe o objeto como primeiro argumento (`self`) e pode usar os atributos
dele. Um `@staticmethod` não recebe `self` nem a classe: é uma função comum guardada dentro da
classe, chamada pela classe ou por um objeto, para uma regra que pertence ao assunto da classe mas
não depende de nenhum objeto, como validar um nome
([MageGuild](../07-ex4/05-mage-guild.md#validate_mage_name-o-método-estático)).

## Mostrar como um decorador transforma uma função

O experimento de [Decoradores](../02-conceitos/06-decoradores.md) mostra os dois lados:
`subtract = announce(subtract)` faz à mão o que a linha `@announce` faz, e o `__name__` da função
decorada mostra o embrulho (`wrapper`) sem o `@wraps`, e o nome original com ele.
