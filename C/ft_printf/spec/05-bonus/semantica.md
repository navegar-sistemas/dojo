# Semântica flag × conversão

O que sai, para cada combinação. Como cada função produz isso está em
[conversoes.md](conversoes.md) e [montagem.md](montagem.md); as linhas com
retorno estão em [../06-aceitacao/casos.md](../06-aceitacao/casos.md).

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

## Regras transversais dos numéricos

| Regra | Exemplo |
|---|---|
| `-` vence `0` | `%-05d` com 42 → `[42   ]` |
| `+` vence espaço | `% +d` ≡ `%+ d` ≡ `%+d` → `[+42]` |
| precisão desliga `0` | `%05.3d` com 42 → `[  042]`; `%08.3p` → `[  0x1234]` |
| precisão 0 com valor 0 não imprime dígito | `%.0d` com 0 → `[]` |
| o prefixo de sinal sobrevive ao valor vazio | `%+.0d` → `[+]`; `% .0d` → `[ ]`; `%5.0d` → `[     ]` |
| o prefixo nunca conta como dígito | `%.5d` com −42 → `[-00042]`, retorno 6 |

## `%c` e `%s`

Campo de texto: só `-` e largura têm efeito, e o preenchimento é **sempre**
espaço — `%05c` com `'a'` → `[    a]`, `%05s` com `"hi"` → `[   hi]`. A
precisão trunca `%s` (`%5.3s` com `"hello"` → `[  hel]`, `%.0s` → `[]`) e é
ignorada em `%c`.

**`%s` com `NULL`** tem um degrau:

| Precisão | Saída |
|---|---|
| ausente, ou ≥ 6 | `(null)` |
| 0 a 5 | vazio, retorno 0 |

`(null)` nunca é truncado pela metade: ou inteiro, ou nada. Com largura,
alinha como string comum (`%8s` → `[  (null)]`).

## `%d` `%i` `%u` `%x` `%X`

O prefixo por conversão:

| Conversão | Prefixo |
|---|---|
| `%d` `%i` negativo | `-` |
| `%d` `%i` ≥ 0 | `+` se `plus`; senão espaço se `space`; senão nada |
| `%u` | nunca |
| `%x` / `%X` | `0x` / `0X` se `hash` **e** valor ≠ 0 |

`%#x` com 0 → `[0]`, sem prefixo; `%#.0x` com 0 → `[]` — as duas regras se
compõem. `+` e espaço em `%u`, `%x` e `%X` não têm efeito (`%+u` → `[42]`,
`% x` → `[ff]`).

## `%p`

**Não nulo:** hexadecimal minúsculo com `0x` inerente e, diferente de `%x`,
os prefixos de sinal funcionam: `%+p` → `[+0x1234]`, `% p` → `[ 0x1234]`. O
prefixo composto vai inteiro antes dos zeros: `% 015p` →
`[ 0x000000001234]`, `%.20p` → `[0x00000000000000001234]`. `#` não muda
nada.

**`NULL`:** vira o texto `(nil)` e segue o caminho de string — largura e `-`
funcionam, `0` alinha com espaços (`%08p` → `[   (nil)]`), precisão e sinais
são ignorados (`%.3p` → `[(nil)]`, inteiro).

## `%%`

`%` seco, sempre: flags, largura e precisão são todos ignorados. `%5%`,
`%05%`, `%-5%`, `%.3%` → `[%]`, retorno 1.

## Diretiva desconhecida

Conversão fora de `cspdiuxX%` não consome argumento e reimprime a diretiva
**reconstruída da struct**, nunca o texto original. A forma é fixa:

```
'%'  flags em ordem canônica  largura  '.' precisão  byte de conversão
```

| Parte | Regra |
|---|---|
| flags | `#`, depois `+` (ou espaço, se não houver `+`), depois `-`, depois `0` (se não houver `-`) |
| largura | em decimal, omitida quando 0 |
| precisão | `.` seguido do valor, inclusive `.0`; omitida quando ausente |

| Formato | Saída | O que mostra |
|---|---|---|
| `%0-5r` | `[%-5r]` | `0` suprimida por `-`; ordem canônica |
| `%+ r` | `[%+r]` | espaço suprimido por `+` |
| `%##7r` | `[%#7r]` | deduplicação |
| `%.r` | `[%.0r]` | precisão vazia vira `.0` |
| `%++--00##  9.12w` | `[%#+-9.12w]` | tudo junto |

`a%rb%d` com 42 → `[a%rb42]`: o argumento sobrevive para o `%d`, porque a
desconhecida não toca a lista variádica.
