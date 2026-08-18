# Tarefas

## Quadro

| # | Tarefa | Depende de | Entrega |
|---|---|---|---|
| [T01](T01-esqueleto-build.md) | Esqueleto de build | — | `Makefile`, `push_swap.h`, `libft/` |
| [T02](T02-pilha.md) | Pilha | T01 | `stack.c` |
| [T03](T03-operacoes.md) | Operações e emissão | T02 | `emit.c`, `ops_*.c` |
| [T04](T04-parsing.md) | Parsing e validação | T02 | `parse.c`, `parse_utils.c` |
| [T05](T05-orquestracao.md) | Orquestração do `main` | T03, T04 | `main.c`, `utils.c` (`zero_counts`) |
| [T06](T06-sort-tiny-simple.md) | Caso base e `--simple` | T05 | `sort_tiny.c`, `sort_simple.c`, `utils.c` |
| [T07](T07-desordem.md) | Desordem | T05 | `disorder.c` |
| [T08](T08-ranks.md) | Ranks | T02 | `rank.c` |
| [T09](T09-sort-complex.md) | `--complex` | T06, T08 | `sort_complex.c` |
| [T10](T10-sort-medium.md) | `--medium` | T06, T08 | `sort_medium.c` |
| [T11](T11-sort-adaptive.md) | `--adaptive` | T07, T09, T10 | `sort_adaptive.c` |
| [T12](T12-bench.md) | `--bench` | T11 | `bench.c` |
| [T13](T13-checker-bonus.md) | `checker` | T12 | `*_bonus.c` |
| [T14](T14-fechamento.md) | Fechamento | T13 | validação final |

## Ordem

T02, T03 e T04 podem ser feitas em paralelo depois de T01, e T08 em paralelo com T05–T07. O
resto é sequencial pelas dependências.

O primeiro ponto verificável de ponta a ponta é **T06**: antes disso não existe receita para
conferir contra o checker de referência.

## Formato de uma tarefa

Cada arquivo tem:

- **Objetivo** — uma frase.
- **Depende de** — tarefas que precisam estar prontas.
- **Arquivos** — o que é criado ou alterado.
- **Especificação** — links para os documentos que definem o comportamento.
- **Implementação** — o que fazer, na granularidade de função.
- **Pronto quando** — comandos com a saída esperada. Todos verdes, sem exceção.

## Header incremental

`push_swap.h` nasce mínimo em T01 (apenas a guarda de inclusão) e cresce junto com as tarefas: a
tarefa que cria um tipo ou função pública é a que acrescenta a declaração ao header, guiada
por [tipos.md](../03-arquitetura/tipos.md) e [modulos.md](../03-arquitetura/modulos.md).
Nenhuma tarefa transcreve declarações de código que ainda não existe.

## Regra de conclusão

Uma tarefa só está pronta com **todos** os comandos de "Pronto quando" executados e verdes, no
estado atual do código. Isso inclui, em toda tarefa que toca `.c` ou `.h`:

```bash
make re            # zero warning
norminette *.c *.h # nenhuma linha "Error:"
```

Tarefa anterior vermelha bloqueia a seguinte.
