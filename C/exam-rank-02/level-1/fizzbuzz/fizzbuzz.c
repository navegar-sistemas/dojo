#include <unistd.h>

void	ft_putnbr(int number)
{
	if (number >= 10)
		ft_putnbr(number / 10);
	write(1, &"0123456789"[number % 10], 1);
}

int	main(void)
{
	int	i = 0;

	while (++i <= 100)
	{
		if (!(i % 3) && !(i % 5))
			write(1, "fizzbuzz", 8);
		else if (!(i % 3))
			write(1, "fizz", 4);
		else if (!(i % 5))
			write(1, "buzz", 4);
		else
			ft_putnbr(i);
		write(1, "\n", 1);
	}
	return (0);
}
