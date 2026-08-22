# Fluxo de uma chamada

```
get_next_line(fd):
    se fd < 0 ou BUFFER_SIZE <= 0:  devolve NULL
    stash = gnl_read_loop(fd, stash)      # fase 1: encher
    se stash == NULL:               devolve NULL
    line  = gnl_extract_line(stash)       # fase 2: copiar a linha
    stash = gnl_trim_stash(stash)         # fase 3: ficar com o resto
    devolve line
```

A ordem das fases 2 e 3 não é trocável: a extração lê o stash que a poda
libera. E cada resultado de fase volta **imediatamente** para a variável
estática — depois de `gnl_read_loop` falhar, a estática já é `NULL`; um teste
feito antes da atribuição deixaria um ponteiro pendurado para a chamada
seguinte (double free).

## Ciclo de vida do stash

O stash é a única memória entre chamadas: `static char *` dentro de
`get_next_line`, zerada pela linguagem antes do primeiro uso, invisível fora
da função.

```
             read_loop                    extract + trim
  NULL ────────────────▶ "a\n\nbb\n" ──────────────────▶ "\nbb\n"   (devolveu "a\n")
   ▲                                                        │
   │                  (sem read: já tem \n)                 ▼
   │ ◀──────────────── trim devolve NULL ◀───────────── "bb\n"      (devolveu "\n", "bb\n")
   │
   └── erro de read / malloc: read_loop libera e devolve NULL
```

**Invariante de repouso** — entre uma chamada e outra, o stash é:

- `NULL` (nada pendente), ou
- uma string **não vazia**, que pode ou não conter `\n`.

A string vazia nunca fica guardada: `gnl_trim_stash` devolve `NULL` quando
não sobra nada depois do `\n`. Não é estética — se `""` ficasse no stash, a
chamada seguinte no fim do arquivo veria stash não-`NULL`, extrairia `""` e a
função devolveria string vazia em vez de `NULL`, violando o contrato de
[../01-contrato/linha.md](../01-contrato/linha.md).

É esse invariante que dispensa `gnl_extract_line` de tratar entrada vazia: ela
só roda com stash não-`NULL` (testado no fluxo) e não-vazio (invariante).

## Quem aloca, quem libera

| Bloco | Alocado por | Liberado por |
|---|---|---|
| buffer de leitura (`B + 1` bytes) | `gnl_read_loop`, a cada chamada | `gnl_read_loop`, sempre, antes de retornar |
| stash | `gnl_strjoin_free` (junção) e `gnl_substr` (poda) | `gnl_strjoin_free` (a versão anterior), `gnl_trim_stash` (a atual), `gnl_read_loop` (no erro) |
| linha devolvida | `gnl_substr` via `gnl_extract_line` | **quem chamou `get_next_line`** |

Consequência observável (medida em
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)): consumido um
arquivo até o `NULL`, `valgrind` reporta `in use at exit: 0 bytes`. Se o
programa sai **sem** consumir tudo, o resto do stash continua alocado e
aparece como `still reachable` (a estática ainda aponta para ele) — nunca como
`definitely lost`.
