# Build

## Dependências externas

A implementação inteira usa, de fora, **apenas**:

- `write`, de `<unistd.h>` — toda a saída;
- o mecanismo variádico de `<stdarg.h>`: `va_start`, `va_arg`, `va_end`
  (`va_copy` está disponível e não é usado).

`malloc` e `free` são permitidos e não são usados
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)). Nenhuma
outra função de biblioteca aparece: comprimento de string, dígitos e padding
são do projeto.

## Estrutura de arquivos

```
ft_printf.h
ft_printf.c  pf_put.c
ft_printf_bonus.h
ft_printf_bonus.c  parse_bonus.c  put_bonus.c
conv_text_bonus.c  conv_num_bonus.c  conv_hex_bonus.c  num_render_bonus.c
Makefile
```

Nenhum arquivo é compartilhado entre as duas variantes: a parte obrigatória é
`ft_printf.h` + 2 `.c`; o bônus é `ft_printf_bonus.h` + 7 `.c`, todos com o
sufixo. Responsabilidades em
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md).

## Makefile

```make
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
```

## Por que cada peça incomum está lá

**`rm -f $(NAME)` antes de cada `ar`.** `ar rcs` **acrescenta** a um arquivo
existente. Sem o `rm`, `make` seguido de `make bonus` produziria um `.a` com
as duas implementações dentro — dois símbolos `ft_printf`, e o linker
escolhendo por ordem de membro. As duas receitas recriam o arquivo do zero,
então `ar t libftprintf.a` lista só os objetos da variante corrente.

**O marcador `.bonus`.** A regra `bonus` não tem como comparar datas com o
`.a`, porque a regra `all` também o produz. O arquivo vazio `.bonus` registra
"o `.a` atual é o do bônus": é ele o alvo real da regra, e é removido tanto
pelo `fclean` quanto pela receita de `$(NAME)`. Assim `make` depois de
`make bonus` volta a montar a variante obrigatória, e o próximo `make bonus`
reconstrói de fato.

**Regras de padrão estático por header.** Cada `.o` depende do header da sua
variante: mudar `ft_printf.h` recompila a parte obrigatória, mudar
`ft_printf_bonus.h` recompila o bônus. Sem isso, uma mudança em `t_fmt`
deixaria objetos incompatíveis linkando em silêncio.

## Propriedades exigidas

| Propriedade | Verificação |
|---|---|
| não relinka | `make && make` responde `Nothing to be done for 'all'.`; `make bonus && make bonus`, o mesmo para `bonus` |
| regras obrigatórias | `all`, `bonus`, `clean`, `fclean`, `re` e `$(NAME)` |
| fontes nomeados um a um | sem `*.c` em lugar nenhum |
| `.a` de uma variante só | `ar t libftprintf.a` lista ou os 2 objetos da obrigatória, ou os 7 do bônus |

| Sequência | Resultado |
|---|---|
| `make` → `make` | a segunda chamada não faz nada |
| `make bonus` → `make bonus` | idem |
| `make` → `make bonus` | `.a` refeito só com objetos `_bonus` |
| `make bonus` → `touch ft_printf.c` → `make` | `.a` refeito só com objetos da obrigatória |

## Verificação

```bash
make && make                    # 2ª: Nothing to be done for 'all'.
make bonus && make bonus        # 2ª: Nothing to be done for 'bonus'.
ar t libftprintf.a              # só objetos _bonus neste ponto
make fclean                     # remove .o, .a e .bonus
make re                         # do zero, zero warning
```
