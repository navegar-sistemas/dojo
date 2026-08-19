# T07 — Caso base e `--simple`

## Objetivo

Primeira receita real. Fim do ciclo `push_swap | checker` com veredito `OK`.

## Depende de

T06.

## Arquivos

- `sort_tiny.c`
- `sort_simple.c`
- `utils.c` (completa: `rotate_a_to_top`, `rotate_b_to_top`, `isqrt`)
- `main.c` (ligar o despacho provisório em `run_strategy`)

## Especificação

- [../04-algoritmos/tiny.md](../04-algoritmos/tiny.md) — as 6 permutações de 3 e por que o limite é 3
- [../04-algoritmos/simple.md](../04-algoritmos/simple.md) — algoritmo e o critério de desempate
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A1 e A4

## Implementação

### `utils.c`

```c
int		isqrt(int n);
void	rotate_a_to_top(t_ctx *c, int i);
void	rotate_b_to_top(t_ctx *c, int i);
```

`isqrt` só é usado em T11; escreva agora para não voltar ao arquivo — com as duas de T03 ele
fecha em 5 funções, a cota exata.

```c
void	rotate_a_to_top(t_ctx *c, int i)
{
	int	size;

	size = c->a->size;
	if (i <= size / 2)
	{
		while (i-- > 0)
			op_ra(c);
	}
	else
	{
		while (size-- > i)
			op_rra(c);
	}
}
```

O `i <= size / 2` com divisão inteira é o que faz o empate escolher `ra`. Trocar por `<`
quebra o caso A1.

`rotate_b_to_top` é o mesmo com `op_rb`/`op_rrb` sobre `c->b`.

### `sort_tiny.c`

`sort_tiny` despacha por tamanho; `sort_three` (static) resolve os três elementos com a cadeia
de condições de [tiny.md](../04-algoritmos/tiny.md). Duas funções.

### `sort_simple.c`

```c
void	sort_simple(t_ctx *c, t_conf *conf)
{
	int	i;

	conf->name = "Simple";
	conf->cclass = "O(n²)";
	if (c->a->size <= 3)
	{
		sort_tiny(c);
		return ;
	}
	if (stack_is_sorted(c->a))
		return ;
	while (c->a->size > 0)
	{
		i = stack_min_index(c->a);
		rotate_a_to_top(c, i);
		op_pb(c);
	}
	while (c->b->size > 0)
		op_pa(c);
}
```

Gravar `name` e `cclass` **antes** dos retornos antecipados: o `--bench` precisa deles mesmo
quando nada é emitido.

### `run_strategy` (`main.c`)

Ligar `STRAT_SIMPLE` a `sort_simple` e, provisoriamente até T13, também `STRAT_ADAPTIVE`:

```c
static void	run_strategy(t_ctx *c, t_conf *conf, double d)
{
	(void)d;
	if (conf->strategy == STRAT_SIMPLE)
		sort_simple(c, conf);
	else if (conf->strategy == STRAT_ADAPTIVE)
		sort_simple(c, conf);
}
```

O `(void)d` sai só em T13, quando o desvio final entrega `d` ao `sort_adaptive`; `--medium` e
`--complex` continuam mudos até T11 e T10 acrescentarem seus ramos. **Não** copie o
`run_strategy` final de [fluxo.md](../03-arquitetura/fluxo.md): ele chama `sort_medium`,
`sort_complex` e `sort_adaptive`, que ainda não existem — o build morre em
`implicit declaration`.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A1 — saída exata:**

```bash
[ "$(./push_swap --simple 5 4 3 2 1 | tr '\n' ' ')" = "rra pb rra pb rra pb ra pb pb pa pa pa pa pa " ] \
  && echo "A1 ok" || echo "A1 FALHOU"
```

**A4 — caso base:**

```bash
for v in "1 2 3:0" "2 1 3:1" "3 1 2:1" "2 3 1:1" "1 3 2:2" "3 2 1:2" "2 1:1" "1 2:0"; do
  arg="${v%%:*}"; esp="${v##*:}"
  n=$(./push_swap --simple $arg | wc -l | tr -d ' ')
  [ "$n" = "$esp" ] && echo "ok   $arg -> $n" || echo "FALHOU $arg -> $n (esperado $esp)"
done
```

**Corretude contra o checker de referência:**

```bash
i=0; falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 20 + 1)) | tr '\n' ' ')
  [ "$(./push_swap --simple $ARG | ../assets/checker_linux $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
```

**Entrada grande:**

```bash
shuf -i 0-9999 -n 500 > args.txt
./push_swap --simple $(cat args.txt) | ../assets/checker_linux $(cat args.txt)   # OK
./push_swap --simple $(cat args.txt) | wc -l    # entre 30000 e 35000, é esperado
```

**Entrada já ordenada e memória:**

```bash
./push_swap --simple 1 2 3 4 5 | wc -l    # 0
valgrind --leak-check=full ./push_swap --simple $(shuf -i 1-10000 -n 200 | tr '\n' ' ')
```
