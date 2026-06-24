/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strlcat.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 11:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 11:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>
#include <bsd/string.h>

#define BUF 32

size_t	ft_strlcat(char *dst, const char *src, size_t size);

int	main(void)
{
	/* Cada caso: {dst_inicial, src, size}.
	   strlcat e APPEND: o buffer ja contem dst_inicial (+ '\0') antes da
	   chamada. Comparamos contra a strlcat da libbsd em DOIS quesitos:
	     1) retorno: deve ser strlen(dst_inicial) + strlen(src) -- com o
	        caso especial: se size <= strlen(dst), o "dlen" vira size e o
	        retorno e size + strlen(src) (nao acha '\0' dentro de size).
	     2) o buffer INTEIRO (BUF bytes): pre-preenchido com '#' alem do
	        conteudo, p/ pegar overflow ou falta de '\0'.

	   size > strlen(dst): append normal, trunca se faltar espaco.
	   size == strlen(dst): nao cabe nada -> dst intacto, ret size+slen(src).
	   size < strlen(dst): idem, "buffer cheio" -> nao escreve.
	   size == 0: nao escreve, retorna strlen(src). */
	struct s_caso
	{
		const char	*dst0;
		const char	*src;
		size_t		size;
	}	casos[] = {
	{"Hello ", "World", 11}, {"Hello ", "World", 32}, {"Hello ", "World", 12}, 
	{"Hello ", "World", 8}, {"Hello ", "World", 7}, {"Hello ", "World", 6},
	{"Hello ", "World", 5}, {"Hello ", "World", 3}, {"Hello ", "World", 0},
	{"", "abc", 5}, {"", "abc", 1}, {"", "abc", 0}, {"", "", 5},
	{"abc", "", 8}, {"abc", "", 3}, {"abc", "", 0}, {"abc", "", 2},
	{"foo", "bar", 7}, {"foo", "bar", 6}, {"foo", "bar", 4},
	{"42 ", "Sao Paulo", 32}, {"42 ", "Sao Paulo", 9}, {"xyz", "abc", 1}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	a[BUF];
	char	b[BUF];
	size_t	dl;
	size_t	r_ft;
	size_t	r_bsd;

	i = 0;
	falhas = 0;
	printf("<ft_strlcat>\n");
	while (i < n)
	{
		dl = strlen(casos[i].dst0);
		memset(a, '#', BUF);
		memset(b, '#', BUF);
		memcpy(a, casos[i].dst0, dl + 1);
		memcpy(b, casos[i].dst0, dl + 1);
		r_ft = ft_strlcat(a, casos[i].src, casos[i].size);
		r_bsd = strlcat(b, casos[i].src, casos[i].size);
		if (r_ft != r_bsd || memcmp(a, b, BUF) != 0)
		{
			printf("FALHA dst=\"%s\" src=\"%s\" size=%zu : ret ft=%zu "
				"bsd=%zu | buf ft=\"%.*s\" bsd=\"%.*s\"\n",
				casos[i].dst0, casos[i].src, casos[i].size, r_ft, r_bsd,
				BUF, a, BUF, b);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strlcat>\n");
	return (falhas != 0);
}
