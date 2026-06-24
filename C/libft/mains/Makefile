CC = cc
CFLAGS = -Wall -Wextra -Werror
AR = ar rcs
RM = rm -f
NORM = norminette
REPO = ../repo
# strnstr e BSD (ausente na glibc): comparamos contra a libbsd via -lbsd.
LDLIBS = -lbsd

# Sanitizers p/ o alvo san-<func>: AddressSanitizer (over-read/write, leak)
# + UBSan (overflow, shift invalido, etc.). Pega bug de MEMORIA que a
# comparacao de conteudo nao ve. Instrumenta o teste + TODOS os fontes da
# lib direto (sem libft.a), p/ nao misturar objetos asan com nao-asan.
SAN = -fsanitize=address,undefined -g3 -fno-omit-frame-pointer
SANSRCS = $(wildcard ${REPO}/ft_*.c)

%:
	@make --no-print-directory -C ${REPO} && ${NORM} ${REPO} \
	&& ${CC} ${CFLAGS} -I${REPO} -o bin.out $@.c ${REPO}/libft.a ${LDLIBS} && ./bin.out \
	&& ${CC} ${CFLAGS} ${SAN} -I${REPO} -o bin_san.out $@.c ${SANSRCS} ${LDLIBS} \
	&& ./bin_san.out > /dev/null && echo "[OK] memoria/UB limpos (asan+ubsan)"

# Uso: make r-split  (dev rapido: so recompila a lib, compila o teste e roda;
# sem norminette e sem sanitizer)
r-%:
	@make --no-print-directory -C ${REPO} \
	&& ${CC} ${CFLAGS} -I${REPO} -o bin.out $*.c ${REPO}/libft.a ${LDLIBS} && ./bin.out

# Uso: make san-substr  (recompila tudo com asan/ubsan e roda; aborta no bug)
san-%:
	@${CC} ${CFLAGS} ${SAN} -I${REPO} -o bin_san.out $*.c ${SANSRCS} ${LDLIBS} && ./bin_san.out

TESTS = $(basename $(wildcard *.c))

all: ${TESTS}

fclean:
	@make --no-print-directory -C ${REPO} fclean
	@${RM} bin.out bin_san.out

.PHONY: all fclean