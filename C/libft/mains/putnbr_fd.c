/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   putnbr_fd.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 16:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 16:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>

void	ft_putnbr_fd(int n, int fd);

/* Escreve n via ft_putnbr_fd num arquivo temp, rebobina e le de volta.
   O esperado e o que o snprintf("%d") produz: so os digitos (e o '-' nos
   negativos), SEM '\n' no fim. Confere tamanho exato + conteudo byte a byte.
   Pega: INT_MIN errado, sinal faltando, digito trocado, '\n' a mais. */
static int	check_nbr(int n)
{
	int		fd;
	char	buf[32];
	char	esperado[32];
	ssize_t	r;
	size_t	len;

	len = (size_t)snprintf(esperado, sizeof(esperado), "%d", n);
	fd = open("putnbr_tmp.txt", O_CREAT | O_TRUNC | O_RDWR, 0644);
	if (fd < 0)
		return (-1);
	ft_putnbr_fd(n, fd);
	lseek(fd, 0, SEEK_SET);
	r = read(fd, buf, sizeof(buf));
	close(fd);
	return (r == (ssize_t)len && memcmp(buf, esperado, len) == 0);
}

int	main(void)
{
	/* 0, 1 digito, multi digito, negativos, e os extremos do int.
	   INT_MIN (-2147483648) e o caso que mata quem faz -n direto. */
	int	casos[] = {9, 7, -7, 42, -42, 9, -9, 100, -100, 12345, -12345,
		1000000000, -1000000000, INT_MAX, INT_MIN};
	int	n = sizeof(casos) / sizeof(casos[0]);
	int	i;
	int	falhas;
	int	res;

	i = 0;
	falhas = 0;
	printf("<ft_putnbr_fd>\n");
	while (i < n)
	{
		res = check_nbr(casos[i]);
		if (res < 0)
			(printf("ERRO: nao abriu o arquivo temporario\n"), falhas++);
		else if (res == 0)
			(printf("FALHA n=%d : tamanho ou conteudo escrito errado\n",
					casos[i]), falhas++);
		i++;
	}
	unlink("putnbr_tmp.txt");
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_putnbr_fd>\n");
	return (falhas != 0);
}
