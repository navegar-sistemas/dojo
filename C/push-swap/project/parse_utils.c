#include "push_swap.h"

int	is_int_token(const char *s)
{
	int	i;

	i = 0;
	if (s[i] == '+' || s[i] == '-')
		i++;
	if (!s[i])
		return (0);
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

/*
** Acumula em long e verifica o intervalo de int a cada dígito, não
** só ao final: um token de 30 dígitos estouraria o próprio long
** antes do loop terminar.
*/
int	token_to_int(const char *s, int *out)
{
	long	acc;
	int		i;
	int		sign;

	acc = 0;
	sign = 1;
	i = 0;
	if (s[i] == '+' || s[i] == '-')
	{
		if (s[i] == '-')
			sign = -1;
		i++;
	}
	while (s[i])
	{
		acc = acc * 10 + (s[i] - '0');
		if (acc * sign > 2147483647 || acc * sign < -2147483648)
			return (0);
		i++;
	}
	*out = (int)(acc * sign);
	return (1);
}

int	has_duplicates(t_stack *s)
{
	int	i;
	int	j;

	i = 0;
	while (i < s->size)
	{
		j = i + 1;
		while (j < s->size)
		{
			if (s->data[i] == s->data[j])
				return (1);
			j++;
		}
		i++;
	}
	return (0);
}

void	free_split(char **parts)
{
	int	i;

	if (!parts)
		return ;
	i = 0;
	while (parts[i])
	{
		free(parts[i]);
		i++;
	}
	free(parts);
}

/*
** O tamanho do literal mais um inclui o terminador, então
** "--simpleX" não é aceito como prefixo.
*/
int	flag_id(const char *s)
{
	if (!ft_strncmp(s, "--simple", 9))
		return (STRAT_SIMPLE);
	if (!ft_strncmp(s, "--medium", 9))
		return (STRAT_MEDIUM);
	if (!ft_strncmp(s, "--complex", 10))
		return (STRAT_COMPLEX);
	if (!ft_strncmp(s, "--adaptive", 11))
		return (STRAT_ADAPTIVE);
	if (!ft_strncmp(s, "--bench", 8))
		return (FLAG_BENCH);
	return (0);
}
