# language: pt
Funcionalidade: Arquivo de configuração
  O arquivo de configuração tem um par KEY=VALUE por linha, comentários com #, seis chaves
  obrigatórias e chaves extras opcionais. Todo erro vira mensagem clara.

  Contexto:
    Dado o config base salvo em "cfg.txt"

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  @obrigatorio @automatizado @pdf-p08-L18 @md-L159
  Cenário: Um par KEY=VALUE por linha é aceito
    Quando eu gero o labirinto
    Então o código de saída é 0
    E a grade do labirinto tem 20 colunas e 15 linhas

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D04 @pdf-p08-L18 @pdf-p08-L15 @md-L159 @md-L155
  Esquema do Cenário: Linha fora do formato KEY=VALUE é erro de sintaxe
    Dado o config com a linha 2 trocada por "<linha>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "cfg.txt", "line 2" e "<linha>"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | linha     |
      | HEIGHT 15 |
      | HEIGHT    |
      | =15       |

  # pdf: "Lines starting with # are comments and must be ignored."
  # md:  "Linhas começando com `#` são comentários e devem ser ignoradas."
  # regua: "Comments lines start with '#'."
  # regua-md: "Linhas de comentário começam com `#`."
  @obrigatorio @automatizado @pdf-p08-L19 @md-L161 @regua-p2
  Esquema do Cenário: Linhas de comentário são ignoradas
    Dado o config com a linha "<comentario>" inserida no início
    Quando eu gero o labirinto
    Então o arquivo de saída é idêntico byte a byte ao gerado com o config base

    Exemplos:
      | comentario                  |
      | # A-Maze-ing default config |
      | #WIDTH=5                    |
      | # PERFECT=False             |
      | #                           |
      | #X=1=2                      |

  # pdf: "Lines starting with # are comments and must be ignored."
  # md:  "Linhas começando com `#` são comentários e devem ser ignoradas."
  @obrigatorio @derivado @decisao-D04 @automatizado @pdf-p08-L19 @md-L161
  Cenário: Comentário com espaços antes do # também é ignorado
    Dado o config com a linha "    # indentado" inserida no início
    Quando eu gero o labirinto
    Então o arquivo de saída é idêntico byte a byte ao gerado com o config base

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  @obrigatorio @derivado @decisao-D04 @automatizado @pdf-p08-L18 @md-L159
  Cenário: Comentário no fim de uma linha de valor não é suportado
    Dado o config com a linha 1 trocada por "WIDTH=20 # largura"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "WIDTH"
    E o código de saída é 1

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  @obrigatorio @derivado @decisao-D04 @automatizado @pdf-p08-L18 @md-L159
  Esquema do Cenário: Linhas vazias e espaços em volta de chave e valor são tolerados
    Dado o config escrito com a variação "<variacao>"
    Quando eu gero o labirinto
    Então o arquivo de saída é idêntico byte a byte ao gerado com o config base

    Exemplos:
      | variacao                                   |
      | uma linha vazia entre cada par             |
      | espaços em volta do igual                  |
      | espaços no fim de cada linha               |
      | finais de linha CRLF                       |
      | sem quebra de linha depois da última linha |

  # pdf: "The following keys are mandatory:"
  # md:  "As seguintes chaves são obrigatórias:"
  # regua: "The expected keys are present (WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT)."
  # regua: "Remove a mandatory key."
  # regua-md: "As chaves esperadas estão presentes (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`)."
  # regua-md: "Remova uma chave obrigatória."
  @obrigatorio @automatizado @decisao-D01 @decisao-I21 @pdf-p08-L20-L27 @md-L163-L172 @regua-p2
  Esquema do Cenário: Cada chave obrigatória ausente gera erro
    Dado o config sem a chave "<chave>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "<chave>"
    E a mensagem de erro explica "chave obrigatória ausente"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | chave       |
      | WIDTH       |
      | HEIGHT      |
      | ENTRY       |
      | EXIT        |
      | OUTPUT_FILE |
      | PERFECT     |

  # pdf: "The following keys are mandatory:"
  # md:  "As seguintes chaves são obrigatórias:"
  @obrigatorio @derivado @decisao-D04 @automatizado @pdf-p08-L20 @md-L163
  Cenário: Arquivo sem nenhuma chave lista todas as chaves ausentes
    Dado o caminho "cfg.txt" preparado como "vazio"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE" e "PERFECT"
    E o código de saída é 1

  # pdf: "WIDTH           Maze width (number of cells) WIDTH=20"
  # md:  "`WIDTH` | Largura do labirinto (número de células) | `WIDTH=20`"
  @obrigatorio @automatizado @pdf-p08-L22 @md-L167
  Esquema do Cenário: WIDTH é o número de colunas
    Dado o config com "WIDTH=<valor>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então a grade do labirinto tem <valor> colunas e 15 linhas

    Exemplos:
      | valor | saida |
      | 20    | 19,14 |
      | 9     | 8,14  |
      | 41    | 40,14 |
      | 1     | 0,14  |
      | 100   | 99,14 |

  # pdf: "WIDTH           Maze width (number of cells) WIDTH=20"
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "`WIDTH` | Largura do labirinto (número de células) | `WIDTH=20`"
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @pdf-p08-L22 @pdf-p08-L15 @md-L167 @md-L155
  Esquema do Cenário: WIDTH inválido gera erro
    Dado o config com "WIDTH=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "WIDTH"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | valor   |
      |         |
      | abc     |
      | 2.5     |
      | 0       |
      | -3      |
      | 1e3     |
      | 20,0    |
      | 101     |
      | 1000000 |

  # pdf: "HEIGHT          Maze height                  HEIGHT=15"
  # md:  "`HEIGHT` | Altura do labirinto | `HEIGHT=15`"
  @obrigatorio @automatizado @pdf-p08-L23 @md-L168
  Esquema do Cenário: HEIGHT é o número de linhas
    Dado o config com "HEIGHT=<valor>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então a grade do labirinto tem 20 colunas e <valor> linhas

    Exemplos:
      | valor | saida |
      | 15    | 19,14 |
      | 9     | 19,8  |
      | 30    | 19,29 |
      | 1     | 19,0  |
      | 100   | 19,99 |

  # pdf: "HEIGHT          Maze height                  HEIGHT=15"
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "`HEIGHT` | Altura do labirinto | `HEIGHT=15`"
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @pdf-p08-L23 @pdf-p08-L15 @md-L168 @md-L155
  Esquema do Cenário: HEIGHT inválido gera erro
    Dado o config com "HEIGHT=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "HEIGHT"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | valor       |
      |             |
      | quinze      |
      | 7.0         |
      | 0           |
      | -1          |
      | 15 WIDTH=20 |
      | 15 # altura |
      | 101         |
      | 99999999    |

  # pdf: "ENTRY           Entry coordinates (x,y)      ENTRY=0,0"
  # pdf: "EXIT            Exit coordinates (x,y)       EXIT=19,14"
  # md:  "`ENTRY` | Coordenadas da entrada (x,y) | `ENTRY=0,0`"
  # md:  "`EXIT` | Coordenadas da saída (x,y) | `EXIT=19,14`"
  @obrigatorio @automatizado @pdf-p08-L24-L25 @md-L169-L170
  Esquema do Cenário: ENTRY e EXIT são coordenadas x,y
    Dado o config com "ENTRY=<entrada>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então a linha 1 do rodapé é "<entrada>"
    E a linha 2 do rodapé é "<saida>"

    Exemplos:
      | entrada | saida |
      | 0,0     | 19,14 |
      | 1,1     | 18,13 |
      | 19,0    | 0,14  |

  # pdf: "ENTRY           Entry coordinates (x,y)      ENTRY=0,0"
  # pdf: "EXIT            Exit coordinates (x,y)       EXIT=19,14"
  # md:  "`ENTRY` | Coordenadas da entrada (x,y) | `ENTRY=0,0`"
  # md:  "`EXIT` | Coordenadas da saída (x,y) | `EXIT=19,14`"
  @obrigatorio @derivado @automatizado @pdf-p08-L22-L25 @md-L167-L170
  Cenário: x é a coluna e y é a linha, contando a partir de 0
    Dado o config com "WIDTH=20", "HEIGHT=15" e "EXIT=19,14"
    Quando eu gero o labirinto
    Então a linha 2 do rodapé é "19,14"
    E o validador da suíte confirma "x é a coluna e y é a linha"

  # pdf: "ENTRY           Entry coordinates (x,y)      ENTRY=0,0"
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "`ENTRY` | Coordenadas da entrada (x,y) | `ENTRY=0,0`"
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @pdf-p08-L24 @pdf-p08-L15 @md-L169 @md-L155
  Esquema do Cenário: ENTRY inválida gera erro
    Dado o config com "ENTRY=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "ENTRY"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | valor |
      |       |
      | 0     |
      | 0,0,0 |
      | a,b   |
      | 0;0   |
      | (0,0) |
      | -1,0  |
      | 20,0  |
      | 0,15  |

  # pdf: "EXIT            Exit coordinates (x,y)       EXIT=19,14"
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "`EXIT` | Coordenadas da saída (x,y) | `EXIT=19,14`"
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @pdf-p08-L25 @pdf-p08-L15 @md-L170 @md-L155
  Esquema do Cenário: EXIT inválida gera erro
    Dado o config com "EXIT=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "EXIT"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | valor |
      |       |
      | 19    |
      | x,y   |
      | 19,-1 |
      | 20,14 |
      | 19,15 |

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @decisao-I21 @pdf-p09-L09 @pdf-p08-L15 @md-L183 @md-L155
  Cenário: ENTRY igual a EXIT é parâmetro impossível
    Dado o config com "ENTRY=5,5" e "EXIT=5,5"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro explica "entrada igual à saída"
    E o código de saída é 1

  # pdf: "OUTPUT_FILE Output filename                  OUTPUT_FILE=maze.txt"
  # md:  "`OUTPUT_FILE` | Nome do arquivo de saída | `OUTPUT_FILE=maze.txt`"
  @obrigatorio @automatizado @pdf-p08-L26 @md-L171
  Cenário: OUTPUT_FILE define o nome do arquivo de saída
    Dado o config com "OUTPUT_FILE=saida_teste.txt"
    E o caminho "saida_teste.txt" preparado como "inexistente"
    Quando eu gero o labirinto
    Então o caminho "saida_teste.txt" existe
    E o validador da suíte confirma "labirinto válido conforme o config"

  # pdf: "OUTPUT_FILE Output filename                  OUTPUT_FILE=maze.txt"
  # md:  "`OUTPUT_FILE` | Nome do arquivo de saída | `OUTPUT_FILE=maze.txt`"
  @obrigatorio @automatizado @decisao-D01 @pdf-p08-L26 @md-L171
  Cenário: OUTPUT_FILE vazio gera erro
    Dado o config com "OUTPUT_FILE="
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "OUTPUT_FILE"
    E o código de saída é 1

  # pdf: "PERFECT         Is the maze perfect?         PERFECT=True"
  # md:  "`PERFECT` | O labirinto é perfeito? | `PERFECT=True`"
  # regua: "Each line is in the 'KEY=VALUE' format (lower case is also OK)."
  # regua-md: "Cada linha está no formato `KEY=VALUE` (minúsculas também são aceitas)."
  @obrigatorio @automatizado @decisao-D03 @pdf-p08-L27 @md-L172 @regua-p2
  Esquema do Cenário: PERFECT aceita True e False sem diferenciar maiúsculas
    Dado o config com "PERFECT=<valor>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "<veredito>"

    Exemplos:
      | valor | veredito       |
      | True  | PERFECT maze   |
      | true  | PERFECT maze   |
      | TRUE  | PERFECT maze   |
      | False | Pac-Man-USABLE |
      | false | Pac-Man-USABLE |

  # pdf: "PERFECT         Is the maze perfect?         PERFECT=True"
  # md:  "`PERFECT` | O labirinto é perfeito? | `PERFECT=True`"
  # regua: "Use an incorrect boolean parameter for 'PERFECT'."
  # regua-md: "Use um booleano incorreto em `PERFECT`."
  @obrigatorio @automatizado @decisao-D01 @decisao-D03 @pdf-p08-L27 @md-L172 @regua-p2
  Esquema do Cenário: PERFECT com valor que não é booleano gera erro
    Dado o config com "PERFECT=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "PERFECT"
    E o código de saída é 1

    Exemplos:
      | valor |
      |       |
      | yes   |
      | 1     |
      | sim   |
      | Truee |

  # pdf: "Key             Description                  Example"
  # md:  "Chave | Descrição | Exemplo"
  @obrigatorio @derivado @automatizado @pdf-p08-L21-L27 @md-L165-L172
  Cenário: O config de exemplo da tabela do subject roda sem erro
    Dado o config sem a chave "SEED"
    Quando eu gero o labirinto
    Então o código de saída é 0
    E a grade do labirinto tem 20 colunas e 15 linhas
    E o validador da suíte confirma "labirinto válido conforme o config"

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  @obrigatorio @derivado @decisao-D04 @automatizado @pdf-p08-L18 @md-L159
  Cenário: Na chave repetida vale a última linha
    Dado o config com a linha "WIDTH=30" acrescentada no fim
    Quando eu gero o labirinto
    Então a grade do labirinto tem 30 colunas e 15 linhas

  # pdf: "You may add additional keys (e.g., seed, algorithm, display mode) if useful."
  # md:  "Você pode adicionar chaves extras (ex.: seed, algoritmo, modo de exibição) se for útil."
  @opcional @automatizado @pdf-p09-L02 @md-L174
  Cenário: Chaves extras conhecidas pelo programa são aceitas
    Dado o config com "SEED=42"
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então o código de saída é 0

  # pdf: "You may add additional keys (e.g., seed, algorithm, display mode) if useful."
  # md:  "Você pode adicionar chaves extras (ex.: seed, algoritmo, modo de exibição) se for útil."
  @opcional @derivado @decisao-D04 @automatizado @pdf-p09-L02 @md-L174
  Esquema do Cenário: Chave desconhecida é ignorada
    Dado o config com a linha "<linha>" acrescentada no fim
    Quando eu gero o labirinto
    Então o arquivo de saída é idêntico byte a byte ao gerado com o config base

    Exemplos:
      | linha     |
      | COLOR=red |
      | FOO=1     |
      | widht=99  |

  # pdf: "The following keys are mandatory:"
  # md:  "As seguintes chaves são obrigatórias:"
  @obrigatorio @derivado @decisao-D01 @decisao-D04 @automatizado @decisao-I21 @pdf-p08-L20 @md-L163
  Cenário: Chave obrigatória com erro de digitação é acusada como ausente
    Dado o config com a linha da chave "WIDTH" trocada por "WIDHT=20"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "WIDTH"
    E a mensagem de erro explica "chave obrigatória ausente"
    E o código de saída é 1

  # pdf: "The configuration file must contain one 'KEY=VALUE' pair per line."
  # md:  "O arquivo de configuração deve conter um par `KEY=VALUE` por linha."
  # regua: "Each line is in the 'KEY=VALUE' format (lower case is also OK)."
  # regua-md: "Cada linha está no formato `KEY=VALUE` (minúsculas também são aceitas)."
  @obrigatorio @automatizado @decisao-D04 @pdf-p08-L18 @md-L159 @regua-p2
  Esquema do Cenário: Chaves e booleanos em minúsculas são aceitos
    Dado o config escrito com a variação "<variacao>"
    Quando eu gero o labirinto
    Então o arquivo de saída é idêntico byte a byte ao gerado com o config base

    Exemplos:
      | variacao                   |
      | chave WIDTH minúscula      |
      | todas as chaves minúsculas |
      | chave HEIGHT capitalizada  |
      | perfect=true minúsculo     |

  # pdf: "Your program must handle all errors gracefully: invalid configuration, file not found, bad"
  # pdf: "syntax, impossible maze parameters, etc. It must never crash unexpectedly, and must"
  # pdf: "always provide a clear error message to the user."
  # md:  "Seu programa deve tratar todos os erros de forma elegante: configuração inválida, arquivo não encontrado, sintaxe incorreta, parâmetros de labirinto impossíveis etc. Ele nunca deve travar inesperadamente e deve sempre fornecer uma mensagem de erro clara ao usuário."
  # regua: "Edit the configuration file to ensure that the program correctly handles its errors:"
  # regua: "Remove a mandatory key."
  # regua: "Add a line that does not respect the 'KEY=VALUE' format (e.g., without the '=' sign)."
  # regua: "Replace numbers by letters."
  # regua: "Use an incorrect boolean parameter for 'PERFECT'."
  # regua: "Use a wrong format of int tuple for 'ENTRY' or 'EXIT'."
  # regua: "Reminder: in case of unexpected end of the program, the evaluation stops and final grade is 0."
  # regua-md: "Edite o arquivo de configuração para garantir que o programa trata corretamente os erros:"
  # regua-md: "Remova uma chave obrigatória."
  # regua-md: "Adicione uma linha que não respeite o formato `KEY=VALUE` (ex.: sem o sinal `=`)."
  # regua-md: "Substitua números por letras."
  # regua-md: "Use um booleano incorreto em `PERFECT`."
  # regua-md: "Use um formato errado de tupla de inteiros em `ENTRY` ou `EXIT`."
  # regua-md: "Lembrete: em caso de encerramento inesperado do programa, a avaliação para e a nota final é 0."
  @obrigatorio @automatizado @decisao-D01 @decisao-I20 @pdf-p08-L14-L16 @md-L155 @regua-p2
  Esquema do Cenário: Os cinco erros que o avaliador provoca no config
    Dado o config do repositório salvo em "cfg.txt"
    E o config com a linha da chave "<chave>" trocada por "<linha>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "<chave>"
    E a saída não contém "Traceback"
    E o processo termina dentro do tempo limite

    Exemplos:
      | chave   | linha         |
      | WIDTH   |               |
      | PERFECT |               |
      | HEIGHT  | HEIGHT 15     |
      | WIDTH   | WIDTH=abc     |
      | HEIGHT  | HEIGHT=xv     |
      | PERFECT | PERFECT=maybe |
      | ENTRY   | ENTRY=0;0     |
      | EXIT    | EXIT=19       |
      | ENTRY   | ENTRY=a,b     |

  # pdf: "A default configuration file must be available in your Git repository."
  # md:  "Um arquivo de configuração padrão deve estar disponível no seu repositório Git."
  @obrigatorio @automatizado @decisao-I20 @pdf-p09-L03 @md-L176
  Cenário: O config padrão está versionado e funciona
    Dado o repositório no estado "clone limpo"
    Quando eu executo "git ls-files config.txt"
    E eu executo "python3 a_maze_ing.py config.txt" com a entrada "4"
    Então a saída de "git ls-files config.txt" é "config.txt"
    E o código de saída é 0

  # pdf: "If the PERFECT flag is not activated (the default), the maze must instead be a board"
  # md:  "Se a flag `PERFECT` não estiver ativada (o padrão), o labirinto deve ser um tabuleiro"
  # regua: "When 'PERFECT' is set to False (the default), the maze is a board usable by a Pac-Man-like game"
  # regua-md: "Quando `PERFECT` é `False` (o padrão), o labirinto é um tabuleiro utilizável por um jogo estilo Pac-Man"
  @obrigatorio @derivado @decisao-D03 @automatizado @decisao-I20 @pdf-p09-L22 @md-L190 @regua-p3
  Cenário: O config padrão usa o modo padrão do subject
    Dado o arquivo "config.txt" na raiz do repositório
    Quando eu leio "config.txt"
    Então o arquivo "config.txt" tem uma linha que casa com a expressão "^PERFECT=False$"

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  # regua: "Run the a_maze_ing.py script, using a default configuration file."
  # regua: "You should get a maze randomly generated, displayed on the terminal or using a dedicated graphic window, and a way to interact with the program."
  # regua-md: "Execute o script `a_maze_ing.py` usando um arquivo de configuração padrão."
  # regua-md: "Você deve obter um labirinto gerado aleatoriamente, exibido no terminal ou numa janela gráfica dedicada, e uma forma de interagir com o programa."
  @obrigatorio @derivado @decisao-D02 @automatizado @decisao-I20 @pdf-p09-L05 @md-L180 @regua-p2
  Cenário: O config padrão gera um labirinto diferente a cada execução
    Dado o config do repositório
    E o arquivo "config.txt" não tem nenhuma linha que casa com a expressão "^SEED="
    Quando eu gero o labirinto 3 vezes
    Então os resultados são diferentes entre si em "grade"
    Quando eu gero o labirinto com cada um de "SEED=42", "SEED=42" e "SEED=42"
    Então os resultados são idênticos em "grade"

  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  @obrigatorio @automatizado @decisao-D01 @decisao-D05 @decisao-I21 @pdf-p08-L15 @md-L155
  Esquema do Cenário: Grade onde o modo Pac-Man é impossível gera erro
    Dado o config com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "PERFECT=False"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro explica "tamanho sem tabuleiro Pac-Man"
    E o código de saída é 1

    Exemplos:
      | largura | altura | saida |
      | 1       | 10     | 0,9   |
      | 10      | 1      | 9,0   |
      | 2       | 2      | 1,1   |
