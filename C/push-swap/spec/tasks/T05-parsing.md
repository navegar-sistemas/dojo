# T05 — Parsing e validação

## Objetivo

`argv` vira `t_conf` e `t_stack`, ou erro.

## Depende de

T02.

## Arquivos

- `parse.c`
- `parse_utils.c`

## Especificação

- [../01-contrato/cli.md](../01-contrato/cli.md) — flags e combinações
- [../01-contrato/entrada.md](../01-contrato/entrada.md) — gramática, limites, ordem da validação
- [../01-contrato/saida.md](../01-contrato/saida.md) — o que sai em erro

## Implementação

### `parse_utils.c`

```c
int		is_int_token(const char *s);
int		token_to_int(const char *s, int *out);
int		has_duplicates(t_stack *s);
void	free_split(char **parts);
int		flag_id(const char *s);
```

Cinco funções — a cota inteira do arquivo. `flag_id` mora aqui, e não em `parse.c`, porque lá a
cota já está tomada pelas três `static` de contagem e preenchimento.

**`is_int_token`** — devolve 1 se a string casa com `[+-]?[0-9]+` inteira. Rejeita string
vazia, só sinal, e qualquer caractere fora de `0-9` depois do sinal.

**`token_to_int`** — acumula em `long` com o sinal aplicado. Rejeita se o acumulado sair de
`-2147483648..2147483647` **durante** a acumulação, não só no fim: um token de 30 dígitos
estoura o `long` antes de terminar. Devolve 1 em sucesso, gravando em `*out`.

**`has_duplicates`** — dois `while` aninhados comparando todos os pares. Devolve 1 se achar
repetição.

**`free_split`** — percorre o array até o `NULL`, libera cada string e depois o array. Aceita
`NULL`.

**`flag_id`** — devolve `STRAT_SIMPLE`..`STRAT_ADAPTIVE`, `FLAG_BENCH`, ou 0 se não for
nenhuma flag conhecida. Compara com o comprimento do literal **mais um**, para incluir o
terminador:

```c
if (!ft_strncmp(s, "--simple", 9))
    return (STRAT_SIMPLE);
```

Sem o `+1`, `--simpleX` casaria como prefixo e seria aceito.

### `parse.c`

```c
int		parse_flags(int argc, char **argv, t_conf *conf);
t_stack	*parse_numbers(int argc, char **argv);
```

**`parse_flags`** — percorre `argv[1..argc-1]`. Token que não começa com `--` é ignorado.
Token que começa com `--` passa por `flag_id`:

- resultado 0 → erro (flag desconhecida, inclusive `--` sozinho).
- `FLAG_BENCH` → marca `conf->bench = 1`, mesmo que já estivesse marcado.
- um dos quatro seletores → erro **apenas** se `conf->strategy` já tiver um valor **diferente**;
  repetir o mesmo seletor é aceito.

```c
if (s == FLAG_BENCH)
    conf->bench = 1;
else if (conf->strategy != STRAT_NONE && conf->strategy != s)
    return (0);
else
    conf->strategy = s;
```

Devolve 0 em erro, 1 em sucesso. Não mexe em `name`/`cclass`.

Cuidado: `-42` começa com um hífen só, é número. A distinção é o prefixo de dois hifens.

**`parse_numbers`** — duas passadas sobre `argv`:

1. Conta quantos tokens numéricos existem no total, para dimensionar a pilha. Cada `argv` que
   não é flag passa por `ft_split(arg, ' ')`; se o resultado tiver zero elementos, erro.
2. Aloca a pilha com essa capacidade e preenche, validando cada token com `is_int_token` e
   `token_to_int`.

Ao final, `has_duplicates`. Qualquer falha: liberar o split em curso, liberar a pilha, devolver
`NULL`.

Duas passadas evitam realocação. Um `argv` de zero tokens numéricos no total (só flags) não é
erro: devolve pilha com `size == 0`, e o `main` encerra em silêncio.

