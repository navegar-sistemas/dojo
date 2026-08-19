# Fluxo do `main`

## Funções de `main.c`

| Função | Papel |
|---|---|
| `setup` (static) | zera `conf` e o contexto inteiro, lê flags, monta as pilhas e o programa |
| `run_strategy` (static) | cadeia de `if` sobre `conf.strategy` |
| `cleanup` (static) | libera pilhas e programa, devolve 0 |
| `main` | sequência principal |

O caminho de erro não mora aqui: `ps_die` vive em `utils.c`, porque `prog.c` também precisa
dele (falha de alocação em `prog_grow`) e porque as quatro funções acima mais o `main`
fechariam a cota de 5 do arquivo sem espaço para ele.

## `main`

```c
int	main(int argc, char **argv)
{
	t_conf	conf;
	t_ctx	c;
	int		counts[11];
	double	d;

	if (!setup(argc, argv, &conf, &c))
		ps_die(&c);
	if (c.a->size == 0)
		return (cleanup(&c));
	zero_counts(counts);
	c.counts = counts;
	d = compute_disorder(c.a);
	if (!build_ranks(c.a))
		ps_die(&c);
	run_strategy(&c, &conf, d);
	prog_flush(&c);
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
	c->bias = 0;
	c->prog = NULL;
	c->up = NULL;
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
	c->prog = prog_new();
	if (!c->b || !c->prog)
		return (0);
	return (1);
}
```

Zerar o contexto **inteiro** nas primeiras linhas — inclusive `bias`, `prog` e `up` — é o que
torna `ps_die(&c)` seguro a partir de qualquer ponto de falha, inclusive antes de qualquer
alocação.

Quatro parâmetros — o teto da norma. Não há espaço para um quinto.

## `cleanup`

```c
static int	cleanup(t_ctx *c)
{
	stack_free(c->a);
	stack_free(c->b);
	prog_free(c->prog);
	return (0);
}
```

Devolver `int` permite `return (cleanup(&c));` no `main`, economizando duas linhas.

## Ordens que não podem ser trocadas

**As flags são lidas antes dos números.** Um token `--foo` precisa ser rejeitado como flag
desconhecida, não tentado como número.

**A desordem é medida antes de `build_ranks`.** O contrato fixa a medida antes de qualquer
movimento; medir também antes da conversão elimina a dúvida. Os dois valores seriam idênticos —
a função valor → rank é estritamente crescente, então preserva todas as comparações par a par —
mas a ordem escrita corresponde literalmente ao pseudocódigo de
[../04-algoritmos/desordem.md](../04-algoritmos/desordem.md).

**`build_ranks` roda no `main`, não dentro das estratégias.** As funções `sort_*` devolvem
`void` e não têm como sinalizar falha; no `main` a falha cai no mesmo `ps_die` dos outros
erros. Rodá-la sempre — inclusive para `--simple`, que não precisa de ranks — custa uma
ordenação em memória e nenhum movimento, e não muda o que o `--simple` emite: ele decide por
`stack_min_index` e `stack_is_sorted`, ambos função apenas da ordem relativa, que os ranks
preservam.

**`prog_flush` vem depois da estratégia e antes de `bench_print`.** Nada é impresso durante a
ordenação: a estratégia grava em `c->prog`, e é o flush que imprime o programa e preenche
`counts`. Um `bench_print` antes do flush reportaria tudo zerado.

**A validação inteira acontece antes de qualquer gravação**, e a impressão é atômica no flush:
não existe caminho em que meia receita foi impressa e então algo falha — uma falha de alocação
durante a gravação morre em `ps_die` com stdout ainda vazio.

## Entrada já ordenada

O `main` não testa: cada `sort_*` grava `conf->name`/`conf->cclass` e retorna cedo se
`stack_is_sorted(c->a)`. Assim o rótulo do `--bench` existe mesmo quando nada é emitido.

Em `--adaptive`, desordem 0 cai no regime baixo e o portfólio roda normalmente: o guloso
devolve um programa vazio para pilha ordenada, o vencedor tem comprimento 0, e o `--bench`
reporta `Adaptive / O(n²)` com `total_ops: 0`.

## Caminho de erro

Um ponto único, `ps_die` (`utils.c`): escreve exatamente `Error\n` em stderr, percorre a
cadeia `up` liberando as duas pilhas e o programa de cada contexto, e sai com 1. É chamado de
quatro lugares: falha de `setup` (flags, números, `malloc` de pilha ou programa), falha de
`build_ranks`, falha de `prog_grow` durante a gravação, e falha da `simulate` do portfólio ao
montar uma simulação — este último é o motivo da cadeia `up` existir.
