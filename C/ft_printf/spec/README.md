# Especificação — ft_printf

`libftprintf.a` expõe uma única função, `ft_printf`, que reproduz a `printf`
da glibc **byte a byte** — saída e valor de retorno — em todo o domínio que o
projeto suporta.

A spec é completa no sentido forte: contrato, restrições, arquitetura e o
algoritmo de cada uma das 32 funções. Quem a seguir inteira chega a uma
implementação indistinguível da referência dentro do domínio.

## Por onde começar

| Objetivo | Caminho |
|---|---|
| Escrever o projeto do zero | [tasks/README.md](tasks/README.md) — oito tarefas em ordem, cada uma com critério de pronto |
| Entender o que a função promete | [01-contrato/api.md](01-contrato/api.md) → [01-contrato/diretivas.md](01-contrato/diretivas.md) |
| Achar o algoritmo de uma função | a tabela "Onde está cada função" em [03-arquitetura/modulos.md](03-arquitetura/modulos.md) |
| Conferir a saída de um formato | [06-aceitacao/casos.md](06-aceitacao/casos.md) |

## Mapa

### Contrato observável

| Documento | Conteúdo |
|---|---|
| [01-contrato/api.md](01-contrato/api.md) | assinatura, entrega, valor de retorno, canal, domínio suportado |
| [01-contrato/diretivas.md](01-contrato/diretivas.md) | gramática da parte obrigatória, as nove conversões, fronteira com o bônus |

### Restrições

| Documento | Conteúdo |
|---|---|
| [02-restricoes/estilo.md](02-restricoes/estilo.md) | regras de estilo e o que cada uma impõe ao desenho |
| [02-restricoes/build.md](02-restricoes/build.md) | dependências externas, estrutura de arquivos, Makefile completo |

### Arquitetura

| Documento | Conteúdo |
|---|---|
| [03-arquitetura/tipos.md](03-arquitetura/tipos.md) | `t_fmt`, invariantes e quem lê cada campo |
| [03-arquitetura/modulos.md](03-arquitetura/modulos.md) | arquivo → funções → responsabilidade, assinaturas, índice de algoritmos |
| [03-arquitetura/fluxo.md](03-arquitetura/fluxo.md) | os dois laços, o avanço do formato, o despacho, o `va_list` por ponteiro |
| [03-arquitetura/decisoes.md](03-arquitetura/decisoes.md) | escolhas de desenho com a razão de cada uma |

### Emissão

| Documento | Conteúdo |
|---|---|
| [04-emissao/escritores.md](04-emissao/escritores.md) | as funções que tocam o descritor 1, nas duas variantes |
| [04-emissao/numeros.md](04-emissao/numeros.md) | dígitos por recursão (obrigatória) e por buffer (bônus) |

### Bônus

| Documento | Conteúdo |
|---|---|
| [05-bonus/formato.md](05-bonus/formato.md) | gramática da diretiva e as três funções de análise |
| [05-bonus/semantica.md](05-bonus/semantica.md) | matriz flag × conversão: o que sai em cada combinação |
| [05-bonus/conversoes.md](05-bonus/conversoes.md) | as oito `conv_*`: prefixo, conteúdo, casos-limite |
| [05-bonus/montagem.md](05-bonus/montagem.md) | `put_num`: prefixo, zeros, espaços e a ordem de emissão |

### Verificação

| Documento | Conteúdo |
|---|---|
| [06-aceitacao/casos.md](06-aceitacao/casos.md) | entradas com saída e retorno exatos |
| [06-aceitacao/validacao.md](06-aceitacao/validacao.md) | build, harness diferencial, fuzz, sanitizers, valgrind |

### Execução

| Documento | Conteúdo |
|---|---|
| [tasks/README.md](tasks/README.md) | quadro das oito tarefas, ordem e dependências |

## Notação

**Pseudocódigo.** Todo algoritmo aparece em blocos como este, com os nomes
reais das funções e dos campos — traduzir para C é mecânico:

```
conv_c(f, c):
    se não f->minus e pf_pad(' ', f->width - 1) < 0:
        devolve -1
    devolve 1
```

| Elemento | Significado |
|---|---|
| `se` / `senão se` / `senão` | condicional |
| `enquanto` | laço; `for` é proibido pelas regras de estilo |
| `e` / `ou` / `não` | `&&` / `\|\|` / `!` |
| `devolve` | `return` |
| `f->campo` | campo da `t_fmt` |
| `x é char[24]` | declaração de buffer local |

**Saídas.** Aparecem entre colchetes: `[  +42]`. Os colchetes delimitam os
bytes e não fazem parte da saída; espaços dentro deles são bytes reais.

**Vocabulário.** "Diretiva" é a sequência iniciada por `%` dentro do formato;
"conversão" é o caractere que a encerra. "Obrigatória" e "bônus" são as duas
variantes da biblioteca.

## O gabarito

Todo valor de saída e de retorno citado nesta spec é o da `printf` da glibc
2.36 — inclusive nos cantos que a linguagem C deixa em aberto, que aqui
viram contrato ([03-arquitetura/decisoes.md](03-arquitetura/decisoes.md)).

O gabarito é executável: o harness de
[06-aceitacao/validacao.md](06-aceitacao/validacao.md) compila cada lote de
casos duas vezes — uma chamando `printf`, outra chamando `ft_printf` — e
exige `stdout` e retornos idênticos byte a byte.

## Layout

- Implementação: `../project/`. Os comandos desta spec rodam de dentro dela.
- Testes: fora da implementação, em `/tmp/ftpf-check/` — não são
  entregáveis.
- As contagens de linhas e de funções citadas são as do código em
  `../project/`, que compila com `-Wall -Wextra -Werror` sem nenhum aviso.
