#ifndef FT_PRINTF_BONUS_H
# define FT_PRINTF_BONUS_H

# include <stdarg.h>

typedef struct s_fmt
{
	int		minus;
	int		zero;
	int		hash;
	int		plus;
	int		space;
	int		width;
	int		prec;
	char	conv;
}	t_fmt;

int			ft_printf(const char *format, ...);
const char	*parse_fmt(const char *s, t_fmt *f);
int			pf_putchar(char c);
int			pf_putn(const char *s, int n);
int			pf_pad(char c, int n);
int			pf_strlen(const char *s);
void		render_base(unsigned long n, const char *base, char *buf);
int			put_num(t_fmt *f, char *pre, char *digits);
int			conv_c(t_fmt *f, char c);
int			conv_s(t_fmt *f, char *s);
int			conv_percent(void);
int			conv_unknown(t_fmt *f);
int			conv_int(t_fmt *f, int n);
int			conv_uint(t_fmt *f, unsigned int n);
int			conv_hex(t_fmt *f, unsigned int n);
int			conv_ptr(t_fmt *f, void *p);

#endif
