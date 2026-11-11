unsigned char	reverse_bits(unsigned char octet)
{
	int	i;
	int	reverse;

	i = 8;
	reverse = 0;
	while (i--)
	{
		reverse = (reverse << 1) | (octet & 1);
		octet >>= 1;
	}
	return (reverse);
}

//#include <stdio.h>
//int main()
//{
//	int octet = 123;
//	printf("octa   : %08b\n", octet);
//	printf("reverse: %08b\n", reverse_bits(octet));
//}
