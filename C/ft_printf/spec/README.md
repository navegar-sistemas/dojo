# Especificação — ft_printf

`libftprintf.a` expõe uma única função, `ft_printf`, que reproduz a `printf`
da glibc **byte a byte** — saída e valor de retorno — em todo o domínio que o
projeto suporta. Esta spec descreve o contrato observável, as restrições, a
arquitetura e a ordem de construção; uma implementação que a siga inteira
termina indistinguível da referência dentro do domínio.

## Mapa

### Contrato observável

| Documento | Conteúdo |
|---|---|
| [01-contrato/api.md](01-contrato/api.md) | assinatura, entrega, valor de retorno, canal, domínio suportado |
| [01-contrato/diretivas.md](01-contrato/diretivas.md) | gramática da parte obrigatória e fronteiras com o bônus |
| [01-contrato/conversoes.md](01-contrato/conversoes.md) | as nove conversões sem flags, com bytes exatos |

### Restrições

| Documento | Conteúdo |
|---|---|
| [02-restricoes/estilo.md](02-restricoes/estilo.md) | regras de estilo do projeto e o que cada uma impõe ao desenho |
| [02-restricoes/build.md](02-restricoes/build.md) | dependências externas, estrutura de arquivos, Makefile completo |

### Arquitetura

| Documento | Conteúdo |
|---|---|
| [03-arquitetura/tipos.md](03-arquitetura/tipos.md) | `t_fmt` e seus invariantes |
| [03-arquitetura/modulos.md](03-arquitetura/modulos.md) | arquivo → funções → responsabilidade, com todas as assinaturas |
| [03-arquitetura/fluxo.md](03-arquitetura/fluxo.md) | o laço, o avanço do formato, o `va_list` por ponteiro, o erro |
| [03-arquitetura/decisoes.md](03-arquitetura/decisoes.md) | escolhas de desenho com a evidência que as sustenta |

### Emissão

| Documento | Conteúdo |
|---|---|
| [04-emissao/escritores.md](04-emissao/escritores.md) | contratos dos escritores de baixo nível das duas partes |
| [04-emissao/numeros.md](04-emissao/numeros.md) | dígitos por recursão (obrigatória) e por buffer (bônus) |

### Bônus e verificação

| Documento | Conteúdo |
|---|---|
| [05-bonus/formato.md](05-bonus/formato.md) | gramática completa da diretiva: flags, largura, precisão |
| [05-bonus/semantica.md](05-bonus/semantica.md) | matriz flag × conversão medida na referência, casos especiais |
| [05-bonus/montagem.md](05-bonus/montagem.md) | `put_num`: prefixo, zeros, espaços e a ordem de emissão |
| [06-aceitacao/casos.md](06-aceitacao/casos.md) | entradas com saída e retorno exatos, medidos na referência |
| [06-aceitacao/validacao.md](06-aceitacao/validacao.md) | build, harness diferencial, fuzz, sanitizers, valgrind |

### Execução

| Documento | Conteúdo |
|---|---|
| [tasks/README.md](tasks/README.md) | quadro das 8 tarefas, ordem e dependências |

## Convenções deste documento

- Pseudocódigo usa `while` e nunca `for`, porque `for` é proibido pelas regras
  de estilo ([02-restricoes/estilo.md](02-restricoes/estilo.md)).
- Saídas aparecem entre colchetes: `[  +42]`. Os colchetes delimitam os bytes
  e não fazem parte da saída; espaços dentro deles são bytes reais.
- "Diretiva" é a sequência iniciada por `%` dentro do formato; "conversão" é o
  caractere que a encerra.
- Todo comportamento que a linguagem C deixa em aberto foi **medido** na
  `printf` da glibc 2.36 e fixado como gabarito — as tabelas de
  [06-aceitacao/casos.md](06-aceitacao/casos.md) são valores observados, não
  estimativas. Onde esta spec diz "medido", é disso que se trata.
- Contagens de linhas e de funções citadas são as da implementação de
  referência desta spec, que compila com `-Wall -Wextra -Werror`.

## Layout

- Implementação: `../project/`. Os comandos desta spec rodam de dentro dela.
- Gabarito executável: a `printf` do próprio sistema (glibc). O harness de
  [06-aceitacao/validacao.md](06-aceitacao/validacao.md) compila cada lote de
  casos duas vezes — uma chamando `printf`, outra chamando `ft_printf` — e
  exige `stdout` e retornos idênticos byte a byte.
