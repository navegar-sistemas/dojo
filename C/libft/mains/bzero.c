/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bzero.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 12:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 12:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

#define BUF 32

void	ft_bzero(void *s, size_t n);

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
	/* Cada caso: {n}. bzero(s, n) == memset(s, 0, n): zera n bytes.
	   Referencia = memset(.., 0, ..) da libc (bzero e descontinuada).
	   bzero retorna void -> so comparamos o BUFFER:
	     - os primeiros n bytes viram 0;
	     - o resto (sentinela '#') NAO pode ser tocado (escrita alem de n).
	   n=0: nao escreve nada, buffer fica todo '#'. */
	size_t			casos[] = {0, 1, 5, 8, 10, 16, 31, 32};
	int				n = sizeof(casos) / sizeof(casos[0]);
	int				i;
	int				falhas;
	int				d;
	unsigned char	a[BUF];
	unsigned char	b[BUF];

	i = 0;
	falhas = 0;
	printf("<ft_bzero>\n");
	while (i < n)
	{
		memset(a, '#', BUF);
		memset(b, '#', BUF);
		ft_bzero(a, casos[i]);
		memset(b, 0, casos[i]);
		d = first_diff(a, b, BUF);
		if (d != -1)
		{
			printf("FALHA n=%zu : 1o byte diff idx=%d (ft=%d ref=%d)\n",
				casos[i], d, a[d], b[d]);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_bzero>\n");
	return (falhas != 0);
}
