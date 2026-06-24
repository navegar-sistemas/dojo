/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memset.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 12:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 12:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

#define BUF 32

void	*ft_memset(void *b, int c, size_t len);

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
	/* Cada caso: {c, len}.
	   c e cortado p/ unsigned char: 256 -> 0, -1 -> 255, 0xAB -> 171.
	   Comparamos contra a memset da libc em DOIS quesitos:
	     1) retorno deve ser O PROPRIO ponteiro recebido (b);
	     2) o buffer INTEIRO (BUF): os primeiros len bytes viram c, e o
	        resto (sentinela '#') NAO pode ser tocado (escrita alem de len).
	   len=0: nao escreve nada, buffer fica todo '#'. */
	struct s_caso
	{
		int		c;
		size_t	len;
	}	casos[] = {
	{'A', 32}, {'A', 10}, {'A', 1}, {'A', 0}, {0, 16}, {255, 16},
	{256, 16}, {-1, 16}, {0xAB, 32}, {'Z', 31}, {'x', 0}, {127, 8},
	{128, 8}, {'\n', 5}};
	int				n = sizeof(casos) / sizeof(casos[0]);
	int				i;
	int				falhas;
	int				d;
	unsigned char	a[BUF];
	unsigned char	b[BUF];
	void			*r_ft;
	void			*r_bsd;

	i = 0;
	falhas = 0;
	printf("<ft_memset>\n");
	while (i < n)
	{
		memset(a, '#', BUF);
		memset(b, '#', BUF);
		r_ft = ft_memset(a, casos[i].c, casos[i].len);
		r_bsd = memset(b, casos[i].c, casos[i].len);
		d = first_diff(a, b, BUF);
		if (r_ft != (void *)a || r_bsd != (void *)b || d != -1)
		{
			printf("FALHA c=%d len=%zu : ret_ok=%d | 1o byte diff idx=%d "
				"(ft=%d bsd=%d)\n", casos[i].c, casos[i].len,
				(r_ft == (void *)a), d,
				d == -1 ? -1 : a[d], d == -1 ? -1 : b[d]);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_memset>\n");
	return (falhas != 0);
}
