NAME	= libftprintf.a
CC		= cc
CFLAGS	= -Wall -Wextra -Werror
AR		= ar rcs

SRCS	= ft_printf.c pf_put.c
OBJS	= $(SRCS:.c=.o)

BSRCS	= ft_printf_bonus.c parse_bonus.c put_bonus.c conv_text_bonus.c \
		  conv_num_bonus.c conv_hex_bonus.c num_render_bonus.c
BOBJS	= $(BSRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	rm -f $(NAME) .bonus
	$(AR) $(NAME) $(OBJS)

$(OBJS): %.o: %.c ft_printf.h
	$(CC) $(CFLAGS) -c $< -o $@

$(BOBJS): %.o: %.c ft_printf_bonus.h
	$(CC) $(CFLAGS) -c $< -o $@

bonus: .bonus

.bonus: $(BOBJS)
	rm -f $(NAME)
	$(AR) $(NAME) $(BOBJS)
	touch .bonus

clean:
	rm -f $(OBJS) $(BOBJS)

fclean: clean
	rm -f $(NAME) .bonus

re: fclean all

.PHONY: all bonus clean fclean re
