# Casos de aceitação

Entradas com saída e retorno exatos, **medidos** na `printf` da glibc 2.36 —
o gabarito do espelho ([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)).
Colchetes delimitam os bytes da saída e não fazem parte dela; espaços dentro
deles são bytes reais. A implementação reproduz cada linha, byte a byte e
retorno a retorno, pelo harness de [validacao.md](validacao.md).

## Encadeamento (parte obrigatória)

```
ft_printf("%c|%s|%p|%d|%i|%u|%x|%X|%%", 'q', "str", (void *)0x42,
	-5, 6, 7u, 8u, 9u)
→ [q|str|0x42|-5|6|7|8|9|%]    retorno 23
```

Uma diretiva de cada conversão na mesma chamada; o retorno soma literais e
campos. As linhas por conversão sem flags estão em
[../01-contrato/conversoes.md](../01-contrato/conversoes.md); daqui para baixo
está a matriz do bônus.

## `%p`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%p"` | `(void *)0` | `[(nil)]` | 5 |
| `"%8p"` | `(void *)0` | `[   (nil)]` | 8 |
| `"%-8p"` | `(void *)0` | `[(nil)   ]` | 8 |
| `"%08p"` | `(void *)0` | `[   (nil)]` | 8 |
| `"%.3p"` | `(void *)0` | `[(nil)]` | 5 |
| `"%+p"` | `(void *)0` | `[(nil)]` | 5 |
| `"%p"` | `0x1234` | `[0x1234]` | 6 |
| `"%020p"` | `0x1234` | `[0x000000000000001234]` | 20 |
| `"%.20p"` | `0x1234` | `[0x00000000000000001234]` | 22 |
| `"%+p"` | `0x1234` | `[+0x1234]` | 7 |
| `"% p"` | `0x1234` | `[ 0x1234]` | 7 |
| `"%#p"` | `0x1234` | `[0x1234]` | 6 |
| `"%08.3p"` | `0x1234` | `[  0x1234]` | 8 |
| `"%+.8p"` | `0x1234` | `[+0x00001234]` | 11 |
| `"% 015p"` | `0x1234` | `[ 0x000000001234]` | 15 |
| `"%p"` | `0xffffffffffffffff` | `[0xffffffffffffffff]` | 18 |

As quatro últimas linhas de `NULL` mostram o caminho de string: largura com
espaços (mesmo com `0`), precisão e sinais ignorados. Nas não nulas, o
prefixo de sinal vem **antes** do `0x` e os zeros depois dele.

## `%c`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%c"` | `'a'` | `[a]` | 1 |
| `"%5c"` | `'a'` | `[    a]` | 5 |
| `"%-5c"` | `'a'` | `[a    ]` | 5 |
| `"%05c"` | `'a'` | `[    a]` | 5 |
| `"%.3c"` | `'a'` | `[a]` | 1 |
| `"%+c"` | `'a'` | `[a]` | 1 |

## `%s`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%s"` | `"hi"` | `[hi]` | 2 |
| `"%s"` | NULL | `[(null)]` | 6 |
| `"%.3s"` | NULL | `[]` | 0 |
| `"%.5s"` | NULL | `[]` | 0 |
| `"%.6s"` | NULL | `[(null)]` | 6 |
| `"%8s"` | NULL | `[  (null)]` | 8 |
| `"%5.3s"` | `"hello"` | `[  hel]` | 5 |
| `"%-5.3s"` | `"hello"` | `[hel  ]` | 5 |
| `"%05s"` | `"hi"` | `[   hi]` | 5 |
| `"%.0s"` | `"hi"` | `[]` | 0 |
| `"%.s"` | `"hi"` | `[]` | 0 |
| `"%5s"` | `""` | `[     ]` | 5 |

O degrau do `NULL`: precisão < 6 suprime o `(null)` inteiro; a partir de 6
(ou sem precisão) ele sai inteiro. `%05s` alinha com espaços — `0` é ignorada
em campo de texto.

## `%%`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%%"` | — | `[%]` | 1 |
| `"%5%"` | — | `[%]` | 1 |
| `"%-5%"` | — | `[%]` | 1 |
| `"%05%"` | — | `[%]` | 1 |
| `"%.3%"` | — | `[%]` | 1 |

