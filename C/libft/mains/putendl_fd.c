/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   putendl_fd.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 13:00:00 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 13:00:00 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

void	ft_putendl_fd(char *s, int fd);

/* Fonte no HEAP de tamanho exato -> over-read vira erro (asan). */
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

/* Escreve via ft_putendl_fd e le de volta. Esperado: s + '\n'
   (tamanho strlen+1, ultimo byte '\n'). s==NULL -> escreve NADA (0 bytes),
   nem o '\n'. Pega "esqueceu o \n" (tamanho) e "trocou o conteudo". */
static int	check_endl(const char *original)
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
	fd = open("putendl_tmp.txt", O_CREAT | O_TRUNC | O_RDWR, 0644);
	if (fd < 0)
		return (-1);
	ft_putendl_fd(src, fd);
	lseek(fd, 0, SEEK_SET);
	n = read(fd, buf, sizeof(buf));
	close(fd);
	free(src);
	if (original == NULL)
		return (n == 0);
	return (n == (ssize_t)(len + 1) && memcmp(buf, original, len) == 0
		&& buf[len] == '\n');
}

int	main(void)
{
	/* Esperado = s + '\n'. NULL -> 0 bytes (nem \n). "" -> so o '\n'. */
	char const	*casos[] = {"hello", "", "42 Sao Paulo",
		"linha1\nlinha2", "x", "AAAAAAAAAABBBBBBBBBB", NULL};
	int			n = sizeof(casos) / sizeof(casos[0]);
	int			i;
	int			falhas;
	int			r;

	i = 0;
	falhas = 0;
	printf("<ft_putendl_fd>\n");
	while (i < n)
	{
		r = check_endl(casos[i]);
		if (r < 0)
			(printf("ERRO: nao abriu o arquivo temporario\n"), falhas++);
		else if (r == 0)
			(printf("FALHA s=\"%s\" : faltou \\n, tamanho ou conteudo errado\n",
					casos[i] ? casos[i] : "(null)"), falhas++);
		i++;
	}
	unlink("putendl_tmp.txt");
	if (falhas == 0)
		printf("[OK] Passou em todos os casos.\n");
	else
		printf("[X] %d falha(s).\n", falhas);
	printf("</ft_putendl_fd>\n");
	return (falhas != 0);
}
