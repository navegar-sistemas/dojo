/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 15:11:46 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 15:11:46 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	char			*mapi;
	unsigned int	i;
	unsigned int	l;

	if (s == NULL || f == NULL)
		return (NULL);
	l = ft_strlen(s);
	mapi = malloc((l + 1) * (sizeof(char)));
	if (!mapi)
		return (NULL);
	i = 0;
	while (s[i] != '\0')
	{
		mapi[i] = f(i, s[i]);
		i++;
	}
	mapi[i] = '\0';
	return (mapi);
}
