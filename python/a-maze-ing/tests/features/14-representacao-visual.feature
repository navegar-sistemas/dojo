# language: pt
Funcionalidade: Representação visual
  O programa exibe o labirinto no terminal, só com caracteres ASCII e cores ANSI, mostrando
  paredes, entrada, saída, o "42" e o caminho da solução.

  # pdf: "file using a hexadecimal wall representation. You will also provide a visual representation"
  # pdf: "of the maze"
  # md:  "Você também fornecerá uma representação visual do labirinto"
  @obrigatorio @automatizado @decisao-I01 @decisao-I03 @pdf-p08-L06-L07 @md-L142
  Cenário: O programa fornece uma representação visual do labirinto
    Dado o config base
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então a renderização confirma "cada renderização seguida do menu"

  # pdf: "Your program must provide a way to display the maze visually, using either:"
  # md:  "Seu programa deve oferecer uma forma de exibir o labirinto visualmente, usando:"
  # regua: "You should get a maze randomly generated, displayed on the terminal or using a dedicated graphic window, and a way to interact with the program."
  # regua-md: "Você deve obter um labirinto gerado aleatoriamente, exibido no terminal ou numa janela gráfica dedicada, e uma forma de interagir com o programa."
  @obrigatorio @automatizado @decisao-I02 @pdf-p12-L03 @md-L256 @regua-p2
  Cenário: Existe uma forma de exibir o labirinto
    Dado o config base
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então a renderização confirma "2 × HEIGHT + 1 linhas"
    E a renderização confirma "2 × WIDTH + 1 posições de 2 caracteres por linha"

  # pdf: "Terminal ASCII rendering, or"
  # pdf: "A graphical display using the MiniLibX (MLX) library."
  # md:  "Renderização ASCII no terminal, ou"
  # md:  "Uma exibição gráfica usando a biblioteca MiniLibX (MLX)."
  @obrigatorio @decisao-D18 @automatizado @decisao-I01 @decisao-I02 @pdf-p12-L04-L05 @md-L258-L259
  Cenário: A exibição é uma renderização ASCII no terminal
    Dado o config base
    E o código-fonte de "."
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    E a análise estática percorre o código-fonte
    Então a renderização confirma "só caracteres ASCII"
    E a renderização confirma "cores por sequências ANSI de fundo"
    E a análise estática confirma "sem MiniLibX"

  # pdf: "The visual should clearly show walls, entry, exit, and the solution path."
  # md:  "O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução."
  @recomendado @automatizado @decisao-I02 @pdf-p12-L06 @md-L261
  Esquema do Cenário: A renderização mostra cada parede fechada
    Dado o config base
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então na última renderização, as células de dígito "<digito>" mostram exatamente as paredes "<paredes>"

    Exemplos:
      | digito | paredes                   |
      | f      | Norte, Leste, Sul e Oeste |
      | 5      | Norte e Sul               |
      | a      | Leste e Oeste             |
      | 3      | Norte e Leste             |

  # pdf: "The visual should clearly show walls, entry, exit, and the solution path."
  # md:  "O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução."
  @recomendado @automatizado @decisao-D13 @decisao-I02 @decisao-I21 @pdf-p12-L06 @md-L261
  Esquema do Cenário: Entrada e saída aparecem destacadas
    Dado o config base
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então a linha <linha> do rodapé é "<celula>"
    E a renderização confirma "entrada e saída iguais às do rodapé"
    E na última renderização, as posições de "<papel>" têm a cor "<cor>"
    E na última renderização, a cor "<cor>" só aparece em "<papel>"

    Exemplos:
      | celula | papel   | linha | cor      |
      | 0,0    | entrada | 1     | magenta  |
      | 19,14  | saída   | 2     | vermelho |

  # pdf: "The visual should clearly show walls, entry, exit, and the solution path."
  # md:  "O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução."
  @recomendado @automatizado @decisao-I02 @decisao-I03 @decisao-I21 @pdf-p12-L06 @md-L261
  Cenário: O caminho da solução aparece quando visível
    Dado o config base
    E o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "2"
    Então a renderização confirma "caminho do arquivo marcado em ciano"
    E na última renderização, as posições de "células do caminho" têm a cor "ciano"
    E na última renderização, as posições de "passagens do caminho" têm a cor "ciano"
    E na última renderização, as posições de "entrada" têm a cor "magenta"
    E na última renderização, as posições de "saída" têm a cor "vermelho"

  # pdf: "The visual should clearly show walls, entry, exit, and the solution path."
  # md:  "O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução."
  @recomendado @manual @decisao-I02 @pdf-p12-L06 @md-L261
  Cenário: Paredes, entrada, saída e caminho são distinguíveis à primeira vista
    - Dado o labirinto exibido com o caminho visível
    - Quando uma pessoa que não conhece o projeto olha a tela
    - Então ela aponta as paredes, a entrada, a saída e o caminho sem explicação

  # pdf: "The shortest path is highlighted in both."
  # md:  "O caminho mais curto está destacado em ambos."
  @informativo @derivado @automatizado @decisao-I02 @decisao-I03 @decisao-I21 @pdf-p10-L04 @md-L200
  Esquema do Cenário: O caminho mais curto pode ser destacado nos dois modos
    Dado o config base com "PERFECT=<perfeito>"
    E o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "2"
    Então na última renderização, as posições de "células do caminho" têm a cor "ciano"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # figura: legenda "entry", "exit", ""42" pattern", "shortest path"
  # md:  "Legenda: entrada, saída, padrão "42", caminho mais curto."
  @informativo @derivado @automatizado @decisao-I02 @decisao-I03 @decisao-I04 @pdf-p10-figura @md-L198
  Cenário: Entrada, saída, "42" e caminho têm cores distintas
    Dado o config base
    E o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "2"
    Então a renderização confirma "cinco cores distintas para entrada, saída, 42, caminho e paredes"

  # pdf: "When visually represented (see below), the maze must contain a visible "42" drawn"
  # pdf: "by several fully closed cells."
  # md:  "Quando representado visualmente (veja abaixo), o labirinto deve conter um "42" visível, desenhado por várias células totalmente fechadas."
  @obrigatorio @automatizado @decisao-D07 @decisao-I02 @decisao-I21 @pdf-p09-L18-L19 @md-L188
  Esquema do Cenário: As células do "42" aparecem na cor do "42"
    Dado o config base com "PERFECT=<perfeito>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então na última renderização, as posições de "células do 42" têm a cor "cinza"
    E na última renderização, a cor "cinza" só aparece em "células do 42"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "Terminal default rendering of the maze"
  # md:  "Figura: Renderização padrão do labirinto no terminal."
  @informativo @manual @pdf-p13-L02 @pdf-p13-figura @md-L272
  Cenário: A figura da renderização padrão no terminal
    - Dada a figura "Terminal default rendering of the maze"
    - Quando eu comparo com o meu programa logo após "python3 ./a_maze_ing.py config.txt"
    - Então os dois mostram paredes em blocos de cor, entrada, saída e o "42" em cor fixa diferente da das paredes
    - E o menu de interação aparece abaixo do labirinto

  # pdf: "Different maze, shortest path and wall colours"
  # md:  "Figura: Labirinto diferente, caminho mais curto e cores de parede alteradas."
  @informativo @manual @pdf-p13-L03 @pdf-p13-figura @md-L274
  Cenário: A figura após as interações
    - Dada a figura "Different maze, shortest path and wall colours"
    - Quando eu regenero, mostro o caminho e troco a cor das paredes no meu programa
    - Então o resultado mostra outro labirinto, o caminho mais curto e paredes de outra cor

  # pdf: "Maze rendering using Mlx"
  # md:  "Figura: Renderização do labirinto usando Mlx."
  @informativo @manual @decisao-I01 @pdf-p14-L02 @pdf-p14-figura @md-L276
  Cenário: A figura da renderização com a MiniLibX
    - Dada a figura "Maze rendering using Mlx"
    - Quando a exibição gráfica é a escolhida
    - Então a janela mostra paredes, entrada, saída, caminho, o "42" preenchido
    - E uma barra com os atalhos "1: regen", "2: path", "3: color" e "4: quit"

  # pdf: "The visual should clearly show walls, entry, exit, and the solution path."
  # pdf: "It must never crash unexpectedly, and must"
  # md:  "O visual deve mostrar claramente as paredes, a entrada, a saída e o caminho da solução."
  # md:  "Ele nunca deve travar inesperadamente"
  @obrigatorio @derivado @decisao-D17 @automatizado @pdf-p12-L06 @pdf-p08-L15 @md-L261 @md-L155
  Cenário: A renderização não trava sem terminal interativo
    Dado o config base
    Quando eu executo "python3 a_maze_ing.py cfg.txt < /dev/null > /dev/null"
    Então a saída de erro não contém "Traceback"
    E o código de saída é 0
