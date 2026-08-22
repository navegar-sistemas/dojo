# T04 — Bônus multi-fd

## Objetivo

A variante `_bonus`: os mesmos corpos, com o estado indexado pelo fd.

## Depende de

T03 inteira verde — bônus não compensa parte obrigatória quebrada.

## Arquivos

- `project/get_next_line_bonus.h`
- `project/get_next_line_bonus.c`
- `project/get_next_line_utils_bonus.c`

## Especificação

- [../05-bonus/multi-fd.md](../05-bonus/multi-fd.md) — a diferença única e o limite documentado
- [../02-restricoes/build.md](../02-restricoes/build.md) — as duas variantes nunca se misturam

## Implementação

1. `get_next_line_bonus.h` = header da obrigatória com a guarda
   `GET_NEXT_LINE_BONUS_H` e, depois do bloco de `BUFFER_SIZE`, o de
   `FD_MAX`:

   ```c
   # ifndef FD_MAX
   #  define FD_MAX 1024
   # endif
   ```

2. `get_next_line_utils_bonus.c` = cópia exata de
   `get_next_line_utils.c`, trocando só o `#include`.

3. `get_next_line_bonus.c` = cópia de `get_next_line.c` trocando o
   `#include` e **apenas** a função pública (as três fases não mudam nem de
   corpo nem de assinatura):

   - `static char *stash;` → `static char *stash[FD_MAX];`
   - guarda: `fd < 0 || BUFFER_SIZE <= 0` → `fd < 0 || fd >= FD_MAX || BUFFER_SIZE <= 0`
   - toda ocorrência de `stash` no corpo → `stash[fd]`

   Continua **uma única variável estática**; o corpo continua com 11 linhas.

## Pronto quando

Do diretório `check/`:

1. a **matriz completa** de
   [../06-aceitacao/validacao.md](../06-aceitacao/validacao.md) — agora com
   as linhas `rec_b`: nove `BS=... ok` sem `FALHOU`;
2. as **bordas de fd** na variante bônus: `bordas ok`;
3. a seção **Bônus** inteira: quatro `intercalado ok`, o valgrind do
   intercalado com `in use at exit: 0 bytes`, e o `fdmax` imprimindo
   `fd 3 dentro:  abc` / `fd 4 barrado: NULL ok`;
4. diff disciplinado — a única diferença de código entre as variantes é a
   descrita acima:

   ```bash
   diff ../project/get_next_line_utils.c ../project/get_next_line_utils_bonus.c   # só o #include
   diff ../project/get_next_line.c ../project/get_next_line_bonus.c               # #include + get_next_line
   ```
