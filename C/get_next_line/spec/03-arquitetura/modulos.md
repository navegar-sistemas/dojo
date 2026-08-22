# Módulos

Uma responsabilidade por arquivo, dentro dos tetos de 5 funções por arquivo e
25 linhas por corpo. As contagens são as da implementação de referência, que
compila com `-Wall -Wextra -Werror` sem warning.

| Arquivo | Funções | Maior corpo | Linhas | Responsabilidade |
|---|---|---|---|---|
| `get_next_line.h` | — | — | 18 | protótipos e default de `BUFFER_SIZE` |
| `get_next_line.c` | 4 | 22 | 70 | as três fases e a orquestração |
| `get_next_line_utils.c` | 5 | 14 | 77 | utilitários de string tolerantes a `NULL` |

Bônus ([../05-bonus/multi-fd.md](../05-bonus/multi-fd.md)) — mesmos números,
exceto o header (22 linhas, pelo bloco de `FD_MAX`); os corpos são idênticos.

## Assinaturas públicas

Todas no header, na ordem do arquivo:

```c
char	*get_next_line(int fd);
size_t	gnl_strlen(const char *s);
char	*gnl_strchr(const char *s, int c);
size_t	gnl_cpy(char *dst, const char *src);
char	*gnl_substr(const char *s, size_t start, size_t len);
char	*gnl_strjoin_free(char *stash, const char *buf);
```

## Funções `static` de `get_next_line.c`

São as três fases de uma chamada — ver
[fluxo.md](fluxo.md) e o pseudocódigo em
[../04-algoritmo/leitura.md](../04-algoritmo/leitura.md).

| Função | Corpo | Papel |
|---|---|---|
| `gnl_read_loop(int fd, char *stash)` | 22 | lê até o stash conter `\n`, acabar o fluxo ou dar erro |
| `gnl_extract_line(const char *stash)` | 8 | copia a primeira linha do stash, `\n` incluído |
| `gnl_trim_stash(char *stash)` | 12 | troca o stash pelo resto depois do `\n` |
| `get_next_line(int fd)` | 11 | guarda de entrada + as três fases |

## Contratos

**`get_next_line`** guarda o stash numa `static char *` local (zerada pela
linguagem no primeiro uso). Devolve `NULL` imediatamente se `fd < 0` ou
`BUFFER_SIZE <= 0`. Atribui o retorno de cada fase **de volta à estática
antes de qualquer teste** — é isso que zera o estado nos caminhos de erro e
impede double free na chamada seguinte.

**`gnl_read_loop`** devolve o stash atualizado, ou `NULL` (e aí liberou tudo).
Aloca um buffer de `(size_t)BUFFER_SIZE + 1` bytes por chamada, sempre
liberado antes de retornar. Só chama `read` enquanto o stash não contém `\n` —
checado **antes** da primeira leitura, então uma linha já bufferizada custa
zero `read`. Em `read < 0` ou falha de `malloc`, libera o stash e devolve
`NULL`. Em fim de fluxo (`read == 0`), devolve o stash como está — possível
`NULL`, nunca string vazia.

**`gnl_extract_line`** exige stash não-`NULL` e não-vazio (garantido pelo
chamador — ver o invariante em [fluxo.md](fluxo.md)) e devolve uma cópia
alocada do prefixo até o primeiro `\n` inclusive, ou do stash inteiro se não
há `\n`. `NULL` só em falha de `malloc`.

**`gnl_trim_stash`** consome o stash antigo (sempre o libera) e devolve o
resto depois do primeiro `\n` — ou `NULL` se não há `\n` ou não há nada depois
dele. É o que mantém o invariante "o stash nunca é a string vazia".

**`gnl_strlen`** — como `strlen`, mas `NULL` conta como 0.

**`gnl_strchr`** — como `strchr` (incluindo achar o `\0` quando `c == '\0'`),
mas `NULL` devolve `NULL`. É a tolerância a `NULL` de `gnl_strlen`/`gnl_strchr`
que dispensa `gnl_read_loop` de tratar "primeira chamada, stash ainda `NULL`"
como caso especial.

**`gnl_cpy(dst, src)`** — copia `src` (até o `\0`, não incluído) para `dst` e
devolve o número de bytes copiados; `src == NULL` copia nada e devolve 0. Não
termina `dst` — o chamador fecha a string.

**`gnl_substr(s, start, len)`** — cópia alocada de `s[start .. start+len)`,
terminada em `\0`. Pré-condição do chamador: o intervalo existe em `s`.
`NULL` só em falha de `malloc`.

**`gnl_strjoin_free(stash, buf)`** — devolve `stash + buf` numa alocação
nova e **libera `stash` em todos os caminhos**, inclusive quando o `malloc`
falha — o chamador nunca precisa liberar o argumento. `stash == NULL` vale
como vazio. `buf` nunca é `NULL` (é o buffer de leitura recém-terminado).

## Direção das dependências

```
get_next_line
 ├── gnl_read_loop ──── gnl_strchr, gnl_strjoin_free ── gnl_strlen, gnl_cpy
 ├── gnl_extract_line ─ gnl_substr
 └── gnl_trim_stash ─── gnl_strchr, gnl_strlen, gnl_substr
```

Os utilitários não conhecem fd, `read` nem `BUFFER_SIZE`; só
`get_next_line.c` toca em I/O. Nenhuma seta aponta para trás.
