# Entrada numérica

## Gramática do token

```
token  := sinal? digito+
sinal  := '+' | '-'
digito := '0'..'9'
```

O token inteiro precisa casar com essa gramática — nada antes, nada depois, nenhum caractere
sobrando.

| Token | Válido | Motivo |
|---|---|---|
| `42` | sim | |
| `-42` | sim | |
| `+42` | sim | |
| `007` | sim | zeros à esquerda não são proibidos |
| `-0` | sim | vale 0 |
| `4a` | não | sobra caractere |
| `4.0` | não | ponto não é dígito |
| `+` | não | sinal sem dígito |
| `-` | não | idem |
| `` | não | vazio |
| ` 42` | não | espaço já foi consumido na divisão |
| `2147483648` | não | não cabe em `int` |
| `-2147483649` | não | idem |

## Divisão dos argumentos

Cada `argv` é dividido por espaços antes da validação, então cada argumento pode conter vários
números:

```bash
./push_swap "4 67 3"     # equivale a ./push_swap 4 67 3
./push_swap "4 67" 3     # idem
```

Um argumento que produza **zero** tokens após a divisão é erro. Isso cobre `""` e `"   "`,
no `push_swap` e no `checker` (`./checker "" 1` é erro).

A ordem final é a ordem de leitura da esquerda para a direita, achatando as divisões: o
primeiro token do primeiro argumento é o topo da pilha `a`.

## Limites e unicidade

- Cada valor precisa caber em `int`: `-2147483648` a `2147483647`.
- A conversão é feita em `long` e o resultado comparado com os limites de `int` antes de ser
  truncado. `ft_atoi` da libft **não serve**: ela não sinaliza estouro, e `2147483648` passaria
  como um valor arbitrário.
- Valores repetidos são erro. A comparação é entre os valores originais, antes de qualquer
  conversão em ranks.

## Ordem da validação

1. Separação entre flags e números ([cli.md](cli.md)).
2. Divisão de cada argumento numérico em tokens.
3. Validação sintática de cada token.
4. Conversão com verificação de faixa.
5. Detecção de duplicatas sobre o conjunto completo.

Qualquer falha interrompe nos passos seguintes e produz a mesma saída — não existe erro
parcial, nem mensagem diferenciada por causa. Todos os passos acontecem antes de qualquer
movimento ser emitido, então nunca sai meia receita seguida de `Error`.

## Entrada vazia

Zero números — seja porque não houve argumento nenhum, seja porque só havia flags — não é
erro: o programa encerra com sucesso sem imprimir nada. `./push_swap --bench` também não
imprime bloco de métricas nesse caso.

Relacionado: [saida.md](saida.md).
