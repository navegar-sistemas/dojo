/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strlcpy.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 10:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 10:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>
#include <bsd/string.h>

#define BUF 32

size_t	ft_strlcpy(char *dst, const char *src, size_t size);

int	main(void)
{
	/* Cada caso: {src, size}.
	   Comparamos contra a strlcpy da libbsd em DOIS quesitos:
	     1) retorno (deve ser strlen(src), independente de size);
	     2) o buffer INTEIRO (BUF bytes), nao so ate size.
	   O buffer e pre-preenchido com '#' (sentinela): assim, se a ft
	   escrever alem de size (overflow) ou nao terminar com '\0' quando
	   devia, o memcmp do buffer todo acusa a diferenca contra a libc.

	   size=0: nao escreve nada, buffer fica intacto, retorna strlen(src).
	   size < strlen(src): trunca p/ size-1 chars + '\0'.
	   size == strlen(src)+1: cabe exatamente.
	   size=1: so escreve o '\0'. */
	struct s_caso
	{
		const char	*src;
		size_t		size;
	}	casos[] = {
	{"hello", 5}, {"hello", 32}, {"hello", 6}, {"hello", 3},
	{"hello", 1}, {"hello", 0}, {"", 32}, {"", 1}, {"", 0},
	{"abc", 4}, {"abc", 3}, {"42 Sao Paulo", 32}, {"42 Sao Paulo", 8},
	{"42 Sao Paulo", 13}, {"42 Sao Paulo", 12}, {"x", 32}, {"x", 2},
	{"x", 1}, {"x", 0}, {"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 32}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	a[BUF];
	char	b[BUF];
	size_t	r_ft;
	size_t	r_bsd;

	i = 0;
	falhas = 0;
	printf("<ft_strlcpy>\n");
	while (i < n)
	{
		memset(a, '#', BUF);
		memset(b, '#', BUF);
		r_ft = ft_strlcpy(a, casos[i].src, casos[i].size);
		r_bsd = strlcpy(b, casos[i].src, casos[i].size);
		if (r_ft != r_bsd || memcmp(a, b, BUF) != 0)
		{
			printf("FALHA src=\"%s\" size=%zu : ret ft=%zu bsd=%zu | "
				"buf ft=\"%.*s\" bsd=\"%.*s\"\n",
				casos[i].src, casos[i].size, r_ft, r_bsd,
				BUF, a, BUF, b);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strlcpy>\n");
	return (falhas != 0);
}
