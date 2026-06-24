/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strjoin.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 18:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 18:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_strjoin(char const *s1, char const *s2);

/* Copia s p/ buffer no HEAP de tamanho EXATO -> over-read de s1/s2 vira
   erro detectavel (valgrind/asan). */
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

int	main(void)
{
	/* {s1, s2, esperado}. ft_strjoin ALOCA: free() + checar NULL.
	   Pegadinhas: esquecer o '+1' do '\0' (over-write no result),
	   trocar a ordem, ou nao tratar s vazio.
	   Rode com asan/valgrind (make strjoin ja faz) p/ o over-write. */
	struct s_caso
	{
		char const	*s1;
		char const	*s2;
		char const	*esperado;
	}	casos[] = {
	{"Hello, ", "World!", "Hello, World!"}, {"", "abc", "abc"},
	{"abc", "", "abc"}, {"", "", ""}, {"42", "Sao Paulo", "42Sao Paulo"},
	{"a", "b", "ab"}, {"foo", "bar", "foobar"},
	{"with ", "spaces here", "with spaces here"},
	{"AAAAAAAAAA", "BBBBBBBBBB", "AAAAAAAAAABBBBBBBBBB"}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*a;
	char	*b;
	char	*got;

	i = 0;
	falhas = 0;
	printf("<ft_strjoin>\n");
	while (i < n)
	{
		a = heapdup(casos[i].s1);
		b = heapdup(casos[i].s2);
		got = ft_strjoin(a, b);
		if (got == NULL)
			(printf("FALHA \"%s\"+\"%s\" : NULL\n", casos[i].s1,
					casos[i].s2), falhas++);
		else if (strcmp(got, casos[i].esperado) != 0)
			(printf("FALHA \"%s\"+\"%s\" : ft=\"%s\" esperado=\"%s\"\n",
					casos[i].s1, casos[i].s2, got, casos[i].esperado),
				falhas++);
		free(got);
		free(a);
		free(b);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strjoin>\n");
	return (falhas != 0);
}
