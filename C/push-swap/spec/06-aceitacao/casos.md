# Casos de aceitação

Entradas com saída exata. Divergir de qualquer um exige entender a causa antes de seguir.

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

14 movimentos, nessa ordem exata. É a saída publicada no enunciado, e o que discrimina é o
critério de desempate `i <= size / 2` na rotação até o topo — ver
[../04-algoritmos/simple.md](../04-algoritmos/simple.md).

```bash
[ "$(./push_swap --simple 5 4 3 2 1 | tr '\n' ' ')" = "rra pb rra pb rra pb ra pb pb pa pa pa pa pa " ] \
  && echo A1 ok || echo A1 FALHOU
```

## A2 — `--adaptive` com o exemplo do enunciado

```
$ ARG="4 67 3 87 23"; ./push_swap --adaptive $ARG | wc -l
13
$ ./push_swap --bench --adaptive $ARG 2>&1 >/dev/null
[bench] disorder:  40.00%
[bench] strategy:  Adaptive / O(n√n)
[bench] total_ops: 13
[bench] sa: 0  sb: 0  ss: 0  pa: 5  pb: 5
[bench] ra: 2  rb: 1  rr: 0  rra: 0  rrb: 0  rrr: 0
```

Sequência completa: `pb ra pb ra pb pb pb pa pa pa rb pa pa`. Traço passo a passo em
[../04-algoritmos/medium.md](../04-algoritmos/medium.md).

Desordem 0.40 cai na faixa média, então a rota é a O(n√n).

## A3 — `--complex` determinístico

| n | movimentos |
|---|---|
| 100 | 1084 |
| 500 | 6784 |

Sem variação entre entradas do mesmo tamanho.

```bash
for i in 1 2 3; do
  shuf -i 0-9999 -n 500 > /tmp/a500.txt
  ./push_swap --complex $(cat /tmp/a500.txt) | wc -l
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

Vale para as quatro flags: o caso base é consultado antes da estratégia.

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
./push_swap --simple --medium 3 2 1    # dois seletores
./push_swap --simple --simple 3 2 1    # seletor repetido
./push_swap --foo 3 2 1                # flag desconhecida
```

## A6 — Casos silenciosos

Saída 0, stdout e stderr vazios:

```bash
./push_swap                # nenhum argumento
./push_swap --bench        # só flag, nenhum número
./push_swap 42             # um elemento
./push_swap 1 2 3          # já ordenada
./push_swap --complex 1 2 3 4 5   # já ordenada, qualquer flag
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

## A7 — Invariantes do `--bench`

Para qualquer entrada válida:

```bash
ARG=$(shuf -i 1-1000 -n 50 | tr '\n' ' ')
linhas=$(./push_swap $ARG | wc -l)
total=$(./push_swap --bench $ARG 2>&1 >/dev/null | grep total_ops | tr -dc '0-9')
[ "$linhas" -eq "$total" ] && echo A7 ok || echo A7 FALHOU
```

A soma das 11 contagens também precisa ser igual a `total_ops`.

## A8 — Formato da saída

```bash
./push_swap 3 2 1 | cat -A
```

Só siglas e `$`. Nenhum espaço, nenhum `^I`, nenhuma linha vazia.
