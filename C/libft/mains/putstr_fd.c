/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   putstr_fd.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 12:30:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 12:30:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

void	ft_putstr_fd(char *s, int fd);

/* Fonte no HEAP de tamanho exato -> se a funcao ler alem do '\0'
   (escrever demais), o asan pega o over-read. */
static char	*heapdup(const char *s)
{
	size_t	n;
	char	*d;

	n = strlen(s) + 1;
	d = malloc(n);
	if (d)
		memcpy(d, s, n);
	return (d);
}

/* Escreve s num arquivo temp via ft_putstr_fd, rebobina e le de volta.
   Confere (1) escreveu strlen(s) bytes (nem mais, nem menos) e
   (2) o conteudo bate byte a byte. s==NULL -> escreve nada (0 bytes). */
static int	check_str(const char *original)
{
	int		fd;
	char	buf[512];
	ssize_t	n;
	char	*src;
	size_t	len;

	src = NULL;
	len = 0;
	if (original)
	{
		src = heapdup(original);
		len = strlen(original);
	}
	fd = open("putstr_tmp.txt", O_CREAT | O_TRUNC | O_RDWR, 0644);
	if (fd < 0)
		return (-1);
	ft_putstr_fd(src, fd);
	lseek(fd, 0, SEEK_SET);
	n = read(fd, buf, sizeof(buf));
	close(fd);
	free(src);
	return (n == (ssize_t)len && (len == 0 || memcmp(buf, original, len) == 0));
}

int	main(void)
{
	/* Strings variadas: normal, vazia, com \n/\t, longa. NULL -> 0 bytes,
	   sem crash. Confere tamanho exato + conteudo. */
	char const	*casos[] = {"hello", "", "42 Sao Paulo",
		"linha1\nlinha2\n", "com\ttab", "x",
		"AAAAAAAAAABBBBBBBBBBCCCCCCCCCC", NULL};
	int			n = sizeof(casos) / sizeof(casos[0]);
	int			i;
	int			falhas;
	int			r;

	i = 0;
	falhas = 0;
	printf("<ft_putstr_fd>\n");
	while (i < n)
	{
		r = check_str(casos[i]);
		if (r < 0)
			(printf("ERRO: nao abriu o arquivo temporario\n"), falhas++);
		else if (r == 0)
			(printf("FALHA s=\"%s\" : conteudo/tamanho escrito errado\n",
					casos[i] ? casos[i] : "(null)"), falhas++);
		i++;
	}
	unlink("putstr_tmp.txt");
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_putstr_fd>\n");
	return (falhas != 0);
}
