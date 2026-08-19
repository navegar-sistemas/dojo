#include "push_swap.h"

/*
** Roda antes de parse_numbers: o parser compartilhado pula tokens que
** começam com dois hífens, então sem isso ./checker --simple 3 2 1
** responderia KO onde o binário de referência responde Error.
*/
static int	reject_flags(int argc, char **argv)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		if (argv[i][0] == '-' && argv[i][1] == '-')
			return (0);
		i++;
	}
	return (1);
}

static void	fail_ck(t_ctx *c, char *buf)
{
	ft_putendl_fd("Error", 2);
	free(buf);
	stack_free(c->a);
	stack_free(c->b);
	exit(255);
}

/*
** Divide o buffer em \n e aplica uma linha por vez. O i == ini final
** é o que rejeita uma última linha sem seu newline: a referência
** responde Error a printf 'ra', não KO.
*/
static int	run_all(t_ctx *c, char *buf)
{
	int	ini;
	int	i;

	ini = 0;
	i = 0;
	while (buf[i])
	{
		if (buf[i] == '\n')
		{
			if (!apply_line(c, buf + ini, i - ini))
				return (0);
			ini = i + 1;
		}
		i++;
	}
	return (i == ini);
}

static int	cleanup_ck(t_ctx *c, char *buf)
{
	free(buf);
	stack_free(c->a);
	stack_free(c->b);
	return (0);
}

/*
** counts = NULL é o que faz emit ficar silencioso, para que as mesmas
** 11 operações do push_swap apliquem seu efeito sem imprimir nada.
*/
int	main(int argc, char **argv)
{
	t_ctx	c;
	char	*buf;

	ft_memset(&c, 0, sizeof(t_ctx));
	buf = NULL;
	if (!reject_flags(argc, argv))
		fail_ck(&c, buf);
	c.a = parse_numbers(argc, argv);
	if (!c.a)
		fail_ck(&c, buf);
	if (c.a->size == 0)
		return (cleanup_ck(&c, buf));
	c.b = stack_new(c.a->size);
	buf = read_all(0);
	if (!c.b || !buf)
		fail_ck(&c, buf);
	if (!run_all(&c, buf))
		fail_ck(&c, buf);
	if (stack_is_sorted(c.a) && c.b->size == 0)
		ft_putendl_fd("OK", 1);
	else
		ft_putendl_fd("KO", 1);
	return (cleanup_ck(&c, buf));
}
