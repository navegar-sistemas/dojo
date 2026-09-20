# Diretivas e conversões

A base das duas variantes: o que uma diretiva é na parte obrigatória, e o que
cada conversão imprime quando não há flag, largura nem precisão. O bônus
acrescenta gramática ([../05-bonus/formato.md](../05-bonus/formato.md)) sem
mudar nada do que está aqui.

## Gramática da parte obrigatória

Uma diretiva são exatamente dois bytes: `%` seguido do caractere de
conversão.

```
diretiva  := '%' conversao
conversao := 'c' | 's' | 'p' | 'd' | 'i' | 'u' | 'x' | 'X' | '%'
```

O que não casa segue uma de duas regras:

| Caso | Comportamento | Exemplo |
|---|---|---|
| `%` seguido de byte que não é conversão | imprime `%` e o byte, literais; **não consome argumento** | `"%r"` → `[%r]`, retorno 2 |
| `%` como último byte do formato | para de processar e devolve `-1`; o que veio antes fica escrito | `"abc%"` → `[abc]`, retorno −1 |

`a%rb%d` com argumento `42` comprova o "não consome": a saída é `[a%rb42]` —
o `42` sobrevive para o `%d`.

## Consumo de argumentos

| Diretiva | Consome |
|---|---|
| `%c` | `int` (promoção de `char`) |
| `%s` | `char *` |
| `%p` | `void *` |
| `%d`, `%i` | `int` |
| `%u`, `%x`, `%X` | `unsigned int` |
| `%%`, desconhecida, incompleta | nada |

## As nove conversões

### `%c` — um byte

Escreve o byte de valor `(char)arg`. O byte zero é escrito de verdade: `%c`
com `'\0'` produz 1 byte `0x00` e retorno 1 — a saída não é uma string C e
nada é truncado.

### `%s` — string

Escreve os bytes até o `'\0'`, excluído. `NULL` imprime `(null)`, 6 bytes.
String vazia escreve nada, retorno 0.

### `%p` — ponteiro

`NULL` imprime `(nil)`, 5 bytes. Qualquer outro valor imprime `0x` seguido do
endereço em hexadecimal minúsculo, sem zeros à esquerda:

| Argumento | Saída | Retorno |
|---|---|---|
| `(void *)0x1234` | `[0x1234]` | 6 |
| `(void *)0xffffffffffffffff` | `[0xffffffffffffffff]` | 18 |

O valor passa por `unsigned long`, que tem o tamanho do ponteiro nas
plataformas-alvo (LP64).

### `%d` e `%i` — inteiro com sinal

Idênticos entre si — a diferença que existe em `scanf` não existe aqui. Base
10, `-` na frente dos negativos.

| Argumento | Saída |
|---|---|
| `0` | `[0]` |
| `-42` | `[-42]` |
| `INT_MIN` | `[-2147483648]` |
| `INT_MAX` | `[2147483647]` |

`INT_MIN` não tem simétrico em `int`; a negação acontece em `long`
([../04-emissao/numeros.md](../04-emissao/numeros.md)).

### `%u` — inteiro sem sinal

Base 10. `UINT_MAX` → `[4294967295]`.

### `%x` e `%X` — hexadecimal

Base 16, minúsculo e maiúsculo. `0` → `[0]`; `UINT_MAX` → `[ffffffff]` e
`[FFFFFFFF]`. Sem prefixo `0x` — isso é a flag `#`, do bônus.

### `%%` — porcentagem literal

Escreve `%`, retorno 1, não consome argumento. `"%%%%"` → `[%%]`, retorno 2.

## Encadeamento

O retorno soma tudo, literais e conversões:

```
ft_printf("%c|%s|%p|%d|%i|%u|%x|%X|%%", 'q', "str", (void *)0x42,
	-5, 6, 7u, 8u, 9u)
→ [q|str|0x42|-5|6|7|8|9|%]    retorno 23
```

## A fronteira com o bônus

Flags (`-0# +`), largura e precisão pertencem à gramática estendida do bônus.
Na parte obrigatória esses bytes caem na regra da conversão desconhecida:

```
ft_printf("%5d", 42)    →  [%5d]     (obrigatória)
printf("%5d", 42)       →  [   42]   (referência)
```

Essa é a **única** região onde a parte obrigatória diverge da referência, e é
deliberado: o contrato obrigatório cobre diretivas de dois bytes, e o espelho
fica total quando a variante bônus é construída.

**A divergência não é só visual.** Como `%5` é tratado como desconhecida e não
consome argumento, toda diretiva posterior lê o argumento **anterior** ao que
deveria. Com `%s` no caminho, isso é ponteiro inválido:

```
ft_printf("[%-8.3d|%s]", 42, "ok")     (obrigatória)
→ o %s recebe o int 42 como endereço → SEGV em 0x2a
```

Formato com flag, largura ou precisão é entrada fora do contrato da variante
obrigatória — quem precisa deles constrói com `make bonus`.

Os lotes de aceitação da parte obrigatória
([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)) não contêm
flags por isso — inclusive `"% "`, que parece inofensivo mas começa com a
flag espaço e, na referência, é diretiva incompleta com retorno −1.
