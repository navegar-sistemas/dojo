# T15 — `checker` (bônus)

## Objetivo

Segundo binário que executa a receita, com respostas idênticas às do binário de referência.

## Depende de

T04, T05 (módulos compartilhados). Roda por último antes do fechamento: bônus só interessa com
a parte obrigatória inteira verde.

## Arquivos

- `checker_bonus.c`
- `read_ops_bonus.c`
- `apply_op_bonus.c`
- `Makefile` (regra `bonus`, variáveis `BSRCS`/`BOBJS`/`SHARED`)

## Especificação

- [../05-bonus/checker.md](../05-bonus/checker.md) — contrato, módulos, fluxo
- [../02-restricoes/build.md](../02-restricoes/build.md) — objetos compartilhados na regra `bonus`

## Implementação

### `read_ops_bonus.c`

```c
static char	*grow(char *buf, int total, char *tmp, int n);
char		*read_all(int fd);
```

Lê em blocos de 1024 com `read` até EOF, acumulando num buffer que cresce por realocação.
Termina com `\0`. Devolve `NULL` em falha de alocação ou se `read` devolver `-1`; `0` é o EOF
normal. `grow` tem 4 parâmetros — o teto — e `read_all` fecha em exatamente 25 linhas de
corpo, o limite sem folga.

### `apply_op_bonus.c`

```c
static int	same(const char *s, int len, char *lit);
int			apply_line(t_ctx *c, const char *s, int len);
int			apply_rot(t_ctx *c, const char *s, int len);
```

`same` compara exatamente `len` bytes **e** exige que o literal termine ali (`lit[len] == '\0'`)
— sem isso, `r` casaria com `ra`. `apply_line` devolve 0 para sigla inexistente e para
`len == 0` (linha vazia); trata as cinco siglas que não são rotação e termina em
`return (apply_rot(c, s, len));`.

### `checker_bonus.c`

`main` mais as quatro `static` (`reject_flags`, `fail_ck`, `run_all`, `cleanup_ck`):

1. Zerar o contexto com `ft_memset` — `prog == NULL` é o modo executor: `emit` não grava nada
   e as 11 operações compartilhadas aplicam só o efeito.
2. `reject_flags` **antes** de `parse_numbers`: `argv` com prefixo `--` → `Error`, saída 255.
3. `parse_numbers`; erro → `Error`, 255. Zero números → nada, saída 0, sem ler stdin.
4. `b = stack_new(a->size)` e `read_all(0)`; falha → `Error`, 255.
5. `run_all` separa por `\n` e aplica cada linha; falha → `Error`, 255. **Sobra de bytes sem
   `\n` final também é erro** — o laço termina com `devolve (i == ini)`.
6. `stack_is_sorted(a) && b->size == 0` → `OK`, senão `KO`. Saída 0.
7. `fail_ck` e `cleanup_ck` liberam tudo, inclusive o buffer.

No `Makefile`, a regra `bonus: checker` linka `BOBJS` + `SHARED` + libft, com `SHARED`
incluindo `prog.o` e `utils.o` — a cadeia `emit → prog_push → ps_die` exige os dois no link
mesmo que o checker nunca grave nada.

## Pronto quando

```bash
make re                     # obrigatório continua verde
make bonus && make bonus    # a segunda não pode relinkar
make && make bonus          # nenhuma das duas relinca
norminette *.c *.h          # inclui os _bonus
```

**Comportamento básico:**

```bash
printf 'sa\nrra\n' | ./checker 3 2 1     ; echo "exit=$?"   # OK,    0
printf 'sa\n'      | ./checker 3 2 1     ; echo "exit=$?"   # KO,    0
printf ''          | ./checker 1 2 3     ; echo "exit=$?"   # OK,    0
printf ''          | ./checker 3 2 1     ; echo "exit=$?"   # KO,    0
printf 'xx\n'      | ./checker 3 2 1     ; echo "exit=$?"   # Error, 255
printf 'RA\n'      | ./checker 3 2 1     ; echo "exit=$?"   # Error, 255
printf 'ra \n'     | ./checker 3 2 1     ; echo "exit=$?"   # Error, 255
./checker 3 2 one  </dev/null            ; echo "exit=$?"   # Error, 255
./checker 3 2 3    </dev/null            ; echo "exit=$?"   # Error, 255
./checker ""       </dev/null            ; echo "exit=$?"   # Error, 255
./checker --simple 3 2 1 </dev/null      ; echo "exit=$?"   # Error, 255
./checker          </dev/null            ; echo "exit=$?"   # nada,  0
```

**Canais:**

```bash
printf 'xx\n' | ./checker 3 2 1 2>/dev/null | wc -c    # 0 — Error não vai para stdout
printf 'sa\nrra\n' | ./checker 3 2 1 2>/dev/null       # OK — veredito vai para stdout
```

**Comparação direta com a referência:**

```bash
i=0; difere=0
while [ $i -lt 100 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 15 + 2)) | tr '\n' ' ')
  OPS=$(./push_swap $ARG)
  meu=$(printf '%s\n' "$OPS" | ./checker $ARG)
  ref=$(printf '%s\n' "$OPS" | ../assets/checker_linux $ARG)
  [ "$meu" = "$ref" ] || { echo "DIFERE: $ARG meu=$meu ref=$ref"; difere=$((difere+1)); }
  i=$((i+1))
done
echo "divergências: $difere"
```

Receitas propositalmente erradas também precisam concordar:

```bash
for ops in "sa" "ra" "pb" "sa
pb" ""; do
  meu=$(printf '%s\n' "$ops" | ./checker 3 2 1)
  ref=$(printf '%s\n' "$ops" | ../assets/checker_linux 3 2 1)
  [ "$meu" = "$ref" ] && echo "ok   [$ops] $meu" || echo "DIFERE [$ops] meu=$meu ref=$ref"
done
```

**Ciclo completo:**

```bash
ARG=$(shuf -i 0-9999 -n 500 | tr '\n' ' ')
./push_swap --bench $ARG 2> /tmp/bench.txt | ./checker $ARG    # OK
cat /tmp/bench.txt
```

```bash
valgrind --leak-check=full ./checker 3 2 1 </dev/null
printf 'sa\nrra\n' | valgrind --leak-check=full ./checker 3 2 1
valgrind --leak-check=full ./checker 3 2 one </dev/null
```
