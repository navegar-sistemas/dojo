/*
** Parte obrigatoria: falha de write. ft_printf deve devolver -1 sem
** encerrar o processo; so o SIGPIPE (disposicao padrao) mata o programa.
*/
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include "ft_printf.h"

#define BIG 199999

static int	report(const char *label, int ok)
{
	fprintf(stderr, "%s  %s\n", ok ? "OK    " : "FALHA ", label);
	return (!ok);
}

static int	closed_fd(void)
{
	int	saved;
	int	ret;

	saved = dup(1);
	close(1);
	ret = ft_printf("abc");
	dup2(saved, 1);
	close(saved);
	return (report("fd 1 fechado -> ret == -1, processo vivo", ret == -1));
}

static int	broken_pipe(int ignore)
{
	int	fd[2];
	int	ret;

	if (ignore)
		signal(SIGPIPE, SIG_IGN);
	pipe(fd);
	close(fd[0]);
	dup2(fd[1], 1);
	ret = ft_printf("abc");
	return (ret);
}

/* Os dois cenarios de pipe quebrado rodam em filho: um deles morre. */
static int	broken_pipe_child(int ignore)
{
	pid_t	pid;
	int		st;

	pid = fork();
	if (pid == 0)
		exit(broken_pipe(ignore) == -1 ? 0 : 1);
	waitpid(pid, &st, 0);
	if (ignore)
		return (report("pipe quebrado, SIGPIPE ignorado -> ret == -1",
				WIFEXITED(st) && WEXITSTATUS(st) == 0));
	return (report("pipe quebrado, SIGPIPE padrao -> morto pelo sinal",
			WIFSIGNALED(st) && WTERMSIG(st) == SIGPIPE));
}

static int	partial_output(void)
{
	char	*big;
	char	drain[4096];
	int		fd[2];
	int		saved;
	int		ret;
	long	got;
	long	n;

	big = malloc(BIG + 1);
	memset(big, 'x', BIG);
	big[BIG] = '\0';
	pipe(fd);
	fcntl(fd[1], F_SETFL, O_NONBLOCK);
	saved = dup(1);
	dup2(fd[1], 1);
	ret = ft_printf("%s", big);
	dup2(saved, 1);
	close(saved);
	close(fd[1]);
	got = 0;
	n = read(fd[0], drain, sizeof(drain));
	while (n > 0)
	{
		got += n;
		n = read(fd[0], drain, sizeof(drain));
	}
	close(fd[0]);
	free(big);
	fprintf(stderr, "        pedidos=%d ja escritos=%ld\n", BIG, got);
	return (report("pipe cheio -> ret == -1 e saida parcial sem rollback",
			ret == -1 && got > 0 && got < BIG));
}

int	main(void)
{
	int	fails;

	fails = 0;
	fails += closed_fd();
	fails += broken_pipe_child(0);
	fails += broken_pipe_child(1);
	fails += partial_output();
	fprintf(stderr, "%s (%d falha(s))\n", fails ? "FALHOU" : "PASSOU", fails);
	return (fails != 0);
}
