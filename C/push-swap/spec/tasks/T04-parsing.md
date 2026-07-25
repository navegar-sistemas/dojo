# T04 — Parsing e validação

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
```

**`is_int_token`** — devolve 1 se a string casa com `[+-]?[0-9]+` inteira. Rejeita string
vazia, só sinal, e qualquer caractere fora de `0-9` depois do sinal.

**`token_to_int`** — acumula em `long`. Rejeita se o acumulado sair de
`-2147483648..2147483647` **durante** a acumulação, não só no fim: um token de 30 dígitos
estoura o `long` antes de terminar. Testar a cada dígito contra os limites de `int` resolve os
dois problemas de uma vez. Devolve 1 em sucesso, gravando em `*out`.

**`has_duplicates`** — dois `while` aninhados comparando todos os pares. Devolve 1 se achar
repetição.

**`free_split`** — percorre o array até o `NULL`, libera cada string e depois o array. Aceita
`NULL`.

### `parse.c`

```c
int		parse_flags(int argc, char **argv, t_conf *conf);
t_stack	*parse_numbers(int argc, char **argv);
```

**`parse_flags`** — percorre `argv[1..argc-1]`. Token que não começa com `--` é ignorado.
Token que começa com `--`:

- `--bench` → se `conf->bench` já é 1, erro; senão marca 1.
- um dos quatro seletores → se `conf->strategy != STRAT_NONE`, erro; senão grava.
- qualquer outro, inclusive `--` sozinho → erro.

Devolve 0 em erro, 1 em sucesso. Não mexe em `name`/`cclass`.

Cuidado: `-42` começa com um hífen só, é número. A distinção é o prefixo de dois hifens.

**`parse_numbers`** — duas passadas sobre `argv`:

1. Conta quantos tokens numéricos existem no total, para dimensionar a pilha. Cada `argv` que
   não é flag passa por `ft_split(arg, ' ')`; se o resultado tiver zero elementos, erro.
2. Aloca a pilha com essa capacidade e preenche, validando cada token com `is_int_token` e
   `token_to_int`.

Ao final, `has_duplicates`. Qualquer falha: liberar o split em curso, liberar a pilha, devolver
`NULL`.

Duas passadas evitam realocação. A alternativa é uma passada só com pilha crescente, o que
adiciona código de crescimento — a escolha é livre desde que a liberação no erro esteja certa.

Um `argv` de zero tokens numéricos no total (só flags) não é erro: devolve pilha com
`size == 0`, e o `main` encerra em silêncio.

O arquivo tem duas funções públicas e cabem até três `static` — use-as para separar contagem de
preenchimento e manter cada corpo abaixo de 25 linhas.

## Pronto quando

```bash
make re
norminette *.c *.h
```

Todos os casos de erro de [../06-aceitacao/casos.md](../06-aceitacao/casos.md) A5, cada um
imprimindo `Error` em stderr, nada em stdout, saída 1:

```bash
for arg in "0 one 2 3" "3 2 3" "2147483648" "-2147483649" "4.2" "+" "--foo 3 2 1" \
           "--simple --medium 3 2 1" "--simple --simple 3 2 1" "--bench --bench 3 2 1"; do
  out=$(./push_swap $arg 2>/dev/null)
  err=$(./push_swap $arg 2>&1 >/dev/null)
  code=$?
  echo "[$arg] stdout=[$out] stderr=[$err]"
done
./push_swap "" ; echo "exit=$?"          # Error, 1
```

Casos silenciosos (A6):

```bash
./push_swap;         echo "exit=$?"      # nada, 0
./push_swap --bench; echo "exit=$?"      # nada, 0
```

Aceitação de números colados num argumento:

```bash
./push_swap "4 67 3" 87 23 | ./assets/checker_Mac 4 67 3 87 23    # OK (após T06)
```

Memória em todos os caminhos de erro:

```bash
leaks --atExit -- ./push_swap 0 one 2 3
leaks --atExit -- ./push_swap "1 2" 3 four
leaks --atExit -- ./push_swap 1 1
leaks --atExit -- ./push_swap 2147483648
```
