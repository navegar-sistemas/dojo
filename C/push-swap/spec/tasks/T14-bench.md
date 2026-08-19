# T14 — `--bench`

## Objetivo

Bloco de métricas em stderr, byte a byte no formato do contrato.

## Depende de

T13.

## Arquivos

- `bench.c`
- `main.c` (trocar o stub de `bench_print` pela chamada real, depois do `prog_flush`)

## Especificação

- [../01-contrato/bench.md](../01-contrato/bench.md) — formato exato, alinhamento, invariantes
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A2 e A7

## Implementação

Três funções, duas `static`:

| Função | Papel |
|---|---|
| `put_percent` (static) | desordem com duas casas decimais |
| `put_counts` (static) | uma linha de contagens, do índice `from` ao `to` |
| `bench_print` | as cinco linhas |

```c
static void	put_percent(double d)
{
	int	cents;

	cents = (int)(d * 10000.0 + 0.5);
	ft_putnbr_fd(cents / 100, 2);
	ft_putchar_fd('.', 2);
	if (cents % 100 < 10)
		ft_putchar_fd('0', 2);
	ft_putnbr_fd(cents % 100, 2);
	ft_putchar_fd('%', 2);
}
```

O `+ 0.5` arredonda em vez de truncar. O zero à esquerda na parte decimal é obrigatório: 5
centésimos imprime `.05`, não `.5`.

As cinco linhas, todas no descritor 2:

```
[bench] disorder:  <percent>
[bench] strategy:  <name> / <cclass>
[bench] total_ops: <soma das contagens>
[bench] sa: n  sb: n  ss: n  pa: n  pb: n
[bench] ra: n  rb: n  rr: n  rra: n  rrb: n  rrr: n
```

**Espaçamento:** dois espaços depois de `disorder:` e `strategy:`, um depois de `total_ops:`.
Dois espaços entre os pares das duas últimas linhas. Nenhum espaço no fim da linha.

**`total_ops`** é a soma de `counts[0..10]`, preenchidos pelo `prog_flush` — assim o invariante
A7 vale por construção. `put_counts(c, OP_SA, OP_PB)` e `put_counts(c, OP_RA, OP_RRR)` imprimem
as duas linhas na ordem do enum.

No `main`, chamar `bench_print(&c, &conf, d)` depois do `prog_flush` e antes da liberação,
apenas se `conf.bench`.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A2 — comparação byte a byte:**

```bash
./push_swap --bench --adaptive 4 67 3 87 23 2> /tmp/meu.txt >/dev/null
cat > /tmp/esperado.txt <<'FIM'
[bench] disorder:  40.00%
[bench] strategy:  Adaptive / O(n√n)
[bench] total_ops: 9
[bench] sa: 1  sb: 0  ss: 0  pa: 2  pb: 2
[bench] ra: 1  rb: 0  rr: 0  rra: 2  rrb: 0  rrr: 1
FIM
diff /tmp/meu.txt /tmp/esperado.txt && echo "A2 bench ok" || echo "A2 bench DIFERE"
```

**A7 — invariantes:**

```bash
ARG=$(shuf -i 0-9999 -n 50 | tr '\n' ' ')
linhas=$(./push_swap $ARG | wc -l | tr -d ' ')
total=$(./push_swap --bench $ARG 2>&1 >/dev/null | grep total_ops | tr -dc '0-9')
soma=$(./push_swap --bench $ARG 2>&1 >/dev/null | tail -2 | tr -dc '0-9 \n' | tr ' ' '\n' | awk 'NF{s+=$1} END{print s}')
echo "linhas=$linhas total=$total soma=$soma"    # os três iguais
```

**Canal e condicionalidade:**

```bash
./push_swap 3 2 1 2>&1 >/dev/null | wc -c        # 0 — sem a flag, nada em stderr
./push_swap --bench 3 2 1 2>/dev/null | wc -l    # só a receita em stdout
```

**Casos de borda do percentual:**

```bash
./push_swap --bench 1 2 3 2>&1 >/dev/null | grep disorder    # 0.00%
./push_swap --bench 3 2 1 2>&1 >/dev/null | grep disorder    # 100.00%
```

**Rótulo por flag:**

```bash
for f in --simple --medium --complex --adaptive; do
  ./push_swap --bench $f 5 4 3 2 1 2>&1 >/dev/null | grep strategy
done
```

Esperado, nessa ordem:

```
[bench] strategy:  Simple / O(n²)
[bench] strategy:  Medium / O(n√n)
[bench] strategy:  Complex / O(n log n)
[bench] strategy:  Adaptive / O(n log n)
```

`5 4 3 2 1` está em ordem exatamente inversa, então a desordem é 1.0 e o adaptativo certifica o
regime O(n log n) — ainda que o programa vencedor venha do guloso. Uma entrada já ordenada tem
desordem 0 e imprime `Adaptive / O(n²)`.

**Entrada ordenada com `--bench`:**

```bash
./push_swap --bench 1 2 3 2>&1 >/dev/null
# total_ops: 0, todas as contagens 0, strategy Adaptive / O(n²)
```
