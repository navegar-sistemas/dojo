/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/20 11:57:52 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/20 11:57:52 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *haystack, const char *needle, size_t len)
{
	size_t	i;
	size_t	needle_l;

	if (*needle == '\0')
		return ((char *) haystack);
	i = 0;
	needle_l = ft_strlen(needle);
	while (i + needle_l <= len && (haystack[i] != '\0'))
	{
		if (ft_strncmp(&haystack[i], needle, needle_l) == 0)
			return ((char *)haystack + i);
		i++;
	}
	return (NULL);
}
