/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strncmp.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/19 17:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/19 17:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

int	ft_strncmp(const char *s1, const char *s2, size_t n);

/* O padrao garante apenas o SINAL do retorno, nao o valor exato:
   normalizamos p/ -1/0/1 antes de comparar ft contra a libc. */
static int	sgn(int v)
{
	if (v < 0)
		return (-1);
	if (v > 0)
		return (1);
	return (0);
}

int	main(void)
{
	/* Cada caso: {s1, s2, n}. \201 = byte 129: pega o cast unsigned char.
	   prefixo ("ab" vs "abc"): pega o bug do && no while.
	   n=0: sempre 0. n alem do '\0': nao pode ler lixo apos terminador. */
	struct s_caso
	{
		const char	*s1;
		const char	*s2;
		size_t		n;
	}	casos[] = {
	{"", "", 1}, {"", "a", 1}, {"a", "", 1},
	{"abc", "abc", 3}, {"abc", "abc", 10}, {"abc", "abc", 0},
	{"ab", "abc", 3}, {"abc", "ab", 3}, {"ab", "abc", 2},
	{"abc", "abd", 5}, {"abd", "abc", 5}, {"abc", "abd", 2},
	{"\201", "A", 1}, {"A", "\201", 1}, {"\377", "\001", 1},
	{"hello", "world", 5}, {"42São", "42Sao", 5},
	{"abcXYZ", "abcQRS", 3}, {"abcXYZ", "abcQRS", 4},
	{"same", "same", 100}, {"", "", 0},
	{"\377", "", 1}, {"", "\377", 1}};
	int	n = sizeof(casos) / sizeof(casos[0]);
	int	i;
	int	falhas;

	i = 0;
	falhas = 0;
	printf("<ft_strncmp>\n");
	while (i < n)
	{
		int	r_ft = sgn(ft_strncmp(casos[i].s1, casos[i].s2, casos[i].n));
		int	r_libc = sgn(strncmp(casos[i].s1, casos[i].s2, casos[i].n));
		if (r_ft != r_libc)
		{
			printf("FALHA s1=\"%s\" s2=\"%s\" n=%zu : ft=%d  libc=%d\n",
				casos[i].s1, casos[i].s2, casos[i].n, r_ft, r_libc);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_strncmp>\n");
	return (falhas != 0);
}
