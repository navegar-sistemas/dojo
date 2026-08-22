# Fluxo

## O laço (bônus)

```c
int	ft_printf(const char *format, ...)
{
	va_list	ap;
	int		total;
	int		r;

	va_start(ap, format);
	total = 0;
	r = 0;
	while (*format && r >= 0)
	{
		if (*format == '%')
			r = pf_directive(&format, &ap);
		else
			r = pf_putchar(*format++);
		if (r > 0)
			total += r;
	}
	va_end(ap);
	if (r < 0)
		return (-1);
	return (total);
}
```

Três estados por iteração, todos carregados em `r`:

| `r` | Significado | Efeito |
|---|---|---|
| > 0 | bytes escritos pelo passo | soma em `total` |
| 0 | passo válido que escreveu nada (`"%.0d"` com 0) | nada a somar |
| −1 | `write` falhou **ou** diretiva incompleta | laço para, retorno −1 |

Os bytes já escritos ficam escritos — é o comportamento medido da referência
(`"abc%"` → `[abc]`, retorno −1).

## Consumo de uma diretiva

```c
static int	pf_directive(const char **fmt, va_list *ap)
{
	t_fmt	f;

	*fmt = parse_fmt(*fmt + 1, &f);
	if (f.conv == '\0')
		return (-1);
	*fmt = *fmt + 1;
	return (pf_dispatch(&f, ap));
}
```

Contrato de avanço: `pf_directive` recebe `*fmt` apontando para o `%` e o
deixa **depois** da diretiva inteira. `parse_fmt` devolve o ponteiro parado no
byte de conversão ([../05-bonus/formato.md](../05-bonus/formato.md)); o
`+ 1` final o consome. No caso incompleto (`f.conv == '\0'`) o retorno é
imediato: o laço vai parar, então a posição de `*fmt` deixa de importar.

A ordem interna não pode ser trocada: **analisar antes de saber se a conversão
é conhecida**. `"%-5r"` precisa das flags e da largura mesmo sendo
desconhecida — a reimpressão canônica usa a struct
([../05-bonus/semantica.md](../05-bonus/semantica.md)).

## Despacho

Cadeia de `if` sobre `f->conv` em `pf_dispatch`, terminando em
`conv_unknown`. Cada ramo faz o `va_arg` com o tipo da conversão e chama o
`conv_*` correspondente — o argumento só é consumido **depois** de saber que a
conversão consome ([../01-contrato/diretivas.md](../01-contrato/diretivas.md)):
`%%` e desconhecidas nunca tocam a lista variádica. Tabela de despacho em
vetor está proibida pelas regras de estilo
([../02-restricoes/estilo.md](../02-restricoes/estilo.md)).

## `va_list` por ponteiro

O laço declara `va_list ap` e passa `&ap` adiante; **todo** `va_arg` acontece
via `*ap`, dentro do despacho. O motivo é de ABI:

- No x86-64 (SysV), `va_list` é um array de uma struct. Passá-lo "por valor" a
  outra função na prática passa ponteiro, e o cursor avança para o chamador —
  funciona por acidente.
- No ARM64 da Apple, `va_list` é um `char *` simples. Por valor, a função
  chamada avança uma **cópia**, o chamador não vê nada, e o segundo `%d` relê
  o primeiro argumento.

`&ap` elimina a diferença: o único `va_list` vivo é o do laço, e todo mundo o
avança através do ponteiro. As duas variantes do projeto seguem a mesma regra
(`pf_conv(char conv, va_list *ap)` na obrigatória).

## O laço da parte obrigatória

Mesma estrutura com duas diferenças mecânicas, porque não existe
`pf_directive`:

- a diretiva incompleta é detectada no próprio laço
  (`*format == '%' && format[1] == '\0'` → `r = -1`);
- o avanço é `format++` no fim da iteração, com `pf_conv(*(++format), &ap)`
  consumindo o byte de conversão — dois bytes por diretiva, um por literal.

## Caminho de erro

Não existe limpeza a fazer: nenhuma alocação, nenhum estado fora da pilha.
Propagar o `-1` **é** o caminho de erro inteiro. Cada escritor devolve `-1`
assim que um `write` falha; montadores e conversões testam cada escrita e
repassam; o laço para na primeira falha e a `ft_printf` devolve `-1`.
