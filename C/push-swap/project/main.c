#include "push_swap.h"

static int	cleanup(t_ctx *c)
{
	stack_free(c->a);
	stack_free(c->b);
	prog_free(c->prog);
	return (0);
}

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
	(void)d;
	if (conf->strategy == STRAT_SIMPLE)
		sort_simple(c, conf);
	else if (conf->strategy == STRAT_ADAPTIVE)
		sort_simple(c, conf);
}

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
	return (cleanup(&c));
}
