/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   itoa.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 15:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 15:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

char	*ft_itoa(int n);

int	main(void)
{
	/* Nao existe itoa na libc -> geramos o esperado com snprintf("%d").
	   ft_itoa ALOCA (malloc): precisamos free() em cada retorno e checar
	   NULL (falha de alocacao). Casos criticos:
	     - INT_MIN (-2147483648): 'n = -n' ESTOURA (UB) -> erro classico;
	     - 0 -> "0"; sinais; 1 digito; INT_MAX. */
	int		casos[] = {-1, 0, 1, -1, 7, -7, 42, -42, 100, -100, 10, -10,
		12345, -99999, INT_MAX, INT_MIN};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	char	esperado[16];
	char	*got;

	i = 0;
	falhas = 0;
	printf("<ft_itoa>\n");
	while (i < n)
	{
		snprintf(esperado, sizeof(esperado), "%d", casos[i]);
		got = ft_itoa(casos[i]);
		if (got == NULL)
		{
			printf("FALHA n=%d : ft_itoa retornou NULL\n", casos[i]);
			falhas++;
		}
		else if (strcmp(got, esperado) != 0)
		{
			printf("FALHA n=%d : ft=\"%s\"  esperado=\"%s\"\n",
				casos[i], got, esperado);
			falhas++;
		}
		free(got);
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_itoa>\n");
	return (falhas != 0);
}
