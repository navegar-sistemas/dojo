# Caso base — n ≤ 3

Chamado pelas quatro estratégias quando `a->size <= 3`, antes de qualquer outra coisa.

```
sort_tiny(c):
    se a.size < 2:
        devolve
    se a.size == 2:
        se a.data[0] > a.data[1]:
            op_sa(c)
        devolve
    sort_three(c)
```

## Três elementos

Com `x = data[0]`, `y = data[1]`, `z = data[2]`, existem 6 ordens possíveis e cada uma resolve
em no máximo 2 movimentos:

| Ordem | Condição | Movimentos |
|---|---|---|
| `1 2 3` | `x < y < z` | nenhum |
| `2 1 3` | `x > y`, `y < z`, `x < z` | `sa` |
| `3 1 2` | `x > y`, `x > z`, `y < z` | `ra` |
| `2 3 1` | `x < y`, `y > z`, `x > z` | `rra` |
| `1 3 2` | `x < y`, `y > z`, `x < z` | `sa` `ra` |
| `3 2 1` | `x > y > z` | `sa` `rra` |

```
sort_three(c):
    se x < y e y < z:                      devolve
    se x > y e y < z e x < z:              op_sa
    senão se x > y e y > z:                op_sa; op_rra
    senão se x > y e x > z:                op_ra
    senão se x < y e y > z e x < z:        op_sa; op_ra
    senão:                                 op_rra
```

As condições são avaliadas sobre `data[0..2]` a cada teste, e o ponteiro `data` não muda com as
rotações — as operações mexem no conteúdo do buffer, não realocam.

## Por que 3 e não 5

O limite maior seria melhor em contagem de movimentos, e é o que a maioria das implementações
de push_swap faz. Aqui ele é 3 porque o enunciado publica a saída exata de
`./push_swap --simple 5 4 3 2 1`: 14 movimentos do selection sort completo. Um caso especial em
n = 5 mudaria essa saída e destruiria a única verificação exata disponível para o `--simple`
(ver [../06-aceitacao/casos.md](../06-aceitacao/casos.md)).

## Ganho

Sem o caso base, as estratégias gerais gastam muito em entradas mínimas:

| Entrada | `--simple` sem caso base | `--complex` sem caso base | com `sort_tiny` |
|---|---|---|---|
| `3 2 1` | 8 | 10 | 2 |
| `3 1 2` | 7 | 10 | 1 |
| `2 1` | 5 | 3 | 1 |

## Efeito no `--bench`

`--complex 3 2 1` continua reportando `Complex / O(n log n)` mesmo rodando o caso base. Todo
algoritmo tem caso base; o rótulo descreve a estratégia escolhida, não o ramo executado para o
menor tamanho possível.
