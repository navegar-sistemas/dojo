# T12 — Guloso por custo

## Objetivo

O gerador de programas curtos do portfólio: inserção gulosa guiada por custo, com duas
variantes de desempate.

## Depende de

T07, T09.

## Arquivos

- `greedy_cost.c`
- `greedy_pick.c`
- `greedy_exec.c`
- `sort_greedy.c`

## Especificação

- [../04-algoritmos/greedy.md](../04-algoritmos/greedy.md) — algoritmo completo
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_move` e o campo `bias`
- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — contratos e cotas

## Implementação

A ordem que compila a cada passo: custo → alvos → candidatos → execução → fases.

### `greedy_cost.c` (5 funções — cota cheia)

- `move_cost(m)` — mesmo sinal custa `max(|a|, |b|)` (a fusão `rr`/`rrr` paga uma vez), sinais
  mistos custam a soma.
- `move_better(c, x, y)` — menor custo vence; empate vai para o lado que `c->bias` escolher.
- `pair_best(c, ia, ib)` — as quatro combinações de sentido: cada índice vira rotação para
  frente (`i`) ou para trás (`i - size`, negativo).
- `target_in_b(b, valor)` — índice do sucessor (maior rank abaixo do valor); sem sucessor, o
  máximo atual. Mantém `b` circularmente decrescente.
- `target_in_a(a, valor)` — espelho: o teto (menor rank acima); sem teto, o mínimo. Mantém `a`
  circularmente crescente.

### `greedy_pick.c`

`best_push` e `best_insert` com a varredura podada — índices 0, 1, n−1, 2, n−2... parando
quando `k` alcança o custo do melhor:

```c
while (k <= size - k && k < move_cost(best))
```

O `size - k != k` evita avaliar o mesmo índice duas vezes no meio. As `static` `cand_push` e
`cand_insert` montam o candidato de um índice (`pair_best` + alvo).

### `greedy_exec.c` (5 funções — cota cheia)

`exec_move` consome os pares de mesmo sinal com `op_rr`/`op_rrr` e delega as sobras às
`static` `rot_a`/`rot_b`. `sort_greedy` (bias 0) e `sort_greedy_alt` (bias 1) moram aqui
porque `sort_greedy.c` fechou a própria cota.

### `sort_greedy.c`

`is_circular_sorted` (≤ 1 descida na leitura cíclica), `push_phase` (empurra o mais barato
enquanto `a.size > 3` e o resto não está circularmente ordenado), `insert_phase` (devolve o
mais barato primeiro) e `sort_greedy_run`:

```
grava "Greedy" / "O(n²)"; devolve se ordenada; sort_tiny se n <= 3
push_phase; sort_tiny se sobraram <= 3; insert_phase
rotate_a_to_top(min)
```

O guloso não tem flag própria: até T13, ligue-o **provisoriamente** em `run_strategy` no lugar
do desvio de `STRAT_ADAPTIVE` para testá-lo de ponta a ponta.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**Corretude (via o desvio provisório):**

```bash
i=0; falhas=0
while [ $i -lt 300 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 40 + 1)) | tr '\n' ' ')
  [ "$(./push_swap $ARG | ../assets/checker_linux $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
shuf -i 0-99999 -n 500 > args.txt
./push_swap $(cat args.txt) | ../assets/checker_linux $(cat args.txt)   # OK
```

**Contagem no alvo do excelente** (uma variante sozinha já chega perto; o portfólio de T13
corta a cauda):

```bash
for i in 1 2 3 4 5; do
  ./push_swap $(shuf -i 1-10000 -n 100 | tr '\n' ' ') | wc -l    # ~500-650
done
./push_swap $(cat args.txt) | wc -l                              # ~4800-5500
```

**Quase ordenada — a saída antecipada trabalhando:**

```bash
ARG=$(seq 1 100 | tr '\n' ' ' | awk '{t=$3; $3=$70; $70=t; print}')
./push_swap $ARG | wc -l          # abaixo dos 1084 do radix e dos ~260 do simple
./push_swap $ARG | ../assets/checker_linux $ARG    # OK
```

**Determinismo:** duas execuções sobre a mesma entrada produzem o mesmo programa.

```bash
diff <(./push_swap $(cat args.txt)) <(./push_swap $(cat args.txt)) && echo "determinístico"
```

```bash
valgrind --leak-check=full ./push_swap $(shuf -i 1-10000 -n 200 | tr '\n' ' ')
```
