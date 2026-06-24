/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 19:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 19:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	**ft_split(char const *s, char c);

static char	*heapdup(const char *s)
{
	size_t	n;
	char	*d;

	n = strlen(s) + 1;
	d = malloc(n);
	if (d)
		memcpy(d, s, n);
	return (d);
}

/* Compara o array de ft_split com o esperado: mesma quantidade de palavras,
   mesmo conteudo, e terminado em NULL no lugar certo. */
static int	cmp_split(char **got, char **exp)
{
	int	i;

	if (got == NULL)
		return (0);
	i = 0;
	while (exp[i] != NULL)
	{
		if (got[i] == NULL || strcmp(got[i], exp[i]) != 0)
			return (0);
		i++;
	}
	return (got[i] == NULL);
}

static void	free_split(char **arr)
{
	int	i;

	i = 0;
	if (arr == NULL)
		return ;
	while (arr[i] != NULL)
	{
		free(arr[i]);
		i++;
	}
	free(arr);
}

static void	print_arr(char **arr)
{
	int	i;

	if (arr == NULL)
	{
		printf("NULL");
		return ;
	}
	i = 0;
	printf("[");
	while (arr[i] != NULL)
	{
		if (i > 0)
			printf(",");
		printf("\"%s\"", arr[i]);
		i++;
	}
	printf("]");
}

int	main(void)
{
	/* delimitadores consecutivos/nas pontas -> SEM strings vazias.
	   "" -> [NULL]; tudo delimitador -> [NULL]; sem delimitador -> [s].
	   Array termina em NULL. Rode com asan/valgrind (make split ja faz)
	   p/ leaks e o free parcial em falha de malloc no meio. */
	static char	*e0[] = {"hello", "world", NULL};
	static char	*e1[] = {"a", "b", NULL};
	static char	*e2[] = {NULL};
	static char	*e3[] = {"hello", NULL};
	static char	*e4[] = {"42", "Sao", "Paulo", NULL};
	static char	*e5[] = {"spaced", "words", NULL};
	struct s_caso
	{
		char const	*s;
		char		c;
		char		**esperado;
	}	casos[] = {
	{"", ' ', e2}, {"hello world", ' ', e0}, {"a,,b", ',', e1}, {",a,b,", ',', e1},
	{"", ' ', e2}, {"xxx", 'x', e2}, {"a", 'a', e2}, {"hello", ',', e3},
	{"42 Sao Paulo", ' ', e4}, {"   spaced   words   ", ' ', e5},
	{"split,by,comma", ',', (char *[]){"split", "by", "comma", NULL}}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*src;
	char	**got;

	i = 0;
	falhas = 0;
	printf("<ft_split>\n");
	while (i < n)
	{
		src = heapdup(casos[i].s);
		got = ft_split(src, casos[i].c);
		if (!cmp_split(got, casos[i].esperado))
		{
			printf("FALHA s=\"%s\" c='%c' : ft=", casos[i].s, casos[i].c);
			print_arr(got);
			printf(" esperado=");
			print_arr(casos[i].esperado);
			printf("\n");
			falhas++;
		}
		free_split(got);
		free(src);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_split>\n");
	return (falhas != 0);
}
