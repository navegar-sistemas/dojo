# Suíte de testes do A-Maze-ing

Executa os cenários de `features/` contra o projeto em `../project/`.

Requisitos: `python3` 3.10 ou posterior no `PATH`, `make` e `git`.

## Comandos

A partir desta pasta:

| Comando | O que faz |
|---|---|
| `make install` | cria `.venv` e instala `requirements.txt` |
| `make run` | roda os cenários automatizados e os testes da própria suíte |
| `make run ETAPA=03` | roda só os cenários de `features/03-*.feature` |
| `make debug` | o mesmo que `run`, dentro do `pdb` (aceita `ETAPA`) |
| `make lint` | `flake8 .` e `mypy .` com as flags do subject |
| `make lint-strict` | `flake8 .` e `mypy . --strict` |
| `make faltantes` | lista as frases dos `.feature` que ainda não têm função |
| `make manuais` | lista os cenários `@manual`, o roteiro de inspeção da defesa |
| `make clean` | apaga `__pycache__`, `.mypy_cache` e `.pytest_cache` |

`make test` é sinônimo de `make run`.

Um cenário só, pelo nome:

```sh
.venv/bin/python -m pytest cenarios/test_02_makefile.py -k "make_run"
```

## Estrutura

```text
tests/
├── Makefile, pyproject.toml, .flake8, requirements.txt
├── conftest.py     módulos de passos carregados, tags, conferência do python3, fixture estado
├── features/       NN-nome.feature; README.md, decisoes.md e vocabulario.md
├── cenarios/       test_NN_nome.py: liga cada .feature ao pytest
├── step_defs/      funções dos passos, um módulo por assunto
├── suporte/        código comum dos passos: tipos de parâmetro, config, estado do cenário
└── autoteste/      testes do suporte e dos passos
```

## Da frase ao código

- `features/NN-nome.feature` roda por `cenarios/test_NN_nome.py`.
- Toda frase tem uma função em `step_defs/`. Para achá-la, busque o texto fixo da frase:

  ```sh
  grep -rn 'termina com código' step_defs/
  grep -rn 'open sempre dentro de with' step_defs/
  ```

| Módulo | Frases |
|---|---|
| `step_defs/execucao.py` | `eu executo ...`, código de saída, conteúdo da saída, mensagem de erro |
| `step_defs/repositorio.py` | estado do repositório, arquivos e caminhos, config, situações de erro |
| `step_defs/analise_estatica.py` | `o código-fonte de ...` e `a análise estática confirma "..."` |
| `step_defs/renderizacao.py` | `a renderização confirma "..."` |

## Criar um passo

1. `make faltantes` mostra a frase sem função e um esqueleto.
2. Escreva a função no módulo do assunto em `step_defs/`:

   ```python
   @then('a análise estática confirma "sem MiniLibX"')
   def sem_minilibx(estado: Estado) -> None:
       """Nenhum módulo importa a MiniLibX.

       Args:
           estado: Estado do cenário, com as árvores da análise.
       """
   ```

3. Módulo novo em `step_defs/` entra na lista `pytest_plugins` de `conftest.py`.
4. Parâmetro `{nome:Tipo}` novo numa frase pede uma entrada em `cucumber.parameterTypes`, no
   `.vscode/settings.json` da raiz do repositório; `autoteste/test_editor.py` falha mostrando
   a entrada que falta.
5. O teste do passo fica em `autoteste/`.

## Onde os cenários rodam

- Os comandos rodam em `../project/`, com o `python3` do `PATH` e tempo limite de 30 s.
- O estado `clone limpo` roda numa cópia temporária do que está versionado em `project/`.
- O estado `instalado` roda `make install` em `project/` uma vez por rodada.
- Arquivo que um cenário cria, troca ou apaga em `project/` volta a ser o que era no fim do
  cenário.
- Cenários `@manual` e os adiados pela decisão I19 ficam fora de `make run`.
