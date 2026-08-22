# T02 — Utilitários de string

## Objetivo

Os cinco utilitários de `get_next_line_utils.c`, com os contratos que
dispensam o núcleo de tratar `NULL` e liberar duas vezes.

## Depende de

T01.

## Arquivos

- `project/get_next_line_utils.c`
- `project/get_next_line.h` (acrescentar os cinco protótipos abaixo do público)

## Especificação

- [../03-arquitetura/modulos.md](../03-arquitetura/modulos.md) — assinaturas e contratos ("Contratos")
- [../02-restricoes/estilo.md](../02-restricoes/estilo.md) — por que `gnl_cpy` existe

## Implementação

Cinco funções — a cota exata do arquivo — na ordem, com os corpos da tabela
de módulos (8, 11, 9, 14, 14 linhas):

| Função | Contrato essencial |
|---|---|
| `gnl_strlen(s)` | `NULL` → 0 |
| `gnl_strchr(s, c)` | `NULL` → `NULL`; acha o `'\0'` se `c == '\0'` |
| `gnl_cpy(dst, src)` | copia `src` sem o `'\0'`, devolve quantos bytes; `src == NULL` → 0; **não** termina `dst` |
| `gnl_substr(s, start, len)` | cópia alocada e terminada de `s[start .. start+len)`; `NULL` só se `malloc` falhar |
| `gnl_strjoin_free(stash, buf)` | `stash + buf` numa alocação nova; **libera `stash` em todos os caminhos**, até no `malloc` falho; `stash == NULL` vale como vazio |

Esqueleto da junção — o único não trivial:

```
gnl_strjoin_free(stash, buf):
    out = malloc(gnl_strlen(stash) + gnl_strlen(buf) + 1)
    se out == NULL:
        free(stash)
        devolve NULL
    len  = gnl_cpy(out, stash)
    len += gnl_cpy(out + len, buf)
    out[len] = '\0'
    free(stash)
    devolve out
```

## Pronto quando

Do diretório `check/`:

```bash
P=../project
cat > utst.c <<'EOF'
#include "get_next_line.h"
#include <stdio.h>
#include <string.h>

int	g_bad = 0;

void	ck(const char *what, int ok)
{
	if (!ok)
	{
		printf("FALHOU %s\n", what);
		g_bad = 1;
	}
}

int	main(void)
{
	const char	*s = "a\nb";
	char		buf[4];
	char		*p;

	ck("strlen NULL", gnl_strlen(NULL) == 0);
	ck("strlen vazia", gnl_strlen("") == 0);
	ck("strlen abc", gnl_strlen("abc") == 3);
	ck("strchr NULL", gnl_strchr(NULL, '\n') == NULL);
	ck("strchr acha", gnl_strchr(s, '\n') == s + 1);
	ck("strchr nao acha", gnl_strchr("abc", '\n') == NULL);
	ck("strchr acha o nul", gnl_strchr(s, '\0') == s + 3);
	memset(buf, 'X', 4);
	ck("cpy NULL", gnl_cpy(buf, NULL) == 0 && buf[0] == 'X');
	ck("cpy ab", gnl_cpy(buf, "ab") == 2 && buf[0] == 'a' && buf[1] == 'b'
		&& buf[2] == 'X');
	p = gnl_substr("abcdef", 2, 3);
	ck("substr cde", p && strcmp(p, "cde") == 0);
	free(p);
	p = gnl_substr("abc", 0, 0);
	ck("substr vazia", p && p[0] == '\0');
	free(p);
	p = gnl_strjoin_free(NULL, "xy");
	ck("join sobre NULL", p && strcmp(p, "xy") == 0);
	p = gnl_strjoin_free(p, "z");
	ck("join consome", p && strcmp(p, "xyz") == 0);
	free(p);
	if (!g_bad)
		printf("utils ok\n");
	return (g_bad);
}
EOF
cc -Wall -Wextra -Werror -I$P utst.c $P/get_next_line_utils.c -o utst
valgrind --leak-check=full --error-exitcode=42 ./utst
```

Gabarito: `utils ok`, `in use at exit: 0 bytes`, `ERROR SUMMARY: 0 errors` —
o valgrind é o que comprova "a junção liberou o argumento" no encadeamento
`join(join(NULL, "xy"), "z")`.
