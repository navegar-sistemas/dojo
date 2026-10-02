int is_delimiter(unsigned char character)
{
	unsigned char delimiters[] = {9, 32, '\0'};
	unsigned char *delimiters_p = delimiters;
	
	while (*delimiters_p)
	{
		if (*delimiters_p == character)
			return (1);
		delimiters_p++;
	}
	return (0);
}