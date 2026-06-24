/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memmove.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 13:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 13:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

#define BUF 32

void	*ft_memmove(void *dst, const void *src, size_t n);

/* Indice do 1o byte diferente entre a e b (ou -1 se iguais), p/ debug. */
static int	first_diff(unsigned char *a, unsigned char *b, int n)
{
	int	k;

	k = 0;
	while (k < n)
	{
		if (a[k] != b[k])
			return (k);
		k++;
	}
	return (-1);
}

int	main(void)
{
	/* Cada caso: {dst_off, src_off, n} dentro de UM mesmo buffer.
	   O que pega memmove (e quebra um memcpy ingenuo):
	     - dst > src (overlap p/ frente): copia ingenua p/ frente CORROMPE
	       -> memmove tem que copiar de tras p/ frente.
	     - dst < src (overlap p/ tras): copia p/ frente funciona.
	   Tambem testamos dst==src, sem overlap, e n=0.
	   Referencia = memmove da libc; comparamos buffer INTEIRO + retorno. */
	struct s_caso
	{
		size_t	dst_off;
		size_t	src_off;
		size_t	n;
	}	casos[] = {
	{2, 0, 6}, {0, 2, 6}, {4, 1, 10}, {1, 4, 10}, {3, 3, 5},
	{0, 16, 8}, {16, 0, 8}, {0, 0, 0}, {5, 5, 0}, {0, 1, 31},
	{1, 0, 31}, {10, 8, 12}};
	int				n = sizeof(casos) / sizeof(casos[0]);
	int				i;
	int				k;
	int				falhas;
	int				d;
	unsigned char	a[BUF];
	unsigned char	b[BUF];
	void			*r_ft;
	void			*r_bsd;

	i = 0;
	falhas = 0;
	printf("<ft_memmove>\n");
	while (i < n)
	{
		k = 0;
		while (k < BUF)
		{
			a[k] = (unsigned char)('A' + (k % 26));
			b[k] = a[k];
			k++;
		}
		r_ft = ft_memmove(a + casos[i].dst_off, a + casos[i].src_off,
				casos[i].n);
		r_bsd = memmove(b + casos[i].dst_off, b + casos[i].src_off,
				casos[i].n);
		d = first_diff(a, b, BUF);
		if (r_ft != (void *)(a + casos[i].dst_off)
			|| r_bsd != (void *)(b + casos[i].dst_off) || d != -1)
		{
			printf("FALHA dst_off=%zu src_off=%zu n=%zu : ret_ok=%d | "
				"1o byte diff idx=%d (ft=%d bsd=%d)\n", casos[i].dst_off,
				casos[i].src_off, casos[i].n,
				(r_ft == (void *)(a + casos[i].dst_off)), d,
				d == -1 ? -1 : a[d], d == -1 ? -1 : b[d]);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_memmove>\n");
	return (falhas != 0);
}
