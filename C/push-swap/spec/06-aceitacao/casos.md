# Casos de aceitação

Entradas com saída exata.

## A1 — `--simple` com 5 elementos

```
$ ./push_swap --simple 5 4 3 2 1
rra
pb
rra
pb
rra
pb
ra
pb
pb
pa
pa
pa
pa
pa
```

14 movimentos, nessa ordem exata, fixados como gabarito. O que discrimina é o
critério de desempate `i <= size / 2` na rotação até o topo — ver
[../04-algoritmos/simple.md](../04-algoritmos/simple.md).

```bash
[ "$(./push_swap --simple 5 4 3 2 1 | tr '\n' ' ')" = "rra pb rra pb rra pb ra pb pb pa pa pa pa pa " ] \
  && echo A1 ok || echo A1 FALHOU
```

## A2 — caminho padrão com 5 elementos

A invocação padrão sobre `4 67 3 87 23` (desordem 0.40, regime médio) emite o programa do
guloso, vencedor do portfólio — 9 movimentos, determinísticos:

```
$ ./push_swap 4 67 3 87 23 | tr '\n' ' '
pb pb sa ra rra pa rrr pa rra
$ ./push_swap --adaptive 4 67 3 87 23 | wc -l
9
$ ./push_swap --bench 4 67 3 87 23 2>&1 >/dev/null
[bench] disorder:  40.00%
[bench] strategy:  Adaptive / O(n√n)
[bench] total_ops: 9
[bench] sa: 1  sb: 0  ss: 0  pa: 2  pb: 2
[bench] ra: 1  rb: 0  rr: 0  rra: 2  rrb: 0  rrr: 1
```

O rótulo certifica o regime (`O(n√n)`), não o candidato vencedor — ver
[../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md).

**Rota certificadora forçada** na mesma entrada — o chunk sort emite 13 movimentos exatos
(traço passo a passo em [../04-algoritmos/medium.md](../04-algoritmos/medium.md)):

```
$ ./push_swap --medium 4 67 3 87 23 | tr '\n' ' '
pb ra pb ra pb pb pb pa pa pa rb pa pa
```

```bash
[ "$(./push_swap 4 67 3 87 23 | tr '\n' ' ')" = "pb pb sa ra rra pa rrr pa rra " ] \
  && echo A2 ok || echo A2 FALHOU
[ "$(./push_swap --medium 4 67 3 87 23 | tr '\n' ' ')" = "pb ra pb ra pb pb pb pa pa pa rb pa pa " ] \
  && echo A2-medium ok || echo A2-medium FALHOU
```

## A3 — `--complex` determinístico

| n | movimentos |
|---|---|
| 100 | 1084 |
| 500 | 6784 |

Sem variação entre entradas **não ordenadas** do mesmo tamanho (com n > 3): entrada já
ordenada retorna cedo com 0 movimentos, e n ≤ 3 cai no caso base.

```bash
for i in 1 2 3; do
  shuf -i 0-9999 -n 500 > args.txt
  ./push_swap --complex $(cat args.txt) | wc -l
done   # precisa imprimir 6784 três vezes
```

## A4 — `sort_tiny`

| Entrada | Movimentos | Sequência |
|---|---|---|
| `1 2 3` | 0 | — |
| `2 1 3` | 1 | `sa` |
| `3 1 2` | 1 | `ra` |
| `2 3 1` | 1 | `rra` |
| `1 3 2` | 2 | `sa` `ra` |
| `3 2 1` | 2 | `sa` `rra` |
| `2 1` | 1 | `sa` |
| `1 2` | 0 | — |

Vale para as quatro flags: o caso base é consultado antes da estratégia, e no `--adaptive` o
portfólio converge para o mesmo programa mínimo.

## A5 — Erros

Todos produzem `Error\n` em stderr, stdout vazio, saída 1:

```bash
./push_swap 0 one 2 3                  # token não numérico
./push_swap --simple 3 2 3             # duplicata
./push_swap 2147483648                 # estoura int
./push_swap -2147483649                # estoura int
./push_swap 4.2                        # ponto não é dígito
./push_swap +                          # sinal sem dígito
./push_swap ""                         # argumento sem token
./push_swap --simple --medium 3 2 1    # dois seletores diferentes
./push_swap --foo 3 2 1                # flag desconhecida
./push_swap --                         # flag desconhecida
```

## A6 — Casos silenciosos

Saída 0, stdout e stderr vazios:

```bash
./push_swap                          # nenhum argumento
./push_swap --bench                  # só flag, nenhum número
./push_swap 42                       # um elemento
./push_swap 1 2 3                    # já ordenada
./push_swap --complex 1 2 3 4 5      # já ordenada, qualquer flag
./push_swap --simple --simple 1 2 3  # seletor repetido, já ordenada
```

Com `--bench` e entrada já ordenada não vazia, o bloco de métricas sai com tudo zerado:

```
$ ./push_swap --bench 1 2 3 2>&1 >/dev/null
[bench] disorder:  0.00%
[bench] strategy:  Adaptive / O(n²)
[bench] total_ops: 0
[bench] sa: 0  sb: 0  ss: 0  pa: 0  pb: 0
[bench] ra: 0  rb: 0  rr: 0  rra: 0  rrb: 0  rrr: 0
```

## A7 — Invariantes

**Bench**: para qualquer entrada válida, o número de linhas em stdout, o `total_ops` e a soma
das 11 contagens são o mesmo número:

```bash
ARG=$(shuf -i 0-9999 -n 50 | tr '\n' ' ')
linhas=$(./push_swap $ARG | wc -l)
total=$(./push_swap --bench $ARG 2>&1 >/dev/null | grep total_ops | tr -dc '0-9')
[ "$linhas" -eq "$total" ] && echo A7 ok || echo A7 FALHOU
```

**Portfólio**: a invocação padrão nunca emite mais que a rota certificadora do seu regime,
forçada sobre a mesma entrada:

```bash
ARG=$(shuf -i 0-9999 -n 500 | tr '\n' ' ')
d=$(./push_swap --bench $ARG 2>&1 >/dev/null | grep disorder | tr -dc '0-9')
ad=$(./push_swap $ARG | wc -l)
if [ "$d" -lt 2000 ]; then cert=$(./push_swap --simple $ARG | wc -l)
elif [ "$d" -lt 5000 ]; then cert=$(./push_swap --medium $ARG | wc -l)
else cert=$(./push_swap --complex $ARG | wc -l); fi
[ "$ad" -le "$cert" ] && echo A7-portfolio ok || echo A7-portfolio FALHOU
```

## A8 — Formato da saída

```bash
./push_swap 3 2 1 | cat -A
```

Só siglas e `$`. Nenhum espaço, nenhum `^I`, nenhuma linha vazia.
