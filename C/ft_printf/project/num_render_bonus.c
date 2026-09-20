#include "ft_printf_bonus.h"

void	render_base(unsigned long n, const char *base, char *buf)
{
	unsigned long	b;
	unsigned long	tmp;
	int				len;

	b = 0;
	while (base[b])
		b++;
	len = 1;
	tmp = n;
	while (tmp >= b)
	{
		tmp = tmp / b;
		len++;
	}
	buf[len] = '\0';
	while (len > 0)
	{
		len--;
		buf[len] = base[n % b];
		n = n / b;
	}
}

int	put_num(t_fmt *f, char *pre, char *digits)
{
	int		zeros;
	int		pad;
	long	total;

	zeros = f->prec - pf_strlen(digits);
	if (zeros < 0)
		zeros = 0;
	total = pf_strlen(pre) + pf_strlen(digits);
	if (f->zero && !f->minus && f->prec < 0 && f->width - total > zeros)
		zeros = (int)(f->width - total);
	total = total + zeros;
	pad = 0;
	if (f->width > total)
		pad = (int)(f->width - total);
	if (!f->minus && pf_pad(' ', pad) < 0)
		return (-1);
	if (pf_putn(pre, pf_strlen(pre)) < 0 || pf_pad('0', zeros) < 0
		|| pf_putn(digits, pf_strlen(digits)) < 0)
		return (-1);
	if (f->minus && pf_pad(' ', pad) < 0)
		return (-1);
	if (total + pad > PF_INT_MAX)
		return (-1);
	return ((int)(total + pad));
}
