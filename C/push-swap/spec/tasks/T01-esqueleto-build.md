# T01 — Esqueleto de build

## Objetivo

`make` compila um binário vazio, linkando a libft, sem relinkar na segunda chamada.

## Depende de

Nada.

## Arquivos

- `Makefile`
- `push_swap.h`
- `libft/` (cópia da libft com o Makefile dela)
- `main.c` com um `main` que retorna 0

## Especificação

- [../02-restricoes/build.md](../02-restricoes/build.md) — Makefile completo e propriedades
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — conteúdo do header

## Implementação

1. Copiar a libft para `libft/`, com o Makefile dela — **somente fontes, `Makefile` e
   `libft.h`; nunca `libft.a` nem `.o` pré-compilados**. Um `libft.a` velho copiado junto
   satisfaz a regra `$(LIBFT):` (que não tem pré-requisitos) e o make nunca o reconstrói; se
   ele veio de outra máquina/arquitetura, o link falha com um erro críptico do `ld`
   (`archive member '/' not a mach-o file`) que não aponta para a causa. Confirmar que
   `make -C libft` gera `libft/libft.a`.
2. Escrever `push_swap.h` **mínimo**: apenas a guarda de inclusão. Isso basta
   para todo o "Pronto quando" desta tarefa passar. O header cresce tarefa a tarefa: cada
   Txx que introduz um tipo ou função pública acrescenta a declaração correspondente —
   [tipos.md](../03-arquitetura/tipos.md) e [modulos.md](../03-arquitetura/modulos.md) são o
   mapa de onde ele vai chegar, não um texto a transcrever agora.
3. Copiar o Makefile de [build.md](../02-restricoes/build.md).
4. `SRCS` começa contendo só `main.c`, com um `main` que retorna 0. Cada tarefa seguinte,
   ao criar um arquivo novo, o acrescenta ao `SRCS` — o Makefile cresce junto com o código,
   e nenhum arquivo existe antes de ter conteúdo. As regras `bonus`/`checker` e as variáveis
   `BSRCS`/`BOBJS`/`SHARED` entram só em T15, quando o checker existe; até lá, `make bonus`
   não faz parte da verificação.

## Pronto quando

```bash
make                        # compila sem warning
make                        # "Nothing to be done for 'all'."
touch push_swap.h && make   # recompila tudo (dependência do header)
make fclean                 # remove push_swap, todos os .o e libft/libft.a
make re                     # reconstrói do zero, zero warning
norminette *.c *.h          # nenhuma linha "Error:"
ls libft/libft.a            # existe após make
```

A verificação de `make bonus && make bonus` (segunda chamada sem relink) acontece em T15,
quando a regra passa a existir.
