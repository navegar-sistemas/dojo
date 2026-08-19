#include "push_swap.h"

/*
** Porcentagem com duas casas decimais sem um formatador de float:
** converte para centésimos primeiro. O + 0.5 arredonda em vez de
** truncar, e a parte decimal precisa do zero à esquerda (5 centésimos
** imprime .05).
*/
static void	put_percent(double d)
{
	int	cents;

	cents = (int)(d * 10000.0 + 0.5);
	ft_putnbr_fd(cents / 100, 2);
	ft_putchar_fd('.', 2);
	if (cents % 100 < 10)
		ft_putchar_fd('0', 2);
	ft_putnbr_fd(cents % 100, 2);
	ft_putchar_fd('%', 2);
}

static void	put_counts(t_ctx *c, int from, int to)
{
	int	i;

	ft_putstr_fd("[bench] ", 2);
	i = from;
	while (i <= to)
	{
		ft_putstr_fd(op_name(i), 2);
		ft_putstr_fd(": ", 2);
		ft_putnbr_fd(c->counts[i], 2);
		if (i < to)
			ft_putstr_fd("  ", 2);
		i++;
	}
	ft_putchar_fd('\n', 2);
}

/*
** Cinco linhas no stderr. disorder: e strategy: levam dois espaços e
** total_ops: leva um, para que os três valores comecem na mesma
** coluna.
*/
void	bench_print(t_ctx *c, t_conf *conf, double d)
{
	int	i;
	int	total;

	ft_putstr_fd("[bench] disorder:  ", 2);
	put_percent(d);
	ft_putchar_fd('\n', 2);
	ft_putstr_fd("[bench] strategy:  ", 2);
	ft_putstr_fd(conf->name, 2);
	ft_putstr_fd(" / ", 2);
	ft_putendl_fd(conf->cclass, 2);
	total = 0;
	i = 0;
	while (i < 11)
	{
		total += c->counts[i];
		i++;
	}
	ft_putstr_fd("[bench] total_ops: ", 2);
	ft_putnbr_fd(total, 2);
	ft_putchar_fd('\n', 2);
	put_counts(c, OP_SA, OP_PB);
	put_counts(c, OP_RA, OP_RRR);
}
