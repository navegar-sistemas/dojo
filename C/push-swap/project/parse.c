#include "push_swap.h"

/*
** Primeira passada: quantos tokens numéricos existem no total, para
** que a pilha seja alocada uma única vez. Um argumento que se divide
** em zero tokens ("" ou "   ") é um erro, que é o caso ./push_swap
** "".
*/
static int	count_tokens(int argc, char **argv, int *total)
{
	char	**parts;
	int		i;
	int		j;

	i = 1;
	*total = 0;
	while (i < argc)
	{
		if (argv[i][0] != '-' || argv[i][1] != '-')
		{
			parts = ft_split(argv[i], ' ');
			if (!parts)
				return (0);
			j = 0;
			while (parts[j])
				j++;
			free_split(parts);
			if (j == 0)
				return (0);
			*total += j;
		}
		i++;
	}
	return (1);
}

static int	add_tokens(char *arg, t_stack *a)
{
	char	**parts;
	int		i;
	int		v;

	parts = ft_split(arg, ' ');
	if (!parts)
		return (0);
	i = 0;
	while (parts[i])
	{
		if (!is_int_token(parts[i]) || !token_to_int(parts[i], &v))
		{
			free_split(parts);
			return (0);
		}
		a->data[a->size] = v;
		a->size++;
		i++;
	}
	free_split(parts);
	return (1);
}

static int	fill_all(int argc, char **argv, t_stack *a)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		if (argv[i][0] != '-' || argv[i][1] != '-')
		{
			if (!add_tokens(argv[i], a))
				return (0);
		}
		i++;
	}
	return (1);
}

/*
** Um token começando com um único '-' é um número negativo; apenas
** dois hífens formam uma flag. Repetir o mesmo seletor é aceito,
** dois diferentes é erro.
*/
int	parse_flags(int argc, char **argv, t_conf *conf)
{
	int	i;
	int	s;

	i = 1;
	while (i < argc)
	{
		if (argv[i][0] == '-' && argv[i][1] == '-')
		{
			s = flag_id(argv[i]);
			if (s == 0)
				return (0);
			if (s == FLAG_BENCH)
				conf->bench = 1;
			else if (conf->strategy != STRAT_NONE && conf->strategy != s)
				return (0);
			else
				conf->strategy = s;
		}
		i++;
	}
	return (1);
}

t_stack	*parse_numbers(int argc, char **argv)
{
	t_stack	*a;
	int		total;

	if (!count_tokens(argc, argv, &total))
		return (NULL);
	a = stack_new(total);
	if (!a)
		return (NULL);
	if (!fill_all(argc, argv, a))
	{
		stack_free(a);
		return (NULL);
	}
	if (has_duplicates(a))
	{
		stack_free(a);
		return (NULL);
	}
	return (a);
}
