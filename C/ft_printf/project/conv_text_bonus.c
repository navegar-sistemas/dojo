#include "ft_printf_bonus.h"

static int	unk_head(t_fmt *f, char *buf)
{
	int	i;

	i = 1;
	buf[0] = '%';
	if (f->hash)
		buf[i++] = '#';
	if (f->plus)
		buf[i++] = '+';
	if (!f->plus && f->space)
		buf[i++] = ' ';
	if (f->minus)
		buf[i++] = '-';
	if (f->zero && !f->minus)
		buf[i++] = '0';
	return (i);
}

int	conv_unknown(t_fmt *f)
{
	char	buf[40];
	int		i;

	i = unk_head(f, buf);
	if (f->width != 0)
	{
		render_base((unsigned long)f->width, "0123456789", buf + i);
		i = i + pf_strlen(buf + i);
	}
	if (f->prec >= 0)
	{
		buf[i] = '.';
		i++;
		render_base((unsigned long)f->prec, "0123456789", buf + i);
		i = i + pf_strlen(buf + i);
	}
	buf[i] = f->conv;
	return (pf_putn(buf, i + 1));
}

int	conv_c(t_fmt *f, char c)
{
	if (!f->minus && pf_pad(' ', f->width - 1) < 0)
		return (-1);
	if (pf_putchar(c) < 0)
		return (-1);
	if (f->minus && pf_pad(' ', f->width - 1) < 0)
		return (-1);
	if (f->width > 1)
		return (f->width);
	return (1);
}

int	conv_s(t_fmt *f, char *s)
{
	int	len;

	if (!s && f->prec >= 0 && f->prec < 6)
		s = "";
	else if (!s)
		s = "(null)";
	len = pf_strlen(s);
	if (f->prec >= 0 && f->prec < len)
		len = f->prec;
	if (!f->minus && pf_pad(' ', f->width - len) < 0)
		return (-1);
	if (pf_putn(s, len) < 0)
		return (-1);
	if (f->minus && pf_pad(' ', f->width - len) < 0)
		return (-1);
	if (f->width > len)
		return (f->width);
	return (len);
}

int	conv_percent(void)
{
	return (pf_putchar('%'));
}
