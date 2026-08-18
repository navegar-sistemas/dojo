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

Cada `up` cria um container **novo** (`docker compose run --rm`) — não anexa a
um já em execução. Para abrir um shell adicional no container que já está
rodando (ex.: compilar enquanto o Claude trabalha):

```bash
docker exec -it "$(docker ps -q -f name=dojo-sandbox | head -1)" bash -l
```

## Atualizando as dependências

`npm`, `@anthropic-ai/claude-code`, o toolchain C e a `norminette` vêm da
**imagem**, presos em `@latest` no momento do build. O cache de camadas do
Docker faz `up`/`build` reaproveitarem a versão antiga; para puxar as novas:

```bash
npx sandbox-vibe@latest build --no-cache   # reconstrói as imagens do zero
npx sandbox-vibe up                        # entra no container já atualizado
```

Conferir o que ficou na imagem:

```bash
docker run --rm --entrypoint sh sandbox-vibe:dojo -c 'claude --version'
```

Atualizar de dentro do container não adianta: o `claude` fica em
`/usr/local/lib` (imagem), e cada `up` cria um container novo com `--rm`.

### As sessões do Claude sobrevivem ao rebuild

Histórico, `~/.claude/projects`, credenciais e plugins moram no volume
`sandbox-vibe_dojo-sandbox-home`, montado em `/home/sandbox` — separado da
imagem. Reconstruir a imagem não o toca.

O único comando que apaga esses dados é `npx sandbox-vibe reset --all`. Para
reinstalar plugins/MCPs preservando as sessões, use
`npx sandbox-vibe reset --marker` (ou `npx sandbox-vibe bump-marker`).

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
