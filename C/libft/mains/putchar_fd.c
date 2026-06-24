/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   putchar_fd.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 12:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 12:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

void	ft_putchar_fd(char c, int fd);

/* Escreve c num arquivo temporario via ft_putchar_fd, rebobina e le de
   volta. Confere que (1) o byte lido == c e (2) escreveu EXATAMENTE 1 byte
   (le ate 2; tem que vir 1). Pega "escreveu char errado" e "escreveu demais". */
static int	check_char(char c)
{
	int		fd;
	char	buf[2];
	ssize_t	n;

	fd = open("putchar_tmp.txt", O_CREAT | O_TRUNC | O_RDWR, 0644);
	if (fd < 0)
		return (-1);
	ft_putchar_fd(c, fd);
	lseek(fd, 0, SEEK_SET);
	n = read(fd, buf, 2);
	close(fd);
	return (n == 1 && buf[0] == c);
}

int	main(void)
{
	/* Testa varios bytes (letra, digito, espaco, \n, byte alto, \0).
	   ft_putchar_fd deve escrever 1 byte exato no fd. */
	char	casos[] = {'A', 'z', '0', ' ', '\n', '\t', (char)200, '\0'};
	int		n = sizeof(casos) / sizeof(casos[0]);
	int		i;
	int		falhas;
	int		r;

	i = 0;
	falhas = 0;
	printf("<ft_putchar_fd>\n");
	while (i < n)
	{
		r = check_char(casos[i]);
		if (r < 0)
			(printf("ERRO: nao abriu o arquivo temporario\n"), falhas++);
		else if (r == 0)
			(printf("FALHA c=%d ('%c') : byte lido != escrito ou tamanho != 1\n",
					casos[i], casos[i]), falhas++);
		i++;
	}
	unlink("putchar_tmp.txt");
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_putchar_fd>\n");
	return (falhas != 0);
}
