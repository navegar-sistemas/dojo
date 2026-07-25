# Fluxo do `main`

## Funções de `main.c`

O `main` não cabe em 25 linhas sozinho. A divisão abaixo é a que fecha nos dois limites da
norma, com 5 funções e nenhum corpo passando de 18 linhas.

| Função | Papel |
|---|---|
| `setup` (static) | zera `conf` e `ctx`, lê flags, monta as pilhas |
| `run_strategy` (static) | cadeia de `if` sobre `conf.strategy` |
| `fail` (static) | `Error` em stderr, liberação, `exit(1)` |
| `cleanup` (static) | liberação, devolve 0 |
| `main` | sequência principal |

## `main`

```c
int	main(int argc, char **argv)
{
	t_conf	conf;
	t_ctx	c;
	int		counts[11];
	double	d;

	if (!setup(argc, argv, &conf, &c))
		fail(&c);
	if (c.a->size == 0)
		return (cleanup(&c));
	zero_counts(counts);
	c.counts = counts;
	d = compute_disorder(c.a);
	if (!build_ranks(c.a))
		fail(&c);
	run_strategy(&c, &conf, d);
	if (conf.bench)
		bench_print(&c, &conf, d);
	return (cleanup(&c));
}
```

`int counts[11];` seguido de `zero_counts(counts)`: a norma proíbe declaração com atribuição,
então `= {0}` está fora.

## `setup`

```c
static int	setup(int argc, char **argv, t_conf *conf, t_ctx *c)
{
	c->a = NULL;
	c->b = NULL;
	c->counts = NULL;
	conf->strategy = STRAT_NONE;
	conf->bench = 0;
	conf->name = "";
	conf->cclass = "";
	if (!parse_flags(argc, argv, conf))
		return (0);
	if (conf->strategy == STRAT_NONE)
		conf->strategy = STRAT_ADAPTIVE;
	c->a = parse_numbers(argc, argv);
	if (!c->a)
		return (0);
	c->b = stack_new(c->a->size);
	if (!c->b)
		return (0);
	return (1);
}
```

Zerar `c->a` e `c->b` na primeira linha é o que torna `fail(&c)` seguro a partir de qualquer
ponto de falha, inclusive antes de qualquer alocação.

Quatro parâmetros — o teto da norma. Não há espaço para um quinto.

## `fail` e `cleanup`

```c
static void	fail(t_ctx *c)
{
	ft_putendl_fd("Error", 2);
	stack_free(c->a);
	stack_free(c->b);
	exit(1);
}

static int	cleanup(t_ctx *c)
{
	stack_free(c->a);
	stack_free(c->b);
	return (0);
}
```

`cleanup` devolver `int` permite `return (cleanup(&c));` no `main`, economizando duas linhas.

## Ordens que não podem ser trocadas

**A desordem é medida antes de `build_ranks`.** O enunciado exige a medida antes de qualquer
movimento; medir também antes da conversão elimina a dúvida. Os dois valores seriam idênticos —
a função valor → rank é estritamente crescente, então preserva todas as comparações par a par —
mas a ordem escrita é a que corresponde literalmente ao pseudocódigo do enunciado.

**`build_ranks` roda no `main`, não dentro das estratégias.** É a única alocação depois do
parsing, e é aqui que existe caminho de erro: as funções `sort_*` devolvem `void` e não têm como
sinalizar falha nem acesso às pilhas para liberá-las. Rodá-la sempre — inclusive para
`--simple`, que não precisa de ranks — custa uma ordenação em memória e nenhum movimento, e
mantém as estratégias sem alocação.

Converter para ranks não muda o que o `--simple` emite: ele decide por `stack_min_index` e
`stack_is_sorted`, ambos função apenas da ordem relativa, que os ranks preservam.

**As flags são lidas antes dos números.** Um token `--foo` precisa ser rejeitado como flag
desconhecida, não tentado como número.

**A validação inteira acontece antes do primeiro movimento.** Nunca sai metade da receita
seguida de `Error`.

## Entrada já ordenada

O `main` não testa: cada `sort_*` grava `conf->name`/`conf->cclass` e então retorna cedo se
`stack_is_sorted(c->a)`. Assim o rótulo do `--bench` existe mesmo quando nada é emitido, e o
`main` fica menor.

Em `--adaptive`, a rota continua sendo escolhida pela desordem mesmo com a pilha ordenada:
desordem 0 cai em `< 0.2`, então o rótulo reportado é `Adaptive / O(n²)`.

## Caminho de erro

Um ponto único, `fail`, chamado de três lugares: falha de `setup` (flags inválidas, números
inválidos, `malloc` da pilha) e falha de `build_ranks`. Sempre escreve exatamente `Error\n` em
stderr, libera as duas pilhas e sai com 1.
