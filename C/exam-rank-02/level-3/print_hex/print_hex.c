#include <stdio.h>
#include <unistd.h>

static	int terminate(void)
{
	write(1, "\n", 1);
	return (0);
}

void	ft_print_hex(int nb)
{
	return ;
}
int	ft_atoi(char *str)
{
	int i = 0;
	int op = 1;
	int result = 0;

	while(str[i] <= 32)
		i++;
	
	if(str[i] == '-')
	{
		op = -1;
		i++;
	}
	else if(str[i] == '+')
		i++;


	return (0);
}

int main(int argc, char **argv)
{
	if(argc != 2)
		return (terminate());
	printf("s: %d, %s\n", argc, argv[1]);
	printf(">: %d\n", ft_atoi(argv[1]));
	

	//ft_print_hex(ft_atoi(argv[1]));

	return (0);
}
