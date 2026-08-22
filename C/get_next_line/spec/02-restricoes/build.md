# Build e entrega

## Arquivos

Parte obrigatória:

| Arquivo | Papel |
|---|---|
| `get_next_line.h` | protótipos, `#include`s de sistema, default de `BUFFER_SIZE` |
| `get_next_line.c` | as três fases e a função pública |
| `get_next_line_utils.c` | os cinco utilitários de string |

Bônus — mesmos papéis, sufixo `_bonus`:

| Arquivo | Papel |
|---|---|
| `get_next_line_bonus.h` | idem, mais o default de `FD_MAX` |
| `get_next_line_bonus.c` | idem, com o estado indexado por fd |
| `get_next_line_utils_bonus.c` | cópia exata dos utilitários (só muda o `#include`) |

Mais um `README.md` de apresentação do diretório: o que a função faz, como
compilar, justificativa do algoritmo e referências.

**Não há Makefile nem binário próprio.** A função é incorporada ao programa
hospedeiro, que compila os `.c` junto dos dele. Obrigatório e bônus nunca são
compilados juntos — definem a mesma função pública.

## Compilação

```sh
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
   get_next_line.c get_next_line_utils.c main_do_hospedeiro.c
```

Regras que a suíte de aceitação exercita:

- compila **sem** `-D BUFFER_SIZE` (o header fornece 42 via `#ifndef`);
- compila e se comporta corretamente com `-D BUFFER_SIZE=` 0, 1, 2, 5, 42,
  43, 9999, 1048576 e 10000000 (com 0, toda chamada devolve `NULL`);
- zero warnings com `-Wall -Wextra -Werror`;
- os headers aguentam dupla inclusão (`#ifndef GET_NEXT_LINE_H`).

## Funções externas

Permitidas: **`read`, `malloc`, `free`** — e nada além. Em particular:

- **`lseek` é proibida**: nada de reposicionar o fd; o resto de buffer
  sobrevive entre chamadas no stash, não no offset do arquivo;
- nenhuma outra função de biblioteca (`strlen`, `strchr`, `strdup`, …): os
  utilitários próprios em `get_next_line_utils.c` cobrem o necessário;
- nenhuma variável global.

## Prefixo `gnl_`

Todo símbolo exportado além de `get_next_line` leva o prefixo `gnl_`. O
hospedeiro tipicamente linca estes arquivos junto de uma biblioteca própria
com `strlen`/`strchr` próprios — nomes como `ft_strlen` colidiriam no link;
`gnl_strlen` não colide com nada.
