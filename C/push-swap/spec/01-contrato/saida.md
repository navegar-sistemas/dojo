# Saídas e códigos de retorno

## Tabela geral

| Situação | stdout | stderr | exit |
|---|---|---|---|
| Ordenação normal | receita, um movimento por linha | — | 0 |
| Entrada já ordenada | nada | — | 0 |
| Zero números (com ou sem flags) | nada | — | 0 |
| `--bench` presente e há o que ordenar | receita | bloco de métricas | 0 |
| Erro de entrada | nada | `Error\n` | 1 |
| Falha de `malloc` | nada | `Error\n` | 1 |

## Receita

- Uma sigla por linha, terminada por `\n`.
- `\n` é o único separador. Sem espaços à direita, sem linha em branco, sem cabeçalho.
- A última linha também termina em `\n`.
- Siglas em minúsculas, exatamente: `sa sb ss pa pb ra rb rr rra rrb rrr`.

Verificação byte a byte:

```bash
./push_swap 3 2 1 | cat -A
```

Não pode aparecer nada além das siglas e do `$` que o `cat -A` usa para marcar o fim de linha.

## Entrada já ordenada

Nenhum movimento é emitido, para qualquer uma das quatro flags. A verificação acontece no
despachante, antes da estratégia rodar — sem ela, o selection sort do `--simple` emitiria
`2n` movimentos numa pilha que já está pronta.

Com `--bench`, o bloco de métricas ainda sai, com `total_ops: 0` e todas as contagens zeradas.
A estratégia reportada é a que teria rodado.

## Erro

A mensagem é exatamente cinco bytes: `E`, `r`, `r`, `o`, `r`, `\n`. Sem prefixo, sem detalhe da
causa, sem ponto final. Sempre em stderr, nunca em stdout.

```bash
./push_swap 0 one 2 3 2>/dev/null    # não imprime nada
./push_swap 0 one 2 3 1>/dev/null    # imprime Error
```

O código de saída em erro não é verificado pelo enunciado; 1 é a escolha deste projeto e vale
para todos os casos de erro, inclusive falha de alocação.

## Falha de alocação

Tratada como erro de entrada: `Error` em stderr e saída 1. Todas as alocações que podem
falhar acontecem antes do primeiro movimento ser emitido — a conversão em ranks, que é a única
alocação dentro de uma estratégia, roda antes de qualquer `pb`. Não existe caminho em que
parte da receita foi impressa e depois a alocação falha.

## Independência dos canais

A receita vai para o descritor 1 e as métricas para o 2, o que permite consumir os dois
separadamente na mesma execução:

```bash
./push_swap --bench $(cat args.txt) 2> bench.txt | ./assets/checker_Mac $(cat args.txt)
```

Relacionado: [bench.md](bench.md) para o formato das métricas.
