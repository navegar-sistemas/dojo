# As nove conversões (sem flags)

Comportamento da parte obrigatória — e do bônus quando a diretiva não traz
flag, largura nem precisão. Cada linha "medido" é gabarito byte a byte.

## `%c` — um byte

Consome `int`, escreve o byte de valor `(char)arg`. O byte zero é escrito de
verdade: `"%c"` com `'\0'` produz 1 byte `0x00` e retorno 1 — a saída não é
uma string C e nada é truncado.

## `%s` — string

Consome `char *`, escreve os bytes até o `'\0'` (excluído). `NULL` imprime
`(null)` — medido, 6 bytes, retorno 6. String vazia escreve nada, retorno 0.

## `%p` — ponteiro

Consome `void *`. `NULL` imprime `(nil)` — medido, 5 bytes. Qualquer outro
valor imprime `0x` seguido do endereço em hexadecimal minúsculo, sem zeros à
esquerda:

```
%p com (void *)0x1234               →  [0x1234]              retorno 6
%p com (void *)0xffffffffffffffff   →  [0xffffffffffffffff]  retorno 18
```

O valor passa por `unsigned long`, que tem o tamanho do ponteiro nas
plataformas-alvo (LP64).

## `%d` e `%i` — inteiro com sinal

Idênticos entre si (a diferença de `scanf` não existe aqui). Base 10, `-` na
frente de negativos.

```
%d com 0           →  [0]
%d com -42         →  [-42]
%d com INT_MIN     →  [-2147483648]
%d com INT_MAX     →  [2147483647]
```

`INT_MIN` não tem simétrico em `int`; a negação acontece em `long`
([../04-emissao/numeros.md](../04-emissao/numeros.md)).

## `%u` — inteiro sem sinal

Base 10. `UINT_MAX` → `[4294967295]`.

## `%x` e `%X` — hexadecimal

Base 16, minúsculo e maiúsculo. `0` → `[0]`; `UINT_MAX` → `[ffffffff]` /
`[FFFFFFFF]`. Sem prefixo `0x` (isso é a flag `#`, do bônus).

## `%%` — porcentagem literal

Escreve `%`, retorno 1, não consome argumento. `"%%%%"` → `[%%]`, retorno 2.

## Encadeamento

O retorno soma tudo — literais e conversões:

```
ft_printf("%c|%s|%p|%d|%i|%u|%x|%X|%%", 'q', "str", (void *)0x42,
	-5, 6, 7u, 8u, 9u)
→ [q|str|0x42|-5|6|7|8|9|%]    retorno 23
```
