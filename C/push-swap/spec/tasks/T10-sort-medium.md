# T10 — `--medium`

## Objetivo

Chunk sort com `k = max(2, isqrt(n / 2))`, abaixo de 8000 movimentos para n = 500.

## Depende de

T06, T08.

## Arquivos

- `sort_medium.c`

## Especificação

- [../04-algoritmos/medium.md](../04-algoritmos/medium.md) — algoritmo, escolha de `k`, traço do caso A2
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A2
- [../06-aceitacao/desempenho.md](../06-aceitacao/desempenho.md) — margem de regressão

## Implementação

Cinco funções, quatro `static` — a cota inteira. Com os laços embutidos em `sort_medium`, o
corpo passa de 25 linhas:

| Função | Papel |
|---|---|
| `count_in_range` (static) | quantos elementos de `a` têm rank entre `lo` e `hi` |
| `collect_chunk` (static) | fase 1 de um bloco |
| `collect_all` (static) | laço sobre os `k` blocos |
| `drain_b` (static) | fase 2 completa |
| `sort_medium` | rótulos, casos base, cálculo de `k` e `width` |

```c
static void	collect_chunk(t_ctx *c, int lo, int hi)
{
	int	rest;

	rest = count_in_range(c->a, lo, hi);
	while (rest > 0)
	{
		if (c->a->data[0] >= lo && c->a->data[0] <= hi)
		{
			op_pb(c);
			rest--;
		}
		else
			op_ra(c);
	}
}

static void	drain_b(t_ctx *c)
{
	int	i;

	while (c->b->size > 0)
	{
		i = stack_max_index(c->b);
		rotate_b_to_top(c, i);
		op_pa(c);
	}
}
```

```c
static void	collect_all(t_ctx *c, int n, int k, int width)
{
	int	bloco;
	int	lo;
	int	hi;

	bloco = 0;
	while (bloco < k)
	{
		lo = bloco * width;
		hi = lo + width - 1;
		if (hi > n - 1)
			hi = n - 1;
		collect_chunk(c, lo, hi);
		bloco++;
	}
}
```

`sort_medium` grava `"Medium"` / `"O(n√n)"`, trata `size <= 3`, retorna se ordenada, calcula:

```
k = isqrt(n / 2)
se k < 2: k = 2
```

e chama `collect_all(c, n, k, (n + k - 1) / k)` seguido de `drain_b(c)`.

A pilha já chega convertida em ranks — o `main` fez isso antes do despacho, e a estratégia não
aloca nada.

**Pontos que decidem o desempenho:**

- **`k = isqrt(n / 2)`, não `isqrt(n)`.** Com `isqrt(n)` o pior caso em n = 500 passa de 8000 e
  o projeto perde a faixa "bom". A varredura completa de k está em
  [medium.md](../04-algoritmos/medium.md).
- **O piso `k >= 2`.** Sem ele, n = 5 daria `isqrt(2) = 1`, um bloco único, e o caso A2 sairia
  com mais de 13 movimentos.
- **Fase 1 só com `ra`.** Girar pelo caminho mais curto até o próximo membro custa de 150 a 200
  movimentos a mais em n = 500.
- **`rest` calculado uma vez por bloco.** É a condição de parada do laço; recalcular a cada
  iteração é desperdício de CPU, e não ter o contador deixa o laço sem parada natural.
- **`hi` limitado a `n - 1`.** O último bloco é mais curto quando `n` não é múltiplo de
  `width`.

Ligar `run_strategy` a `sort_medium` para `STRAT_MEDIUM`.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A2 — o exemplo do enunciado, movimento a movimento:**

```bash
[ "$(./push_swap --medium 4 67 3 87 23 | tr '\n' ' ')" = "pb ra pb ra pb pb pb pa pa pa rb pa pa " ] \
  && echo "A2 ok" || echo "A2 FALHOU: $(./push_swap --medium 4 67 3 87 23 | tr '\n' ' ')"
```

**Desempenho — pior caso de 20 rodadas:**

```bash
for n in 100 500; do
  pior=0; i=0
  while [ $i -lt 20 ]; do
    ARG=$(shuf -i 1-10000 -n $n | tr '
' ' ')
    m=$(./push_swap --medium $ARG | wc -l | tr -d ' ')
    [ "$m" -gt "$pior" ] && pior=$m
    i=$((i+1))
  done
  echo "n=$n pior=$pior"
done
# n=100 esperado em torno de 700-810
# n=500 esperado em torno de 7000-7600, e obrigatoriamente abaixo de 8000
```

Pior caso acima de 8000 em n = 500 significa que `k` ou a fase 1 divergiram da spec.

**Corretude:**

```bash
i=0; falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 30 + 1)) | tr '\n' ' ')
  [ "$(./push_swap --medium $ARG | ./assets/checker_linux $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
```

**Bordas de tamanho**, onde o último bloco fica truncado:

```bash
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13 49 50 51; do
  ARG=$(shuf -i 1-10000 -n $n | tr '
' ' ')
  echo -n "n=$n: "
  ./push_swap --medium $ARG | ./assets/checker_linux $ARG
done
```

```bash
valgrind --leak-check=full ./push_swap --medium $(shuf -i 1-10000 -n 200 | tr '\n' ' ')
```
