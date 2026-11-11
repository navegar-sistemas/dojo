unsigned char	swap_bits(unsigned char octet)
{
	return ((unsigned char)(octet >> 4) | (octet << 4));
}

//#include <stdio.h>
//int main()
//{
//	int octet = 123;
//	printf("octa   : %08b\n", octet);
//	printf("swap   : %08b\n", swap_bits(octet));
//}
