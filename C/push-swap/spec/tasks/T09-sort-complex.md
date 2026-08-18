# T09 — `--complex`

## Objetivo

Radix binário LSD com contagem determinística: 1084 movimentos para n = 100, 6784 para n = 500.

## Depende de

T06, T08.

## Arquivos

- `sort_complex.c`

## Especificação

- [../04-algoritmos/complex.md](../04-algoritmos/complex.md)
- [../06-aceitacao/casos.md](../06-aceitacao/casos.md) — A3

## Implementação

Três funções, duas `static`:

| Função | Papel |
|---|---|
| `bit_count` (static) | quantos bits o maior rank precisa |
| `radix_pass` (static) | uma passada sobre um bit |
| `sort_complex` | rótulos, casos base, ranks, laço de bits |

```c
static int	bit_count(int n)
{
	int	bits;

	bits = 0;
	while ((n - 1) >> bits)
		bits++;
	return (bits);
}

static void	radix_pass(t_ctx *c, int bit)
{
	int	i;
	int	size;

	i = 0;
	size = c->a->size;
	while (i < size)
	{
		if (((c->a->data[0] >> bit) & 1) == 0)
			op_pb(c);
		else
			op_ra(c);
		i++;
	}
	while (c->b->size > 0)
		op_pa(c);
}
```

`sort_complex` grava `"Complex"` / `"O(n log n)"`, trata `size <= 3` com `sort_tiny`, retorna se
já ordenada, calcula `bits` e roda `radix_pass` para `bit` de 0 até `bits - 1`. A pilha já chega
convertida em ranks — o `main` chamou `build_ranks` antes do despacho
([../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md)); a estratégia não aloca nada.

**Três armadilhas:**

- `size` é capturado **antes** do laço interno. Usar `c->a->size` na condição faz a varredura
  encurtar a cada `pb` e deixar elementos sem examinar — a pilha sai desordenada.
- `bit_count` usa `n - 1`, o maior rank. Com `n` em vez de `n - 1`, uma entrada de 256
  elementos gastaria 9 passadas em vez de 8.
- A contagem precisa ser **idêntica** entre entradas do mesmo tamanho. Variação indica bug em
  um dos dois pontos acima.

Ligar `run_strategy` a `sort_complex` para `STRAT_COMPLEX`.

## Pronto quando

```bash
make re
norminette *.c *.h
```

**A3 — determinismo e valores exatos:**

```bash
for i in 1 2 3 4 5; do
  ./push_swap --complex $(shuf -i 1-10000 -n 100 | tr '\n' ' ') | wc -l
done    # cinco vezes 1084

for i in 1 2 3; do
  shuf -i 0-9999 -n 500 > args.txt
  ./push_swap --complex $(cat args.txt) | wc -l
done    # três vezes 6784
```

**Corretude:**

```bash
i=0; falhas=0
while [ $i -lt 200 ]; do
  ARG=$(shuf -i 1-1000 -n $((RANDOM % 30 + 1)) | tr '\n' ' ')
  [ "$(./push_swap --complex $ARG | ../assets/checker_linux $ARG)" = "OK" ] || { echo "FALHOU: $ARG"; falhas=$((falhas+1)); }
  i=$((i+1))
done
echo "falhas: $falhas"
```

**Bordas de tamanho**, incluindo potências de 2 e vizinhos, onde a contagem de bits erra:

```bash
for n in 1 2 3 4 5 7 8 9 15 16 17 31 32 33 255 256 257; do
  ARG=$(shuf -i 1-10000 -n $n | tr '\n' ' ')
  echo -n "n=$n: "
  ./push_swap --complex $ARG | ../assets/checker_linux $ARG
done
```

**Valores negativos e extremos:**

```bash
ARG="-2147483648 2147483647 0 -1 1"
./push_swap --complex $ARG | ../assets/checker_linux $ARG    # OK
```

```bash
valgrind --leak-check=full ./push_swap --complex $(shuf -i 1-10000 -n 200 | tr '\n' ' ')
```
