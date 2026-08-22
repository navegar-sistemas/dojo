# O que é uma linha

Uma **linha** é a menor sequência de bytes do fluxo que termina em `\n`
(0x0A), **incluindo** o próprio `\n` — ou, se o fluxo acaba sem `\n`, tudo o
que resta dele.

Consequências, todas observáveis:

- O `\n` **faz parte** da linha devolvida: `"abc\n"`, não `"abc"`.
- A única linha devolvida sem `\n` final é a última de um fluxo que não
  termina em `\n`.
- Uma linha vazia do arquivo (`\n\n`) vira o retorno `"\n"` — 1 byte, nunca
  string vazia.
- `\r` não é tratado: `"linha um\r\n"` é devolvida inteira, com os dois bytes
  finais. Só `\n` termina linha.
- Um arquivo de tamanho zero não tem linha nenhuma: primeira chamada já
  devolve `NULL`.

## A sequência de retornos de um fd

Para um fluxo com conteúdo `L₁ L₂ … Lₖ` (partição do conteúdo em linhas como
definido acima), a sequência de retornos é exatamente

```
L₁, L₂, …, Lₖ, NULL, NULL, NULL, …
```

e ela é **a mesma para qualquer `BUFFER_SIZE ≥ 1`**. Três invariantes que a
suíte de aceitação verifica mecanicamente sobre cada retorno
([../06-aceitacao/validacao.md](../06-aceitacao/validacao.md)):

1. nenhum retorno é a string vazia;
2. nenhum retorno contém `\n` fora da última posição;
3. a concatenação de todos os retornos reproduz o fluxo **byte a byte**.

Os invariantes 1–3 juntos equivalem à definição: qualquer erro de fatiamento
(perder um byte, duplicar um pedaço de buffer, quebrar linha no lugar errado)
viola pelo menos um deles.

## Tabelas canônicas

Medidas na implementação de referência — e idênticas com B = 1, 42 e
10 000 000. `printf` é o gerador; aspas delimitam o retorno.

`printf 'a\n\nbb\n'`:

| chamada | retorno |
|---|---|
| 1 | `"a\n"` |
| 2 | `"\n"` |
| 3 | `"bb\n"` |
| 4 | `NULL` |
| 5 | `NULL` |

`printf 'abc'` (sem quebra final):

| chamada | retorno |
|---|---|
| 1 | `"abc"` |
| 2 | `NULL` |

`printf '\n'`:

| chamada | retorno |
|---|---|
| 1 | `"\n"` |
| 2 | `NULL` |

`printf ''` (arquivo vazio) e `/dev/null`:

| chamada | retorno |
|---|---|
| 1 | `NULL` |

Mais casos, incluindo bordas de buffer, em
[../06-aceitacao/casos.md](../06-aceitacao/casos.md).
