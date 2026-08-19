# `--medium` — O(n√n)

Ordenação por blocos (chunk sort) sobre [ranks](ranks.md), que o `main` já converteu antes de
chamar a estratégia.

```
sort_medium(c, conf):
    conf.name = "Medium"
    conf.cclass = "O(n√n)"
    se a.size <= 3:
        sort_tiny(c); devolve
    se stack_is_sorted(a):
        devolve

    n     = a.size
    k     = isqrt(n / 2)
    se k < 2: k = 2
    width = (n + k - 1) / k

    collect_all(c, n, k, width)
    drain_b(c)
```

As duas fases ficam em funções `static` próprias — `sort_medium` com os laços embutidos passaria
de 25 linhas:

```
collect_all(c, n, k, width):
    bloco = 0
    enquanto bloco < k:
        lo = bloco * width
        hi = lo + width - 1
        se hi > n - 1: hi = n - 1
        collect_chunk(c, lo, hi)
        bloco += 1

collect_chunk(c, lo, hi):
    rest = count_in_range(a, lo, hi)
    enquanto rest > 0:
        se lo <= a.data[0] e a.data[0] <= hi:
            op_pb(c)
            rest -= 1
        senão:
            op_ra(c)

drain_b(c):
    enquanto b.size > 0:
        i = stack_max_index(b)
        rotate_b_to_top(c, i)
        op_pa(c)
```

Com `count_in_range`, são cinco funções no arquivo — a cota inteira.

Raiz inteira sem `math.h`:

```
isqrt(n):
    i = 1
    enquanto (i + 1) * (i + 1) <= n:
        i += 1
    devolve i
```

O domínio de uso é n ≥ 2 (a estratégia só chega aqui com `a->size >= 4`); fora dele a função
devolveria 1 para n = 0.

## Como funciona

**Fase 1 — espalhar.** Os ranks são divididos em `k` faixas contíguas. Percorrendo as faixas da
menor para a maior, `a` é varrida empurrando para `b` todo elemento da faixa corrente; quando o
topo não pertence, um `ra` o manda para o fundo e a varredura continua. Cada passada leva
`width` elementos de uma vez, contra um só do `--simple`.

O contador `rest` é o que dá condição de parada: sem ele o laço não sabe quando a faixa acabou.
Ele é calculado uma vez por bloco varrendo `a` em CPU, sem emitir movimento.

**Fase 2 — recolher.** Com `a` vazia, o maior rank restante de `b` é trazido ao topo pelo
caminho mais curto e devolvido com `pa`, n vezes. Do maior para o menor, `a` cresce ordenada.

A fase 2 é barata porque a fase 1 já entrega `b` aproximadamente decrescente do topo: o
primeiro bloco empurrado (valores menores) fica no fundo, o último (maiores) no topo. Dentro de
um bloco a ordem é arbitrária, mas o bloco tem só `width` elementos, então o giro para achar o
máximo é curto. Procurar o extremo entre 34 elementos em vez de entre 500 é todo o ganho.

## Número de blocos

`k = max(2, isqrt(n / 2))`, o que dá:

| n | k | width |
|---|---|---|
| 5 | 2 | 3 |
| 10 | 2 | 5 |
| 50 | 5 | 10 |
| 100 | 7 | 15 |
| 500 | 15 | 34 |
| 1000 | 22 | 46 |

A escolha aparentemente natural, `k = isqrt(n)`, é pior. O custo total tem duas parcelas que
puxam em direções opostas: a fase 1 gasta cerca de `k·n/2` rotações (mais blocos, mais
varreduras) e a fase 2 gasta cerca de `n·width/8` (blocos maiores, buscas mais longas). Com
`width = n/k`, minimizar `k/2 + n/(8k)` dá `k ≈ √n / 2`, e `isqrt(n / 2)` é a forma inteira mais
simples que cai nessa região.

Medido sobre 8 entradas aleatórias de 500 elementos, as mesmas para todo k:

| k | movimentos |
|---|---|
| 11 | 7295 – 7652 |
| 14 | 7142 – 7663 |
| 15 = `isqrt(250)` | **7104 – 7542** |
| 16 | 7301 – 7568 |
| 18 | 7382 – 7732 |
| 20 | 7729 – 7987 |
| 22 = `isqrt(500)` | 7927 – 8151 |
| 25 | 8493 – 8694 |

A região 11–16 é plana — a variação entre amostras é maior que a diferença entre esses k — e
`isqrt(n / 2)` cai dentro dela; a partir de `isqrt(n)` o custo sobe degrau a degrau. Em 15
entradas de 100 elementos, a mesma varredura dá 687 – 796 para k entre 5 e 9, contra 764 – 850
em `isqrt(100) = 10`.

O piso de 2 preserva o comportamento em entradas pequenas: para n = 5, `isqrt(2) = 1` daria um
único bloco e degeneraria a fase 2 em busca linear, quebrando a rota forçada de 13 movimentos
do caso A2.

## Fase 1 só com `ra`

Girar sempre para cima é mais simples e não perde para o caminho mais curto: girar para trás
desorganiza a ordem em que os elementos chegam em `b` e encarece a fase 2, devolvendo em média
o que economizou na fase 1 — com cauda pior. Medido em 20 entradas de 500 elementos (k = 15),
a variante de caminho mais curto gastou em média ~60 movimentos **a mais**, variando de −108 a
+257 por entrada.

## Traço da rota forçada do caso A2

`4 67 3 87 23` → ranks `1 3 0 4 2`, n = 5, k = 2, width = 3.

| Bloco | Estado de `a` | Ação |
|---|---|---|
| `[0,2]`, rest=3 | `1 3 0 4 2` | topo 1 pertence → `pb` |
| | `3 0 4 2` | topo 3 não pertence → `ra` |
| | `0 4 2 3` | topo 0 pertence → `pb` |
| | `4 2 3` | topo 4 não pertence → `ra` |
| | `2 3 4` | topo 2 pertence → `pb` |
| `[3,4]`, rest=2 | `3 4` | topo 3 pertence → `pb` |
| | `4` | topo 4 pertence → `pb` |

`b = 4 3 2 0 1`. Fase 2: os três primeiros máximos já estão no topo (`pa` `pa` `pa`), sobra
`b = 0 1` cujo máximo está no índice 1 com `size = 2`, então `1 <= 1` → `rb` × 1, depois `pa`
`pa`.

Total: `pb ra pb ra pb pb pb pa pa pa rb pa pa` — 13 movimentos, com `pa: 5`, `pb: 5`, `ra: 2`,
`rb: 1` — os 13 movimentos exatos da rota forçada `--medium` do caso A2
([../06-aceitacao/casos.md](../06-aceitacao/casos.md)).

## Custo e contagens medidas

`k` varreduras de O(n) rotações cada, com `k` proporcional a √n: **O(n√n) movimentos**.

Faixas observadas em 20 a 40 permutações aleatórias por tamanho:

| n | faixa |
|---|---|
| 100 | ~680 – 800 |
| 500 | ~6970 – 7590 |
