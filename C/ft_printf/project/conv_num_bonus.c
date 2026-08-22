#include "ft_printf_bonus.h"

int	conv_int(t_fmt *f, int n)
{
	char	buf[24];
	char	*pre;
	long	v;

	v = n;
	pre = "";
	if (v < 0)
	{
		pre = "-";
		v = -v;
	}
	else if (f->plus)
		pre = "+";
	else if (f->space)
		pre = " ";
	render_base((unsigned long)v, "0123456789", buf);
	if (f->prec == 0 && n == 0)
		buf[0] = '\0';
	return (put_num(f, pre, buf));
}

int	conv_uint(t_fmt *f, unsigned int n)
{
	char	buf[24];

	render_base(n, "0123456789", buf);
	if (f->prec == 0 && n == 0)
		buf[0] = '\0';
	return (put_num(f, "", buf));
}
