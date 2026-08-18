# `--simple` — O(n²)

Selection sort por extração de mínimo. Opera sobre a pilha como o `main` a entrega — já
convertida em [ranks](ranks.md) —, o que não muda nada: as decisões dependem só da ordem
relativa.

```
sort_simple(c, conf):
    conf.name = "Simple"
    conf.cclass = "O(n²)"
    se a.size <= 3:
        sort_tiny(c); devolve
    se stack_is_sorted(a):
        devolve

    enquanto a.size > 0:
        i = stack_min_index(a)
        rotate_a_to_top(c, i)
        op_pb(c)

    enquanto b.size > 0:
        op_pa(c)
```

`rotate_a_to_top(c, i)` leva ao topo o elemento do índice `i` pelo caminho mais curto:

```
rotate_a_to_top(c, i):
    size = a.size
    se i <= size / 2:
        repete op_ra(c) i vezes
    senão:
        repete op_rra(c) (size - i) vezes
```

## O critério de desempate é observável

`i <= size / 2` com divisão inteira: no empate, escolhe `ra`. Isso não é detalhe estético — é o
que reproduz exatamente a saída fixada no caso A1.

Rodando `--simple 5 4 3 2 1`:

| Rodada | `a` | mínimo em `i` | `size` | Escolha | Movimentos |
|---|---|---|---|---|---|
| 1 | `5 4 3 2 1` | 4 | 5 | `4 > 5/2 = 2` → `rra` × 1 | `rra` `pb` |
| 2 | `5 4 3 2` | 3 | 4 | `3 > 2` → `rra` × 1 | `rra` `pb` |
| 3 | `5 4 3` | 2 | 3 | `2 > 1` → `rra` × 1 | `rra` `pb` |
| 4 | `5 4` | 1 | 2 | `1 <= 1` → `ra` × 1 | `ra` `pb` |
| 5 | `5` | 0 | 1 | `0 <= 0` → nada | `pb` |
| — | devolução | | | | `pa` × 5 |

Resultado: `rra pb rra pb rra pb ra pb pb pa pa pa pa pa`, 14 movimentos, idêntico ao caso A1.
A rodada 4 é a que discrimina: com `i < size / 2` em vez de `i <= size / 2`, sairia `rra` no
lugar de `ra`.

## Por que funciona

O que sai de `a` é sempre o menor restante, então `b` recebe os valores em ordem crescente de
baixo para cima — ou seja, decrescente vista do topo. A devolução com `pa` inverte de novo, e
`a` termina crescente.

## Custo

Cada uma das n rodadas faz uma busca O(n) em CPU e até `size / 2` rotações. O somatório das
rotações é O(n²) movimentos.

## Contagens medidas

Faixas observadas em 20 a 40 permutações aleatórias por tamanho:

| n | faixa |
|---|---|
| 100 | ~1270 – 1730 |
| 500 | ~30 300 – 34 300 |

Em n = 500 isso está muito acima do limite de 12 000 — o `--simple` só é viável no regime para
o qual o `--adaptive` o reserva.

## O regime em que ganha

Entradas quase ordenadas, onde o mínimo restante já está perto do topo e quase não há rotação.
Medido em 8 entradas com desordem entre 0.01 e 0.13:

| n | desordem | `--simple` | `--complex` na mesma entrada |
|---|---|---|---|
| 100 | 0.036 – 0.131 | 294 – 470 | 1084 |
| 500 | 0.011 – 0.071 | 1634 – 4225 | 6784 |

É esse cruzamento que o [adaptive.md](adaptive.md) explora: abaixo de 0.2 o quadrático é 2 a 4
vezes mais barato que o radix.
