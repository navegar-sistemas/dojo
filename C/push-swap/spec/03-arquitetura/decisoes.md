# Decisões de desenho

Escolhas que não são óbvias a partir do contrato, com a evidência que as sustenta.

## Pilha em array, não em lista encadeada

`data[0]` é o topo; rotação é um `ft_memmove` de `size - 1` inteiros mais a reposição de um
elemento.

A lista encadeada dá rotação O(1) contra O(n) do array, mas o custo em CPU é irrelevante aqui:
o pior caso do projeto é `--simple` com 500 elementos, ~34000 rotações de no máximo 2 KB, o que
é ordem de dezenas de milissegundos. Em troca, o array elimina toda a manipulação de ponteiros,
`stack_min_index` vira um `while` sobre índices, e cada função fica bem abaixo do limite de 25
linhas.

## Contagens por ponteiro em vez de flag booleana

`t_ctx.counts` sendo `NULL` significa "não imprime, não conta". O `checker` monta o contexto
com `NULL` e reaproveita as 11 operações intactas.

A alternativa — um campo `int silent` — exigiria que o `checker` também linkasse o vetor de
contagens sem usá-lo. O ponteiro carrega as duas informações numa coisa só.

## Sem buffer de operações e sem passe de otimização

Cada operação imprime a sigla no momento em que acontece e incrementa a contagem. Não existe
buffer intermediário nem otimizador de pares.

Um otimizador que cancela `ra`+`rra` e funde `ra`+`rb` em `rr` é a extensão natural, e foi
descartado por medição: simulando as três estratégias sobre 5 entradas aleatórias de 200
elementos cada, o número de pares adjacentes canceláveis ou fundíveis produzidos foi **zero**
em todas elas.

O motivo é estrutural. Toda rotação emitida pelas três estratégias é seguida de um `pb` ou de
um `pa`:

| Estratégia | Padrão emitido |
|---|---|
| `--simple` | `ra`×i ou `rra`×j, depois `pb` |
| `--medium` fase 1 | `ra` até o topo pertencer ao bloco, depois `pb` |
| `--medium` fase 2 | `rb`×i ou `rrb`×j, depois `pa` |
| `--complex` | `ra` ou `pb` alternando, depois `pa` em sequência |

Nunca aparecem `ra` e `rra` adjacentes, nem `ra` e `rb` adjacentes — e sem `a` e `b` girando ao
mesmo tempo, `rr`, `rrr` e `ss` nunca são gerados. O perfil de contagens do caso A2
([../06-aceitacao/casos.md](../06-aceitacao/casos.md)) mostra o mesmo: `rr`, `rrr` e `ss`
zerados.

Um otimizador aqui seria código morto que ainda assim precisaria passar na norma e no teste.
Ele só passa a valer a pena junto com uma estratégia gulosa, que gira as duas pilhas em direção
a um alvo comum e produz `rr`/`rrr` naturalmente.

## Caso base em n ≤ 3, não em n ≤ 5

As quatro estratégias delegam para `sort_tiny` quando restam 3 elementos ou menos. O limite é
3, e não os 5 usuais, para preservar a saída exata do caso A1: o selection sort completo
rodando em `--simple 5 4 3 2 1` é a única verificação exata do `--simple`. Números e ganho em
[../04-algoritmos/tiny.md](../04-algoritmos/tiny.md).

## Número de blocos do chunk sort: `max(2, isqrt(n / 2))`

A escolha aparentemente natural, `k = isqrt(n)`, não é a melhor: com ela o pior caso de 500
elementos passa de 8000 movimentos e o projeto cai para a faixa "passa"; com `isqrt(n / 2)`
fica em ~7590 e alcança "bom". A varredura de k que sustenta a escolha e o papel do piso de 2
estão em [../04-algoritmos/medium.md](../04-algoritmos/medium.md).

## Fase 1 do chunk sort só com `ra`

Girar sempre para cima é mais simples **e** mais barato que escolher o caminho mais curto até o
próximo membro do bloco: girar para trás embaralha a ordem em que os elementos chegam em `b` e
encarece a fase 2 mais do que economiza na fase 1. Medições em
[../04-algoritmos/medium.md](../04-algoritmos/medium.md).

## Tabela de nomes por cadeia de `if`

Ver [../02-restricoes/norma.md](../02-restricoes/norma.md): array local com inicializador viola
`DECL_ASSIGN_LINE` e tabela em escopo de arquivo é variável global, proibida neste projeto. A
cadeia de 11 `if` cabe em 23 linhas.

## Radix como estratégia O(n log n), não guloso

O radix binário tem contagem fechada e demonstrável: `bits × n` mais um `pa` por elemento com
bit zero, o que dá exatamente 1084 movimentos para n = 100 e 6784 para n = 500, sem variação
entre entradas.

A estratégia gulosa de custo mínimo gasta menos (é o caminho para "excelente"), mas seu número
de movimentos depende da entrada e o limite superior no modelo push_swap é O(n²), não
O(n log n) — declará-la como O(n log n) seria falso, e a classe declarada precisa ser válida no
modelo.
