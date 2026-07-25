# Especificação — push_swap

## Mapa

### Contrato observável

| Documento | Conteúdo |
|---|---|
| [01-contrato/cli.md](01-contrato/cli.md) | sintaxe da linha de comando, flags, combinações válidas |
| [01-contrato/entrada.md](01-contrato/entrada.md) | gramática dos tokens, limites, duplicatas, ordem da validação |
| [01-contrato/saida.md](01-contrato/saida.md) | canais, formatos, códigos de saída, casos que não imprimem nada |
| [01-contrato/bench.md](01-contrato/bench.md) | formato exato do `--bench`, alinhamento, invariantes |

### Restrições

| Documento | Conteúdo |
|---|---|
| [02-restricoes/norma.md](02-restricoes/norma.md) | regras da norminette e o que cada uma impõe ao desenho |
| [02-restricoes/build.md](02-restricoes/build.md) | funções externas permitidas, libft, Makefile completo |

### Arquitetura

| Documento | Conteúdo |
|---|---|
| [03-arquitetura/tipos.md](03-arquitetura/tipos.md) | `t_stack`, `t_op`, `t_ctx`, `t_conf` e seus invariantes |
| [03-arquitetura/modulos.md](03-arquitetura/modulos.md) | arquivo → funções → responsabilidade, com todas as assinaturas |
| [03-arquitetura/fluxo.md](03-arquitetura/fluxo.md) | sequência do `main` e as ordens que não podem ser trocadas |
| [03-arquitetura/decisoes.md](03-arquitetura/decisoes.md) | escolhas de desenho com a evidência que as sustenta |

### Algoritmos

| Documento | Conteúdo |
|---|---|
| [04-algoritmos/desordem.md](04-algoritmos/desordem.md) | métrica de desordem, valores de referência, distribuição medida |
| [04-algoritmos/ranks.md](04-algoritmos/ranks.md) | conversão valor → posição, pré-requisito de duas estratégias |
| [04-algoritmos/tiny.md](04-algoritmos/tiny.md) | caso base n ≤ 3, comum às quatro estratégias |
| [04-algoritmos/simple.md](04-algoritmos/simple.md) | O(n²), extração de mínimo |
| [04-algoritmos/medium.md](04-algoritmos/medium.md) | O(n√n), ordenação por blocos |
| [04-algoritmos/complex.md](04-algoritmos/complex.md) | O(n log n), radix binário |
| [04-algoritmos/adaptive.md](04-algoritmos/adaptive.md) | despacho por desordem |

### Bônus e verificação

| Documento | Conteúdo |
|---|---|
| [05-bonus/checker.md](05-bonus/checker.md) | o `checker` próprio, espelhando o binário de referência |
| [06-aceitacao/casos.md](06-aceitacao/casos.md) | entradas com saída exata esperada |
| [06-aceitacao/desempenho.md](06-aceitacao/desempenho.md) | contagens medidas por estratégia e tamanho |
| [06-aceitacao/validacao.md](06-aceitacao/validacao.md) | comandos de verificação |

### Execução

| Documento | Conteúdo |
|---|---|
| [tasks/README.md](tasks/README.md) | quadro das 14 tarefas, ordem, dependências e estado |

## Convenções deste documento

- Pseudocódigo usa `while` e nunca `for`, porque `for` é proibido pela norma. O que está
  escrito no pseudocódigo é traduzível linha a linha.
- Em qualquer notação `a = [1 2 3]`, o índice 0 é o **topo** da pilha.
- Contagens de operações são valores medidos numa implementação em C desta spec, não
  estimativas de complexidade.
- "Movimento" e "operação" são a mesma coisa: uma das 11 siglas impressas em stdout.

## Estado do repositório

`project/` contém um `main.c` vazio. Nenhum módulo desta spec existe ainda. O ponto de partida
é [tasks/T01-esqueleto-build.md](tasks/T01-esqueleto-build.md).
