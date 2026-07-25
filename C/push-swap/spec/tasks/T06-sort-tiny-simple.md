# T06 — Caso base e `--simple`

## Objetivo

Primeira receita real. Fim do ciclo `push_swap | checker` com veredito `OK`.

## Depende de

T05.

## Arquivos

- `sort_tiny.c`
- `sort_simple.c`
- `utils.c`

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

`isqrt` só é usado em T10; escreva agora para não voltar ao arquivo.

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
		return (sort_tiny(c));
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

`return (sort_tiny(c))` em função `void` compila, mas a forma segura para a norma é chamar e
retornar em duas linhas.

Gravar `name` e `cclass` **antes** dos retornos antecipados: o `--bench` precisa deles mesmo
quando nada é emitido.

Ligar `run_strategy` do T05 a `sort_simple` para `STRAT_SIMPLE` e, provisoriamente, também para
`STRAT_ADAPTIVE` até T11.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A1 — saída exata do enunciado:**

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
  [ "$(./push_swap --simple $ARG | ./assets/checker_Mac $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
```

**Entrada grande:**

```bash
shuf -i 0-9999 -n 500 > /tmp/a500.txt
./push_swap --simple $(cat /tmp/a500.txt) | ./assets/checker_Mac $(cat /tmp/a500.txt)   # OK
./push_swap --simple $(cat /tmp/a500.txt) | wc -l    # entre 30000 e 35000
```

**Entrada já ordenada e memória:**

```bash
./push_swap --simple 1 2 3 4 5 | wc -l    # 0
leaks --atExit -- ./push_swap --simple $(shuf -i 1-1000 -n 200 | tr '\n' ' ')
```
