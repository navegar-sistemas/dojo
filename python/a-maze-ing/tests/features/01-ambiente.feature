# language: pt
Funcionalidade: Ambiente de desenvolvimento
  Python 3.10 ou posterior, ambiente virtual, .gitignore e suíte de testes,
  preparados antes da primeira linha de código do labirinto.

  # pdf: "Your project must be written in Python 3.10 or later."
  # md:  "Seu projeto deve ser escrito em Python 3.10 ou posterior."
  @obrigatorio @automatizado @pdf-p06-L04 @md-L99
  Cenário: O interpretador do projeto é Python 3.10 ou posterior
    Dado o repositório no estado "instalado"
    Quando eu executo "python -c 'import sys; print(sys.version_info >= (3, 10))'"
    Então a saída padrão é "True"

  # pdf: "Your project must be written in Python 3.10 or later."
  # md:  "Seu projeto deve ser escrito em Python 3.10 ou posterior."
  @obrigatorio @derivado @automatizado @pdf-p06-L04 @md-L99
  Cenário: O código não usa recurso de linguagem posterior ao Python 3.10
    Dado o repositório no estado "instalado"
    Quando eu executo "mypy . --python-version 3.10"
    Então a saída contém "Success: no issues found"

  # pdf: "It is recommended to use virtual environments (e.g., venv or conda) for dependency"
  # pdf: "isolation during development."
  # md:  "Recomenda-se usar ambientes virtuais (ex.: `venv` ou `conda`) para isolamento de dependências durante o desenvolvimento."
  @recomendado @automatizado @decisao-I14 @pdf-p07-L10-L11 @md-L132
  Cenário: As dependências ficam isoladas num ambiente virtual
    Dado o repositório no estado "clone limpo"
    Quando eu executo "make install"
    Então o código de saída é 0
    E o caminho ".venv" existe
    E o comando ".venv/bin/python -m flake8 --version" termina com código 0
    E o comando ".venv/bin/python -m mypy --version" termina com código 0
    E o comando ".venv/bin/python -m build --version" termina com código 0
    E o comando ".venv/bin/python -m pytest --version" termina com código 1
    E a saída de ".venv/bin/python -c 'import sys; print(sys.prefix != sys.base_prefix)'" é "True"
    E a saída de ".venv/bin/python -c 'import sys, flake8, mypy, build; print(all(m.__file__.startswith(sys.prefix) for m in (flake8, mypy, build)))'" é "True"

  # pdf: "Include a .gitignore file to exclude Python artifacts."
  # md:  "Inclua um arquivo `.gitignore` para excluir artefatos do Python."
  @obrigatorio @automatizado @decisao-I14 @pdf-p07-L09 @md-L131
  Esquema do Cenário: O .gitignore exclui artefatos do Python
    Dado o repositório no estado "clone limpo"
    E o arquivo ".gitignore" na raiz do repositório
    Quando eu executo "git check-ignore <caminho>"
    Então o caminho "<caminho>" é ignorado pelo git

    Exemplos:
      | caminho                              |
      | __pycache__/modulo.cpython-310.pyc   |
      | pacote/__pycache__/x.cpython-314.pyc |
      | .mypy_cache/                         |
      | .venv/                               |
      | build/                               |
      | dist/                                |
      | mazegen.egg-info/                    |
      | maze.txt                             |

  # pdf: "Include a .gitignore file to exclude Python artifacts."
  # pdf: "This package must be called mazegen-* and the file must be located at the root of your"
  # pdf: "A default configuration file must be available in your Git repository."
  # md:  "Inclua um arquivo `.gitignore` para excluir artefatos do Python."
  # md:  "Este pacote deve se chamar `mazegen-*` e o arquivo deve estar localizado na raiz do seu repositório Git."
  # md:  "Um arquivo de configuração padrão deve estar disponível no seu repositório Git."
  @obrigatorio @derivado @automatizado @pdf-p07-L09 @pdf-p15-L13-L14 @pdf-p09-L03 @md-L131 @md-L294 @md-L176
  Esquema do Cenário: O .gitignore não esconde arquivos que precisam ser entregues
    Dado o repositório no estado "clone limpo"
    E o arquivo ".gitignore" na raiz do repositório
    Quando eu executo "git check-ignore <arquivo>"
    Então o caminho "<arquivo>" não é ignorado pelo git

    Exemplos:
      | arquivo                        |
      | a_maze_ing.py                  |
      | config.txt                     |
      | Makefile                       |
      | README.md                      |
      | LICENSE.md                     |
      | pyproject.toml                 |
      | mazegen-1.0.0-py3-none-any.whl |
      | mazegen-1.0.0.tar.gz           |

  # pdf: "Create test programs to verify project functionality (not submitted or graded). Use"
  # pdf: "frameworks like pytest or unittest for unit tests, covering edge cases."
  # md:  "Crie programas de teste para verificar a funcionalidade do projeto (não são submetidos nem avaliados). Use frameworks como `pytest` ou `unittest` para testes unitários, cobrindo casos de borda."
  @obrigatorio @manual @decisao-I15 @pdf-p07-L07-L08 @md-L130
  Cenário: Existe uma suíte de testes automatizados que passa
    Dada a suíte em "a-maze-ing/tests/", com o virtualenv dela instalado
    Quando eu executo ".venv/bin/pytest -m "not manual"" nessa pasta
    Então todos os testes automatizados passam
    E nenhum warning é emitido durante a suíte

  # pdf: "frameworks like pytest or unittest for unit tests, covering edge cases."
  # md:  "Use frameworks como `pytest` ou `unittest` para testes unitários, cobrindo casos de borda."
  @obrigatorio @automatizado @decisao-I15 @pdf-p07-L08 @md-L130
  Cenário: A suíte usa pytest ou unittest
    Dado o código-fonte de "../tests"
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "testes usam pytest ou unittest"

  # pdf: "frameworks like pytest or unittest for unit tests, covering edge cases."
  # md:  "Use frameworks como `pytest` ou `unittest` para testes unitários, cobrindo casos de borda."
  @obrigatorio @manual @pdf-p07-L08 @md-L130
  Cenário: A suíte cobre casos de borda
    Dada cada função pública do projeto
    Quando eu procuro os testes dela
    Então existe teste para o caminho feliz
    E existe teste para cada entrada inválida que ela trata
    E existe teste para os limites dos valores aceitos

  # pdf: "Create test programs to verify project functionality (not submitted or graded). Use"
  # md:  "Crie programas de teste para verificar a funcionalidade do projeto (não são submetidos nem avaliados)."
  @informativo @manual @pdf-p07-L07 @md-L130
  Cenário: O resultado do pytest não é avaliado
    Dada a entrega do projeto
    Quando a avaliação acontece
    Então a nota não depende do resultado do pytest
    E a suíte fica em "a-maze-ing/tests/", fora do repositório de entrega, que não tem pasta "tests/" (D20)
    Mas a suíte passa no flake8 e no mypy rodados na própria pasta (D20)
    E a suíte roda verde antes de cada entrega

  # pdf: "If any additional project-specific requirements apply, they will be stated immediately below"
  # pdf: "this section."
  # md:  "Se houver requisitos adicionais específicos do projeto, eles serão declarados imediatamente abaixo desta seção."
  @informativo @manual @pdf-p07-L12-L13 @md-L134
  Cenário: Os requisitos específicos do projeto começam no Capítulo IV
    Dado o fim das Instruções Comuns
    Quando eu procuro requisitos adicionais logo abaixo da seção III.3
    Então os requisitos específicos do projeto são os dos Capítulos IV a IX
