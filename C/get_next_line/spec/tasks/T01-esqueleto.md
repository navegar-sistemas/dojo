# T01 — Esqueleto do header

## Objetivo

`get_next_line.h` com a guarda, os `#include` de sistema, o default de
`BUFFER_SIZE` e o protótipo público.

## Depende de

Nada. Criar também os diretórios: `project/` para o código, `check/` ao lado
para a validação ([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)).

## Arquivos

- `project/get_next_line.h`

## Especificação

- [../01-contrato/api.md](../01-contrato/api.md) — o protótipo e o contrato de `BUFFER_SIZE`
- [../02-restricoes/build.md](../02-restricoes/build.md) — headers protegidos, compila com e sem `-D`

## Implementação

O arquivo inteiro, na ordem:

```c
#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

char	*get_next_line(int fd);

#endif
```

`<stdlib.h>` traz `malloc`/`free`/`size_t`; `<unistd.h>` traz `read` e
`ssize_t`. O `#ifndef BUFFER_SIZE` interno é o que permite compilar com e sem
`-D BUFFER_SIZE=n` — a flag, quando presente, vence porque o `#define` do
header nem é processado.

Diretivas aninhadas indentam um espaço por nível depois do `#`
(`# define`, `#  define`), e a guarda é o nome do arquivo em maiúsculas com
`_` no lugar do ponto.

## Pronto quando

Do diretório `check/`:

```bash
P=../project
# o default vale sem -D...
printf 'BUFFER_SIZE\n' | cc -E -I$P -include get_next_line.h - | tail -1   # 42
# ...e a flag vence quando presente
printf 'BUFFER_SIZE\n' | cc -D BUFFER_SIZE=7 -E -I$P -include get_next_line.h - | tail -1   # 7
# dupla inclusão compila
printf '#include "get_next_line.h"\n#include "get_next_line.h"\n' \
  | cc -Wall -Wextra -Werror -fsyntax-only -I$P -x c - && echo "guarda ok"
```
