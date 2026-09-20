# Testes do ft_printf

Rodar a partir desta pasta (`C/ft_printf/tests`). Cada teste imprime `OK` /
`FALHA` por caso e termina com `PASSOU` ou `FALHOU` (exit code 0 ou 1).

| Arquivo | Parte | O que verifica |
|---|---|---|
| `test_unknown.c` | obrigatória | conversão desconhecida (`%z`) e `%` no fim do formato |
| `test_write_error.c` | obrigatória | falha de `write`: retorno `-1`, SIGPIPE, saída parcial |
| `test_precision.c` | bônus | precisão (`.`) comparada byte a byte com a `printf` da libc |

## Parte obrigatória

```sh
make -C ../project re
cc -Wall -Wextra -Werror -I../project test_unknown.c capture.c -L../project -lftprintf -o test_unknown
cc -Wall -Wextra -Werror -I../project test_write_error.c -L../project -lftprintf -o test_write_error
./test_unknown
./test_write_error
```

## Bônus

```sh
make -C ../project fclean
make -C ../project bonus
cc -Wall -Wextra -Werror -I../project test_precision.c capture.c -L../project -lftprintf -o test_precision
./test_precision
```

As linhas `INFO` de `test_precision` mostram `NULL` em `%s` / `%p`:
comportamento indefinido em C, varia entre libcs e não conta como falha.

## Limpeza

```sh
rm -f test_unknown test_write_error test_precision
make -C ../project fclean
```
