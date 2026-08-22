# Bônus — múltiplos descritores

A variante `_bonus` mantém o estado de leitura de **vários fds ao mesmo
tempo**: intercalar chamadas com os fds 3, 4 e 5 devolve as linhas de cada um
na ordem própria de cada arquivo, sem contaminação — verificado por
reconstrução byte a byte de 8 arquivos intercalados em
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md).

## A única diferença

Continua havendo **uma única variável estática** — agora um array de stashes
indexado pelo fd:

```
get_next_line(fd):                            # versão bônus
    se fd < 0 ou fd >= FD_MAX ou BUFFER_SIZE <= 0:  devolve NULL
    stash[fd] = gnl_read_loop(fd, stash[fd])
    se stash[fd] == NULL:                     devolve NULL
    line      = gnl_extract_line(stash[fd])
    stash[fd] = gnl_trim_stash(stash[fd])
    devolve line
```

`static char *stash[FD_MAX];` é zerada pela linguagem; cada posição segue,
sozinha, exatamente o ciclo de vida de
[../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md). As três fases e os
cinco utilitários são **byte a byte os mesmos** da parte obrigatória — só o
`#include` aponta para o header `_bonus`. Nenhuma função nova, nenhum corpo
mudou de tamanho.

## `FD_MAX`

```c
# ifndef FD_MAX
#  define FD_MAX 1024
# endif
```

Mesmo padrão do `BUFFER_SIZE`: default no header, sobrescrevível com
`-D FD_MAX=n`. Custo em repouso: `FD_MAX` ponteiros zerados no BSS — 8 KiB
com o default, nada na heap. `fd >= FD_MAX` cai na guarda de entrada e devolve
`NULL` sem efeito colateral (coberto na aceitação com `-D FD_MAX=4`).

A escolha do array em vez de lista de pares (fd, stash) está em
[../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md).

## Limite documentado

O estado é indexado pelo **número** do fd. Fechar um fd no meio de um arquivo
e reabrir outro arquivo no mesmo número herda o resto não consumido do
primeiro — não há como a função perceber a troca. Está fora do contrato
([../01-contrato/api.md](../01-contrato/api.md)); quem precisa descartar o
resto de um fd fechado pode chamar a função até `NULL` antes de reutilizar o
número.

## Obrigatório × bônus

| | obrigatória | bônus |
|---|---|---|
| estática | `char *stash` | `char *stash[FD_MAX]` |
| guarda | `fd < 0 \|\| BUFFER_SIZE <= 0` | idem `+ fd >= FD_MAX` |
| fds simultâneos | 1 (o último lido "ganha" o stash) | até `FD_MAX` |
| arquivos | `get_next_line.{c,h}`, `get_next_line_utils.c` | os mesmos com sufixo `_bonus` |

As duas variantes definem a mesma função pública e **não podem ser compiladas
juntas**.
