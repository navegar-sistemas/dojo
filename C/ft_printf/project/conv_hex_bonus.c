#include "ft_printf_bonus.h"

int	conv_hex(t_fmt *f, unsigned int n)
{
	char	buf[24];
	char	*pre;

	pre = "";
	if (f->hash && n != 0 && f->conv == 'x')
		pre = "0x";
	if (f->hash && n != 0 && f->conv == 'X')
		pre = "0X";
	if (f->conv == 'X')
		render_base(n, "0123456789ABCDEF", buf);
	else
		render_base(n, "0123456789abcdef", buf);
	if (f->prec == 0 && n == 0)
		buf[0] = '\0';
	return (put_num(f, pre, buf));
}

int	conv_ptr(t_fmt *f, void *p)
{
	char	buf[24];
	char	*pre;

	if (!p)
	{
		f->prec = -1;
		return (conv_s(f, "(nil)"));
	}
	pre = "0x";
	if (f->plus)
		pre = "+0x";
	else if (f->space)
		pre = " 0x";
	render_base((unsigned long)p, "0123456789abcdef", buf);
	return (put_num(f, pre, buf));
}
