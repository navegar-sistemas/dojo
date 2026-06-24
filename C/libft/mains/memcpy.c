/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memcpy.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 13:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 13:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

#define BUF 32

void	*ft_memcpy(void *dst, const void *src, size_t n);

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
	/* src tem um '\0' no meio (idx 5) DE PROPOSITO: memcpy copia bytes
	   crus, entao tem que copiar ALEM do '\0' (diferente de strcpy).
	   Para cada n: comparamos contra a memcpy da libc em 2 quesitos:
	     1) retorno = o proprio ponteiro dst;
	     2) buffer INTEIRO: primeiros n bytes copiados, resto ('#') intacto.
	   n=0: nada copiado, buffer todo '#'. Caso extra: (NULL,NULL,0). */
	size_t			casos[] = {0, 1, 2, 5, 6, 8, 16, 32};
	int				n = sizeof(casos) / sizeof(casos[0]);
	int				i;
	int				k;
	int				falhas;
	int				d;
	unsigned char	src[BUF];
	unsigned char	a[BUF];
	unsigned char	b[BUF];
	void			*r_ft;
	void			*r_bsd;

	k = 0;
	while (k < BUF)
	{
		src[k] = (unsigned char)('A' + (k % 26));
		k++;
	}
	src[5] = 0;
	i = 0;
	falhas = 0;
	printf("<ft_memcpy>\n");
	while (i < n)
	{
		memset(a, '#', BUF);
		memset(b, '#', BUF);
		r_ft = ft_memcpy(a, src, casos[i]);
		r_bsd = memcpy(b, src, casos[i]);
		d = first_diff(a, b, BUF);
		if (r_ft != (void *)a || r_bsd != (void *)b || d != -1)
		{
			printf("FALHA n=%zu : ret_ok=%d | 1o byte diff idx=%d "
				"(ft=%d bsd=%d)\n", casos[i], (r_ft == (void *)a), d,
				d == -1 ? -1 : a[d], d == -1 ? -1 : b[d]);
			falhas++;
		}
		i++;
	}
	if (ft_memcpy(NULL, NULL, 0) != NULL)
	{
		printf("FALHA (NULL, NULL, 0) deveria retornar NULL\n");
		falhas++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_memcpy>\n");
	return (falhas != 0);
}
