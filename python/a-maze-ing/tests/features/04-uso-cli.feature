# language: pt
Funcionalidade: Uso pela linha de comando
  O programa principal se chama a_maze_ing.py, recebe um único argumento (o arquivo de
  configuração) e nunca termina com exceção não tratada.

  # pdf: "You will implement a maze generator in Python that takes a configuration file, generates"
  # md:  "Você implementará um gerador de labirintos em Python que recebe um arquivo de configuração, gera um labirinto"
  @obrigatorio @automatizado @pdf-p08-L04 @md-L142
  Cenário: O gerador é escrito em Python e recebe um arquivo de configuração
    Dado o config base
    Quando eu gero o labirinto
    Então o código de saída é 0
    E o validador da suíte confirma "labirinto válido conforme o config"

  # pdf: "Your program must be run with the following command:"
  # pdf: "python3 a_maze_ing.py config.txt"
  # md:  "Seu programa deve ser executado com o seguinte comando:"
  # md:  "python3 a_maze_ing.py config.txt"
  @obrigatorio @automatizado @decisao-I03 @decisao-I20 @pdf-p08-L09-L10 @md-L146-L150
  Cenário: O programa roda com o comando exato do subject
    Dado o arquivo "config.txt" na raiz do repositório
    Quando eu executo "python3 a_maze_ing.py config.txt" com a entrada "4"
    Então o código de saída é 0
    E a saída não contém "Traceback"

  # pdf: "a_maze_ing.py is your main program file. You must use this name."
  # md:  "`a_maze_ing.py` é o arquivo principal do seu programa. Você deve usar este nome."
  @obrigatorio @automatizado @pdf-p08-L11 @md-L152
  Cenário: O arquivo principal se chama a_maze_ing.py
    Dado o arquivo "a_maze_ing.py" na raiz do repositório
    Quando eu executo "git ls-files a_maze_ing.py"
    Então a saída padrão é "a_maze_ing.py"
    E a saída de "make -n run" contém "a_maze_ing.py"
    E a seção "Instructions" do README contém "a_maze_ing.py"

  # pdf: "config.txt is the only argument."
  # md:  "`config.txt` é o único argumento."
  @obrigatorio @automatizado @decisao-D01 @decisao-I12 @pdf-p08-L12 @md-L153
  Esquema do Cenário: Quantidade de argumentos diferente de um é recusada
    Quando eu executo "python3 a_maze_ing.py <argumentos>"
    Então a saída de erro contém "Usage: python3 a_maze_ing.py" e "config_file"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | argumentos             |
      |                        |
      | config.txt outro.txt   |
      | config.txt a.txt b.txt |

  # pdf: "It is a plain text file that defines the maze"
  # pdf: "generation options."
  # md:  "É um arquivo de texto simples que define as opções de geração do labirinto."
  @informativo @automatizado @pdf-p08-L12-L13 @md-L153
  Cenário: O arquivo de configuração é texto simples
    Dado o config base
    Quando eu gero o labirinto
    Então o validador da suíte confirma "labirinto válido conforme o config"

  # pdf: "You can use a different filename."
  # md:  "Você pode usar um nome de arquivo diferente."
  @opcional @automatizado @pdf-p08-L13 @md-L153
  Esquema do Cenário: O arquivo de configuração pode ter qualquer nome
    Dado o config do repositório salvo em "<nome>"
    Quando eu executo "python3 a_maze_ing.py <nome>" com a entrada "4"
    Então o código de saída é 0

    Exemplos:
      | nome               |
      | outro.cfg          |
      | configs/grande.txt |
      | sem_extensao       |

  # pdf: "Your program must handle all errors gracefully: invalid configuration, file not found, bad"
  # md:  "Seu programa deve tratar todos os erros de forma elegante: configuração inválida, arquivo não encontrado, sintaxe incorreta"
  @obrigatorio @automatizado @decisao-D01 @decisao-I21 @pdf-p08-L14 @md-L155
  Cenário: Arquivo de configuração inexistente
    Dado o caminho "nao_existe.txt" preparado como "inexistente"
    Quando eu executo "python3 a_maze_ing.py nao_existe.txt"
    Então a mensagem de erro cita "nao_existe.txt"
    E a mensagem de erro explica "arquivo não encontrado"
    E o código de saída é 1
    E a saída não contém "Traceback"

  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @pdf-p08-L14-L15 @md-L155
  Esquema do Cenário: Outros erros de leitura do arquivo de configuração
    Dado o caminho "<argumento>" preparado como "<tipo>"
    Quando eu executo "python3 a_maze_ing.py <argumento>"
    Então a mensagem de erro cita "<argumento>"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | tipo                     | argumento   |
      | diretório                | pasta       |
      | sem permissão de leitura | fechado.txt |
      | não UTF-8                | latin1.txt  |

  # pdf: "It must never crash unexpectedly, and must"
  # md:  "Ele nunca deve travar inesperadamente"
  @obrigatorio @automatizado @pdf-p08-L15 @md-L155
  Cenário: O programa nunca trava inesperadamente
    Dados os casos de erro do catálogo da suíte
    Quando cada caso do catálogo é executado com tempo limite
    Então o catálogo de casos de erro confirma "nenhum caso termina com Traceback"
    E o catálogo de casos de erro confirma "nenhum caso estoura o tempo limite"

  # pdf: "always provide a clear error message to the user."
  # md:  "e deve sempre fornecer uma mensagem de erro clara ao usuário."
  @obrigatorio @automatizado @decisao-D01 @pdf-p08-L16 @md-L155
  Cenário: Toda mensagem de erro é clara
    Dados os casos de erro do catálogo da suíte
    Quando cada caso do catálogo é executado com tempo limite
    Então o catálogo de casos de erro confirma "mensagem começa com Error:"
    E o catálogo de casos de erro confirma "mensagem cita o arquivo, a linha ou a chave"
    E o catálogo de casos de erro confirma "mensagem sem nome de exceção do Python"
