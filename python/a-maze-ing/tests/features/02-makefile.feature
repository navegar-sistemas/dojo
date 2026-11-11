# language: pt
Funcionalidade: Makefile
  O Makefile automatiza instalação, execução, depuração, limpeza e lint.

  Contexto:
    Dado o arquivo "Makefile" na raiz do repositório

  # pdf: "Include a Makefile in your project to automate common tasks. It must contain the"
  # pdf: "following rules"
  # md:  "Inclua um `Makefile` no seu projeto para automatizar tarefas comuns. Ele deve conter as seguintes regras"
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L18-L19 @md-L106-L108
  Cenário: O Makefile existe na raiz do repositório
    Quando eu executo "test -f Makefile"
    Então o código de saída é 0
    E o caminho "Makefile" está versionado no git

  # pdf: "install: Install project dependencies using pip, uv, pipx, or any other package"
  # pdf: "manager of your choice."
  # md:  "install: Instala as dependências do projeto usando `pip`, `uv`, `pipx` ou qualquer outro gerenciador de pacotes de sua escolha."
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L21-L22 @md-L110
  Cenário: make install instala as dependências do projeto
    Dado o repositório no estado "clone limpo"
    Quando eu executo "make install"
    Então o código de saída é 0
    E o comando ".venv/bin/python -m flake8 --version" termina com código 0
    E o comando ".venv/bin/python -m mypy --version" termina com código 0
    E o comando ".venv/bin/python -m build --version" termina com código 0

  # pdf: "run: Execute the main script of your project (e.g., via Python interpreter)."
  # md:  "run: Executa o script principal do projeto (ex.: via interpretador Python)."
  @obrigatorio @automatizado @decisao-I14 @decisao-I03 @decisao-I20 @pdf-p06-L23 @md-L111
  Cenário: make run executa o script principal com o config padrão
    Dado o repositório no estado "instalado"
    E o caminho "maze.txt" preparado como "inexistente"
    Quando eu executo "make run" com a entrada "4"
    Então o código de saída é 0
    E a saída de "make -n run" contém "a_maze_ing.py config.txt"

  # pdf: "debug: Run the main script in debug mode using Python's built-in debugger (e.g.,"
  # pdf: "pdb)."
  # md:  "debug: Executa o script principal em modo de depuração usando o depurador embutido do Python (ex.: `pdb`)."
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L24-L25 @md-L112
  Cenário: make debug abre o script principal no pdb
    Dado o repositório no estado "instalado"
    Quando eu executo "make debug" com a entrada "q"
    Então a saída contém "(Pdb)"
    E a saída de "make -n debug" contém "-m pdb a_maze_ing.py config.txt"

  # pdf: "clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to"
  # pdf: "keep the project environment clean."
  # md:  "clean: Remove arquivos temporários ou caches (ex.: `__pycache__`, `.mypy_cache`) para manter o ambiente do projeto limpo."
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L26-L27 @md-L113
  Esquema do Cenário: make clean remove arquivos temporários e caches
    Dado o repositório no estado "clone limpo"
    E o caminho "<temporario>" preparado como "diretório"
    Quando eu executo "make clean"
    Então o caminho "<temporario>" não existe

    Exemplos:
      | temporario          |
      | __pycache__         |
      | mazegen/__pycache__ |
      | .mypy_cache         |
      | build               |
      | mazegen.egg-info    |

  # pdf: "clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to"
  # pdf: "This package must be called mazegen-* and the file must be located at the root of your"
  # md:  "clean: Remove arquivos temporários ou caches (ex.: `__pycache__`, `.mypy_cache`) para manter o ambiente do projeto limpo."
  # md:  "Este pacote deve se chamar `mazegen-*` e o arquivo deve estar localizado na raiz do seu repositório Git."
  @obrigatorio @derivado @automatizado @decisao-I14 @decisao-I13 @pdf-p06-L26-L27 @pdf-p15-L13-L14 @md-L113 @md-L294
  Esquema do Cenário: make clean preserva os arquivos de entrega
    Dado o repositório no estado "clone limpo"
    E o caminho "<entrega>" preparado como "vazio"
    Quando eu executo "make clean"
    Então o caminho "<entrega>" existe

    Exemplos:
      | entrega                        |
      | mazegen-1.0.0-py3-none-any.whl |
      | mazegen-1.0.0.tar.gz           |
      | config.txt                     |
      | a_maze_ing.py                  |
      | README.md                      |
      | LICENSE.md                     |

  # pdf: "lint: Execute the commands flake8 . and mypy . --warn-return-any"
  # md:  "lint: Executa os comandos:"
  # md:  "flake8 ."
  @obrigatorio @automatizado @decisao-I14 @pdf-p07-L02 @md-L114-L117
  Cenário: make lint executa flake8 em todo o projeto
    Quando eu executo "make -n lint"
    Então a saída contém "flake8 ."

  # pdf: "following rules (mandatory lint implies the specified flags"
  # pdf: "lint: Execute the commands flake8 . and mypy . --warn-return-any"
  # pdf: "--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs"
  # pdf: "--check-untyped-defs"
  # md:  "o `lint` obrigatório implica as flags especificadas"
  # md:  "mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L19 @pdf-p07-L02-L04 @md-L108 @md-L118
  Esquema do Cenário: make lint executa mypy com cada flag obrigatória
    Quando eu executo "make -n lint"
    Então a linha da saída que contém "mypy ." também contém "<flag>"

    Exemplos:
      | flag                     |
      | --warn-return-any        |
      | --warn-unused-ignores    |
      | --ignore-missing-imports |
      | --disallow-untyped-defs  |
      | --check-untyped-defs     |

  # pdf: "lint: Execute the commands flake8 . and mypy . --warn-return-any"
  # md:  "lint: Executa os comandos:"
  # md:  "flake8 ."
  # md:  "mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
  @obrigatorio @derivado @automatizado @decisao-I14 @pdf-p07-L02-L04 @md-L114-L119
  Cenário: make lint passa no repositório entregue
    Dado o repositório no estado "instalado"
    Quando eu executo "make lint"
    Então o código de saída é 0
    E a saída contém "Success: no issues found"
    E a saída de ".venv/bin/flake8 ." é ""

  # pdf: "lint-strict (optional): Execute the commands flake8 . and mypy . --strict"
  # md:  "lint-strict (opcional): Executa os comandos:"
  # md:  "flake8 ."
  # md:  "mypy . --strict"
  @opcional @automatizado @decisao-I14 @pdf-p07-L05 @md-L121-L126
  Cenário: make lint-strict executa flake8 e mypy --strict
    Quando eu executo "make -n lint-strict"
    Então a saída contém "flake8 ." e "mypy . --strict"

  # pdf: "it is strongly recommended to"
  # pdf: "try –strict for enhanced checking"
  # md:  "é fortemente recomendado experimentar `--strict` para uma verificação mais rigorosa"
  @recomendado @automatizado @decisao-I14 @pdf-p06-L19-L20 @md-L108
  Cenário: O código passa no mypy --strict
    Dado o repositório no estado "instalado"
    Quando eu executo "make lint-strict"
    Então o código de saída é 0
    E a saída contém "Success: no issues found"
