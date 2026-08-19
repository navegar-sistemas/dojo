# T08 — Desordem

## Objetivo

`compute_disorder` devolvendo a densidade de inversões da pilha inicial.

## Depende de

T06.

## Arquivos

- `disorder.c`
- `main.c` (trocar o stub `0.0` pela chamada real)

## Especificação

- [../04-algoritmos/desordem.md](../04-algoritmos/desordem.md)

## Implementação

```c
double	compute_disorder(t_stack *a)
{
	long	erros;
	long	pares;
	int		i;
	int		j;

	erros = 0;
	pares = 0;
	i = 0;
	while (i < a->size)
	{
		j = i + 1;
		while (j < a->size)
		{
			pares++;
			if (a->data[i] > a->data[j])
				erros++;
			j++;
		}
		i++;
	}
	if (pares == 0)
		return (0.0);
	return ((double)erros / (double)pares);
}
```

Quatro variáveis, quatro declarações separadas — a norma proíbe declaração com atribuição.

Os dois pontos que quebram silenciosamente:

- **A divisão precisa dos dois operandos em `double`.** Em inteiro o resultado é sempre 0, e o
  `--adaptive` do T13 cairia sempre no regime O(n²) sem nenhum sintoma visível até o benchmark.
- **`pares == 0`** acontece com 0 ou 1 elemento. Sem o teste, divisão por zero.

No `main`, trocar o `0.0` provisório pela chamada real, mantendo-a **antes** do despacho e de
`build_ranks` — ver [../03-arquitetura/fluxo.md](../03-arquitetura/fluxo.md).

## Pronto quando

```bash
make re
norminette *.c *.h
```

O `main` real já existe (T06), então aqui não entra `main` novo, e sim uma **sonda
temporária**: duas linhas logo depois de `d = compute_disorder(c.a);`, imprimindo a desordem
×10000 no stderr (libft não imprime `double`; o inteiro é exato). O `main` fica com 21 linhas
e a norminette continua verde. **Apague depois de conferir** — o contrato só permite stderr
com `--bench`.

```c
	ft_putnbr_fd((int)(d * 10000.0 + 0.5), 2);
	ft_putchar_fd('\n', 2);
```

| Entrada | Desordem | Sonda |
|---|---|---|
| `1 2 3` | 0.0000 | `0` |
| `3 2 1` | 1.0000 | `10000` |
| `4 67 3 87 23` | 0.4000 | `4000` |
| `2 1` | 1.0000 | `10000` |
| `42` | 0.0000 | `0` |
| nenhum elemento | 0.0000 | — |

```bash
for arg in "1 2 3" "3 2 1" "4 67 3 87 23" "2 1" "42"; do
  printf '%-16s -> %s\n' "$arg" "$(./push_swap $arg 2>&1 >/dev/null)"
done    # 0, 10000, 4000, 10000, 0
```

A linha "nenhum elemento" não passa pela sonda — o `main` encerra antes com `n = 0`. A guarda
`pares == 0` é exercitada em execução pelo `42` (1 elemento, zero pares).

O valor de `4 67 3 87 23` é o que aparece como `40.00%` no `--bench` do caso A2 — confirma de
uma vez a fórmula e a conversão para porcentagem que vem em T14.

Faixa em entrada aleatória, para conferir que a medida não está saturando em 0 ou 1:

```bash
# após T14, com --bench disponível
for i in 1 2 3 4 5; do
  ./push_swap --bench $(shuf -i 1-10000 -n 100 | tr '\n' ' ') 2>&1 >/dev/null | grep disorder
done
# todos entre 40% e 60%
```
