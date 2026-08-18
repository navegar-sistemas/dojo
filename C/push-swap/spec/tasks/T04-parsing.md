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
int		flag_id(const char *s);
```

Cinco funções — a cota inteira do arquivo. `flag_id` mora aqui, e não em `parse.c`, porque lá a
cota já está tomada pelas três `static` de contagem e preenchimento.

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

Duas passadas evitam realocação. A alternativa é uma passada só com pilha crescente, o que
adiciona código de crescimento — a escolha é livre desde que a liberação no erro esteja certa.

Um `argv` de zero tokens numéricos no total (só flags) não é erro: devolve pilha com
`size == 0`, e o `main` encerra em silêncio.

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
imprimindo `Error` em stderr, nada em stdout, saída 1. A bateria exige o `main` com o caminho
de erro, que só chega em T05 — registre-a aqui e execute-a ao fechar T05 (T02 e T03 usam a
mesma tática do `main` temporário; aqui ele teria de duplicar o `fail` de T05, sem ganho):

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

Flags repetidas **não** são erro:

```bash
./push_swap --simple --simple 3 2 1 ; echo "exit=$?"   # equivale a --simple
./push_swap --bench --bench 3 2 1   ; echo "exit=$?"   # equivale a --bench
```

Casos silenciosos (A6):

```bash
./push_swap;         echo "exit=$?"      # nada, 0
./push_swap --bench; echo "exit=$?"      # nada, 0
```

Aceitação de números colados num argumento:

```bash
./push_swap "4 67 3" 87 23 | ../assets/checker_linux 4 67 3 87 23    # OK (após T06)
```

Memória em todos os caminhos de erro:

```bash
valgrind --leak-check=full ./push_swap 0 one 2 3
valgrind --leak-check=full ./push_swap "1 2" 3 four
valgrind --leak-check=full ./push_swap 1 1
valgrind --leak-check=full ./push_swap 2147483648
```
