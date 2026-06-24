/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strtrim.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 18:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 18:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_strtrim(char const *s1, char const *set);

/* Fontes no HEAP (tamanho exato) -> over-read de s1/set vira erro
   detectavel (valgrind/asan). */
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
	/* {s1, set, esperado}. ft_strtrim ALOCA: free() + checar NULL.
	   Regras: corta set so do INICIO e FIM; meio intacto; tudo set -> "";
	   set vazio -> copia de s1; s1 vazio -> "". */
	struct s_caso
	{
		char const	*s1;
		char const	*set;
		char const	*esperado;
	}	casos[] = {
	{"  hi  there  ", " ", "hi  there"}, {"   hello   ", " ", "hello"}, {"xxhelloxx", "x", "hello"},
	{"hello", "x", "hello"}, {"xxxxx", "x", ""}, {"", "x", ""},
	{"hello", "", "hello"}, {"  hi  there  ", " ", "hi  there"},
	{"aabbccbbaa", "ab", "cc"}, {"\t\n hello \n\t", " \t\n", "hello"},
	{"42", "0123456789", ""}, {"abc", "abc", ""}, {"banana", "an", "b"}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*a;
	char	*b;
	char	*got;

	i = 0;
	falhas = 0;
	printf("<ft_strtrim>\n");
	while (i < n)
	{
		a = heapdup(casos[i].s1);
		b = heapdup(casos[i].set);
		got = ft_strtrim(a, b);
		if (got == NULL)
			(printf("FALHA s1=\"%s\" set=\"%s\" : NULL\n", casos[i].s1,
					casos[i].set), falhas++);
		else if (strcmp(got, casos[i].esperado) != 0)
			(printf("FALHA s1=\"%s\" set=\"%s\" : ft=\"%s\" esperado=\"%s\"\n",
					casos[i].s1, casos[i].set, got, casos[i].esperado),
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
	printf("</ft_strtrim>\n");
	return (falhas != 0);
}
