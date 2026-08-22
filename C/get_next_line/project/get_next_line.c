#include "get_next_line.h"

static char	*gnl_read_loop(int fd, char *stash)
{
	char	*buf;
	ssize_t	n;

	buf = malloc((size_t)BUFFER_SIZE + 1);
	n = 1;
	while (buf && n > 0 && !gnl_strchr(stash, '\n'))
	{
		n = read(fd, buf, BUFFER_SIZE);
		if (n <= 0)
			break ;
		buf[n] = '\0';
		stash = gnl_strjoin_free(stash, buf);
		if (!stash)
			break ;
	}
	if (!buf || n < 0)
	{
		free(stash);
		stash = NULL;
	}
	free(buf);
	return (stash);
}

static char	*gnl_extract_line(const char *stash)
{
	size_t	len;

	len = 0;
	while (stash[len] && stash[len] != '\n')
		len++;
	if (stash[len] == '\n')
		len++;
	return (gnl_substr(stash, 0, len));
}

static char	*gnl_trim_stash(char *stash)
{
	char	*rest;
	char	*nl;

	nl = gnl_strchr(stash, '\n');
	if (!nl || !nl[1])
	{
		free(stash);
		return (NULL);
	}
	rest = gnl_substr(nl + 1, 0, gnl_strlen(nl + 1));
	free(stash);
	return (rest);
}

char	*get_next_line(int fd)
{
	static char	*stash;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	stash = gnl_read_loop(fd, stash);
	if (!stash)
		return (NULL);
	line = gnl_extract_line(stash);
	stash = gnl_trim_stash(stash);
	return (line);
}
