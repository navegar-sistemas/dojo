#include "push_swap.h"

static int	fail(void)
{
	ft_putendl_fd("Error", 2);
	return (1);
}

static void	put_conf(t_conf *conf)
{
	ft_putstr_fd("strategy=", 1);
	ft_putnbr_fd(conf->strategy, 1);
	ft_putstr_fd(" bench=", 1);
	ft_putnbr_fd(conf->bench, 1);
}

int	main(int argc, char **argv)
{
	t_conf	conf;
	t_stack	*a;
	int		i;

	conf.strategy = STRAT_NONE;
	conf.bench = 0;
	if (!parse_flags(argc, argv, &conf))
		return (fail());
	a = parse_numbers(argc, argv);
	if (a == NULL)
		return (fail());
	put_conf(&conf);
	ft_putstr_fd(" n=", 1);
	ft_putnbr_fd(a->size, 1);
	i = -1;
	while (++i < a->size)
	{
		ft_putchar_fd(' ', 1);
		ft_putnbr_fd(a->data[i], 1);
	}
	ft_putchar_fd('\n', 1);
	stack_free(a);
	return (0);
}