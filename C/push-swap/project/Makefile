NAME	= push_swap
CC		= cc
CFLAGS	= -Wall -Wextra -Werror
LIBFT	= libft/libft.a

SRCS	= main.c \
			stack.c emit.c prog.c utils.c \
			ops_swap.c ops_push.c ops_rotate.c ops_rrotate.c \
			parse.c parse_utils.c \
			sort_tiny.c sort_simple.c \
			disorder.c 
#			rank.c  portfolio.c 
#		  sort_medium.c sort_complex.c \
#		  sort_greedy.c greedy_cost.c greedy_pick.c greedy_exec.c \
#		  sort_adaptive.c bench.c
OBJS	= $(SRCS:.c=.o)

#BSRCS	= checker_bonus.c read_ops_bonus.c apply_op_bonus.c
#BOBJS	= $(BSRCS:.c=.o)
#SHARED	= parse.o parse_utils.o stack.o emit.o prog.o utils.o \
#		  ops_swap.o ops_push.o ops_rotate.o ops_rrotate.o

all: $(NAME)

$(NAME): $(LIBFT) $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

$(LIBFT):
	$(MAKE) -C libft

%.o: %.c push_swap.h
	$(CC) $(CFLAGS) -c $< -o $@

#bonus: checker

#checker: $(LIBFT) $(BOBJS) $(SHARED)
#	$(CC) $(CFLAGS) $(BOBJS) $(SHARED) $(LIBFT) -o checker

clean:
	rm -f $(OBJS) $(BOBJS)
	$(MAKE) -C libft clean

fclean: clean
	rm -f $(NAME) checker
	$(MAKE) -C libft fclean

re: fclean all

.PHONY: all clean fclean re
#.PHONY: all bonus clean fclean re
