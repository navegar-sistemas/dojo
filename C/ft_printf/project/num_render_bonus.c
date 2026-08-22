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
	int	zeros;
	int	total;

	zeros = f->prec - pf_strlen(digits);
	if (zeros < 0)
		zeros = 0;
	if (f->zero && !f->minus && f->prec < 0)
	{
		total = pf_strlen(pre) + pf_strlen(digits);
		if (f->width - total > zeros)
			zeros = f->width - total;
	}
	total = pf_strlen(pre) + zeros + pf_strlen(digits);
	if (!f->minus && pf_pad(' ', f->width - total) < 0)
		return (-1);
	if (pf_putn(pre, pf_strlen(pre)) < 0 || pf_pad('0', zeros) < 0
		|| pf_putn(digits, pf_strlen(digits)) < 0)
		return (-1);
	if (f->minus && pf_pad(' ', f->width - total) < 0)
		return (-1);
	if (f->width > total)
		return (f->width);
	return (total);
}
