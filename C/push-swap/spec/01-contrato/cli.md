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
- Dois seletores **diferentes** na mesma linha é erro: a intenção é ambígua.
- Repetir o **mesmo** seletor (`--simple --simple`) é aceito, assim como repetir `--bench`:
  não há ambiguidade. A regra é: só é erro o que não dá para resolver.
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
./push_swap --simple --medium 3 2 1    # Error (dois seletores diferentes)
./push_swap --foo 3 2 1                # Error (flag desconhecida)
./push_swap --simple --simple 3 2 1    # ok, equivale a --simple
./push_swap --bench --bench 3 2 1      # ok, equivale a --bench
```

Relacionado: [entrada.md](entrada.md) para a validação dos números, [saida.md](saida.md) para
o que cada caso imprime.