As três `static` que fecham o arquivo em 5 funções:

| Função | Papel |
|---|---|
| `count_tokens(argc, argv, *total)` | primeira passada, dimensiona a pilha |
| `add_tokens(arg, a)` | divide um argumento, valida e empilha os tokens |
| `fill_all(argc, argv, a)` | laço sobre `argv` chamando `add_tokens` |

Sem essa separação `parse_numbers` passa de 25 linhas.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Todos os casos de erro de [../06-aceitacao/casos.md](../06-aceitacao/casos.md) A5, cada um
imprimindo `Error` em stderr, nada em stdout, saída 1. O `main` temporário abaixo (no lugar do
vigente; some em T06) liga os dois parses ao contrato de erro e, em sucesso, imprime o que o
parse produziu — a bateria roda **agora** e de novo em T06 com o `main` definitivo:

```c
#include "push_swap.h"

static int	fail(void)
{
	ft_putendl_fd("Error", 2);
	return (1);
}

static void	put_conf(t_conf *conf)
{
	ft_putstr_fd("strategy=", 1);
	ft_putnbr_fd(conf->strategy, 1);
	ft_putstr_fd(" bench=", 1);
	ft_putnbr_fd(conf->bench, 1);
}

int	main(int argc, char **argv)
{
	t_conf	conf;
	t_stack	*a;
	int		i;

	conf.strategy = STRAT_NONE;
	conf.bench = 0;
	if (!parse_flags(argc, argv, &conf))
		return (fail());
	a = parse_numbers(argc, argv);
	if (a == NULL)
		return (fail());
	put_conf(&conf);
	ft_putstr_fd(" n=", 1);
	ft_putnbr_fd(a->size, 1);
	i = -1;
	while (++i < a->size)
	{
		ft_putchar_fd(' ', 1);
		ft_putnbr_fd(a->data[i], 1);
	}
	ft_putchar_fd('\n', 1);
	stack_free(a);
	return (0);
}
```

`strategy=0` é `STRAT_NONE`: o desvio para `STRAT_ADAPTIVE` é papel do `setup` de T06, não do
parse. Sem argumentos imprime `n=0` — o silêncio nesse caso também é do `main` definitivo.

```bash
err_case() {
  out=$(./push_swap "$@" 2>/dev/null)
  err=$(./push_swap "$@" 2>&1 >/dev/null)
  ./push_swap "$@" >/dev/null 2>&1
  printf '%-32s stdout=[%s] stderr=[%s] exit=%s\n' "$*" "$out" "$err" "$?"
}
err_case 0 one 2 3
err_case 3 2 3
err_case 2147483648
err_case -2147483649
err_case 4.2
err_case +
err_case ""
err_case --foo 3 2 1
err_case --simple --medium 3 2 1
err_case --
```

Todos precisam sair com `stdout=[]`, `stderr=[Error]` e `exit=1`.

Flags repetidas **não** são erro — a equivalência fica visível na linha impressa:

```bash
./push_swap --simple --simple 3 2 1 ; echo "exit=$?"   # strategy=1 bench=0 n=3 3 2 1, exit=0
./push_swap --bench --bench 3 2 1   ; echo "exit=$?"   # strategy=0 bench=1 n=3 3 2 1, exit=0
```

Aceitação de números colados num argumento:

```bash
./push_swap "4 67 3" 87 23    # strategy=0 bench=0 n=5 4 67 3 87 23
./push_swap "4 67 3" 87 23 | ../assets/checker_linux 4 67 3 87 23    # OK (após T07)
```

Memória em todos os caminhos de erro:

```bash
valgrind --leak-check=full ./push_swap 0 one 2 3
valgrind --leak-check=full ./push_swap "1 2" 3 four
valgrind --leak-check=full ./push_swap 1 1
valgrind --leak-check=full ./push_swap 2147483648
```
