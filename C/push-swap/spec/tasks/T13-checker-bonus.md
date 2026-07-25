# T13 — `checker` (bônus)

## Objetivo

Segundo binário que executa a receita, com respostas idênticas às do binário de referência.

## Depende de

T12.

## Arquivos

- `checker_bonus.c`
- `read_ops_bonus.c`
- `apply_op_bonus.c`

## Especificação

- [../05-bonus/checker.md](../05-bonus/checker.md) — contrato, módulos, fluxo
- [../02-restricoes/build.md](../02-restricoes/build.md) — objetos compartilhados na regra `bonus`

## Implementação

### `read_ops_bonus.c`

```c
char	*read_all(int fd);
```

Lê em blocos com `read` até EOF, acumulando num buffer que cresce por realocação. Termina com
`\0`. Devolve `NULL` em falha de alocação ou se `read` devolver `-1`. `read` devolvendo `0` é o
EOF normal.

Ler tudo antes de aplicar é o que o enunciado descreve, e simplifica o erro: uma instrução
inválida no meio aborta antes de qualquer aplicação.

### `apply_op_bonus.c`

```c
int	apply_line(t_ctx *c, const char *s, int len);
```

Traduz o trecho de `len` bytes na sigla correspondente e chama a operação. Devolve 0 se a sigla
não existir.

A comparação é exata sobre os `len` bytes: `ra` é válido, `ra ` com espaço, `RA` e `ra;` não.
Linha vazia no meio da entrada é erro.

### `checker_bonus.c`

`main` mais os `static` que couberem:

1. `parse_numbers` sobre `argv`. Erro → `Error` em stderr, saída 255. O `checker` não tem
   flags, então um argumento começando com `--` é token numérico inválido.
2. Zero números → nada, saída 0.
3. `b = stack_new(a->size)`; contexto com **`counts = NULL`**.
4. `read_all(0)`.
5. Percorre o buffer separando por `\n` e chamando `apply_line`. Falha → `Error`, saída 255.
6. `stack_is_sorted(a) && b->size == 0` → `OK`, senão `KO`. Saída 0.
7. Libera tudo, inclusive o buffer.

O `counts = NULL` é o que faz `emit` não imprimir nada, permitindo reaproveitar as mesmas 11
operações do `push_swap` sem alteração.

## Pronto quando

```bash
make bonus && make bonus    # a segunda não pode relinkar
make re
norminette *.c *.h          # inclui os _bonus; erro neles zera o projeto
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
  ref=$(printf '%s\n' "$OPS" | ./assets/checker_Mac $ARG)
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
  ref=$(printf '%s\n' "$ops" | ./assets/checker_Mac 3 2 1)
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
leaks --atExit -- ./checker 3 2 1 </dev/null
printf 'sa\nrra\n' | leaks --atExit -- ./checker 3 2 1
leaks --atExit -- ./checker 3 2 one </dev/null
```
