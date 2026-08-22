#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>

int	ft_printf(const char *format, ...);
int	pf_putchar(char c);
int	pf_putstr(char *s);
int	pf_putnbr_base(unsigned long n, const char *base);
int	pf_putptr(void *ptr);

#endif
