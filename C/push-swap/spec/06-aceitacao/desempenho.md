# Desempenho

## Metas

| n | passa | bom | excelente |
|---|---|---|---|
| 100 | < 2000 | < 1500 | < 700 |
| 500 | < 12 000 | < 8000 | < 5500 |

Verificadas com entrada aleatória e o comportamento padrão do programa, ou seja `--adaptive`.

## Contagens medidas

Faixas observadas na implementação de referência. São faixas amostrais: um extremo pode se
deslocar com outras amostras, e é por isso que a margem é medida no pior caso de várias
rodadas, nunca numa execução só.

| Estratégia | n = 100 | n = 500 | teto que precisa respeitar |
|---|---|---|---|
| `--adaptive` (padrão) | 498 – 589, média ~544 | 4789 – 5208, média ~5035 | < 700 e < 5500 |
| `--simple` | ~1270 – 1730 | ~30 300 – 34 300 | nenhum (rota forçada) |
| `--medium` | ~680 – 800 | ~6970 – 7590 | teto do regime médio |
| `--complex` | 1084 (fixo) | 6784 (fixo) | teto do regime alto |

O `--adaptive` foi medido em 60 entradas por tamanho; as rotas forçadas, em 20 a 40. O
`--complex` é o único com valor exato: a contagem não depende da entrada (não ordenada,
n > 3).

## Leitura

**A meta "excelente" é atingida nos dois tamanhos.** Quem responde por ela é o
[guloso](../04-algoritmos/greedy.md) dentro do portfólio — os certificadores sozinhos ficariam
em 1084 e ~7600.

**A margem em n = 100 é folgada** (pior caso 589 contra 700, ~16%).

**A margem em n = 500 é real, mas a cauda existe.** Média ~5035 contra 5500 (~8%); em ~250
execuções acumuladas o pior caso observado foi **5507**, uma vez — acima da meta. Numa
medição por média de várias rodadas a meta fecha com folga; numa rodada única e azarada, a
cauda pode custar o "excelente" (nunca o "bom", que passa de largo).

**`--simple` com 500 elementos estoura todos os limites por larga margem.** Isso não é
defeito: a flag força explicitamente a rota O(n²), e o que se exige dela é funcionar em
qualquer entrada, não bater as metas. No `--adaptive` o selection só aparece como certificador
do regime de desordem baixa, onde custa pouco.

## Margem para regressão

Mudanças que mexem com a cauda do `--adaptive` e não devem entrar sem medir de novo:

- **Poda ou desempate do guloso** (`best_push`/`best_insert`, `move_better`): a poda é
  comprovadamente neutra; qualquer "melhoria" que altere a resposta muda a distribuição
  inteira.
- **Remover uma das variantes de `bias`**: é o mínimo entre as duas que corta a cauda.
- **`GREEDY_MAX_N` abaixo de 500**: os benchmarks passariam a medir só o certificador — n = 500
  cairia para ~6800–7600 e perderia o "excelente".
- **`k` do chunk sort e fase 1 só com `ra`** ([medium.md](../04-algoritmos/medium.md)): afetam
  o teto do regime médio e a rota forçada `--medium`.

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
