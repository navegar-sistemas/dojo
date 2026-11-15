# language: pt
Funcionalidade: Geração aleatória reproduzível por seed
  O labirinto é gerado aleatoriamente por uma classe geradora num módulo independente;
  a mesma seed produz o mesmo labirinto; toda célula fora do "42" é alcançável.

  # pdf: "a maze, possibly perfect (with a single path between entrance and exit), and writes it to a"
  # pdf: "You may use it to check that your generator produces the mode requested by"
  # pdf: "the configuration file."
  # md:  "gera um labirinto — possivelmente perfeito (com um único caminho entre entrada e saída) — e o escreve em um arquivo"
  # md:  "Você pode usá-lo para verificar se o seu gerador produz o modo solicitado pelo arquivo de configuração."
  # regua: "Run the provided analysis script "python3 maze_analyzer.py <output_file>": it controls the walls coherence and reports whether the maze matches the mode set in the configuration file (perfect single-path vs. playable board). Any incoherence or mismatch marks this question as failed."
  # regua-md: "Execute o script de análise fornecido: `python3 maze_analyzer.py <output_file>`; ele controla a coerência das paredes e informa se o labirinto corresponde ao modo definido no arquivo de configuração (perfeito de caminho único vs. tabuleiro jogável). Qualquer incoerência ou divergência marca esta questão como reprovada."
  @obrigatorio @automatizado @decisao-I05 @decisao-I06 @pdf-p08-L04-L05 @pdf-p11-L08-L09 @md-L142 @md-L220 @regua-p3
  Esquema do Cenário: O programa gera um labirinto, perfeito ou não, conforme o config
    Dado o config base com "PERFECT=<perfeito>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então a linha "Verdict:" do maze_analyzer começa com "<veredito>"

    Exemplos:
      | perfeito | veredito       |
      | True     | PERFECT maze   |
      | False    | Pac-Man-USABLE |

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  # regua: "A randomly generated maze, eventually using a suitable standard module of Python (e.g., the module 'random')."
  # regua-md: "Um labirinto gerado aleatoriamente, eventualmente usando um módulo padrão adequado do Python (ex.: o módulo `random`)."
  @obrigatorio @automatizado @decisao-D02 @pdf-p09-L05 @md-L180 @regua-p3
  Cenário: Sem seed, cada execução gera um labirinto diferente
    Dado o config base
    E o config sem a chave "SEED"
    Quando eu gero o labirinto 5 vezes
    Então os resultados são diferentes entre si em "grade"

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  # regua: "The same maze is replicable when using an identical seed (update the configuration file or the code to verify)."
  # regua-md: "O mesmo labirinto é replicável quando se usa um seed idêntico (atualize o arquivo de configuração ou o código para verificar)."
  @obrigatorio @automatizado @decisao-D02 @pdf-p09-L05 @md-L180 @regua-p3
  Esquema do Cenário: A mesma seed reproduz o mesmo labirinto
    Dado o config base com "SEED=<seed>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto 2 vezes
    Então os resultados são idênticos em "arquivo de saída"

    Exemplos:
      | seed       | perfeito |
      | 0          | True     |
      | 42         | True     |
      | 42         | False    |
      | 2147483647 | False    |

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  @obrigatorio @derivado @decisao-D02 @automatizado @pdf-p09-L05 @md-L180
  Cenário: Seeds diferentes geram labirintos diferentes
    Dado o config base
    Quando eu gero o labirinto com cada um de "SEED=1" e "SEED=2"
    Então os resultados são diferentes entre si em "grade"

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  @obrigatorio @derivado @decisao-D02 @automatizado @decisao-I09 @pdf-p09-L05 @md-L180
  Cenário: A reprodutibilidade vale também pela classe geradora
    Dado o gerador "MazeGenerator(width=20, height=15, seed=42)"
    Quando eu gero o labirinto com 2 instâncias novas do gerador
    Então os resultados são idênticos em "grade"
    E os resultados são idênticos em "solução"

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  @obrigatorio @derivado @decisao-D01 @decisao-D02 @automatizado @pdf-p09-L05 @md-L180
  Esquema do Cenário: SEED inválida gera erro
    Dado o config base com "SEED=<valor>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "SEED"
    E o código de saída é 1

    Exemplos:
      | valor |
      |       |
      | abc   |
      | 4.2   |

  # pdf: "The structure ensures full connectivity and no isolated cells (except the '42'"
  # md:  "A estrutura garante conectividade total e nenhuma célula isolada (exceto o padrão "42", veja abaixo)."
  # regua: "All cells can be reached, except, eventually, those creating the '42' pattern."
  # regua-md: "Todas as células podem ser alcançadas, exceto, eventualmente, as que formam o padrão "42"."
  @obrigatorio @automatizado @pdf-p09-L10 @md-L184 @regua-p3
  Esquema do Cenário: Conectividade total a partir da entrada
    Dado um labirinto gerado pelo programa com o config base mais "SEED=<seed>" e "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "toda célula fora do 42 alcançável"
    E a linha "Reachable region" do maze_analyzer contém "(0 corridor(s) unreachable)"

    Exemplos:
      | seed | perfeito |
      | 7    | True     |
      | 7    | False    |
      | 99   | True     |
      | 99   | False    |

  # pdf: "The structure ensures full connectivity and no isolated cells (except the '42'"
  # pdf: "pattern, see below)."
  # md:  "A estrutura garante conectividade total e nenhuma célula isolada (exceto o padrão "42", veja abaixo)."
  @obrigatorio @automatizado @pdf-p09-L10-L11 @md-L184
  Cenário: As únicas células não alcançáveis são as do "42"
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "inalcançáveis são as células do 42"

  # pdf: "You must implement the maze generation as a unique class (e.g., 'MazeGenerator') inside"
  # pdf: "a standalone module that can be imported in a future project."
  # md:  "Você deve implementar a geração do labirinto como uma classe única (ex.: `MazeGenerator`) dentro de um módulo independente que possa ser importado em um projeto futuro."
  @obrigatorio @automatizado @decisao-D19 @decisao-I09 @decisao-I11 @pdf-p15-L03-L04 @md-L282
  Cenário: A geração é implementada por uma classe única num módulo independente
    Dado o arquivo "mazegen/__init__.py" na raiz do repositório
    Quando eu executo "python3 -c 'from mazegen import MazeGenerator'"
    Então o código de saída é 0
    E o módulo mazegen confirma "uma única classe pública de geração"

  # pdf: "a standalone module that can be imported in a future project."
  # md:  "dentro de um módulo independente que possa ser importado em um projeto futuro."
  @obrigatorio @automatizado @decisao-I11 @pdf-p15-L04 @md-L282
  Cenário: O módulo gerador não depende do programa principal
    Dado o código-fonte de "mazegen"
    Quando a análise estática percorre o código-fonte
    Então a análise estática confirma "mazegen só importa a biblioteca padrão"

  # pdf: "of the maze and organize your code so that the generation logic can be reused later."
  # md:  "organizará seu código de forma que a lógica de geração possa ser reutilizada depois."
  @obrigatorio @automatizado @decisao-I09 @pdf-p08-L07 @md-L142
  Cenário: A lógica de geração fica separada do programa
    Dado o gerador "MazeGenerator(width=20, height=15, seed=42)"
    Quando o gerador gera o labirinto
    Então o módulo mazegen confirma "grid e solution preenchidos após generate"

  # pdf: "of the maze and organize your code so that the generation logic can be reused later."
  # md:  "organizará seu código de forma que a lógica de geração possa ser reutilizada depois."
  @obrigatorio @derivado @manual @decisao-I11 @pdf-p08-L07 @md-L142
  Cenário: O programa principal usa o módulo reutilizável
    - Dado "a_maze_ing.py" e o código do programa
    - Quando eu procuro o código que gera o labirinto
    - Então o programa gera o labirinto pela classe do módulo reutilizável
    - E não existe uma segunda implementação da geração fora do módulo

  # pdf: "Your program must handle all errors gracefully: invalid configuration, file not found, bad"
  # pdf: "syntax, impossible maze parameters, etc."
  # md:  "Seu programa deve tratar todos os erros de forma elegante: configuração inválida, arquivo não encontrado, sintaxe incorreta, parâmetros de labirinto impossíveis etc."
  # regua: "Adopt a relevant behaviour in case some parameters may be inconsistent (e.g., the entry or exit cells are outside the maze, width or height is negative, ...)."
  # regua-md: "Adota um comportamento adequado caso alguns parâmetros sejam inconsistentes (ex.: células de entrada ou saída fora do labirinto, largura ou altura negativas, ...)."
  @obrigatorio @automatizado @decisao-D05 @decisao-I09 @decisao-I21 @pdf-p08-L14-L15 @md-L155 @regua-p3
  Esquema do Cenário: A classe geradora recusa parâmetros inconsistentes
    Quando eu tento criar o gerador "<expressao>"
    Então o construtor levanta "MazeError"
    E a mensagem da exceção cita "<citado>"
    E o módulo mazegen confirma "só MazeError escapa do construtor"

    Exemplos:
      | expressao                                                     | citado  |
      | MazeGenerator(width=-5, height=15)                            | width   |
      | MazeGenerator(width=20, height=-1)                            | height  |
      | MazeGenerator(width=0, height=0)                              | width   |
      | MazeGenerator(width=20, height=15, entry=(20, 0))             | entry   |
      | MazeGenerator(width=20, height=15, exit=(19, 15))             | exit    |
      | MazeGenerator(width=20, height=15, entry=(-1, 0))             | entry   |
      | MazeGenerator(width=20, height=15, entry=(5, 5), exit=(5, 5)) | entry   |
      | MazeGenerator(width=20, height=15, entry=(5, 5), exit=(5, 5)) | exit    |
      | MazeGenerator(width=20, height=15, entry=(6, 5))              | entry   |
      | MazeGenerator(width=2, height=2, perfect=False)               | perfect |
      | MazeGenerator(width=101, height=15)                           | width   |
      | MazeGenerator(width=20, height=1000000)                       | height  |
      | MazeGenerator(width='20', height=15)                          | width   |
      | MazeGenerator(width=2.5, height=15)                           | width   |
      | MazeGenerator(width=True, height=15)                          | width   |
      | MazeGenerator(width=20, height=15, entry=(0,))                | entry   |
      | MazeGenerator(width=20, height=15, exit=[19, 14])             | exit    |
      | MazeGenerator(width=20, height=15, perfect='no')              | perfect |
      | MazeGenerator(width=20, height=15, seed='x')                  | seed    |
