# Escritores

O andar de baixo das duas variantes: funções que tocam o descritor 1 e mais
nada. Todas seguem o contrato de retorno comum — bytes escritos ou `-1`
([../03-arquitetura/modulos.md](../03-arquitetura/modulos.md)).

## `pf_putchar` — as duas variantes

```c
int	pf_putchar(char c)
{
	if (write(1, &c, 1) < 0)
		return (-1);
	return (1);
}
```

O único código repetido byte a byte entre obrigatória e bônus
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)). Todo byte do
projeto sai por aqui.

## Obrigatória: `pf_putstr`

```
pf_putstr(s):
    se s == NULL: s = "(null)"
    i = 0
    enquanto s[i]:
        se pf_putchar(s[i]) < 0: devolve -1
        i += 1
    devolve i
```

O `(null)` mora aqui — na obrigatória não existe precisão, então a
substituição incondicional basta. No bônus a regra é condicional à precisão e
mora em `conv_s` ([../05-bonus/semantica.md](../05-bonus/semantica.md)).

## Bônus: `pf_putn` e `pf_pad`

```
pf_putn(s, n):                      pf_pad(c, n):
    i = 0                               i = 0
    enquanto i < n:                     enquanto i < n:
        putchar ou -1                       putchar ou -1
        i += 1                              i += 1
    devolve n                           se n < 0: devolve 0
                                        devolve n
```

`pf_putn` escreve os `n` primeiros bytes — é o truncamento de `%.3s` e a
reimpressão da desconhecida. `pf_pad` repete um byte `n` vezes e **aceita `n`
negativo devolvendo 0**: quem chama escreve `pf_pad(' ', f->width - len)` sem
testar se a largura já foi vencida — o caso "conteúdo maior que a largura"
desaparece nos chamadores.

## Bônus: `pf_strlen`

Comprimento de string do projeto (nenhuma função de biblioteca entra no
build — [../02-restricoes/build.md](../02-restricoes/build.md)). O montador o
chama até três vezes por campo; O(n) sobre strings de até 20 bytes não
justifica cache.
