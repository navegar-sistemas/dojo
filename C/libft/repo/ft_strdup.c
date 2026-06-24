/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 14:34:30 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 14:34:30 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s)
{
	char	*d;
	size_t	len;

	len = ft_strlen(s) + 1;
	d = malloc(sizeof(char) * len);
	if (!d)
		return (NULL);
	ft_strlcpy(d, s, len);
	return (d);
}
