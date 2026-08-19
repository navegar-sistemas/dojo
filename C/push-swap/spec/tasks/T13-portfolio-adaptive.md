# T13 — Portfólio e `--adaptive`

## Objetivo

O comportamento padrão: despacho por desordem rodando guloso ×2 + certificador em cópias das
pilhas, com o programa mais curto indo para stdout.

## Depende de

T08, T10, T11, T12.

## Arquivos

- `portfolio.c`
- `sort_adaptive.c`
- `main.c` (remover o desvio provisório de T12 e ligar `STRAT_ADAPTIVE` ao despacho real)

## Especificação

- [../04-algoritmos/adaptive.md](../04-algoritmos/adaptive.md) — regimes, portfólio, certificação
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — `t_sortfn`, `up`, ciclo de vida dos programas

## Implementação

### `portfolio.c`

| Função | Papel |
|---|---|
| `stack_dup` (static) | cópia de uma pilha (`stack_new` + `ft_memcpy`) |
| `simulate` (static) | roda uma estratégia em cópias privadas e devolve o programa gravado |
| `take_if_shorter` (static) | fica com o candidato se for **estritamente** menor |
| `run_portfolio` | orquestra os candidatos |

`simulate` monta o contexto da simulação com `counts = NULL`, `bias = 0`, `up = c` e um
`prog_new` próprio; roda `fn(&sim, conf)`, libera as pilhas da simulação e devolve o programa.
Falha de alocação em qualquer ponto cai em `ps_die(&sim)` — e a cadeia `up` libera também o
contexto real.

```
run_portfolio(c, conf, alt):
    prog_free(c->prog); c->prog = NULL
    se a.size <= GREEDY_MAX_N:
        c->prog = simulate(sort_greedy)
        take_if_shorter(simulate(sort_greedy_alt))
        take_if_shorter(simulate(alt))
    senão:
        c->prog = simulate(alt)
```

### `sort_adaptive.c`

Uma função: despacha pelo `d` recebido do `main` (medido antes de qualquer movimento e antes
da conversão em ranks) e certifica o regime:

```
d < 0.2  -> run_portfolio(sort_simple);  cclass = "O(n²)"
d < 0.5  -> run_portfolio(sort_medium);  cclass = "O(n√n)"
senão    -> run_portfolio(sort_complex); cclass = "O(n log n)"
name = "Adaptive"
```

Cortes com `<` estrito: `0.2` exato cai no regime médio, `0.5` exato no alto. `cclass` é
gravado **depois** do portfólio (as simulações sobrescrevem `conf` ao rodar) e reporta o
regime, não o candidato vencedor.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A2 — caminho padrão, saída exata:**

```bash
[ "$(./push_swap 4 67 3 87 23 | tr '\n' ' ')" = "pb pb sa ra rra pa rrr pa rra " ] \
  && echo "A2 ok" || echo "A2 FALHOU"
./push_swap --adaptive 4 67 3 87 23 | wc -l    # 9 (adaptive é o padrão)
```

**Invariante do portfólio — nunca pior que o certificador:**

```bash
[ "$(./push_swap 5 4 3 2 1 | wc -l)" -le "$(./push_swap --complex 5 4 3 2 1 | wc -l)" ] && echo ok
ARG=$(seq 1 100 | tr '\n' ' ' | awk '{t=$3; $3=$70; $70=t; print}')   # desordem 0.027: regime baixo
[ "$(./push_swap $ARG | wc -l)" -le "$(./push_swap --simple $ARG | wc -l)" ] && echo ok
```

**Corretude nas quatro flags:**

```bash
shuf -i 0-9999 -n 500 > args.txt
for f in --simple --medium --complex --adaptive; do
  echo -n "$f: "
  ./push_swap $f $(cat args.txt) | ../assets/checker_linux $(cat args.txt)
done
```

**Desempenho combinado — pior caso de 20 rodadas:**

```bash
for n in 100 500; do
  pior=0; i=0
  while [ $i -lt 20 ]; do
    ARG=$(shuf -i 1-10000 -n $n | tr '\n' ' ')
    m=$(./push_swap $ARG | wc -l | tr -d ' ')
    [ "$m" -gt "$pior" ] && pior=$m
    i=$((i+1))
  done
  echo "n=$n pior=$pior"
done
# n=100 abaixo de 700; n=500 abaixo de 5500 (cauda rara pode encostar — ver desempenho.md)
```

**Entrada já ordenada e acima do teto do guloso:**

```bash
for f in --simple --medium --complex --adaptive; do
  echo "$f: $(./push_swap $f 1 2 3 4 5 | wc -l)"    # todos 0
done
ARG=$(shuf -i 1-100000 -n 1501 | tr '\n' ' ')
./push_swap $ARG | ../assets/checker_linux $ARG     # OK — só o certificador rodou
```

**Memória — o portfólio inteiro, candidatos descartados inclusos:**

```bash
valgrind --leak-check=full ./push_swap 4 67 3 87 23
valgrind --leak-check=full ./push_swap $(cat args.txt)
```
