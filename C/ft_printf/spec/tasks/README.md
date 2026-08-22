# Tarefas

## Quadro

| # | Tarefa | Depende de | Entrega |
|---|---|---|---|
| [T01](T01-esqueleto-build.md) | Esqueleto de build | — | `Makefile`, `ft_printf.h`, `pf_put.c` (só `pf_putchar`) |
| [T02](T02-escritores.md) | Escritores da obrigatória | T01 | `pf_put.c` completo |
| [T03](T03-nucleo.md) | Laço e despacho | T02 | `ft_printf.c` |
| [T04](T04-aceitacao-obrigatoria.md) | Aceitação da obrigatória | T03 | validação completa da parte obrigatória |
| [T05](T05-gramatica-bonus.md) | Gramática do bônus | T01 | `ft_printf_bonus.h`, `parse_bonus.c`, `put_bonus.c`, regra `bonus` |
| [T06](T06-montagem.md) | Montagem numérica | T05 | `num_render_bonus.c` |
| [T07](T07-conversoes-bonus.md) | Conversões e laço do bônus | T04, T06 | `conv_*_bonus.c`, `ft_printf_bonus.c` |
| [T08](T08-fechamento.md) | Fechamento | T07 | validação final integral |

## Ordem

T01 → T02 → T03 → T04 fecham a parte obrigatória, cada uma verificável no fim.
T05 e T06 só dependem do esqueleto e poderiam andar em paralelo com a
obrigatória, mas T07 — que liga tudo — exige T04 verde: bônus só interessa com
a parte obrigatória inteira verificada, e o lote diferencial do bônus reusa a
disciplina montada em T04.

O primeiro ponto verificável de ponta a ponta contra a referência é **T03**:
antes disso não existe `ft_printf` para comparar, e as tarefas se verificam
por mains temporários de unidade.

## Formato de uma tarefa

- **Objetivo** — uma frase.
- **Depende de** — tarefas que precisam estar prontas.
- **Arquivos** — o que é criado ou alterado.
- **Especificação** — links para os documentos que definem o comportamento.
- **Implementação** — o que fazer, na granularidade de função.
- **Pronto quando** — comandos com a saída esperada. Todos verdes, sem exceção.

## Header incremental

Os dois headers nascem mínimos e crescem com as tarefas: quem cria uma função
pública é quem acrescenta o protótipo, guiado por
[../03-arquitetura/modulos.md](../03-arquitetura/modulos.md). O mesmo vale
para o Makefile: `SRCS`/`BSRCS` listam só arquivos que existem — nenhuma
tarefa declara código que ainda não foi escrito.

## Mains temporários

Toda verificação de unidade usa um `main` descartável compilado **fora** da
implementação (`/tmp/ftpf-check/`), linkando a biblioteca ou os `.c` direto.
Nada disso entra em `SRCS`, no repositório ou no `.a`. O gabarito executável
das tarefas diferenciais é a `printf` do sistema, via harness de
[../06-aceitacao/validacao.md](../06-aceitacao/validacao.md).

## Regra de conclusão

Uma tarefa só está pronta com **todos** os comandos de "Pronto quando"
executados e verdes, no estado atual do código. Em toda tarefa que toca `.c`
ou `.h`, isso inclui:

```bash
make re                                  # zero warning
```

e a auditoria mecânica de estilo de
[../02-restricoes/estilo.md](../02-restricoes/estilo.md). Tarefa anterior
vermelha bloqueia a seguinte.
