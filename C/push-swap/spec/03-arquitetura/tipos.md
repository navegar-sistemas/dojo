# Tipos

Tudo em `push_swap.h`.

## Constantes de estratégia

```c
# define STRAT_NONE     0
# define STRAT_SIMPLE   1
# define STRAT_MEDIUM   2
# define STRAT_COMPLEX  3
# define STRAT_ADAPTIVE 4
```

`STRAT_NONE` é o valor inicial durante o parsing e serve para detectar dois seletores: gravar
por cima de qualquer coisa diferente de `STRAT_NONE` é erro.

## Pilha

```c
typedef struct s_stack
{
	int	*data;
	int	size;
	int	cap;
}	t_stack;
```

| Invariante | |
|---|---|
| `data[0]` | topo |
| `data[size - 1]` | fundo |
| `size` | 0 ≤ `size` ≤ `cap` |
| `cap` | fixado em `n` na criação; nunca muda |

As duas pilhas juntas nunca contêm mais que `n` elementos, então alocar `cap = n` para cada uma
elimina qualquer realocação durante a ordenação. O ponteiro `data` é estável do início ao fim,
o que permite guardá-lo numa variável local através de rotações.

## Operações

```c
typedef enum e_op
{
	OP_SA,
	OP_SB,
	OP_SS,
	OP_PA,
	OP_PB,
	OP_RA,
	OP_RB,
	OP_RR,
	OP_RRA,
	OP_RRB,
	OP_RRR
}	t_op;
```

A ordem dos membros é a ordem das colunas do `--bench`, o que permite indexar o vetor de
contagens direto pelo enum e imprimir as duas linhas de métricas percorrendo `0..10`.

## Contexto de execução

```c
typedef struct s_ctx
{
	t_stack	*a;
	t_stack	*b;
	int		*counts;
}	t_ctx;
```

`counts` aponta para um `int[11]` indexado por `t_op`, e define o modo de operação:

| `counts` | Modo | Quem usa |
|---|---|---|
| não-`NULL` | gerador: aplica o efeito, imprime a sigla em stdout, incrementa a contagem | `push_swap` |
| `NULL` | executor: aplica só o efeito | `checker` |

É esse ponteiro que permite ao `checker` reaproveitar as mesmas 11 funções de operação sem
imprimir nada. Também é o que garante o invariante do `--bench`: a contagem e a impressão
acontecem na mesma linha de código, então stdout e métricas não têm como divergir.

Um único parâmetro também resolve o problema do `-Wunused-parameter`: se as operações
recebessem `(t_stack *a, t_stack *b)`, `op_sa` não usaria `b` e a compilação falharia com
`-Werror`.

## Configuração

```c
typedef struct s_conf
{
	int		strategy;
	int		bench;
	char	*name;
	char	*cclass;
}	t_conf;
```

`name` e `cclass` são `char *`, **não** `const char *`. Receber literais de string num `char *`
é legal em C e não gera aviso; já declarar os campos como `const char *` faz
`ft_putstr_fd(conf->name, 2)` falhar na compilação, porque o parâmetro da libft é `char *` e o
descarte do qualificador é erro sob `-Werror`:

```
error: passing 'const char *' to parameter of type 'char *' discards qualifiers
       [-Werror,-Wincompatible-pointer-types-discards-qualifiers]
```

| Campo | Origem | Uso |
|---|---|---|
| `strategy` | flags | despacho |
| `bench` | flag `--bench` | decide se as métricas saem |
| `name` | gravado pela estratégia que roda | `--bench` |
| `cclass` | gravado pela estratégia que roda | `--bench` |

`name` e `cclass` são preenchidos em tempo de execução, não na configuração: em `--adaptive`,
só depois de medir a desordem se sabe qual classe reportar. A estratégia escolhida grava a
própria classe e o `sort_adaptive` sobrescreve apenas o nome com `"Adaptive"`.

## Ciclo de vida da memória

| Bloco | Alocado em | Liberado em |
|---|---|---|
| `a` e `a->data` | parsing | fim do `main`, e em todo caminho de erro |
| `b` e `b->data` | após o parsing | fim do `main` |
| array do `ft_split` | por argumento, durante o parsing | logo após consumir os tokens, inclusive no caminho de erro |
| cópia ordenada dos ranks | `build_ranks` | antes de `build_ranks` retornar |

O vetor `counts` é uma variável local do `main`, sem alocação.
