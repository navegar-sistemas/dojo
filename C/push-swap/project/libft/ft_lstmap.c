/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: macoelho <macoelho@student.42sp.org.br>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 21:45:01 by macoelho          #+#    #+#             */
/*   Updated: 2026/06/23 21:45:01 by macoelho         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	*ft_clear(t_list **lst, void (*del)(void *))
{
	ft_lstclear(lst, del);
	return (NULL);
}

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*lst_new;
	t_list	*node_new;
	void	*content_new;

	if (!lst || !f || !del)
		return (NULL);
	lst_new = NULL;
	while (lst)
	{
		content_new = f(lst->content);
		if (content_new == NULL)
			return (ft_clear(&lst_new, del));
		node_new = ft_lstnew(content_new);
		if (!node_new)
		{
			del(content_new);
			return (ft_clear(&lst_new, del));
		}
		ft_lstadd_back(&lst_new, node_new);
		lst = lst->next;
	}
	return (lst_new);
}
