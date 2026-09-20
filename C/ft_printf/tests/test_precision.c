/*
** Bonus: precisao ('.') comparada byte a byte com a printf da libc.
** O formato chega por parametro para o compilador nao validar os casos
** propositalmente estranhos. NULL em %s / %p e comportamento indefinido e
** varia entre libcs: esses casos sao exibidos, mas nao contam como falha.
*/
#include <stdio.h>
#include <string.h>
#include "ft_printf_bonus.h"
#include "capture.h"

static int	cmp_int(const char *fmt, int v)
{
	char	want[CAP_SIZE];
	char	got[CAP_SIZE];
	int		want_ret;
	int		got_ret;

	cap_begin();
	want_ret = printf(fmt, v);
	cap_end(want);
	cap_begin();
	got_ret = ft_printf(fmt, v);
	cap_end(got);
	return (check(fmt, got, got_ret, want, want_ret));
}

static int	cmp_str(const char *fmt, char *s)
{
	char	want[CAP_SIZE];
	char	got[CAP_SIZE];
	int		want_ret;
	int		got_ret;

	cap_begin();
	want_ret = printf(fmt, s);
	cap_end(want);
	cap_begin();
	got_ret = ft_printf(fmt, s);
	cap_end(got);
	return (check(fmt, got, got_ret, want, want_ret));
}

static void	info_ptr(const char *fmt, void *p)
{
	char	want[CAP_SIZE];
	char	got[CAP_SIZE];
	int		want_ret;
	int		got_ret;

	cap_begin();
	want_ret = printf(fmt, p);
	cap_end(want);
	cap_begin();
	got_ret = ft_printf(fmt, p);
	cap_end(got);
	printf("INFO   %-22s libc [%s] ret=%d | ft [%s] ret=%d\n",
		fmt, want, want_ret, got, got_ret);
}

int	main(void)
{
	int	fails;

	fails = 0;
	fails += cmp_int("%.3d", 42);
	fails += cmp_int("%.0d", 0);
	fails += cmp_int("%d", 0);
	fails += cmp_int("%.0d", 5);
	fails += cmp_int("%.5d", -42);
	fails += cmp_int("%08.3d", 42);
	fails += cmp_int("%-8.3d|", 42);
	fails += cmp_int("%.3x", 255);
	fails += cmp_int("%#.5x", 255);
	fails += cmp_int("%.0x", 0);
	fails += cmp_int("%.3u", 7);
	fails += cmp_int("%.3c", 'A');
	fails += cmp_str("%.5s", "hello world");
	fails += cmp_str("%.0s", "hello");
	fails += cmp_str("%10.3s|", "hello");
	fails += cmp_str("%-10.3s|", "hello");
	info_ptr("%.3s", NULL);
	info_ptr("%.10s", NULL);
	info_ptr("%.3p", NULL);
	printf("%s (%d falha(s))\n", fails ? "FALHOU" : "PASSOU", fails);
	return (fails != 0);
}
