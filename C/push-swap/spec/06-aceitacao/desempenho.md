# Desempenho

## Metas

| n | passa | bom | excelente |
|---|---|---|---|
| 100 | < 2000 | < 1500 | < 700 |
| 500 | < 12 000 | < 8000 | < 5500 |

Verificadas com entrada aleatória e o comportamento padrão do programa, ou seja
`--adaptive`.

## Contagens medidas

40 permutações aleatórias por tamanho, valores mínimo e máximo observados:

| Estratégia | n = 100 | n = 500 |
|---|---|---|
| `--simple` | 1269 – 1732 | 30 313 – 34 319 |
| `--medium` | 696 – 802 | 7027 – 7576 |
| `--complex` | 1084 (fixo) | 6784 (fixo) |
| `--adaptive` | 696 – 1084 | 6784 – 7555 |

## Leitura

**O `--adaptive` fica em "bom" nos dois tamanhos.** O pior caso é 1084 em n = 100 e 7555 em
n = 500, contra os limites de 1500 e 8000.

**O pior caso do `--adaptive` é o pior entre medium e complex**, porque com entrada aleatória a
desordem straddle o limiar de 0.5 e as duas rotas são usadas — 22/18 e 20/20 nas amostras. Em
n = 100 o teto vem do complex (1084); em n = 500 vem do medium (7555).

**"Excelente" não é alcançado** e não é alcançável com estas quatro estratégias. Em n = 500 o
melhor resultado é 6784, contra a meta de 5500. Chegar lá exige a estratégia gulosa de custo
mínimo descrita em [../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md), fora do
escopo desta spec.

**`--simple` com 500 elementos estoura todos os limites por larga margem.** Isso não é defeito:
a flag força explicitamente a rota O(n²), e o enunciado exige que ela funcione em qualquer
entrada, não que bata as metas. O `--adaptive` só a escolhe quando a desordem é menor que 0.2,
regime em que ela custa de 294 a 4225 movimentos.

## Margem para regressão

| n | pior caso medido | limite "bom" | folga |
|---|---|---|---|
| 100 | 1084 | 1500 | 28% |
| 500 | 7555 | 8000 | 6% |

A folga em n = 500 é estreita. Duas mudanças a evitar sem medir de novo:

- Trocar `k = max(2, isqrt(n / 2))` por `isqrt(n)` no chunk sort leva o pior caso a 8258 e
  perde o "bom".
- Trocar a fase 1 do chunk sort para rotação de caminho mais curto acrescenta de 150 a 200
  movimentos.

## Como medir

Uma amostra só não vale — a variação entre entradas é de centenas de movimentos:

```bash
pior=0
i=0
while [ $i -lt 20 ]; do
  shuf -i 0-9999 -n 500 > /tmp/a.txt
  n=$(./push_swap $(cat /tmp/a.txt) | wc -l)
  [ "$n" -gt "$pior" ] && pior=$n
  i=$((i + 1))
done
echo "pior caso em 20 rodadas: $pior"
```
