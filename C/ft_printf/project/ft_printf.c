#include "ft_printf.h"

static int	pf_putnbr(int n)
{
	long	v;
	int		len;
	int		r;

	v = n;
	len = 0;
	if (v < 0)
	{
		if (pf_putchar('-') < 0)
			return (-1);
		len = 1;
		v = -v;
	}
	r = pf_putnbr_base((unsigned long)v, "0123456789");
	if (r < 0)
		return (-1);
	return (len + r);
}

static int	pf_conv(char conv, va_list *ap)
{
	if (conv == 'c')
		return (pf_putchar((char)va_arg(*ap, int)));
	if (conv == 's')
		return (pf_putstr(va_arg(*ap, char *)));
	if (conv == 'p')
		return (pf_putptr(va_arg(*ap, void *)));
	if (conv == 'd' || conv == 'i')
		return (pf_putnbr(va_arg(*ap, int)));
	if (conv == 'u')
		return (pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789"));
	if (conv == 'x')
		return (pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789abcdef"));
	if (conv == 'X')
		return (pf_putnbr_base(va_arg(*ap, unsigned int), "0123456789ABCDEF"));
	if (conv == '%')
		return (pf_putchar('%'));
	if (pf_putchar('%') < 0 || pf_putchar(conv) < 0)
		return (-1);
	return (2);
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
		if (*format == '%' && format[1] == '\0')
			r = -1;
		else if (*format == '%')
			r = pf_conv(*(++format), &ap);
		else
			r = pf_putchar(*format);
		format++;
		if (r > 0)
			total += r;
	}
	va_end(ap);
	if (r < 0)
		return (-1);
	return (total);
}
