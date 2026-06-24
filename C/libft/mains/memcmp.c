/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memcmp.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 14:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 14:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

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

int	ft_memcmp(const void *s1, const void *s2, size_t n);

/* memcmp le n bytes CRUS: NAO para no '\0' (ao contrario de strncmp). Logo
   n nunca pode exceder o tamanho dos buffers -- pedir alem disso e leitura
   invalida (UB) que nem a libc sobrevive sob AddressSanitizer. Para exercitar
   "n grande, muitos bytes iguais" de forma VALIDA, usamos buffers locais de
   64 bytes (iguais; iguais nos 60 primeiros; e diferenca no byte 60). */
static int	teste_n_grande(void)
{
	unsigned char	g1[64];
	unsigned char	g2[64];
	int				falhas;

	falhas = 0;
	memset(g1, 'k', 64);
	memset(g2, 'k', 64);
	if (sgn(ft_memcmp(g1, g2, 64)) != 0)
		falhas++;
	if (sgn(ft_memcmp(g1, g2, 60)) != 0)
		falhas++;
	g2[60] = 'z';
	if (sgn(ft_memcmp(g1, g2, 64)) != sgn(memcmp(g1, g2, 64)))
		falhas++;
	if (sgn(ft_memcmp(g1, g2, 60)) != 0)
		falhas++;
	return (falhas);
}

int	main(void)
{
	/* Cada caso: {s1, s2, n}.
	   \200=128, \177=127, \377=255: pegam o cast unsigned char (se voce
	   comparar como signed char, o sinal do retorno inverte -> bug).
	   "ab\0cd": tem '\0' no meio -> memcmp NAO para nele, compara os n
	   bytes crus (diferenca depois do '\0' tem que ser detectada).
	   n menor que a 1a diferenca -> 0. n=0 -> 0. n DENTRO do buffer. */
	struct s_caso
	{
		const char	*s1;
		const char	*s2;
		size_t		n;
	}	casos[] = {
	{"abc", "abc", 3}, {"abc", "abd", 3}, {"abd", "abc", 3},
	{"abc", "abd", 2}, {"hello", "help!", 5}, {"hello", "hello", 5},
	{"ab\0cd", "ab\0ce", 5}, {"ab\0cd", "ab\0cd", 5},
	{"\200", "\177", 1}, {"\177", "\200", 1}, {"\377", "\001", 1},
	{"\001", "\377", 1}, {"abc", "xyz", 0}, {"same", "same", 4}};
	int	n = sizeof(casos) / sizeof(casos[0]);
	int	i;
	int	falhas;

	i = 0;
	falhas = 0;
	printf("<ft_memcmp>\n");
	while (i < n)
	{
		int	r_ft = sgn(ft_memcmp(casos[i].s1, casos[i].s2, casos[i].n));
		int	r_libc = sgn(memcmp(casos[i].s1, casos[i].s2, casos[i].n));
		if (r_ft != r_libc)
		{
			printf("FALHA caso %d (n=%zu) : ft=%d  libc=%d\n",
				i, casos[i].n, r_ft, r_libc);
			falhas++;
		}
		i++;
	}
	falhas += teste_n_grande();
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_memcmp>\n");
	return (falhas != 0);
}
