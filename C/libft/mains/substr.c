/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   substr.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 17:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 17:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	*ft_substr(char const *s, unsigned int start, size_t len);

/* Copia s p/ um buffer no HEAP de tamanho EXATO (strlen+1). Assim, se o
   ft_substr ler alem do fim de s (falta de clamp, ou start alem do fim),
   vira over-read no heap -> valgrind PEGA. Com string literal (memoria
   estatica) o valgrind nao pegaria; so o ASan. */
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
	/* {s, start, len, esperado}. ft_substr ALOCA: free() + checar NULL.
	   Rode tambem sob valgrind: cobre o over-read (len sem clamp / start
	   alem do fim) que a comparacao de conteudo sozinha nao ve. */
	struct s_caso
	{
		char const		*s;
		unsigned int	start;
		size_t			len;
		char const		*esperado;
	}	casos[] = {
	{"hello world", 6, 5, "world"}, {"hello world", 0, 5, "hello"},
	{"hello", 3, 100, "lo"}, {"hello", 0, 5, "hello"},
	{"hello", 0, 100, "hello"}, {"hello", 10, 5, ""},
	{"hello", 5, 3, ""}, {"hello", 2, 0, ""}, {"", 0, 5, ""},
	{"42 Sao Paulo", 3, 3, "Sao"}, {"abcdef", 2, 3, "cde"},
	{"abc", 1, 10, "bc"}, {"abcdef", 0, 0, ""}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	*src;
	char	*got;

	i = 0;
	falhas = 0;
	printf("<ft_substr>\n");
	while (i < n)
	{
		src = heapdup(casos[i].s);
		got = ft_substr(src, casos[i].start, casos[i].len);
		if (got == NULL)
		{
			printf("FALHA s=\"%s\" start=%u len=%zu : retornou NULL "
				"(esperado \"%s\" alocado)\n", casos[i].s, casos[i].start,
				casos[i].len, casos[i].esperado);
			falhas++;
		}
		else if (strcmp(got, casos[i].esperado) != 0)
		{
			printf("FALHA s=\"%s\" start=%u len=%zu : ft=\"%s\" "
				"esperado=\"%s\"\n", casos[i].s, casos[i].start,
				casos[i].len, got, casos[i].esperado);
			falhas++;
		}
		free(got);
		free(src);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_substr>\n");
	return (falhas != 0);
}
