/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:20:23 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 16:20:23 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	is_set(char c, char const *set)
{
	while (*set)
	{
		if (*set == c)
			return (1);
		set++;
	}
	return (0);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t		start;
	size_t		end;
	size_t		s1_l;
	char		*result;

	if (s1 == NULL || set == NULL)
		return (NULL);
	s1_l = ft_strlen(s1);
	if (s1_l == 0)
		return (ft_strdup(""));
	start = 0;
	end = s1_l;
	while (s1[start] != '\0' && is_set(s1[start], set))
		start++;
	while (end > start && is_set(s1[end - 1], set))
		end--;
	result = malloc((sizeof(char)) * (end - start + 1));
	if (!result)
		return (NULL);
	result = ft_memcpy(result, s1 + start, end - start);
	result[end - start] = '\0';
	return (result);
}
