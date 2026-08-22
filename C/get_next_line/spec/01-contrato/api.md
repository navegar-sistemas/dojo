# API

Uma única função pública:

```c
char	*get_next_line(int fd);
```

| | |
|---|---|
| **Parâmetro** | `fd`: descritor de arquivo aberto para leitura |
| **Retorno** | a próxima linha do fd, alocada com `malloc` — ou `NULL` |
| **Efeito** | consome do fd apenas o necessário para completar uma linha |
| **Estado** | uma única variável estática interna; nenhuma variável global |

Quem chama é dono do retorno e deve dar `free` nele. A função nunca devolve a
string vazia: ou devolve uma linha com pelo menos 1 byte, ou devolve `NULL`.

Funciona com qualquer descritor legível — arquivo regular, `stdin`, pipe. Não
há reposicionamento (`lseek` é proibido — ver
[../02-restricoes/build.md](../02-restricoes/build.md)): bytes lidos do fd são
consumidos uma única vez, e o que ainda não foi devolvido fica guardado no
stash interno para as próximas chamadas.

## `BUFFER_SIZE`

O tamanho de cada `read` é a macro `BUFFER_SIZE`, fixada na linha de
compilação:

```sh
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c ...
```

O header define o padrão **42** dentro de `#ifndef BUFFER_SIZE`, então o
projeto compila **com e sem** a flag `-D`. O comportamento observável (a
sequência de retornos) é idêntico para todo `BUFFER_SIZE ≥ 1` — a suíte
verifica de 1 a 10 000 000 — e só o desempenho muda
(ver [../04-algoritmo/leitura.md](../04-algoritmo/leitura.md)).

## Todos os retornos `NULL`

| Situação | O que acontece antes do `NULL` |
|---|---|
| fim: não há mais nenhum byte para devolver | stash já é `NULL`; nada a fazer |
| `fd < 0` | nada — guarda de entrada, nenhum efeito colateral |
| `BUFFER_SIZE ≤ 0` na compilação | nada — mesma guarda, avaliada em tempo de compilação |
| `read` devolve negativo (fd inválido, fechado, diretório, sem permissão de leitura) | o stash pendente é **liberado**; o estado volta a zero |
| `malloc` falha (buffer, junção ou extração) | o stash é liberado; estado a zero; nenhum byte é perdido em silêncio no meio de uma linha |

Depois de um `NULL`, chamar de novo com o mesmo fd é seguro e devolve `NULL`
de novo (ou volta a ler, se o fd voltou a ter dados — o estado foi zerado).

Uma sutileza que os testes cobrem: se uma chamada anterior deixou linhas
completas bufferizadas no stash, `read` não é chamado — então um fd **já
fechado** ainda devolve essas linhas até o stash ficar sem `\n`, e só aí o
`read` falha e a função devolve `NULL` liberando o resto. É consequência
direta de "consome do fd apenas o necessário".

## Fora do contrato

Comportamento não especificado (nenhum teste cobre, nenhuma garantia):

- o arquivo é **modificado** entre chamadas, antes de o fd chegar ao fim;
- o fd aponta para conteúdo **binário** (bytes 0x00 no meio do fluxo: as
  funções internas tratam o stash como string terminada em `\0`);
- no bônus, um fd é fechado no meio de um arquivo e o mesmo número é
  reaproveitado para outro arquivo — o resto não consumido é herdado
  (ver [../05-bonus/multi-fd.md](../05-bonus/multi-fd.md)).
