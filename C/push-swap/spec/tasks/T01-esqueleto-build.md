# T01 — Esqueleto de build

## Objetivo

`make` compila um binário vazio, linkando a libft, sem relinkar na segunda chamada.

## Depende de

Nada.

## Arquivos

- `Makefile`
- `push_swap.h`
- `libft/` (cópia da libft com o Makefile dela)
- `main.c` com um `main` que retorna 0

## Especificação

- [../02-restricoes/build.md](../02-restricoes/build.md) — Makefile completo e propriedades
- [../02-restricoes/norma.md](../02-restricoes/norma.md) — header 42 obrigatório em todo arquivo
- [../03-arquitetura/tipos.md](../03-arquitetura/tipos.md) — conteúdo do header

## Implementação

1. Copiar a libft para `libft/`, com o Makefile dela. Confirmar que `make -C libft` gera
   `libft/libft.a`.
2. Escrever `push_swap.h` com: header 42, guarda de inclusão, os `# define STRAT_*`, as quatro
   `struct`/`enum` de [tipos.md](../03-arquitetura/tipos.md), e os protótipos de
   [modulos.md](../03-arquitetura/modulos.md). Protótipos de funções ainda não escritas podem
   ficar declarados — o header é o contrato.
3. Copiar o Makefile de [build.md](../02-restricoes/build.md).
4. Criar os `.c` da lista `SRCS` contendo apenas o header 42 e, quando necessário para o link,
   uma definição vazia. `main.c` recebe um `main` que retorna 0.

Alternativa ao passo 4: reduzir `SRCS` a `main.c` e ir acrescentando os arquivos conforme as
tarefas seguintes os criam. Menos arquivos vazios, mas exige editar o Makefile a cada tarefa.

## Pronto quando

```bash
make                        # compila sem warning
make                        # "Nothing to be done for 'all'."
make bonus && make bonus    # a segunda: "Nothing to be done for 'bonus'."
make                        # ainda "Nothing to be done" depois do bonus
make fclean                 # remove push_swap, checker, todos os .o e libft/libft.a
make re                     # reconstrói do zero, zero warning
norminette *.c *.h          # nenhuma linha "Error:"
ls libft/libft.a            # existe após make
```

A regra `bonus` só passa nesta tarefa se os três `*_bonus.c` existirem, ainda que vazios com
`main` em `checker_bonus.c`. Se optar por adiá-los, adie também a verificação de `make bonus`
para T13.
