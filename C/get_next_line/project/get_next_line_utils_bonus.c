#include "get_next_line_bonus.h"

size_t	gnl_strlen(const char *s)
{
	size_t	i;

	i = 0;
	if (!s)
		return (0);
	while (s[i])
		i++;
	return (i);
}

char	*gnl_strchr(const char *s, int c)
{
	if (!s)
		return (NULL);
	while (*s)
	{
		if (*s == (char)c)
			return ((char *)s);
		s++;
	}
	if ((char)c == '\0')
		return ((char *)s);
	return (NULL);
}

size_t	gnl_cpy(char *dst, const char *src)
{
	size_t	i;

	i = 0;
	while (src && src[i])
	{
		dst[i] = src[i];
		i++;
	}
	return (i);
}

char	*gnl_substr(const char *s, size_t start, size_t len)
{
	char	*sub;
	size_t	i;

	sub = malloc(len + 1);
	if (!sub)
		return (NULL);
	i = 0;
	while (i < len)
	{
		sub[i] = s[start + i];
		i++;
	}
	sub[i] = '\0';
	return (sub);
}

char	*gnl_strjoin_free(char *stash, const char *buf)
{
	char	*out;
	size_t	len;

	out = malloc(gnl_strlen(stash) + gnl_strlen(buf) + 1);
	if (!out)
	{
		free(stash);
		return (NULL);
	}
	len = gnl_cpy(out, stash);
	len += gnl_cpy(out + len, buf);
	out[len] = '\0';
	free(stash);
	return (out);
}
