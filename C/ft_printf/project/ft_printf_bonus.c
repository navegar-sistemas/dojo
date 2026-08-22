#include "ft_printf_bonus.h"

static int	pf_dispatch(t_fmt *f, va_list *ap)
{
	if (f->conv == 'c')
		return (conv_c(f, (char)va_arg(*ap, int)));
	if (f->conv == 's')
		return (conv_s(f, va_arg(*ap, char *)));
	if (f->conv == 'p')
		return (conv_ptr(f, va_arg(*ap, void *)));
	if (f->conv == 'd' || f->conv == 'i')
		return (conv_int(f, va_arg(*ap, int)));
	if (f->conv == 'u')
		return (conv_uint(f, va_arg(*ap, unsigned int)));
	if (f->conv == 'x' || f->conv == 'X')
		return (conv_hex(f, va_arg(*ap, unsigned int)));
	if (f->conv == '%')
		return (conv_percent());
	return (conv_unknown(f));
}

static int	pf_directive(const char **fmt, va_list *ap)
{
	t_fmt	f;

	*fmt = parse_fmt(*fmt + 1, &f);
	if (f.conv == '\0')
		return (-1);
	*fmt = *fmt + 1;
	return (pf_dispatch(&f, ap));
}

int	ft_printf(const char *format, ...)
{
	va_list	ap;
	int		total;
	int		r;

	va_start(ap, format);
	total = 0;
	r = 0;
	while (*format && r >= 0)
	{
		if (*format == '%')
			r = pf_directive(&format, &ap);
		else
			r = pf_putchar(*format++);
		if (r > 0)
			total += r;
	}
	va_end(ap);
	if (r < 0)
		return (-1);
	return (total);
}
