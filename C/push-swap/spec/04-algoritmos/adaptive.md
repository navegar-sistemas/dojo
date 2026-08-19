# `--adaptive` — padrão

Despacho por [desordem](desordem.md) com um **portfólio certificado** por regime. É o
comportamento quando nenhum seletor é passado.

```
sort_adaptive(c, conf, d):
    se d < 0.2:      run_portfolio(c, conf, sort_simple);  conf.cclass = "O(n²)"
    senão se d < 0.5: run_portfolio(c, conf, sort_medium);  conf.cclass = "O(n√n)"
    senão:            run_portfolio(c, conf, sort_complex); conf.cclass = "O(n log n)"
    conf.name = "Adaptive"
```

| Desordem | Certificador | Teto garantido |
|---|---|---|
| `d < 0.2` | [simple](simple.md) | O(n²) |
| `0.2 ≤ d < 0.5` | [medium](medium.md) | O(n√n) |
| `d ≥ 0.5` | [complex](complex.md) | O(n log n) |

Os cortes usam `<` estrito: `0.2` exato cai no regime médio, `0.5` exato no alto.

## O portfólio

```
run_portfolio(c, conf, certificador):
    descarta c.prog
    se a.size <= GREEDY_MAX_N:
        c.prog = simulate(sort_greedy)
        take_if_shorter(simulate(sort_greedy_alt))
        take_if_shorter(simulate(certificador))
    senão:
        c.prog = simulate(certificador)
```

Cada candidato roda numa **simulação**: cópias privadas das pilhas (`stack_dup`), um `t_prog`
próprio, `counts = NULL` e `up` apontando para o contexto real — é essa cadeia que deixa
`ps_die` liberar tudo se uma alocação falhar no meio de uma simulação. `take_if_shorter`
compara com `<` estrito e libera o candidato perdedor na hora.

Só o programa vencedor sobrevive em `c->prog`; o `main` o imprime de uma vez com `prog_flush`
([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)).

## Por que certificar

O [guloso](greedy.md) é quem produz os programas curtos, mas seu pior caso não tem teto melhor
que O(n²) operações — declará-lo como a rota do regime médio ou alto seria falso. Como o
programa emitido nunca excede o do certificador, o custo de cada regime é limitado **por
construção**: ≤ O(n²) com desordem baixa, ≤ O(n√n) com média, ≤ O(n log n) com alta — no pior
caso, não na média. O guloso serve para *encurtar*; o certificador serve para *provar o
limite*.

Na prática, um dos dois gulosos vence em praticamente toda entrada aleatória — o certificador
ganhar é raro e acontece em entradas pequenas ou patológicas. Invariante verificável: a
contagem do `--adaptive` nunca passa a da rota certificadora forçada na mesma entrada
([../06-aceitacao/casos.md](../06-aceitacao/casos.md), A7).

## Acima de `GREEDY_MAX_N`

Com mais de 1500 elementos só o certificador roda: a varredura de candidatos do guloso é
O(n²) em CPU e os benchmarks param em 500. O contrato não muda — qualquer seletor funciona em
qualquer tamanho — só o tempo de parede é preservado.

## Rótulo do `--bench`

`cclass` recebe a classe **do regime**, gravada depois do portfólio: o rótulo certifica o
teto, não conta qual candidato venceu. `name` vira `"Adaptive"` por último, por cima do que a
estratégia simulada gravou. Uma entrada com desordem 0.40 imprime `Adaptive / O(n√n)` mesmo
quando o programa vencedor veio do guloso.

## Rotas em entrada aleatória

A desordem de permutação aleatória se concentra em 0.5 ([desordem.md](desordem.md)), então o
corte de 0.5 divide as entradas quase ao meio entre os regimes médio e alto — 10/10 e 10/10 em
20 amostras por tamanho. **Os dois regimes respondem pelos benchmarks**, e nos dois o vencedor
típico é um guloso; os certificadores medium e complex seguem importantes como teto e como
rotas forçadas.

## Entrada já ordenada

Desordem 0 cai no regime baixo e o portfólio roda normalmente: o guloso devolve programa vazio
(`stack_is_sorted` na entrada), o vencedor tem comprimento 0 e nada é impresso. O `--bench`
reporta `Adaptive / O(n²)` com `total_ops: 0`.

## Entrada quase ordenada

O regime baixo é onde a saída antecipada do guloso aparece: com `seq 1 100` e as posições 3 e
70 trocadas (desordem 2.69%), a invocação padrão emite 202 movimentos contra 263 do
certificador `--simple` na mesma entrada.

## Resultados medidos (invocação padrão)

| n | mínimo | média | máximo | meta |
|---|---|---|---|---|
| 100 | 498 | ~544 | 589 | < 700 |
| 500 | 4789 | ~5035 | 5208 | < 5500 |

Faixas de 60 entradas aleatórias por tamanho. Em lotes maiores acumulados (~250 execuções) o
pior caso observado em n = 500 foi 5507 — a média fica longe da meta, mas a cauda encosta
nela; ver a margem em [../06-aceitacao/desempenho.md](../06-aceitacao/desempenho.md).
