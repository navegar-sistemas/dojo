/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 15:54:55 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 15:54:55 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*result;
	size_t	s1_l;
	size_t	s2_l;
	size_t	st_l;

	if (s1 == NULL || s2 == NULL)
		return (NULL);
	s1_l = ft_strlen(s1);
	s2_l = ft_strlen(s2);
	st_l = s1_l + s2_l + 1;
	result = malloc(sizeof(char) * (st_l));
	if (!result)
		return (NULL);
	ft_strlcpy(result, s1, st_l);
	ft_strlcat(result, s2, st_l);
	return (result);
}
