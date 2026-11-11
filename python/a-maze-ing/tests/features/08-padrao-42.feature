# language: pt
Funcionalidade: Padrão "42"
  O labirinto contém um "42" visível desenhado por células totalmente fechadas (valor F).
  Em grade pequena demais, o "42" é omitido e uma mensagem de erro aparece no console.

  # pdf: "When visually represented (see below), the maze must contain a visible "42" drawn"
  # md:  "Quando representado visualmente (veja abaixo), o labirinto deve conter um "42" visível"
  @obrigatorio @manual @pdf-p09-L18 @md-L188
  Esquema do Cenário: O "42" é visível na representação visual
    Dado o config base com "PERFECT=<perfeito>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então eu leio "42" no labirinto exibido sem precisar procurar

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "by several fully closed cells."
  # md:  "desenhado por várias células totalmente fechadas."
  @obrigatorio @automatizado @decisao-D07 @pdf-p09-L18-L19 @md-L188
  Esquema do Cenário: O "42" é desenhado por várias células totalmente fechadas
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "células F em dois componentes 4-conexos"
    E o validador da suíte confirma "componente da esquerda com a forma do 4"
    E o validador da suíte confirma "componente da direita com a forma do 2"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "The structure ensures full connectivity and no isolated cells (except the '42'"
  # pdf: "pattern, see below)."
  # md:  "A estrutura garante conectividade total e nenhuma célula isolada (exceto o padrão "42", veja abaixo)."
  @obrigatorio @automatizado @decisao-D07 @pdf-p09-L10-L11 @md-L184
  Cenário: As células totalmente fechadas são exatamente as do "42"
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "células F iguais ao padrão 42"
    E o validador da suíte confirma "nenhuma célula F fora do padrão"

  # pdf: "pattern, see below)."
  # md:  "nenhuma célula isolada (exceto o padrão "42", veja abaixo)."
  @obrigatorio @automatizado @pdf-p09-L10-L11 @md-L184
  Cenário: As células do "42" ficam isoladas do resto do labirinto
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "42 sem passagem aberta"

  # figura: "user@42:~/a_maze_ing$ cat output_maze.txt"
  # md:  "a951292c2f816fffaac296852"
  # md:  "8416c2852fc4157f829285452"
  # md:  "81453ac56fffafff86aa8153a"
  # md:  "84112813913fafd503c2ac102"
  # md:  "812a82ac6c2fafffac54692aa"
  @informativo @derivado @automatizado @pdf-p11-figura @md-L233-L237
  Cenário: O exemplo do subject é a referência de forma do "42"
    Dado o labirinto de teste "exemplo do subject"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte conta 18 "células de valor F"
    E as células de valor F ocupam as colunas "9 a 11 e 13 a 15" e as linhas "7 a 11"
    E o validador da suíte confirma "glifos 3x5 com uma coluna livre entre os dígitos"

  # pdf: "The "42" pattern may be omitted in case the maze size does not allow"
  # pdf: "it (i.e. too small)."
  # md:  "O padrão "42" pode ser omitido caso o tamanho do labirinto não permita (ou seja, pequeno demais)."
  # regua: "There is the '42' pattern in the maze (except is size does not allow it, then you should have a message on the terminal)."
  # regua-md: "Há o padrão "42" no labirinto (exceto se o tamanho não permitir; nesse caso deve haver uma mensagem no terminal)."
  @opcional @automatizado @decisao-D06 @pdf-p09-L33-L34 @md-L196 @regua-p3
  Esquema do Cenário: Em grade pequena demais o "42" é omitido
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto
    Então o código de saída é 0
    E o validador da suíte conta 0 "células de valor F"
    E o validador da suíte confirma "labirinto válido conforme o config"

    Exemplos:
      | largura | altura | saida | perfeito |
      | 5       | 5      | 4,4   | True     |
      | 6       | 4      | 5,3   | True     |
      | 3       | 20     | 2,19  | True     |
      | 6       | 6      | 5,5   | False    |

  # pdf: "Print an error message on the console in that"
  # pdf: "case."
  # md:  "Nesse caso, imprima uma mensagem de erro no console."
  # regua: "There is the '42' pattern in the maze (except is size does not allow it, then you should have a message on the terminal)."
  # regua-md: "Há o padrão "42" no labirinto (exceto se o tamanho não permitir; nesse caso deve haver uma mensagem no terminal)."
  @obrigatorio @automatizado @decisao-D06 @decisao-I10 @pdf-p09-L34-L35 @md-L196 @regua-p3
  Cenário: Omitir o "42" imprime uma mensagem de erro no console
    Dado o config base com "WIDTH=5", "HEIGHT=5" e "EXIT=4,4"
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então a saída de erro contém "Error: maze too small for the \"42\" pattern"
    E o código de saída é 0

  # pdf: "The "42" pattern may be omitted in case the maze size does not allow"
  # md:  "O padrão "42" pode ser omitido caso o tamanho do labirinto não permita"
  # regua: "There is the '42' pattern in the maze (except is size does not allow it, then you should have a message on the terminal)."
  # regua-md: "Há o padrão "42" no labirinto (exceto se o tamanho não permitir; nesse caso deve haver uma mensagem no terminal)."
  @obrigatorio @derivado @decisao-D06 @decisao-D07 @automatizado @pdf-p09-L33-L34 @md-L196 @regua-p3
  Esquema do Cenário: O "42" aparece a partir de 9 colunas por 7 linhas
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então o validador da suíte confirma "42 <presenca>"
    E o veredito do maze_analyzer.py corresponde ao PERFECT do config

    Exemplos:
      | largura | altura | saida | perfeito | presenca |
      | 9       | 7      | 8,6   | True     | presente |
      | 9       | 7      | 8,6   | False    | presente |
      | 8       | 7      | 7,6   | True     | ausente  |
      | 8       | 7      | 7,6   | False    | ausente  |
      | 9       | 6      | 8,5   | True     | ausente  |
      | 9       | 6      | 8,5   | False    | ausente  |

  # pdf: "When visually represented (see below), the maze must contain a visible "42" drawn"
  # pdf: "by several fully closed cells."
  # md:  "Quando representado visualmente (veja abaixo), o labirinto deve conter um "42" visível, desenhado por várias células totalmente fechadas."
  @obrigatorio @derivado @decisao-D07 @automatizado @pdf-p09-L18-L19 @md-L188
  Esquema do Cenário: O "42" fica centralizado, com uma coluna livre entre os dígitos
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então as células de valor F ocupam as colunas "<colunas>" e as linhas "<linhas>"
    E o validador da suíte confirma "glifos 3x5 com uma coluna livre entre os dígitos"
    E o validador da suíte confirma "42 com margem de corredor"

    Exemplos:
      | largura | altura | saida | colunas          | linhas |
      | 9       | 7      | 8,6   | 1 a 3 e 5 a 7    | 1 a 5  |
      | 20      | 15     | 19,14 | 6 a 8 e 10 a 12  | 5 a 9  |
      | 21      | 15     | 20,14 | 7 a 9 e 11 a 13  | 5 a 9  |
      | 25      | 20     | 19,14 | 9 a 11 e 13 a 15 | 7 a 11 |

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # pdf: "The structure ensures full connectivity and no isolated cells (except the '42'"
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  # md:  "A estrutura garante conectividade total e nenhuma célula isolada (exceto o padrão "42", veja abaixo)."
  @obrigatorio @derivado @decisao-D01 @decisao-D05 @automatizado @decisao-I21 @pdf-p09-L09-L10 @md-L183-L184
  Esquema do Cenário: ENTRY ou EXIT sobre uma célula do "42" gera erro
    Dado o config base com "<chave>=<coordenada>"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "<chave>"
    E a mensagem de erro explica "coordenada no padrão 42"
    E o código de saída é 1

    Exemplos:
      | chave | coordenada |
      | ENTRY | 6,5        |
      | ENTRY | 8,7        |
      | EXIT  | 12,9       |
      | EXIT  | 10,5       |

  # pdf: "the four corners and the centre are open corridors (the ghosts and super-pac-"
  # pdf: "When visually represented (see below), the maze must contain a visible "42" drawn"
  # md:  "os quatro cantos e o centro são corredores abertos (os fantasmas e as super-pac-gums ficam nos cantos; o jogador começa no centro);"
  # md:  "Quando representado visualmente (veja abaixo), o labirinto deve conter um "42" visível"
  # regua: "the 4 corners and the centre are open corridors"
  # regua-md: "os 4 cantos e o centro são corredores abertos"
  @obrigatorio @derivado @decisao-D08 @automatizado @pdf-p09-L26-L27 @pdf-p09-L18 @md-L192 @md-L188 @regua-p3
  Esquema do Cenário: No modo Pac-Man o "42" não ocupa cantos nem centro
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "PERFECT=False"
    Quando eu gero o labirinto
    Então o validador da suíte confirma "42 fora dos cantos"
    E o validador da suíte confirma "centro livre do 42"

    Exemplos:
      | largura | altura | saida |
      | 20      | 15     | 19,14 |
      | 21      | 15     | 20,14 |
      | 20      | 14     | 19,13 |
      | 21      | 16     | 20,15 |

  # figura: "PERFECT = True" / "PERFECT = False (default)"
  # md:  "À esquerda, `PERFECT = True` (um único caminho · labirinto acadêmico / de laboratório); à direita, `PERFECT = False (default)`"
  @informativo @derivado @decisao-D07 @automatizado @pdf-p10-figura @md-L198
  Cenário: O "42" fica na mesma posição nos dois modos
    Dado o config base
    Quando eu gero o labirinto com cada um de "PERFECT=True" e "PERFECT=False"
    Então os resultados são idênticos em "células de valor F"
