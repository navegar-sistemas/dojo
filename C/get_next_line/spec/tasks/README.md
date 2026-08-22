# Tarefas

## Quadro

| # | Tarefa | Depende de | Entrega |
|---|---|---|---|
| [T01](T01-esqueleto.md) | Esqueleto do header | — | `get_next_line.h` |
| [T02](T02-utils.md) | Utilitários de string | T01 | `get_next_line_utils.c`, protótipos no header |
| [T03](T03-nucleo.md) | As três fases e a função pública | T02 | `get_next_line.c` |
| [T04](T04-bonus.md) | Bônus multi-fd | T03 | `get_next_line_bonus.{c,h}`, `get_next_line_utils_bonus.c` |
| [T05](T05-fechamento.md) | Fechamento | T04 | `README.md` do projeto, validação completa |

## Ordem

Estritamente linear: cada tarefa depende da anterior. T02 antes de T03 de
propósito: os utilitários têm contratos próprios testáveis isoladamente
(tolerância a `NULL`, junção que consome o argumento), e o núcleo nasce em
cima deles sem reescrever nada. O primeiro ponto verificável de ponta a ponta
é **T03** — antes disso não existe `get_next_line` para chamar.

T04 é uma cópia disciplinada, não desenvolvimento novo: os corpos não mudam,
só o estado muda de forma. Bônus só interessa com T03 inteira verde.

## Formato de uma tarefa

Cada arquivo tem:

- **Objetivo** — uma frase.
- **Depende de** — tarefas que precisam estar prontas.
- **Arquivos** — o que é criado ou alterado.
- **Especificação** — links para os documentos que definem o comportamento.
- **Implementação** — o que fazer, na granularidade de função.
- **Pronto quando** — comandos com a saída esperada. Todos verdes, sem exceção.

## Header incremental

`get_next_line.h` nasce em T01 com a guarda, os `#include` e o protótipo
público; T02 acrescenta os protótipos dos cinco utilitários. A tarefa que cria
uma função é a que a declara no header — nenhuma tarefa transcreve declaração
de código que ainda não existe.

## Regra de conclusão

Os comandos das tarefas rodam do mesmo diretório `check/` da
[validação](../06-aceitacao/validacao.md), criado em T01 ao lado de
`project/`.

Uma tarefa só está pronta com **todos** os comandos de "Pronto quando"
executados e verdes, no estado atual do código. Isso inclui, em toda tarefa
que toca `.c` ou `.h`, compilar com as flags do contrato sem nenhum warning:

```bash
cc -Wall -Wextra -Werror -c ../project/*.c -I../project && rm -f *.o
```

e conferir os tetos de estilo ([../02-restricoes/estilo.md](../02-restricoes/estilo.md))
contra a tabela de contagens de
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md). Tarefa anterior
vermelha bloqueia a seguinte.
