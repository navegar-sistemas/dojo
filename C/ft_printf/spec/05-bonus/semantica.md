# Semântica flag × conversão

Tudo aqui é comportamento **medido** na referência
([../03-arquitetura/decisoes.md](../03-arquitetura/decisoes.md)); as linhas
`[…]` citadas estão, com retorno, em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).

## Visão geral

| | `-` | `0` | `#` | `+` / espaço | largura | precisão |
|---|---|---|---|---|---|---|
| `%c` | alinha à esquerda | **ignorada** (espaços) | ign. | ign. | espaços | **ignorada** |
| `%s` | idem | **ignorada** (espaços) | ign. | ign. | espaços | trunca |
| `%%` | ign. | ign. | ign. | ign. | **ignorada** | ign. |
| `%d` `%i` | esquerda | zeros | ign. | prefixo de sinal | sim | mínimo de dígitos |
| `%u` | esquerda | zeros | ign. | **ignorados** | sim | mínimo de dígitos |
| `%x` `%X` | esquerda | zeros | `0x`/`0X` se valor ≠ 0 | **ignorados** | sim | mínimo de dígitos |
| `%p` ≠ NULL | esquerda | zeros | ign. (`0x` já é inerente) | **prefixo de sinal** | sim | mínimo de dígitos |
| `%p` = NULL | esquerda | **ignorada** (espaços) | ign. | ign. | espaços | **ignorada** |

## Regras transversais (numéricas)

- **`-` vence `0`**: `%-05d` com 42 → `[42   ]`.
- **`+` vence espaço**: `% +d` ≡ `%+ d` ≡ `%+d` → `[+42]`.
- **Precisão desliga `0`**: `%05.3d` com 42 → `[  042]` — os 3 zeros são da
  precisão, o resto é espaço. Vale para `%p`: `%08.3p` → `[  0x1234]`.
- **Precisão 0 com valor 0 imprime vazio**, e o prefixo de sinal sobrevive:
  `%.0d` com 0 → `[]`; `%+.0d` com 0 → `[+]`; `% .0d` → `[ ]`;
  `%5.0d` → `[     ]`.
- O prefixo **nunca** conta como dígito: `%.5d` com −42 → `[-00042]`
  (5 dígitos + sinal, retorno 6).

## `%c` e `%s`

Campo de texto: só `-` e largura, padding **sempre** com espaço — `%05c` com
`'a'` → `[    a]`, `%05s` com `"hi"` → `[   hi]`. Precisão trunca `%s`
(`%5.3s` com `"hello"` → `[  hel]`, `%.0s` → `[]`) e é ignorada em `%c`.

**`%s` com `NULL`** — a regra medida tem um degrau:

| Precisão | Saída |
|---|---|
| ausente, ou ≥ 6 | `(null)` |
| 0 a 5 | vazio (retorno 0) |

`(null)` nunca é truncado pela metade: ou inteiro, ou nada. Com largura,
alinha como string comum (`%8s` → `[  (null)]`).

## `%d` `%i` `%u` `%x` `%X`

O prefixo por conversão (montagem em [montagem.md](montagem.md)):

| Conversão | Prefixo |
|---|---|
| `%d` `%i` negativo | `-` |
| `%d` `%i` ≥ 0 | `+` se `plus`; senão espaço se `space`; senão nada |
| `%u` | nunca |
| `%x` / `%X` | `0x` / `0X` se `hash` **e valor ≠ 0** |

`%#x` com 0 → `[0]`, sem prefixo; `%#.0x` com 0 → `[]` — as duas regras se
compõem. `+`/espaço em `%u`/`%x`/`%X` são ignorados (`%+u` → `[42]`,
`% x` → `[ff]`).

## `%p`

**Não nulo:** hexadecimal minúsculo com `0x` inerente — e, diferente de
`%x`, os prefixos de sinal **funcionam**: `%+p` → `[+0x1234]`,
`% p` → `[ 0x1234]`. O prefixo composto vai inteiro antes dos zeros:
`% 015p` → `[ 0x000000001234]`, `%.20p` → `[0x00000000000000001234]`.
`#` não muda nada.

**`NULL`:** vira o texto `(nil)` no caminho de string — largura e `-`
funcionam, `0` alinha com espaços (`%08p` → `[   (nil)]`), precisão e sinais
são ignorados (`%.3p` → `[(nil)]`, inteiro). Implementação: `conv_ptr` zera a
precisão (`prec = -1`) e delega a `conv_s`
([../03-arquitetura/tipos.md](../03-arquitetura/tipos.md)).

## `%%`

`%` seco, sempre: flags, largura e precisão são todos ignorados — `%5%`,
`%05%`, `%-5%`, `%.3%` → `[%]`, retorno 1.

## Diretiva desconhecida — reimpressão canônica

Conversão fora de `cspdiuxX%` não consome argumento e reimprime a diretiva
**reconstruída do estado analisado**, nunca o texto original:

```
'%'
'#'  se hash
'+'  se plus            (senão ' ' se space)
'-'  se minus
'0'  se zero e não minus
largura em decimal      se ≠ 0
'.' + precisão          se presente (0 imprime ".0")
byte de conversão
```

| Formato | Saída | O que mostra |
|---|---|---|
| `%0-5r` | `[%-5r]` | `0` suprimida por `-`; ordem canônica |
| `%+ r` | `[%+r]` | espaço suprimido por `+` |
| `%##7r` | `[%#7r]` | deduplicação |
| `%.r` | `[%.0r]` | precisão vazia vira `.0` |
| `%++--00##  9.12w` | `[%#+-9.12w]` | tudo junto |

`a%rb%d` com 42 → `[a%rb42]`: o argumento sobrevive para o `%d` — desconhecida
não toca a lista variádica.
