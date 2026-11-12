# language: pt
Funcionalidade: Módulo reutilizável e pacote mazegen
  A geração fica numa classe única de um módulo independente, documentado e empacotado num
  único arquivo mazegen-* instalável por pip, na raiz do repositório.

  # pdf: "You must implement the maze generation as a unique class (e.g., 'MazeGenerator') inside"
  # md:  "Você deve implementar a geração do labirinto como uma classe única (ex.: `MazeGenerator`)"
  @obrigatorio @automatizado @decisao-D19 @decisao-I09 @decisao-I11 @pdf-p15-L03 @md-L282
  Cenário: O pacote instalado expõe uma única classe geradora
    Dado um virtualenv novo "pacote" em que rodou "pip install mazegen-1.0.0-py3-none-any.whl"
    E o caminho "fora-do-repositorio" preparado como "diretório"
    Quando o ambiente de execução é o virtualenv "pacote" na pasta "fora-do-repositorio"
    E eu executo "python -c 'from mazegen import MazeGenerator, MazeError'"
    Então o código de saída é 0
    E o módulo mazegen confirma "uma única classe pública de geração"

  # pdf: "a standalone module that can be imported in a future project."
  # md:  "dentro de um módulo independente que possa ser importado em um projeto futuro."
  @obrigatorio @automatizado @pdf-p15-L04 @md-L282
  Cenário: O módulo é importável num projeto futuro
    Dado um virtualenv novo "futuro" em que rodou "pip install mazegen-1.0.0-py3-none-any.whl"
    E o caminho "projeto-futuro" preparado como "diretório"
    Quando o ambiente de execução é o virtualenv "futuro" na pasta "projeto-futuro"
    E eu executo "python -c 'from mazegen import MazeGenerator'"
    Então todos os comandos terminam com código 0

  # pdf: "You must provide a short documentation describing how to:"
  # pdf: "Instantiate and use your generator, with at least a basic example."
  # md:  "Você deve fornecer uma documentação curta descrevendo como:"
  # md:  "Instanciar e usar seu gerador, com pelo menos um exemplo básico."
  @obrigatorio @manual @decisao-I11 @decisao-I22 @pdf-p15-L05-L06 @md-L284-L286
  Cenário: A documentação explica como instanciar e usar o gerador
    - Dada a docstring de "mazegen/__init__.py", que é a documentação do módulo
    - Quando eu a leio sem conhecer o projeto
    - Então eu sei criar uma instância do gerador e gerar um labirinto

  # pdf: "Instantiate and use your generator, with at least a basic example."
  # md:  "Instanciar e usar seu gerador, com pelo menos um exemplo básico."
  @obrigatorio @automatizado @decisao-I11 @decisao-I22 @pdf-p15-L06 @md-L286
  Cenário: O exemplo básico da documentação roda
    Dado o caminho "exemplo" preparado como "diretório"
    E o exemplo de uso da docstring de "mazegen" salvo em "exemplo/exemplo.py"
    E um virtualenv novo "exemplo" em que rodou "pip install mazegen-1.0.0-py3-none-any.whl"
    Quando o ambiente de execução é o virtualenv "exemplo" na pasta "exemplo"
    E eu executo "python exemplo.py"
    Então o código de saída é 0
    E a última linha da saída padrão casa com a expressão "^[NESW]+$"

  # pdf: "Pass custom parameters (e.g., size, seed)."
  # md:  "Passar parâmetros personalizados (ex.: tamanho, seed)."
  @obrigatorio @manual @decisao-I09 @decisao-I11 @decisao-I22 @pdf-p15-L07 @md-L287
  Cenário: A documentação explica os parâmetros personalizados
    - Dada a docstring de "mazegen/__init__.py", que é a documentação do módulo
    - Quando eu procuro como mudar tamanho e seed
    - Então cada parâmetro aceito tem nome, tipo, valor padrão e um exemplo

  # pdf: "Pass custom parameters (e.g., size, seed)."
  # md:  "Passar parâmetros personalizados (ex.: tamanho, seed)."
  @obrigatorio @automatizado @decisao-I09 @pdf-p15-L07 @md-L287
  Esquema do Cenário: A classe aceita tamanho e seed
    Dado o gerador "MazeGenerator(width=<largura>, height=<altura>, seed=<seed>)"
    Quando o gerador gera o labirinto
    Então a grade do labirinto tem <largura> colunas e <altura> linhas
    E o módulo mazegen confirma "mesmos parâmetros geram a mesma grade"

    Exemplos:
      | largura | altura | seed |
      | 10      | 8      | 1    |
      | 20      | 15     | 42   |
      | 33      | 21     | 7    |

  # pdf: "Access the generated structure, and access at least a solution."
  # md:  "Acessar a estrutura gerada e acessar pelo menos uma solução."
  @obrigatorio @manual @decisao-I09 @decisao-I11 @decisao-I22 @pdf-p15-L08 @md-L288
  Cenário: A documentação explica como acessar a estrutura e a solução
    - Dada a docstring de "mazegen/__init__.py", que é a documentação do módulo
    - Quando eu procuro como ler o labirinto gerado
    - Então ela mostra como obter as paredes de cada célula
    - E ela mostra como obter pelo menos uma solução

  # pdf: "Access the generated structure, and access at least a solution."
  # md:  "Acessar a estrutura gerada e acessar pelo menos uma solução."
  @obrigatorio @automatizado @decisao-I09 @pdf-p15-L08 @md-L288
  Cenário: A estrutura gerada é acessível pela API
    Dado um labirinto gerado pelo módulo mazegen com o config base
    Quando o validador da suíte lê o labirinto
    Então o módulo mazegen confirma "grid público com as paredes de cada célula"
    E o validador da suíte confirma "paredes coerentes"

  # pdf: "The maze generator module grants access to the maze structure, but it"
  # pdf: "is not necessarily the same format as the output file."
  # md:  "O módulo gerador de labirintos dá acesso à estrutura do labirinto, mas não necessariamente no mesmo formato do arquivo de saída."
  @opcional @manual @decisao-I09 @decisao-I22 @pdf-p15-L09-L10 @md-L290
  Cenário: A estrutura da API pode ter formato próprio
    - Dada a estrutura "grid" exposta pela API
    - Quando eu a comparo com o arquivo de saída
    - Então a documentação do módulo descreve os bits de "grid" (N=1, E=2, S=4, W=8)
    - E o programa grava cada célula de "grid" no arquivo com format(valor, "x")

  # pdf: "This entire reusable module (code and documentation) must be available in a single file"
  # pdf: "suitable for a later installation by pip."
  # md:  "Todo esse módulo reutilizável (código e documentação) deve estar disponível em um único arquivo adequado para instalação posterior via `pip`."
  @obrigatorio @automatizado @decisao-I13 @pdf-p15-L11-L12 @md-L292
  Cenário: Código e documentação cabem num único arquivo instalável por pip
    Dado o arquivo "mazegen-*" na raiz do repositório
    Quando eu leio "mazegen-*"
    Então o pacote "mazegen-*" confirma "contém o código do módulo"
    E o pacote "mazegen-*" confirma "contém a docstring de mazegen/__init__.py"
    E o pacote "mazegen-*" confirma "README como descrição longa"
    E o pacote "mazegen-*" confirma "instala e importa MazeGenerator num virtualenv novo"

  # pdf: "This package must be called mazegen-* and the file must be located at the root of your"
  # pdf: "git repository."
  # md:  "Este pacote deve se chamar `mazegen-*` e o arquivo deve estar localizado na raiz do seu repositório Git."
  @obrigatorio @automatizado @decisao-I13 @pdf-p15-L13-L14 @md-L294
  Cenário: O pacote se chama mazegen e o arquivo fica na raiz do repositório
    Dado o repositório no estado "clone limpo"
    Quando eu executo "git ls-files 'mazegen-*'"
    Então a saída padrão contém "mazegen-"
    E a saída padrão não contém "/"
    E o metadado "Name" do pacote "mazegen-*" é "mazegen"

  # pdf: "Both .tar.gz and .whl extensions are allowed, as generated by the standard build of a"
  # pdf: "Python package."
  # md:  "Tanto a extensão `.tar.gz` quanto `.whl` são permitidas, conforme geradas pelo build padrão de um pacote Python."
  @opcional @automatizado @decisao-I13 @pdf-p15-L15-L16 @md-L296
  Cenário: O arquivo é .whl ou .tar.gz gerado pelo build padrão
    Dado o arquivo "mazegen-*" na raiz do repositório
    Quando eu leio "mazegen-*"
    Então o nome de cada arquivo selecionado casa com a expressão "^mazegen-.+(\.whl|\.tar\.gz)$"
    E o pacote "mazegen-*" confirma "formato produzido por python -m build"

  # pdf: "Example of a full filename: mazegen-1.0.0-py3-none-any.whl ."
  # md:  "Exemplo de nome de arquivo completo: `mazegen-1.0.0-py3-none-any.whl`."
  @informativo @automatizado @decisao-I13 @pdf-p15-L17 @md-L298
  Cenário: O nome do wheel segue o padrão do exemplo
    Dado o arquivo "mazegen-*.whl" na raiz do repositório
    Quando eu leio "mazegen-*.whl"
    Então o nome de cada arquivo selecionado casa com a expressão "^mazegen-\d+\.\d+\.\d+-py3-none-any\.whl$"

  # pdf: "You must provide in your Git repository all needed elements to build the package."
  # md:  "Você deve fornecer no seu repositório Git todos os elementos necessários para construir o pacote."
  @obrigatorio @automatizado @decisao-I13 @pdf-p15-L18 @md-L300
  Cenário: O repositório contém tudo para construir o pacote
    Dado o repositório no estado "clone limpo"
    Quando eu executo "git ls-files"
    Então o código de saída é 0
    E o caminho "pyproject.toml" está versionado no git
    E o caminho "mazegen/__init__.py" está versionado no git
    E o caminho "mazegen/generator.py" está versionado no git
    E o caminho "mazegen/py.typed" está versionado no git
    E o caminho "README.md" está versionado no git
    E o caminho "LICENSE.md" está versionado no git
    E o pacote "mazegen-*" confirma "nada do build ignorado pelo git"

  # pdf: "This"
  # pdf: "will be asked during the evaluation: in a virtualenv or equivalent, install the needed tools"
  # pdf: "and build your package again from your sources."
  # md:  "Isso será solicitado durante a avaliação: em um virtualenv ou equivalente, instalar as ferramentas necessárias e reconstruir o pacote a partir dos seus fontes."
  @obrigatorio @automatizado @decisao-I13 @pdf-p15-L18-L20 @md-L300
  Cenário: O pacote é reconstruído do zero num virtualenv
    Dado o repositório no estado "clone limpo"
    E um virtualenv novo "build" em que rodou "pip install build"
    Quando o ambiente de execução é o virtualenv "build" na pasta "."
    E eu executo "python -m build"
    Então o código de saída é 0
    E a saída de erro não contém "warning" e "Warning"
    E o caminho "dist/mazegen-*.whl" existe
    E o caminho "dist/mazegen-*.tar.gz" existe
    E o pacote "dist/mazegen-*.whl" confirma "instala e importa MazeGenerator num virtualenv novo"

  # pdf: "will be asked during the evaluation: in a virtualenv or equivalent, install the needed tools"
  # pdf: "and build your package again from your sources."
  # md:  "Isso será solicitado durante a avaliação: em um virtualenv ou equivalente, instalar as ferramentas necessárias e reconstruir o pacote a partir dos seus fontes."
  # regua: "Have the evaluated student/team re-generate the package, most preferably in a virtualenv or similar. This must re-create the mazegen-*.tar.gz or .whl file."
  # regua: "Then, in a different virtualenv or similar, install the newly created package, and test it with the a_maze_ing.py script and its configuration file."
  # regua-md: "Peça ao estudante/equipe avaliado(a) que regenere o pacote, de preferência num virtualenv ou similar. Isso deve recriar o arquivo `mazegen-*.tar.gz` ou `.whl`."
  # regua-md: "Em seguida, num virtualenv diferente ou similar, instale o pacote recém-criado e teste-o com o script `a_maze_ing.py` e seu arquivo de configuração."
  @obrigatorio @automatizado @decisao-I11 @decisao-I13 @pdf-p15-L19-L20 @md-L300 @regua-p4
  Esquema do Cenário: O programa roda com o pacote recém-construído instalado em outro virtualenv
    Dado o repositório no estado "clone limpo"
    E um virtualenv novo "build" em que rodou "pip install build" e "python -m build"
    E um virtualenv novo "uso" em que rodou "pip install dist/<arquivo>"
    E o caminho "teste" preparado como "pasta com a_maze_ing.py, amazeing/ e config.txt"
    E o config do repositório
    Quando o ambiente de execução é o virtualenv "uso" na pasta "teste"
    E eu executo "python a_maze_ing.py config.txt" com a entrada "4"
    Então o código de saída é 0
    E a saída de "python -c 'import mazegen; print(mazegen.__file__)'" contém "site-packages"
    Quando eu analiso o labirinto com o maze_analyzer
    Então o veredito do maze_analyzer corresponde ao PERFECT do config

    Exemplos:
      | arquivo                        |
      | mazegen-1.0.0-py3-none-any.whl |
      | mazegen-1.0.0.tar.gz           |

  # pdf: "Both .tar.gz and .whl extensions are allowed, as generated by the standard build of a"
  # pdf: "Python package."
  # md:  "Tanto a extensão `.tar.gz` quanto `.whl` são permitidas, conforme geradas pelo build padrão de um pacote Python."
  # regua: "mazegen-*.tar.gz and/or .whl file"
  # regua-md: "`mazegen-*.tar.gz` e/ou arquivo `.whl`"
  @opcional @automatizado @decisao-I13 @pdf-p15-L15-L16 @md-L296 @regua-p1
  Cenário: O .tar.gz e o .whl podem estar os dois na raiz
    Dado o arquivo "mazegen-*.whl" na raiz do repositório
    E o arquivo "mazegen-*.tar.gz" na raiz do repositório
    Quando eu leio "mazegen-*"
    Então o pacote "mazegen-*" confirma "mesma versão no nome dos arquivos"
    E o pacote "mazegen-*" confirma "versão igual à do pyproject.toml"

  # pdf: "The main README.md file (not part of the reusable module) must also contain this short"
  # pdf: "documentation."
  # md:  "O arquivo `README.md` principal (que não faz parte do módulo reutilizável) também deve conter essa documentação curta."
  @obrigatorio @manual @decisao-I11 @decisao-I22 @pdf-p16-L03-L04 @md-L304
  Cenário: O README principal também contém a documentação do módulo
    - Dado o "README.md" da raiz do repositório
    - Quando eu procuro a documentação do módulo
    - Então ele explica como instanciar e usar o gerador, com exemplo
    - E ele explica como passar tamanho e seed
    - E ele explica como acessar a estrutura e uma solução
    - E o texto é o mesmo da docstring de "mazegen/__init__.py"
