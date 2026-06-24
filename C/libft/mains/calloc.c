/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   calloc.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 16:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void	*ft_calloc(size_t nmemb, size_t size);

static int	all_zero(unsigned char *p, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		if (p[i] != 0)
			return (0);
		i++;
	}
	return (1);
}

int	main(void)
{
	/* 3 categorias auto-classificadas a partir de {nmemb,size}:
	   - OVERFLOW (nmemb*size estoura size_t): DEVE retornar NULL (guarda).
	     casos onde o produto "da a volta" p/ um valor pequeno (ex.
	     SIZE_MAX*SIZE_MAX -> 1) forcam a guarda: sem ela, malloc(1) da
	     non-NULL e o teste pega.
	   - ZERO (nmemb==0 || size==0): ponteiro LIBERAVEL (NULL ou nao,
	     ambos validos p/ free) -> so checamos que da free sem crashar.
	   - NORMAL: non-NULL E todos os nmemb*size bytes == 0. (Tamanhos
	     pequenos que sempre alocam; SIZE_MAX bytes legitimamente falha.) */
	struct s_caso
	{
		size_t	nmemb;
		size_t	size;
	}	casos[] = {
	{1, 1}, {10, 1}, {1, 10}, {5, 4}, {100, 8}, {1, sizeof(int)},
	{256, 1}, {3, 7}, {1000, 1},
	{0, 0}, {0, 10}, {10, 0}, {0, 1}, {1, 0},
	{SIZE_MAX, SIZE_MAX}, {2, SIZE_MAX / 2 + 2},
	{SIZE_MAX / 4 + 1, 4}, {SIZE_MAX, 3}};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	int		overflow;
	void	*p;
	void	*lc;
	size_t	nm;
	size_t	sz;

	i = 0;
	falhas = 0;
	printf("<ft_calloc>\n");
	while (i < n)
	{
		nm = casos[i].nmemb;
		sz = casos[i].size;
		overflow = (sz != 0 && nm > SIZE_MAX / sz);
		p = ft_calloc(nm, sz);
		if (overflow)
		{
			if (p != NULL)
			{
				printf("FALHA nmemb=%zu size=%zu : overflow deveria dar "
					"NULL (guarda ausente)\n", nm, sz);
				falhas++;
			}
			free(p);
		}
		else if (nm == 0 || sz == 0)
		{
			lc = calloc(nm, sz);
			if ((p == NULL) != (lc == NULL))
				printf("NOTA nmemb=%zu size=%zu : ft=%s libc=%s "
					"(ambos validos p/ free)\n", nm, sz,
					p ? "ptr" : "NULL", lc ? "ptr" : "NULL");
			free(p);
			free(lc);
		}
		else
		{
			if (p == NULL)
			{
				printf("FALHA nmemb=%zu size=%zu : NULL numa alocacao "
					"valida\n", nm, sz);
				falhas++;
			}
			else if (!all_zero(p, nm * sz))
			{
				printf("FALHA nmemb=%zu size=%zu : memoria NAO zerada\n",
					nm, sz);
				falhas++;
			}
			free(p);
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_calloc>\n");
	return (falhas != 0);
}
