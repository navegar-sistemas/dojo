/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   atoi.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 15:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 15:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>

int	ft_atoi(const char *str);

int	main(void)
{
	/* Comparamos contra a atoi da libc. Regras da atoi:
	   - pula espacos iniciais (' ' \t \n \v \f \r);
	   - UM sinal opcional (+ ou -);
	   - digitos ate o 1o nao-digito (resto e ignorado).
	   Casos cobrem: espacos/whitespace variado, sinais, lixo no fim,
	   sinal duplo ("+-5" -> 0), zeros a esquerda, INT_MAX/INT_MIN exatos.
	   NAO testamos overflow (ex.: "9999999999") -> e UB na atoi. */
	const char	*casos[] = {
	"42", "   42", "-42", "+42", "  -42abc", "0", "", "abc",
	"\t\n\v\f\r 123", " 1 2 3", "2147483647", "-2147483648",
	"+-5", "-+5", "   +007", "-0", "+0", "007abc", "   -2147483648",
	"  +2147483647", "z123", "  ", "123 456", "++42", "--42", "+ 42"};
	int	n = sizeof(casos) / sizeof(casos[0]);
	int	i;
	int	falhas;

	i = 0;
	falhas = 0;
	printf("<ft_atoi>\n");
	while (i < n)
	{
		int	r_ft = ft_atoi(casos[i]);
		int	r_libc = atoi(casos[i]);
		if (r_ft != r_libc)
		{
			printf("FALHA caso %d \"%s\" : ft=%d  libc=%d\n",
				i, casos[i], r_ft, r_libc);
			falhas++;
		}
		i++;
	}
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_atoi>\n");
	return (falhas != 0);
}
