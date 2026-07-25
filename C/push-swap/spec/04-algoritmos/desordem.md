# Desordem

Fração dos pares de posições que estão fora de ordem, medida **antes** de qualquer movimento.

```
compute_disorder(a):
    erros = 0
    pares = 0
    i = 0
    enquanto i < a.size:
        j = i + 1
        enquanto j < a.size:
            pares += 1
            se a.data[i] > a.data[j]:
                erros += 1
            j += 1
        i += 1
    se pares == 0:
        devolve 0.0
    devolve (double)erros / (double)pares
```

## Cuidados de implementação

- Os dois contadores são `long`. Para n = 500 são 124 750 pares, o que cabe em `int`, mas o
  tipo maior remove qualquer limite prático de tamanho de entrada.
- A divisão precisa dos dois operandos convertidos para `double`. Em inteiro o resultado seria
  sempre 0, e o `--adaptive` cairia sempre na rota O(n²).
- `n < 2` produz `pares == 0`; devolver 0.0 evita a divisão.

## Valores de referência

| Entrada | Desordem |
|---|---|
| `1 2 3` | 0.00 — nenhum par errado |
| `3 2 1` | 1.00 — todos os pares errados |
| `4 67 3 87 23` | 0.40 — 4 dos 10 pares |
| `2 1` | 1.00 |
| entrada de 1 elemento | 0.00 |

O cálculo de `4 67 3 87 23`: dos 10 pares, estão invertidos `(4,3)`, `(67,3)`, `(67,23)` e
`(87,23)`.

## Distribuição em entrada aleatória

Medida em 40 permutações aleatórias por tamanho:

| n | mínimo | máximo |
|---|---|---|
| 100 | 0.4335 | 0.5715 |
| 500 | 0.4648 | 0.5312 |

A concentração em torno de 0.5 é esperada: em uma permutação aleatória cada par tem
probabilidade 1/2 de estar invertido, e a dispersão encolhe conforme n cresce.

A consequência para o `--adaptive` é direta: o limiar de 0.5 corta bem no meio dessa
distribuição, então entrada aleatória cai ora na rota O(n√n), ora na O(n log n). Nas 40
amostras de 500 elementos a divisão foi 20 para cada lado. **As duas rotas precisam bater as
metas de desempenho** — nenhuma delas é caminho secundário.

## Por que essa métrica e não outra

Contar elementos fora da posição final não distingue uma lista quase ordenada de uma
embaralhada: rotacionar uma lista ordenada em uma posição move todos os elementos, mas cria
apenas `n - 1` inversões de um total de `n(n-1)/2`, ou seja desordem próxima de 0 para n
grande. A densidade de inversões captura o esforço real de reordenação, que é o que decide qual
algoritmo compensa.

Uso: [adaptive.md](adaptive.md). Formato de impressão: [../01-contrato/bench.md](../01-contrato/bench.md).
