#ifndef CAPTURE_H
# define CAPTURE_H

# define CAP_SIZE 4096

void	cap_begin(void);
int		cap_end(char *buf);
int		check(const char *label, const char *got, int got_ret,
			const char *want, int want_ret);

#endif
