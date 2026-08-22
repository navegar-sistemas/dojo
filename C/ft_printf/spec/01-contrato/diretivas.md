# Diretivas — parte obrigatória

## Gramática

Na parte obrigatória, uma diretiva são exatamente dois bytes: `%` seguido do
caractere de conversão.

```
diretiva := '%' conversao
conversao := 'c' | 's' | 'p' | 'd' | 'i' | 'u' | 'x' | 'X' | '%'
```

O que não casa com a gramática segue uma de duas regras, ambas medidas na
referência:

| Caso | Comportamento | Medido |
|---|---|---|
| `%` seguido de byte que não é conversão | imprime `%` e o byte, literais; **não consome argumento** | `"%r"` → `[%r]`, retorno 2 |
| `%` como último byte do formato | para de processar e devolve `-1`; o que veio antes fica escrito | `"abc%"` → `[abc]`, retorno −1 |

O caso `a%rb%d` com argumento `42` comprova o "não consome": a saída é
`[a%rb42]` — o `42` sobrevive para o `%d`.

## A fronteira com o bônus

Flags (`-0# +`), largura e precisão pertencem à gramática estendida do bônus
([../05-bonus/formato.md](../05-bonus/formato.md)). Na parte obrigatória esses
bytes caem na regra da conversão desconhecida:

```
ft_printf("%5d", 42)    →  [%5d]     (obrigatória)
printf("%5d", 42)       →  [   42]   (referência)
```

Essa é a **única** região onde a parte obrigatória diverge da referência, e é
deliberado: o contrato obrigatório cobre diretivas de dois bytes; o espelho
fica total quando a variante bônus é construída. Os lotes de aceitação da
parte obrigatória ([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md))
não contêm flags por isso — inclusive `"% "`, que parece inofensivo mas começa
com a flag espaço, e na referência é diretiva incompleta (retorno −1).

## Consumo de argumentos

| Diretiva | Consome |
|---|---|
| `%c` | `int` (promoção de `char`) |
| `%s` | `char *` |
| `%p` | `void *` |
| `%d`, `%i` | `int` |
| `%u`, `%x`, `%X` | `unsigned int` |
| `%%`, desconhecida, incompleta | nada |

Semântica de cada conversão em [conversoes.md](conversoes.md).
