# Build

## Funções externas permitidas

`read`, `write`, `malloc`, `free`, `exit`, mais a libft.

Ficam de fora, entre outras: `printf` e toda a família `*printf`, `qsort`, `atoi`, `strtol`,
`memmove` da libc (usa-se `ft_memmove`), e `math.h` inteira — a raiz quadrada inteira é
implementada à mão, ver [../04-algoritmos/medium.md](../04-algoritmos/medium.md).

Da libft, este projeto usa: `ft_split` (divisão dos argumentos), `ft_strncmp` (flags e siglas
do checker), `ft_memmove` (rotações e push), `ft_memcpy` (crescimento do programa gravado e
cópia de pilhas no portfólio), `ft_memset` (zerar o contexto do checker), `ft_putstr_fd`,
`ft_putendl_fd`, `ft_putnbr_fd`, `ft_putchar_fd` (toda a saída).

A libft entra copiada em `libft/`, com o Makefile dela, e é compilada pela regra do projeto que
chama esse Makefile.

## Estrutura de arquivos

```
libft/                  cópia da libft + Makefile dela
push_swap.h
main.c
parse.c  parse_utils.c
stack.c  emit.c  prog.c  utils.c
ops_swap.c  ops_push.c  ops_rotate.c  ops_rrotate.c
disorder.c  rank.c
sort_tiny.c  sort_simple.c  sort_medium.c  sort_complex.c
sort_greedy.c  greedy_cost.c  greedy_pick.c  greedy_exec.c
portfolio.c  sort_adaptive.c
bench.c
checker_bonus.c  read_ops_bonus.c  apply_op_bonus.c
Makefile
```

Responsabilidade de cada arquivo em [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md).

## Makefile

```make
NAME	= push_swap
CC		= cc
CFLAGS	= -Wall -Wextra -Werror
LIBFT	= libft/libft.a

SRCS	= main.c parse.c parse_utils.c stack.c emit.c utils.c \
		  ops_swap.c ops_push.c ops_rotate.c ops_rrotate.c \
		  disorder.c rank.c prog.c portfolio.c \
		  sort_tiny.c sort_simple.c sort_medium.c sort_complex.c \
		  sort_greedy.c greedy_cost.c greedy_pick.c greedy_exec.c \
		  sort_adaptive.c bench.c
OBJS	= $(SRCS:.c=.o)

BSRCS	= checker_bonus.c read_ops_bonus.c apply_op_bonus.c
BOBJS	= $(BSRCS:.c=.o)
SHARED	= parse.o parse_utils.o stack.o emit.o prog.o utils.o \
		  ops_swap.o ops_push.o ops_rotate.o ops_rrotate.o

all: $(NAME)

$(NAME): $(LIBFT) $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

$(LIBFT):
	$(MAKE) -C libft

%.o: %.c push_swap.h
	$(CC) $(CFLAGS) -c $< -o $@

bonus: checker

checker: $(LIBFT) $(BOBJS) $(SHARED)
	$(CC) $(CFLAGS) $(BOBJS) $(SHARED) $(LIBFT) -o checker

clean:
	rm -f $(OBJS) $(BOBJS)
	$(MAKE) -C libft clean

fclean: clean
	rm -f $(NAME) checker
	$(MAKE) -C libft fclean

re: fclean all

.PHONY: all bonus clean fclean re
```

## Propriedades exigidas

**Não relinka.** `make` duas vezes seguidas precisa responder `Nothing to be done for 'all'.`
na segunda. O mesmo vale para `make bonus`, e para `make` logo depois de `make bonus`.

**Regras obrigatórias.** `all`, `clean`, `fclean`, `re`, `$(NAME)` e `bonus`.

**Dependência do header.** Os `.o` dependem de `push_swap.h`, então mudar o header recompila
tudo. Sem isso, uma mudança de `struct` deixaria objetos incompatíveis linkando em silêncio.

**Regra do `libft.a` sem pré-requisitos.** Depois da primeira compilação o arquivo existe, e o
make não reentra no diretório — é o que evita o relink. O `$(MAKE) -C libft` continua sendo o
caminho de construção quando o arquivo não existe.

**Objetos compartilhados no bônus.** O `checker` linka os `.o` dos módulos comuns em vez de
duplicar código. A lista vai além do óbvio por causa da cadeia de dependências: as operações
chamam `emit` (`emit.o`), `emit` grava via `prog_push` (`prog.o`), e o crescimento do programa
morre em `ps_die` (`utils.o`) — os três entram mesmo que o checker rode com `prog == NULL` e
nunca grave nada.

Os arquivos exclusivos do bônus levam o sufixo `_bonus`; os compartilhados com a parte
obrigatória mantêm os nomes.

## Verificação

```bash
make && make            # segunda chamada não pode relinkar
make bonus && make bonus
make fclean             # remove push_swap, checker, todos os .o e libft.a
make re
```
