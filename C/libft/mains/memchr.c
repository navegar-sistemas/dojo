/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memchr.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 14:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 14:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

#define BUF 32

void	*ft_memchr(const void *s, int c, size_t n);

int	main(void)
{
	/* buf tem um '\0' no idx 5 e 'Z' no idx 10 DE PROPOSITO:
	   - procurar 0 prova que memchr acha o byte nulo (nao para nele);
	   - 'Z'/'\0' em posicoes conhecidas testam o limite n (acha so se
	     a posicao estiver DENTRO dos n primeiros bytes).
	   c e cortado p/ unsigned char: 256 -> 0 (acha o '\0'); -1 -> 255
	   (nao existe no buf -> NULL).
	   Retorna ponteiro p/ dentro de s, ou NULL. Comparamos PONTEIROS. */
	struct s_caso
	{
		int		c;
		size_t	n;
	}	casos[] = {
	{'A', 32}, {'Z', 32}, {'Z', 11}, {'Z', 10}, {0, 32}, {0, 6},
	{0, 5}, {'A', 0}, {'~', 32}, {256, 32}, {-1, 32}, {'B', 1}, {'B', 2}};
	int				n = sizeof(casos) / sizeof(casos[0]);
	int				i;
	int				k;
	int				falhas;
	unsigned char	buf[BUF];
	void			*r_ft;
	void			*r_bsd;

	k = 0;
	while (k < BUF)
	{
		buf[k] = (unsigned char)('A' + (k % 26));
		k++;
	}
	buf[5] = 0;
	buf[10] = 'Z';
	i = 0;
	falhas = 0;
	printf("<ft_memchr>\n");
	while (i < n)
	{
		r_ft = ft_memchr(buf, casos[i].c, casos[i].n);
		r_bsd = memchr(buf, casos[i].c, casos[i].n);
		if (r_ft != r_bsd)
		{
			printf("FALHA c=%d n=%zu : ft=%p bsd=%p\n",
				casos[i].c, casos[i].n, r_ft, r_bsd);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_memchr>\n");
	return (falhas != 0);
}
