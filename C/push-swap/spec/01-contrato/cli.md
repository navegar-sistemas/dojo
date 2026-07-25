# Linha de comando

```
./push_swap [--simple|--medium|--complex|--adaptive] [--bench] <inteiros...>
```

## Flags

| Flag | Efeito |
|---|---|
| `--simple` | força a estratégia O(n²) |
| `--medium` | força a estratégia O(n√n) |
| `--complex` | força a estratégia O(n log n) |
| `--adaptive` | força o despacho por desordem |
| `--bench` | acrescenta o bloco de métricas em stderr |

## Regras de combinação

- Flags aparecem em qualquer posição: antes dos números, depois, ou intercaladas.
  `./push_swap 3 --bench 2 1` é válido e equivale a `./push_swap --bench 3 2 1`.
- Sem nenhum seletor de estratégia, vale `--adaptive`.
- `--bench` combina com qualquer seletor, e também sozinho.
- Repetir o **mesmo** seletor (`--simple --simple`) é erro, pelo mesmo caminho que dois
  seletores diferentes: o campo de estratégia só pode ser gravado uma vez.
- Dois seletores diferentes na mesma linha é erro.
- Repetir `--bench` é erro, pela mesma regra.
- Qualquer token que comece com `--` e não esteja na tabela é erro, inclusive `--` sozinho.

Um token que começa com `-` seguido de dígito (`-42`) é um número negativo, não uma flag. A
distinção é o prefixo de **dois** hifens.

## Precedência sobre a validação numérica

A separação entre flags e números acontece antes de qualquer conversão. Um token que começa
com `--` nunca é tentado como número: `./push_swap --5 1 2` é erro de flag desconhecida, não
de token numérico inválido. Nos dois casos a saída é a mesma (`Error`), então a distinção só
importa para quem lê o código.

## Exemplos

```bash
./push_swap 3 2 1                      # adaptive (padrão)
./push_swap --complex 3 2 1            # radix
./push_swap --bench 3 2 1              # adaptive + métricas em stderr
./push_swap --bench --medium 3 2 1     # chunk sort + métricas
./push_swap 3 --medium 2 --bench 1     # idem, flags intercaladas
./push_swap --simple --medium 3 2 1    # Error (dois seletores)
./push_swap --foo 3 2 1                # Error (flag desconhecida)
```

Relacionado: [entrada.md](entrada.md) para a validação dos números, [saida.md](saida.md) para
o que cada caso imprime.
