# language: pt
Funcionalidade: Qualidade de código
  flake8, type hints verificados pelo mypy, docstrings PEP 257, tratamento de exceções
  e gerenciamento de recursos valem para todo arquivo .py do repositório.

  # pdf: "Your project must adhere to the flake8 coding standard."
  # md:  "Seu projeto deve aderir ao padrão de código flake8."
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L05 @md-L100
  Cenário: Todo o código segue o padrão flake8
    Dado o repositório no estado "instalado"
    Quando eu executo ".venv/bin/flake8 ."
    Então o código de saída é 0
    E a saída é ""
    E nenhum arquivo .py do projeto contém "# noqa"

  # pdf: "Your functions should handle exceptions gracefully to avoid crashes. Use try-except"
  # pdf: "It must never crash unexpectedly, and must"
  # md:  "Suas funções devem tratar exceções de forma elegante para evitar crashes."
  # md:  "Ele nunca deve travar inesperadamente"
  @obrigatorio @automatizado @decisao-D04 @decisao-D05 @decisao-I21 @pdf-p06-L06 @pdf-p08-L15 @md-L101 @md-L155
  Esquema do Cenário: Entradas hostis não derrubam o programa
    Dado o caminho "cfg.txt" preparado como "<conteudo>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então a saída não contém "Traceback"
    E o processo termina dentro do tempo limite
    E o resultado da execução é "<resultado>"

    Exemplos:
      | conteudo                                | resultado                                                                                        |
      | bytes binários aleatórios               | erro citando cfg.txt; motivo: arquivo não é UTF-8                                                |
      | config base com WIDTH de 100000 dígitos | erro citando WIDTH                                                                               |
      | só WÍDTH=20 e HEÍGHT=15, com acento     | erro citando WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT; motivo: chave obrigatória ausente |
      | só espaços e tabulações                 | erro citando WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT; motivo: chave obrigatória ausente |
      | BOM UTF-8 + config base                 | sucesso                                                                                          |

  # pdf: "Use try-except"
  # pdf: "blocks to manage potential errors."
  # md:  "Use blocos `try-except` para gerenciar erros potenciais."
  @obrigatorio @manual @pdf-p06-L06-L07 @md-L101
  Cenário: Operações que podem falhar ficam em blocos try-except
    Dado o código do projeto
    Quando eu localizo leitura de arquivo, conversão de número e escrita do arquivo de saída
    Então cada uma está dentro de um bloco try-except
    E cada except termina numa mensagem ao usuário ou relança a exceção
    E nenhum except está vazio ou engole o erro em silêncio
    Mas o "except" de KeyboardInterrupt e EOFError em "main" só imprime uma linha vazia e encerra com código 0 (D17)

  # pdf: "Prefer context managers for resources like files or"
  # pdf: "connections to ensure automatic cleanup."
  # md:  "Prefira context managers para recursos como arquivos ou conexões, garantindo limpeza automática."
  @recomendado @automatizado @pdf-p06-L07-L08 @md-L101
  Cenário: Arquivos são abertos dentro de with
    Dado o código-fonte de "."
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "open sempre dentro de with"

  # pdf: "If your program crashes due to unhandled"
  # pdf: "exceptions during the review, it will be considered non-functional."
  # md:  "Se seu programa travar por exceções não tratadas durante a revisão, será considerado não funcional."
  @obrigatorio @automatizado @decisao-D01 @pdf-p06-L08-L09 @md-L101
  Esquema do Cenário: Nenhum caminho de erro termina em exceção não tratada
    Dado o config base
    E a situação de erro "<situacao>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a saída não contém "Traceback"
    E o código de saída é 1

    Exemplos:
      | situacao                                         |
      | arquivo de configuração inexistente              |
      | arquivo de configuração sem permissão de leitura |
      | chave obrigatória ausente                        |
      | valor inválido                                   |
      | parâmetros impossíveis                           |
      | OUTPUT_FILE num diretório inexistente            |

  # pdf: "All resources (e.g., file handles, network connections) must be properly managed to"
  # pdf: "prevent leaks."
  # md:  "Todos os recursos (ex.: handles de arquivo, conexões de rede) devem ser gerenciados corretamente para evitar vazamentos."
  @obrigatorio @manual @pdf-p06-L10-L11 @md-L102
  Cenário: Nenhum recurso vaza durante a suíte
    Dada a suíte em "a-maze-ing/tests/", com o virtualenv dela instalado
    Quando eu executo ".venv/bin/python -X dev -W error::ResourceWarning -m pytest -m "not manual"" nessa pasta
    Então todos os testes automatizados passam
    E nenhum "ResourceWarning" é emitido

  # pdf: "All resources (e.g., file handles, network connections) must be properly managed to"
  # pdf: "prevent leaks."
  # md:  "Todos os recursos (ex.: handles de arquivo, conexões de rede) devem ser gerenciados corretamente para evitar vazamentos."
  @obrigatorio @automatizado @pdf-p06-L10-L11 @md-L102
  Cenário: Nenhum recurso vaza na execução do programa
    Dado o arquivo "config.txt" na raiz do repositório
    Quando eu executo "python3 -X dev a_maze_ing.py config.txt" com a entrada "4"
    Então a saída de erro não contém "ResourceWarning"
    E a renderização confirma "cada linha termina com o reset ANSI"

  # pdf: "Use context managers where possible for automatic handling."
  # md:  "Use context managers sempre que possível para tratamento automático."
  @obrigatorio @manual @pdf-p06-L11 @md-L102
  Cenário: Todo recurso que tem context manager é usado com with
    Dado o código do projeto
    Quando eu localizo os arquivos abertos
    Então cada arquivo é aberto e fechado por um "with"
    E a liberação acontece também quando uma exceção interrompe o bloco

  # pdf: "Your code must include type hints for function parameters, return types, and vari-"
  # md:  "Seu código deve incluir type hints para parâmetros de função, tipos de retorno e variáveis onde aplicável"
  @obrigatorio @automatizado @pdf-p06-L12 @md-L103
  Cenário: Todo parâmetro de função tem type hint
    Dado o repositório no estado "instalado"
    Quando eu executo "mypy . --disallow-untyped-defs"
    Então a saída não contém "Function is missing a type annotation"

  # pdf: "Your code must include type hints for function parameters, return types, and vari-"
  # md:  "Seu código deve incluir type hints para parâmetros de função, tipos de retorno e variáveis onde aplicável"
  @obrigatorio @automatizado @pdf-p06-L12 @md-L103
  Cenário: Toda função tem type hint de retorno
    Dado o código-fonte de "."
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "anotação de retorno em toda definição"

  # pdf: "ables where applicable (using the typing module)."
  # md:  "variáveis onde aplicável (usando o módulo `typing`)."
  @obrigatorio @automatizado @pdf-p06-L12-L13 @md-L103
  Cenário: Variáveis cujo tipo não é inferível têm type hint
    Dado o repositório no estado "instalado"
    E o código-fonte de "."
    Quando eu executo "make lint"
    E a análise estática percorre o código-fonte
    Então a saída não contém "Need type annotation"
    E a análise estática confirma "coleções vazias com tipo anotado"

  # pdf: "Use mypy for static type check-"
  # pdf: "ing."
  # md:  "Use mypy para verificação estática de tipos."
  @obrigatorio @automatizado @pdf-p06-L13-L14 @md-L103
  Cenário: O mypy faz parte do fluxo do projeto
    Dado o repositório no estado "instalado"
    Quando eu executo "make -n lint"
    Então a saída contém "mypy ."
    E o comando ".venv/bin/mypy --version" termina com código 0

  # pdf: "All functions must pass mypy without errors."
  # md:  "Todas as funções devem passar no mypy sem erros."
  @obrigatorio @automatizado @decisao-I14 @pdf-p06-L14 @md-L103
  Cenário: Todas as funções passam no mypy sem erros
    Dado o repositório no estado "instalado"
    Quando eu executo "mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
    Então a saída contém "Success: no issues found"
    E nenhum arquivo .py do projeto contém "# type: ignore"

  # pdf: "Include docstrings in functions and classes following PEP 257"
  # md:  "Inclua docstrings em funções e classes seguindo a PEP 257"
  @obrigatorio @automatizado @decisao-I16 @pdf-p06-L15 @md-L104
  Esquema do Cenário: Cada <definicao> tem docstring
    Dado o código-fonte de "a_maze_ing.py" e "mazegen/"
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "docstring em cada <definicao>"

    Exemplos:
      | definicao |
      | função    |
      | método    |
      | classe    |

  # pdf: "Include docstrings in functions and classes following PEP 257 (e.g., Google or"
  # md:  "Inclua docstrings em funções e classes seguindo a PEP 257 (ex.: estilo Google ou NumPy)"
  @obrigatorio @automatizado @decisao-I16 @pdf-p06-L15 @md-L104
  Cenário: As docstrings seguem a PEP 257
    Dado o código-fonte de "a_maze_ing.py" e "mazegen/"
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "docstrings com aspas triplas duplas"
    E a análise estática confirma "resumo de uma frase terminado em ponto"
    E a análise estática confirma "linha em branco entre resumo e descrição"

  # pdf: "NumPy style) to document purpose, parameters, and returns."
  # md:  "(ex.: estilo Google ou NumPy) para documentar propósito, parâmetros e retornos."
  @obrigatorio @automatizado @decisao-I16 @pdf-p06-L15-L16 @md-L104
  Cenário: As docstrings documentam propósito, parâmetros e retorno
    Dado o código-fonte de "a_maze_ing.py" e "mazegen/"
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "seção Args: nas funções com parâmetros"
    E a análise estática confirma "seção Returns: nas funções que retornam valor"

  # pdf: "Your project must adhere to the flake8 coding standard."
  # pdf: "All functions must pass mypy without errors."
  # md:  "Seu projeto deve aderir ao padrão de código flake8."
  # md:  "Todas as funções devem passar no mypy sem erros."
  # regua: "Also the flake8 Norm must pass on the python files, as well as mypy."
  # regua-md: "Além disso, a norma `flake8` deve passar nos arquivos Python, assim como o `mypy`."
  @recomendado @derivado @decisao-D20 @manual @decisao-I16 @pdf-p06-L05 @pdf-p06-L14 @md-L100 @md-L103 @regua-p1
  Cenário: Os arquivos de teste também passam no flake8 e no mypy
    Dada a suíte em "a-maze-ing/tests/", com o virtualenv dela instalado
    Quando eu rodo o flake8 e o mypy nessa pasta
    Então os dois passam sem nenhum erro ou warning
    Mas as funções de teste dispensam docstring (I16)