## `%d` / `%i`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%d"` | `0` | `[0]` | 1 |
| `"%.0d"` | `0` | `[]` | 0 |
| `"%.d"` | `0` | `[]` | 0 |
| `"%5.0d"` | `0` | `[     ]` | 5 |
| `"%05.0d"` | `0` | `[     ]` | 5 |
| `"%.3d"` | `0` | `[000]` | 3 |
| `"%+.0d"` | `0` | `[+]` | 1 |
| `"% .0d"` | `0` | `[ ]` | 1 |
| `"%05d"` | `42` | `[00042]` | 5 |
| `"%-5d"` | `42` | `[42   ]` | 5 |
| `"%-05d"` | `42` | `[42   ]` | 5 |
| `"% d"` | `42` | `[ 42]` | 3 |
| `"%+d"` | `42` | `[+42]` | 3 |
| `"% +d"` | `42` | `[+42]` | 3 |
| `"%+05d"` | `42` | `[+0042]` | 5 |
| `"% 05d"` | `42` | `[ 0042]` | 5 |
| `"%.5d"` | `42` | `[00042]` | 5 |
| `"%5.3d"` | `42` | `[  042]` | 5 |
| `"%05.3d"` | `42` | `[  042]` | 5 |
| `"%#d"` | `42` | `[42]` | 2 |
| `"%05d"` | `-42` | `[-0042]` | 5 |
| `"%.5d"` | `-42` | `[-00042]` | 6 |
| `"%+d"` | `-42` | `[-42]` | 3 |
| `"%5.3d"` | `-42` | `[ -042]` | 5 |
| `"%-8.5d"` | `-42` | `[-00042  ]` | 8 |
| `"%09.5d"` | `-42` | `[   -00042]` | 9 |
| `"%d"` | `INT_MIN` | `[-2147483648]` | 11 |
| `"%020d"` | `INT_MIN` | `[-0000000002147483648]` | 20 |
| `"%d"` | `INT_MAX` | `[2147483647]` | 10 |

## `%u`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%u"` | `0` | `[0]` | 1 |
| `"%u"` | `UINT_MAX` | `[4294967295]` | 10 |
| `"%+u"` | `42` | `[42]` | 2 |
| `"% u"` | `42` | `[42]` | 2 |
| `"%#u"` | `42` | `[42]` | 2 |
| `"%.0u"` | `0` | `[]` | 0 |
| `"%.5u"` | `42` | `[00042]` | 5 |

## `%x` / `%X`

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%x"` | `0` | `[0]` | 1 |
| `"%#x"` | `0` | `[0]` | 1 |
| `"%#.0x"` | `0` | `[]` | 0 |
| `"%.0x"` | `0` | `[]` | 0 |
| `"%#x"` | `255` | `[0xff]` | 4 |
| `"%#X"` | `255` | `[0XFF]` | 4 |
| `"%#08x"` | `255` | `[0x0000ff]` | 8 |
| `"%-#8x"` | `255` | `[0xff    ]` | 8 |
| `"%#.5x"` | `255` | `[0x000ff]` | 7 |
| `"% #08X"` | `255` | `[0X0000FF]` | 8 |
| `"%+x"` | `255` | `[ff]` | 2 |
| `"%x"` | `UINT_MAX` | `[ffffffff]` | 8 |
| `"%.0x"` | `5` | `[5]` | 1 |

## Diretivas desconhecidas — forma canônica

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%r"` | — | `[%r]` | 2 |
| `"%-5r"` | — | `[%-5r]` | 4 |
| `"%05r"` | — | `[%05r]` | 4 |
| `"% r"` | — | `[% r]` | 3 |
| `"%5.2r"` | — | `[%5.2r]` | 5 |
| `"%-05r"` | — | `[%-5r]` | 4 |
| `"%0-5r"` | — | `[%-5r]` | 4 |
| `"%+ r"` | — | `[%+r]` | 3 |
| `"%##7r"` | — | `[%#7r]` | 4 |
| `"%.r"` | — | `[%.0r]` | 4 |
| `"%00r"` | — | `[%0r]` | 3 |
| `"%0#+ -8.3k"` | — | `[%#+-8.3k]` | 8 |
| `"%++--00##  9.12w"` | — | `[%#+-9.12w]` | 9 |
| `"a%rb%d"` | `42` (nao consumido) | `[a%rb42]` | 6 |

Regras da reconstrução em
[../05-bonus/semantica.md](../05-bonus/semantica.md). A última linha comprova
que desconhecida não consome argumento.

## Diretivas incompletas

| Formato | Argumento | Saída | Retorno |
|---|---|---|---|
| `"%"` | — | `[]` | -1 |
| `"%5"` | — | `[]` | -1 |
| `"%0"` | — | `[]` | -1 |
| `"%."` | — | `[]` | -1 |
| `"%-"` | — | `[]` | -1 |
| `"% "` | — | `[]` | -1 |

Nada da diretiva parcial é impresso e o retorno é −1; literais anteriores
ficam: `"abc%"` → `[abc]`, retorno −1
([../01-contrato/api.md](../01-contrato/api.md)).
