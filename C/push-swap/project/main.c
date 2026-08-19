#include "push_swap.h"

/*
** Retorna int para que main possa escrever return (cleanup(&c));
*/
static int	cleanup(t_ctx *c)
{
	stack_free(c->a);
	stack_free(c->b);
	prog_free(c->prog);
	return (0);
}

/*
** As flags são lidas antes dos números: um token --foo precisa ser
** recusado como flag desconhecida, não tratado como tentativa de
** número. setup zera todo o contexto logo nas primeiras linhas, para
** que ps_die seja seguro a partir de qualquer ponto de falha.
*/
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

static void	run_strategy(t_ctx *c, t_conf *conf, double d)
{
	if (conf->strategy == STRAT_SIMPLE)
		sort_simple(c, conf);
	else if (conf->strategy == STRAT_MEDIUM)
		sort_medium(c, conf);
	else if (conf->strategy == STRAT_COMPLEX)
		sort_complex(c, conf);
	else
		sort_adaptive(c, conf, d);
}

/*
** A desordem é medida antes de build_ranks, que é o que o subject
** pede: antes de qualquer movimento. build_ranks roda aqui e não
** dentro das estratégias porque sort_* retornam void, sem como
** reportar uma falha. A estratégia registra suas operações em
** c->prog; prog_flush imprime o programa final de uma vez e preenche
** os contadores do --bench a partir dele.
*/
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
