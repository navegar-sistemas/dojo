#include "ft_printf_bonus.h"

static void	fmt_init(t_fmt *f)
{
	f->minus = 0;
	f->zero = 0;
	f->hash = 0;
	f->plus = 0;
	f->space = 0;
	f->width = 0;
	f->prec = -1;
	f->conv = '\0';
}

static const char	*parse_flags(const char *s, t_fmt *f)
{
	while (*s == '-' || *s == '0' || *s == '#'
		|| *s == '+' || *s == ' ')
	{
		if (*s == '-')
			f->minus = 1;
		if (*s == '0')
			f->zero = 1;
		if (*s == '#')
			f->hash = 1;
		if (*s == '+')
			f->plus = 1;
		if (*s == ' ')
			f->space = 1;
		s++;
	}
	return (s);
}

static int	parse_num(const char **s, int *n)
{
	*n = 0;
	while (**s >= '0' && **s <= '9')
	{
		if (*n > (PF_INT_MAX - (**s - '0')) / 10)
			return (-1);
		*n = *n * 10 + (**s - '0');
		(*s)++;
	}
	return (0);
}

const char	*parse_fmt(const char *s, t_fmt *f)
{
	fmt_init(f);
	s = parse_flags(s, f);
	if (parse_num(&s, &f->width) < 0)
		return (s);
	if (*s == '.')
	{
		s++;
		if (parse_num(&s, &f->prec) < 0)
			return (s);
	}
	f->conv = *s;
	return (s);
}
