/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 19:26:29 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/22 19:26:29 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_words_count(char const *s, char c)
{
	int	r;
	int	i;

	r = 0;
	i = 0;
	while (s[i] != '\0')
	{
		if (i > 0 && s[i] == c && s[i - 1] != c)
			r++;
		i++;
	}
	if (i > 0 && s[i - 1] != c)
		r++;
	return (r);
}

static int	ft_word_len(char const *s, char c)
{
	int	i;

	i = 0;
	while (s[i] != c && s[i] != '\0')
		i++;
	return (i);
}

static char	*ft_set_next_line(char const **s, char c)
{
	char	*word;
	int		word_l;

	while (**s == c)
		(*s)++;
	if (**s == '\0')
		return (NULL);
	word_l = ft_word_len(*s, c);
	word = ft_substr(*s, 0, word_l);
	if (!word)
		return (NULL);
	while (**s != c && **s != '\0')
		(*s)++;
	return (word);
}

static void	*ft_free(char **split, int i)
{
	while (i > 0)
	{
		i--;
		free(split[i]);
	}
	free(split);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	char	**split;
	int		words_n;
	int		i;

	if (s == NULL)
		return (NULL);
	words_n = ft_words_count(s, c);
	split = malloc((words_n + 1) * sizeof(char *));
	if (!split)
		return (NULL);
	i = 0;
	while (i < words_n)
	{
		split[i] = ft_set_next_line(&s, c);
		if (!split[i])
			return (ft_free(split, i));
		i++;
	}
	split[words_n] = NULL;
	return (split);
}
