# Desempenho

## Metas

| n | passa | bom | excelente |
|---|---|---|---|
| 100 | < 2000 | < 1500 | < 700 |
| 500 | < 12 000 | < 8000 | < 5500 |

Verificadas com entrada aleatória e o comportamento padrão do programa, ou seja
`--adaptive`.

## Contagens medidas

Faixas observadas numa implementação em C desta spec, sobre 20 a 40 permutações aleatórias por
tamanho. São faixas amostrais: um extremo pode se deslocar algumas dezenas de movimentos com
outras amostras, e é por isso que a coluna que importa é a última.

| Estratégia | n = 100 | n = 500 | teto que precisa respeitar |
|---|---|---|---|
| `--simple` | ~1270 – 1730 | ~30 300 – 34 300 | nenhum (rota forçada) |
| `--medium` | ~695 – 805 | ~7020 – 7590 | < 8000 |
| `--complex` | 1084 (fixo) | 6784 (fixo) | < 8000 |
| `--adaptive` | ~680 – 1084 | 6784 – ~7590 | < 1500 e < 8000 |

`--complex` é o único com valor exato: a contagem não depende da entrada.

## Leitura

**O `--adaptive` fica em "bom" nos dois tamanhos.** O pior caso observado é 1084 em n = 100 e
cerca de 7590 em n = 500, contra os limites de 1500 e 8000.

**O pior caso do `--adaptive` é o pior entre medium e complex**, porque com entrada aleatória a
desordem straddle o limiar de 0.5 e as duas rotas são usadas — 22/18 e 20/20 nas amostras. Em
n = 100 o teto vem do complex (1084); em n = 500 vem do medium (~7590).

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
| 500 | ~7590 | 8000 | 5% |

A folga em n = 500 é estreita. Duas mudanças a evitar sem medir de novo:

- Trocar `k = max(2, isqrt(n / 2))` por `isqrt(n)` no chunk sort leva o pior caso a 8258 e
  perde o "bom".
- Trocar a fase 1 do chunk sort para rotação de caminho mais curto acrescenta em média na
  ordem de 100 a 200 movimentos ao pior caso.

## Como medir

Uma amostra só não vale — a variação entre entradas é de centenas de movimentos:

```bash
pior=0
i=0
while [ $i -lt 20 ]; do
  shuf -i 0-9999 -n 500 > args.txt
  n=$(./push_swap $(cat args.txt) | wc -l)
  [ "$n" -gt "$pior" ] && pior=$n
  i=$((i + 1))
done
echo "pior caso em 20 rodadas: $pior"
```
