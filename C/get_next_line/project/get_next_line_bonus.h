#ifndef GET_NEXT_LINE_BONUS_H
# define GET_NEXT_LINE_BONUS_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

# ifndef FD_MAX
#  define FD_MAX 1024
# endif

char	*get_next_line(int fd);
size_t	gnl_strlen(const char *s);
char	*gnl_strchr(const char *s, int c);
size_t	gnl_cpy(char *dst, const char *src);
char	*gnl_substr(const char *s, size_t start, size_t len);
char	*gnl_strjoin_free(char *stash, const char *buf);

#endif
