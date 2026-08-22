#include <unistd.h>
#include "ft_printf_bonus.h"

int	pf_putchar(char c)
{
	if (write(1, &c, 1) < 0)
		return (-1);
	return (1);
}

int	pf_putn(const char *s, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (pf_putchar(s[i]) < 0)
			return (-1);
		i++;
	}
	return (n);
}

int	pf_pad(char c, int n)
{
	int	i;

	i = 0;
	while (i < n)
	{
		if (pf_putchar(c) < 0)
			return (-1);
		i++;
	}
	if (n < 0)
		return (0);
	return (n);
}

int	pf_strlen(const char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}
