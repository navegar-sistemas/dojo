# `--adaptive` — padrão

Despacho por [desordem](desordem.md). Não ordena nada por conta própria.

```
sort_adaptive(c, conf, d):
    se d < 0.2:
        sort_simple(c, conf)
    senão se d < 0.5:
        sort_medium(c, conf)
    senão:
        sort_complex(c, conf)
    conf.name = "Adaptive"
```

`conf.cclass` permanece o que a rota gravou, então o `--bench` reporta `Adaptive / O(n√n)`,
`Adaptive / O(n log n)` ou `Adaptive / O(n²)` conforme o caminho tomado. A sobrescrita do nome
acontece **depois** da chamada, porque a rota grava os dois campos.

Os limiares e as classes exigidas em cada faixa vêm do enunciado:

| Desordem | Classe exigida | Rota |
|---|---|---|
| `d < 0.2` | O(n²) | [simple](simple.md) |
| `0.2 ≤ d < 0.5` | O(n√n) | [medium](medium.md) |
| `d ≥ 0.5` | O(n log n) | [complex](complex.md) |

## Por que o despacho compensa

Nenhum dos três algoritmos ganha em todo regime, e o cruzamento é grande.

Em entradas quase ordenadas o quadrático mal precisa girar — o mínimo restante já está perto do
topo — enquanto o radix gasta suas passadas fixas de qualquer jeito. Medido em 8 entradas por
tamanho, com desordem entre 0.01 e 0.13:

| n | desordem | rota escolhida (`simple`) | `complex` na mesma entrada |
|---|---|---|---|
| 100 | 0.036 – 0.131 | 294 – 470 | 1084 |
| 500 | 0.011 – 0.071 | 1634 – 4225 | 6784 |

Na direção oposta, com entrada aleatória o quadrático explode para mais de 30 000 movimentos em
n = 500 e o radix fica em 6784.

## As duas rotas altas são igualmente críticas

A desordem de entrada aleatória fica colada em 0.5, então o limiar corta bem no meio da
distribuição. Em 40 amostras por tamanho:

| n | desordem observada | rotas escolhidas |
|---|---|---|
| 100 | 0.4335 – 0.5715 | 22 medium, 18 complex |
| 500 | 0.4648 – 0.5312 | 20 medium, 20 complex |

O benchmark oficial usa entrada aleatória, então **medium e complex precisam ambos bater as
metas** — qual dos dois roda depende do sorteio, e não há como escolher.

## Resultado combinado

Pior caso do `--adaptive` em 40 amostras aleatórias:

| n | mínimo | máximo | meta "passa" | meta "bom" |
|---|---|---|---|---|
| 100 | 696 | 1084 | < 2000 | < 1500 |
| 500 | 6784 | 7555 | < 12 000 | < 8000 |

Os dois tamanhos ficam dentro de "bom". "Excelente" (< 700 e < 5500) exigiria uma estratégia
gulosa de custo mínimo, que não está entre as quatro especificadas — ver
[../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md).

## Entrada já ordenada

Desordem 0 cai na faixa `< 0.2`, então a rota resolvida é `Simple / O(n²)`. O `sort_simple`
detecta a pilha ordenada e retorna sem emitir nada, e o `--bench` reporta
`Adaptive / O(n²)` com `total_ops: 0`.
