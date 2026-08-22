#include <unistd.h>
#include "ft_printf.h"

int	pf_putchar(char c)
{
	if (write(1, &c, 1) < 0)
		return (-1);
	return (1);
}

int	pf_putstr(char *s)
{
	int	i;

	if (!s)
		s = "(null)";
	i = 0;
	while (s[i])
	{
		if (pf_putchar(s[i]) < 0)
			return (-1);
		i++;
	}
	return (i);
}

int	pf_putnbr_base(unsigned long n, const char *base)
{
	unsigned long	b;
	int				len;

	b = 0;
	while (base[b])
		b++;
	len = 0;
	if (n >= b)
	{
		len = pf_putnbr_base(n / b, base);
		if (len < 0)
			return (-1);
	}
	if (pf_putchar(base[n % b]) < 0)
		return (-1);
	return (len + 1);
}

int	pf_putptr(void *ptr)
{
	int	r;

	if (!ptr)
		return (pf_putstr("(nil)"));
	if (pf_putstr("0x") < 0)
		return (-1);
	r = pf_putnbr_base((unsigned long)ptr, "0123456789abcdef");
	if (r < 0)
		return (-1);
	return (r + 2);
}
