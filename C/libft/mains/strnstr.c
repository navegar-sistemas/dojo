/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strnstr.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/20 10:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/20 10:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <bsd/string.h>

char	*ft_strnstr(const char *big, const char *little, size_t len);

int	main(void)
{
	const char	*big = "Foo Bar Baz Bar";

	/* Cada caso: {big, little, len}.
	   little="": deve retornar big (ponteiro de inicio).
	   ocorrencia alem de len: trunca -> NULL mesmo "existindo" depois.
	   len exatamente cobrindo o fim do match: limite inferior do achar. */
	struct s_caso
	{
		const char	*big;
		const char	*little;
		size_t		len;
	}	casos[] = {
	{big, "Bar", 6}, {big, "", 0}, {big, "", 15}, {big, "", 3},
	{big, "Bar", 15}, {big, "Bar", 7},
	{big, "Bar", 5}, {big, "Baz", 15}, {big, "Baz", 10},
	{big, "Foo", 3}, {big, "Foo", 2}, {big, "Foo", 0},
	{big, "Bar Baz", 15}, {big, "Bar Baz", 11}, {big, "Bar Baz", 10},
	{big, "xyz", 15}, {big, "Foo Bar Baz Bar", 15},
	{big, "Foo Bar Baz Bar!", 15}, {big, "r", 15},
	{"", "", 0}, {"", "", 5}, {"", "a", 5},
	{"aaaa", "aa", 4}, {"aaaa", "aaaaa", 4}, {big, "BAR", 15}};
	int	n = sizeof(casos) / sizeof(casos[0]);
	int	i;
	int	falhas;

	i = 0;
	falhas = 0;
	printf("<ft_strnstr>\n");
	while (i < n)
	{
		char	*r_ft = ft_strnstr(casos[i].big, casos[i].little, casos[i].len);
		char	*r_bsd = strnstr(casos[i].big, casos[i].little, casos[i].len);
		if (r_ft != r_bsd)
		{
			printf("FALHA big=\"%s\" little=\"%s\" len=%zu : ft=%p  bsd=%p\n",
				casos[i].big, casos[i].little, casos[i].len,
				(void *)r_ft, (void *)r_bsd);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strnstr>\n");
	return (falhas != 0);
}
