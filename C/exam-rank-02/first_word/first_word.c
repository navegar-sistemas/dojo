#include <unistd.h>

static int	terminate(void)
{
	write(1, "\n", 1);
	return (0);
}

static int	is_delimiter(unsigned char character)
{
	if (character == 9 || character == 32)
		return (1);
	return (0);
}

static void	first_word(unsigned char *raw_string)
{
	while (is_delimiter(*raw_string))
		raw_string++;
	while (*raw_string && !is_delimiter(*raw_string))
	{
		write(1, raw_string, 1);
		raw_string++;
	}
	write(1, "\n", 1);
	return ;
}

int	main(int argc, char **argv)
{
	if (argc != 2)
		return (terminate());
	first_word((unsigned char *)argv[1]);
	return (0);
}
