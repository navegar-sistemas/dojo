# language: pt
Funcionalidade: Arquivo de saída
  O labirinto é gravado em OUTPUT_FILE com um dígito hexadecimal por célula, uma linha da
  grade por linha do arquivo, seguido de linha vazia, entrada, saída e caminho mais curto.

  # pdf: "a maze, possibly perfect (with a single path between entrance and exit), and writes it to a"
  # pdf: "file using a hexadecimal wall representation."
  # md:  "gera um labirinto — possivelmente perfeito (com um único caminho entre entrada e saída) — e o escreve em um arquivo usando uma representação hexadecimal das paredes."
  @obrigatorio @automatizado @pdf-p08-L05-L06 @md-L142
  Cenário: O programa grava o labirinto num arquivo em hexadecimal
    Dado o config base
    Quando eu gero o labirinto
    Então o caminho "maze.txt" existe
    E cada linha da grade casa com a expressão "^[0-9a-fA-F]+$"

  # pdf: "a maze, possibly perfect (with a single path between entrance and exit), and writes it to a"
  # pdf: "file using a hexadecimal wall representation. You will also provide a visual representation"
  # md:  "e o escreve em um arquivo usando uma representação hexadecimal das paredes. Você também fornecerá uma representação visual do labirinto"
  # regua: "Run the a_maze_ing.py script and verify that the first generated (and displayed) maze is also stored in the defined output file."
  # regua-md: "Execute o script `a_maze_ing.py` e verifique que o primeiro labirinto gerado (e exibido) também é armazenado no arquivo de saída definido."
  @obrigatorio @automatizado @decisao-I02 @pdf-p08-L05-L06 @md-L142 @regua-p3
  Esquema do Cenário: O primeiro labirinto exibido é o que está no arquivo de saída
    Dado o config base com "PERFECT=<perfeito>"
    E o config sem a chave "SEED"
    E o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Então o caminho "maze.txt" existe
    E o programa aguarda no prompt "Choice? (1-4): "
    E a renderização confirma "paredes iguais às do arquivo de saída"
    E a renderização confirma "entrada e saída iguais às do rodapé"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "OUTPUT_FILE Output filename                  OUTPUT_FILE=maze.txt"
  # md:  "`OUTPUT_FILE` | Nome do arquivo de saída | `OUTPUT_FILE=maze.txt`"
  @obrigatorio @derivado @automatizado @pdf-p08-L26 @md-L171
  Esquema do Cenário: O arquivo é gravado no caminho indicado por OUTPUT_FILE
    Dado o config base com "OUTPUT_FILE=<caminho>"
    E o caminho "<caminho>" preparado como "diretório pai criado"
    Quando eu gero o labirinto
    E o validador da suíte lê o labirinto
    Então o caminho "<caminho>" não está vazio
    E o validador da suíte confirma "labirinto válido conforme o config"

    Exemplos:
      | caminho             |
      | maze.txt            |
      | saida/labirinto.txt |
      | resultado           |

  # pdf: "Your program must handle all errors gracefully: invalid configuration, file not found, bad"
  # md:  "Seu programa deve tratar todos os erros de forma elegante: configuração inválida, arquivo não encontrado, sintaxe incorreta"
  @obrigatorio @derivado @decisao-D01 @automatizado @pdf-p08-L14-L16 @md-L155
  Esquema do Cenário: Erro ao gravar o arquivo de saída vira mensagem clara
    Dado o config base com "OUTPUT_FILE=<caminho>"
    E o caminho "<diretorio>" preparado como "<tipo>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "<caminho>"
    E o código de saída é 1
    E a saída não contém "Traceback"

    Exemplos:
      | caminho             | diretorio  | tipo                               |
      | nao_existe/maze.txt | nao_existe | inexistente                        |
      | trancado/maze.txt   | trancado   | diretório sem permissão de escrita |
      | pasta               | pasta      | diretório                          |

  # pdf: "The maze must be written in the output file using one hexadecimal digit per cell, where"
  # md:  "O labirinto deve ser escrito no arquivo de saída usando um dígito hexadecimal por célula"
  @obrigatorio @automatizado @pdf-p10-L06 @md-L204
  Cenário: Um dígito hexadecimal por célula
    Dado o config base
    Quando eu gero o labirinto
    Então cada linha da grade casa com a expressão "^[0-9a-f]{20}$"
    E a grade do labirinto tem 20 colunas e 15 linhas

  # pdf: "each digit encodes which walls are closed:"
  # md:  "onde cada dígito codifica quais paredes estão fechadas:"
  @obrigatorio @automatizado @decisao-I09 @pdf-p10-L06-L07 @md-L204
  Cenário: O dígito codifica as paredes fechadas da célula
    Dado um labirinto gerado pelo módulo mazegen com o config base
    Quando eu gero o labirinto
    Então o módulo mazegen confirma "grade igual à do arquivo de saída"

  # pdf: "Bit      Direction"
  # pdf: "0 (LSB)     North"
  # md:  "Bit | Direção"
  # md:  "0 (LSB) | Norte"
  @obrigatorio @automatizado @pdf-p10-L08-L12 @md-L206-L211
  Esquema do Cenário: Cada bit representa uma direção
    Dada a célula com as paredes fechadas "<direcao>"
    Quando o validador da suíte converte a célula
    Então o bit <bit> da célula está ligado
    E o dígito da célula é "<digito>"

    Exemplos:
      | direcao | bit | digito |
      | Norte   | 0   | 1      |
      | Leste   | 1   | 2      |
      | Sul     | 2   | 4      |
      | Oeste   | 3   | 8      |

  # pdf: "A wall being closed sets the bit to 1, open means 0."
  # md:  "Uma parede fechada define o bit como `1`; aberta significa `0`."
  @obrigatorio @automatizado @pdf-p10-L13 @md-L213
  Esquema do Cenário: Parede fechada vale 1 e parede aberta vale 0
    Dada a célula com as paredes fechadas "<fechadas>"
    Quando o validador da suíte converte a célula
    Então o dígito da célula é "<digito>"

    Exemplos:
      | fechadas                  | digito |
      | nenhuma                   | 0      |
      | Norte, Leste, Sul e Oeste | f      |
      | Norte e Sul               | 5      |
      | Sul e Oeste               | c      |

  # pdf: "Example: 3 (binary 0011) means walls are open to the south and west."
  # md:  "Exemplo: `3` (binário `0011`) significa que as paredes estão abertas ao sul e a oeste."
  @obrigatorio @automatizado @pdf-p10-L14 @md-L214
  Cenário: O dígito 3 tem Sul e Oeste abertas
    Dada a célula de dígito "3"
    Quando o validador da suíte converte a célula
    Então as paredes fechadas da célula são "Norte e Leste"
    E as paredes abertas da célula são "Sul e Oeste"

  # pdf: "Or A"
  # pdf: "(binary 1010) means that east and west walls are closed."
  # md:  "Já `A` (binário `1010`) significa que as paredes leste e oeste estão fechadas."
  @obrigatorio @automatizado @pdf-p10-L14-L15 @md-L214
  Cenário: O dígito A tem Leste e Oeste fechadas
    Dada a célula de dígito "A"
    Quando o validador da suíte converte a célula
    Então as paredes fechadas da célula são "Leste e Oeste"
    E as paredes abertas da célula são "Norte e Sul"

  # pdf: "Cells are stored row by row, one row per line."
  # md:  "As células são armazenadas linha por linha, uma linha da grade por linha do arquivo."
  @obrigatorio @automatizado @pdf-p10-L16 @md-L215
  Cenário: Uma linha da grade por linha do arquivo
    Dado o config base
    Quando eu gero o labirinto
    Então a grade do labirinto tem 20 colunas e 15 linhas
    E o validador da suíte confirma "x é a coluna e y é a linha"

  # pdf: "Cells are stored row by row, one row per line."
  # md:  "As células são armazenadas linha por linha, uma linha da grade por linha do arquivo."
  # regua: "'HEIGHT' lines of 'WIDTH' chars each,"
  # regua-md: "`HEIGHT` linhas de `WIDTH` caracteres cada,"
  @obrigatorio @derivado @automatizado @pdf-p10-L16 @md-L215 @regua-p3
  Esquema do Cenário: A grade tem HEIGHT linhas de WIDTH dígitos, sem separadores
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então a grade do labirinto tem <largura> colunas e <altura> linhas
    E cada linha da grade casa com a expressão "^[0-9a-fA-F]{<largura>}$"

    Exemplos:
      | largura | altura | saida |
      | 20      | 15     | 19,14 |
      | 25      | 20     | 19,14 |
      | 9       | 30     | 8,29  |

  # pdf: "After an empty line, the following 3 elements are inserted in the output file on 3"
  # pdf: "lines:"
  # md:  "Após uma linha vazia, os 3 elementos a seguir são inseridos no arquivo de saída em 3 linhas:"
  # regua: "an empty line,"
  # regua-md: "uma linha vazia,"
  @obrigatorio @automatizado @pdf-p10-L17-L18 @md-L216 @regua-p3
  Cenário: Uma linha vazia separa a grade dos três elementos finais
    Dado o config base
    Quando eu gero o labirinto
    Então o validador da suíte confirma "uma linha vazia logo após a grade"
    E o validador da suíte confirma "exatamente 3 linhas após a linha vazia"

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "as coordenadas da entrada"
  # regua: "the 'ENTRY' tuple,"
  # regua-md: "a tupla `ENTRY`,"
  @obrigatorio @automatizado @decisao-D13 @pdf-p10-L19 @md-L217 @regua-p3
  Cenário: A primeira linha após a linha vazia é a entrada
    Dado o config base com "ENTRY=1,1"
    Quando eu gero o labirinto
    Então a linha 1 do rodapé é "1,1"

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "as coordenadas da saída"
  # regua: "the 'EXIT' tuple,"
  # regua-md: "a tupla `EXIT`,"
  @obrigatorio @automatizado @decisao-D13 @pdf-p10-L19 @md-L217 @regua-p3
  Cenário: A segunda linha após a linha vazia é a saída
    Dado o config base com "EXIT=18,13"
    Quando eu gero o labirinto
    Então a linha 2 do rodapé é "18,13"

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "as coordenadas da entrada, as coordenadas da saída"
  # md:  "1,1        # entry  (x,y)"
  # md:  "19,14      # exit   (x,y)"
  # regua: "the 'ENTRY' tuple,"
  # regua: "the 'EXIT' tuple,"
  # regua-md: "a tupla `ENTRY`,"
  # regua-md: "a tupla `EXIT`,"
  @obrigatorio @derivado @decisao-D13 @automatizado @pdf-p10-L19 @pdf-p11-figura @md-L217 @md-L247-L248 @regua-p3
  Cenário: As coordenadas do rodapé são x,y sem anotação
    Dado o config base
    Quando eu gero o labirinto
    Então cada linha de coordenadas do rodapé casa com a expressão "^\d+,\d+$"
    E a linha "Entry" do maze_analyzer contém "(0, 0)" e "Exit: (19, 14) (reachable)"

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # pdf: "entry to exit, using the four letters N , E , S , W ."
  # md:  "o caminho válido mais curto da entrada até a saída, usando as quatro letras `N`, `E`, `S`, `W`."
  # regua: "the shortest path from entry to exit described using directions 'N', 'E', 'S', 'W'."
  # regua-md: "o caminho mais curto da entrada até a saída descrito com as direções `N`, `E`, `S`, `W`."
  @obrigatorio @automatizado @decisao-D15 @decisao-I08 @pdf-p10-L19-L20 @md-L217 @regua-p3
  Esquema do Cenário: A terceira linha é o caminho mais curto válido
    Dado o config base com "PERFECT=<perfeito>"
    Quando eu gero o labirinto
    Então a linha 3 do rodapé casa com a expressão "^[NESW]+$"
    E o validador da suíte confirma "solução válida e mais curta"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "All lines end with a \n ."
  # md:  "Todas as linhas terminam com `\n`."
  @obrigatorio @automatizado @pdf-p10-L21 @md-L218
  Cenário: Todas as linhas terminam com \n
    Dado o config base
    Quando eu gero o labirinto
    Então o validador da suíte confirma "arquivo termina com quebra de linha"
    E o validador da suíte confirma "linha vazia contém só a quebra de linha"
    E o arquivo "maze.txt" não contém "\r"
    E o validador da suíte confirma "nenhuma linha com espaço no fim"

  # pdf: "The maze must be written in the output file using one hexadecimal digit per cell, where"
  # md:  "O labirinto deve ser escrito no arquivo de saída usando um dígito hexadecimal por célula"
  @obrigatorio @derivado @decisao-D14 @automatizado @pdf-p10-L06 @md-L204
  Cenário: Os dígitos de a a f são gravados em minúsculas
    Dado o config base
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então cada linha da grade casa com a expressão "^[0-9a-f]+$"
    E a saída não contém "Malformed maze file"

  # pdf: "In conjunction with its specific configuration file, this output file could be tested auto-"
  # pdf: "matically by a Moulinette."
  # md:  "Em conjunto com seu arquivo de configuração específico, este arquivo de saída poderá ser testado automaticamente por uma Moulinette."
  @informativo @derivado @automatizado @pdf-p11-L02-L03 @md-L220
  Cenário: O arquivo é estritamente analisável junto com o config
    Dado o config base
    Quando eu gero o labirinto
    E o validador da suíte lê o labirinto
    Então a grade do labirinto tem 20 colunas e 15 linhas
    E o validador da suíte confirma "rodapé com ENTRY, EXIT e caminho válido"
    E o validador da suíte confirma "modo igual ao PERFECT do config"

  # pdf: "An analysis script (maze_analyzer.py) is also provided with"
  # pdf: "this subject."
  # md:  "Um script de análise (`maze_analyzer.py`) também é fornecido com este subject."
  @informativo @automatizado @pdf-p11-L03-L04 @md-L220
  Cenário: O maze_analyzer.py lê o arquivo sem erro de formato
    Dado o config base
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então o código de saída é 0
    E a saída não contém "Malformed maze file"
    E a saída não contém "no valid entry in footer"

  # pdf: "Given an output file, it checks that the wall encoding is coherent (each"
  # pdf: "shared wall is encoded the same way by both neighbouring cells)"
  # md:  "Dado um arquivo de saída, ele verifica que a codificação das paredes é coerente (cada parede compartilhada é codificada da mesma forma pelas duas células vizinhas)"
  @informativo @automatizado @pdf-p11-L04-L05 @md-L220
  Cenário: O maze_analyzer.py confirma a coerência das paredes
    Dado o config base
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então a linha "Wall coherence" do maze_analyzer contém "OK (all shared walls match)"

  # pdf: "You may use it to check that your generator produces the mode requested by"
  # pdf: "the configuration file."
  # md:  "Você pode usá-lo para verificar se o seu gerador produz o modo solicitado pelo arquivo de configuração."
  # regua: "Run the provided analysis script "python3 maze_analyzer.py <output_file>": it controls the walls coherence and reports whether the maze matches the mode set in the configuration file (perfect single-path vs. playable board). Any incoherence or mismatch marks this question as failed."
  # regua-md: "Execute o script de análise fornecido: `python3 maze_analyzer.py <output_file>`; ele controla a coerência das paredes e informa se o labirinto corresponde ao modo definido no arquivo de configuração (perfeito de caminho único vs. tabuleiro jogável). Qualquer incoerência ou divergência marca esta questão como reprovada."
  @opcional @automatizado @pdf-p11-L08-L09 @md-L220 @regua-p3
  Esquema do Cenário: O modo gerado é o modo pedido no config
    Dado o config base com "PERFECT=<perfeito>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então a linha "Verdict:" do maze_analyzer começa com "<veredito>"

    Exemplos:
      | perfeito | veredito       |
      | True     | PERFECT maze   |
      | False    | Pac-Man-USABLE |

  # pdf: "Output file example"
  # md:  "Exemplo de arquivo de saída (transcrito da captura de tela do subject, `output_maze.txt`):"
  # md:  "9139551111555515515395153"
  @informativo @automatizado @pdf-p11-L10 @pdf-p11-figura @md-L222-L245
  Cenário: O exemplo do subject é uma grade 25x20 em hexadecimal minúsculo
    Dado o labirinto de teste "exemplo do subject"
    Quando o validador da suíte lê o labirinto
    Então a grade do labirinto tem 25 colunas e 20 linhas
    E cada linha da grade casa com a expressão "^[0-9a-f]{25}$"

  # pdf: "Output file example"
  # md:  "1,1"
  # md:  "19,14"
  # md:  "ESEENEEESSSEESESSESESSSSEEEEEESES"
  # regua: "the 'ENTRY' tuple,"
  # regua-md: "a tupla `ENTRY`,"
  @informativo @derivado @decisao-D13 @automatizado @pdf-p11-L10 @pdf-p11-figura @md-L247-L249 @regua-p3
  Cenário: O exemplo do subject passa no validador da suíte
    Dado o labirinto de teste "exemplo do subject"
    Quando o validador da suíte lê o labirinto
    Então a linha 1 do rodapé é "1,1"
    E a linha 2 do rodapé é "19,14"
    E a linha 3 do rodapé é "ESEENEEESSSEESESSESESSSSEEEEEESES"
    E o validador da suíte confirma "paredes coerentes"
    E o validador da suíte confirma "borda fechada"
    E o validador da suíte confirma "sem área aberta 3x3"
    E o validador da suíte confirma "toda célula fora do 42 alcançável"
    E o validador da suíte conta 482 "células alcançáveis"
    E o validador da suíte conta 33 "letras da solução"
    E o validador da suíte confirma "solução válida e mais curta"
    E a linha "Verdict:" do maze_analyzer começa com "Pac-Man-USABLE"
    E a linha "Verdict:" do maze_analyzer contém "no real dead-end -> bonus-grade"

  # figura: "1,1        # entry  (x,y)"
  # md:  "1,1        # entry  (x,y)"
  # md:  "19,14      # exit   (x,y)"
  # regua: "the 'ENTRY' tuple,"
  # regua: "the 'EXIT' tuple,"
  # regua-md: "a tupla `ENTRY`,"
  # regua-md: "a tupla `EXIT`,"
  @informativo @derivado @decisao-D13 @automatizado @pdf-p11-figura @md-L247-L248 @regua-p3
  Cenário: As anotações do exemplo não fazem parte do arquivo
    Dado o labirinto de teste "exemplo do subject com o rodapé anotado"
    Quando eu analiso o labirinto com o maze_analyzer
    Então a saída contém "no valid entry in footer"
