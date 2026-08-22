# Especificação — get_next_line

## Mapa

### Contrato observável

| Documento | Conteúdo |
|---|---|
| [01-contrato/api.md](01-contrato/api.md) | protótipo, parâmetro de compilação `BUFFER_SIZE`, todos os retornos `NULL` |
| [01-contrato/linha.md](01-contrato/linha.md) | definição exata de "linha" e a sequência de retornos de um fd |

### Restrições

| Documento | Conteúdo |
|---|---|
| [02-restricoes/estilo.md](02-restricoes/estilo.md) | regras de estilo do código e o que cada uma impõe ao desenho |
| [02-restricoes/build.md](02-restricoes/build.md) | arquivos entregues, funções externas permitidas, compilação exata |

### Arquitetura

| Documento | Conteúdo |
|---|---|
| [03-arquitetura/modulos.md](03-arquitetura/modulos.md) | arquivo → funções → responsabilidade, com todas as assinaturas e contratos |
| [03-arquitetura/fluxo.md](03-arquitetura/fluxo.md) | as três fases de uma chamada e o ciclo de vida do stash |
| [03-arquitetura/decisoes.md](03-arquitetura/decisoes.md) | escolhas de desenho com a evidência que as sustenta |

### Algoritmo

| Documento | Conteúdo |
|---|---|
| [04-algoritmo/leitura.md](04-algoritmo/leitura.md) | pseudocódigo das três fases, detalhes que quebram se trocados, custos medidos |

### Bônus e verificação

| Documento | Conteúdo |
|---|---|
| [05-bonus/multi-fd.md](05-bonus/multi-fd.md) | variante com vários descritores simultâneos numa única variável estática |
| [06-aceitacao/casos.md](06-aceitacao/casos.md) | entradas com a sequência exata de retornos esperada |
| [06-aceitacao/validacao.md](06-aceitacao/validacao.md) | comandos de verificação, com harness completo embutido |

### Execução

| Documento | Conteúdo |
|---|---|
| [tasks/README.md](tasks/README.md) | quadro das 5 tarefas, ordem e dependências |

## Convenções deste documento

- Pseudocódigo usa `enquanto` e nunca `for`, porque `for` é proibido pelas
  [regras de estilo](02-restricoes/estilo.md).
- **B** abrevia o valor de `BUFFER_SIZE`; **stash** é a string estática que
  carrega o resto lido e ainda não devolvido (o termo é o nome da variável no
  código).
- Contagens (linhas de corpo, chamadas a `read`, tempos) são valores medidos
  numa implementação em C desta spec, não estimativas.
- Em exemplos de conteúdo de arquivo, `\n` é o byte 0x0A escrito por
  `printf '...\n'`.

## Layout

- Implementação: `../project/`. Os comandos desta spec rodam de dentro dela.
- A entrega são seis arquivos-fonte e um `README.md` — não existe Makefile nem
  binário próprio; quem compila a função é o programa hospedeiro
  (ver [02-restricoes/build.md](02-restricoes/build.md)).
