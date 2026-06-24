# dojo

Coletivo de *coding katas*: prática deliberada de fundamentos, um módulo por
linguagem — cada um com ambiente reproduzível, testes e lint automatizados,
tratado como código de produção.

Primeiro módulo: **`C/libft`** — funções essenciais da biblioteca padrão C.

## Ambiente

O repositório roda dentro de um container com o toolchain completo
(`gcc`, `make`, `libbsd`, `norminette`, `gdb`, `valgrind`), definido em
`.sandbox-vibe/`. Os caminhos são **relativos**, então funciona em qualquer
máquina com Docker — basta clonar.

### Opção A — VSCode Dev Container
1. Abra a pasta no VSCode com a extensão *Dev Containers*.
2. **Reopen in Container**. O repositório é montado em `/workspace`.

### Opção B — CLI sandbox-vibe
```bash
npx sandbox-vibe up           # sobe o container e entra no Claude
npx sandbox-vibe up --shell   # ou apenas um shell
```

## Clonando (com submódulos)

O tester de terceiros `libft-god` é um submódulo git:

```bash
git clone --recursive git@github-navegarsistemas:navegar-sistemas/dojo.git
# se já clonou sem --recursive:
git submodule update --init --recursive
```

## Projeto libft

Compilar a biblioteca (só precisa de `cc` + `ar` — funciona até fora do container):

```bash
cd C/libft/repo
make            # gera libft.a
make re         # recompila do zero
make clean      # remove os .o
make fclean     # remove .o e libft.a
```

### Testes

Os testes ficam em `C/libft/mains` e precisam do container (usam `-lbsd` como
referência de `strnstr` e a `norminette`):

```bash
cd C/libft/mains
make strlen     # compila + roda o teste de ft_strlen, com norminette + asan/ubsan
make r-strlen   # versão rápida (sem norminette nem sanitizer)
make san-strlen # apenas asan/ubsan (caça bug de memória/UB)
make all        # roda todos os testes
make fclean     # limpa os binários de teste e a lib
```

> **Compile sempre dentro do container.** Os artefatos (`.o`/`.a`) são
> específicos da arquitetura. Se você compilou no host (ex.: macOS) e depois
> entrou no container (Linux), rode `make fclean` antes — objetos de outra
> arquitetura causam `undefined reference` no link, pois o working tree é
> compartilhado com o container.
