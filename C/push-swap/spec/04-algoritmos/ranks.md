# Ranks

Substituição de cada valor pela posição que ele ocuparia na lista ordenada, de `0` a `n-1`.

```
entrada:  -5   1000000   3
ranks:     0      2      1
```

Pré-requisito de [medium.md](medium.md) e [complex.md](complex.md), executado pelo `main` para
**todas** as estratégias — ver [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md).

## Algoritmo

```
build_ranks(a):
    copia = malloc(n inteiros)
    se copia == NULL: devolve 0
    copia recebe a.data[0..n-1]
    ordena copia com insertion sort
    i = 0
    enquanto i < n:
        a.data[i] = indice de a.data[i] em copia   (busca binária)
        i += 1
    free(copia)
    devolve 1
```

A ordenação auxiliar é insertion sort com dois `while` aninhados. Para n = 500 são até 125 000
comparações em memória — trabalho de CPU, não movimentos push_swap.

A busca binária funciona porque não há duplicatas: cada valor aparece exatamente uma vez na
cópia ordenada, e o índice encontrado é único. Uma busca linear daria o mesmo resultado com
custo total O(n²); a binária cabe no mesmo espaço de código.

## Por que a substituição é segura

Ordenar os ranks é o mesmo problema que ordenar os valores: a função valor → rank é
estritamente crescente, então `valor[i] < valor[j]` se e somente se `rank[i] < rank[j]`. A
sequência de movimentos que ordena os ranks ordena os valores originais, e é essa sequência que
o programa imprime.

O `checker` recebe os **valores originais** como argumento e a receita gerada sobre os ranks.
Funciona porque as operações não olham para os valores: `ra` gira a pilha independentemente do
que há nela.

## Por que converter

**Densidade.** Os ranks ocupam exatamente `0..n-1`, o que permite dividir em faixas uniformes
sem inspecionar a distribuição dos valores. Com os valores originais, `-5`, `3` e `1000000`
cairiam quase todos no mesmo bloco de um particionamento por faixa de valor.

**Número de bits.** O radix precisa de `⌈log₂ n⌉` passadas sobre os ranks — 9 para n = 500 —
contra 32 passadas se operasse sobre `int` arbitrário, e ainda com o complicador do bit de
sinal em valores negativos.

## Contagem de complexidade

A conversão não emite nenhum movimento. A classe declarada de cada estratégia conta apenas
movimentos push_swap, então o insertion sort interno não entra em O(n²) do `--medium` nem do
`--complex`. Esse é o modelo de custo definido pelo enunciado.

## Momento da chamada

No `main`, logo depois de `compute_disorder` e antes do despacho.

Dentro da estratégia não funcionaria: as funções `sort_*` devolvem `void`, não têm como
sinalizar falha de alocação e não têm acesso às pilhas para liberá-las. No `main` a falha cai no
mesmo `fail()` de todos os outros erros, e nenhuma linha foi impressa ainda.

Rodar para as quatro estratégias, inclusive `--simple`, que não precisa de ranks, custa uma
ordenação em memória e nenhum movimento. E não altera o que o `--simple` emite: ele decide por
`stack_min_index` e `stack_is_sorted`, ambos função apenas da ordem relativa, que os ranks
preservam.
