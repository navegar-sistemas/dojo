# language: pt
Funcionalidade: Grade, paredes e validade estrutural
  Cada célula tem até quatro paredes; entrada e saída existem dentro da grade; a borda externa
  é fechada; vizinhas codificam a parede compartilhada do mesmo jeito.

  # pdf: "Each cell of the maze has between 0 and 4 walls, at each cardinal point (North,"
  # pdf: "East, South, West)."
  # md:  "Cada célula do labirinto tem entre 0 e 4 paredes, uma em cada ponto cardeal (Norte, Leste, Sul, Oeste)."
  @obrigatorio @automatizado @pdf-p09-L06-L07 @md-L181
  Esquema do Cenário: Cada célula tem de 0 a 4 paredes, uma por ponto cardeal
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "valores de 0 a 15"
    E o validador da suíte confirma "bits na convenção N=1, E=2, S=4, W=8"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "Each cell of the maze has between 0 and 4 walls, at each cardinal point (North,"
  # md:  "Cada célula do labirinto tem entre 0 e 4 paredes, uma em cada ponto cardeal"
  @obrigatorio @derivado @automatizado @pdf-p09-L06 @md-L181
  Esquema do Cenário: O validador aceita qualquer quantidade de paredes de 0 a 4
    Dada a célula de dígito "<valor>"
    Quando o validador da suíte converte a célula
    Então a célula tem <paredes> paredes fechadas
    E as paredes fechadas da célula são "<fechadas>"

    Exemplos:
      | valor | paredes | fechadas                  |
      | 0     | 0       | nenhuma                   |
      | 1     | 1       | Norte                     |
      | 3     | 2       | Norte e Leste             |
      | 7     | 3       | Norte, Leste e Sul        |
      | F     | 4       | Norte, Leste, Sul e Oeste |

  # pdf: "The maze must be valid, meaning:"
  # md:  "O labirinto deve ser válido, ou seja:"
  @obrigatorio @automatizado @pdf-p09-L08 @md-L182
  Esquema do Cenário: Todo labirinto gerado é válido
    Dado um labirinto gerado pelo programa com o config base mais "SEED=<seed>" e "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "entrada e saída válidas"
    E o validador da suíte confirma "toda célula fora do 42 alcançável"
    E o validador da suíte confirma "borda fechada"
    E o validador da suíte confirma "paredes coerentes"

    Exemplos:
      | seed | perfeito |
      | 1    | True     |
      | 2    | True     |
      | 3    | False    |
      | 4    | False    |

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  @obrigatorio @automatizado @decisao-D13 @pdf-p09-L09 @md-L183
  Cenário: A entrada existe no labirinto gerado
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então a linha 1 do rodapé é "0,0"
    E a célula "0,0" não tem valor F

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  @obrigatorio @automatizado @decisao-D13 @pdf-p09-L09 @md-L183
  Cenário: A saída existe no labirinto gerado
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então a linha 2 do rodapé é "19,14"
    E a célula "19,14" não tem valor F

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  @obrigatorio @automatizado @pdf-p09-L09 @md-L183
  Cenário: Entrada e saída são células diferentes
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "entrada diferente da saída"

  # pdf: "Entry and exit exist and are different, inside the maze bounds."
  # md:  "Entrada e saída existem, são diferentes e estão dentro dos limites do labirinto."
  @obrigatorio @automatizado @pdf-p09-L09 @md-L183
  Cenário: Entrada e saída estão dentro dos limites
    Dado um labirinto gerado pelo programa com o config base
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "x de entrada e saída dentro da largura"
    E o validador da suíte confirma "y de entrada e saída dentro da altura"

  # pdf: "As entry and exit are specific cells, there must be walls at the external borders."
  # md:  "Como entrada e saída são células específicas, deve haver paredes nas bordas externas."
  # regua: "Have walls all around the maze."
  # regua-md: "Há paredes em toda a volta do labirinto."
  @obrigatorio @automatizado @decisao-D12 @pdf-p09-L12 @md-L185 @regua-p3
  Esquema do Cenário: A borda externa é toda fechada
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então todas as células da "<borda>" têm a parede "<direcao>" fechada

    Exemplos:
      | perfeito | borda           | direcao |
      | True     | primeira linha  | Norte   |
      | True     | última coluna   | Leste   |
      | True     | última linha    | Sul     |
      | True     | primeira coluna | Oeste   |
      | False    | primeira linha  | Norte   |
      | False    | última coluna   | Leste   |
      | False    | última linha    | Sul     |
      | False    | primeira coluna | Oeste   |

  # pdf: "As entry and exit are specific cells, there must be walls at the external borders."
  # md:  "Como entrada e saída são células específicas, deve haver paredes nas bordas externas."
  # regua: "Have walls all around the maze."
  # regua-md: "Há paredes em toda a volta do labirinto."
  @obrigatorio @automatizado @decisao-D12 @pdf-p09-L12 @md-L185 @regua-p3
  Esquema do Cenário: Entrada e saída na borda não abrem a parede externa
    Dado o config base com "ENTRY=<entrada>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então a célula "<entrada>" tem as paredes externas fechadas
    E a célula "<saida>" tem as paredes externas fechadas

    Exemplos:
      | entrada | saida |
      | 0,0     | 19,14 |
      | 10,0    | 10,14 |
      | 0,7     | 19,7  |

  # pdf: "Your generated data must be coherent: each neighbouring cell must have the"
  # pdf: "same wall if any."
  # md:  "Os dados gerados devem ser coerentes: células vizinhas devem compartilhar a mesma parede, se houver."
  @obrigatorio @automatizado @pdf-p09-L13-L14 @md-L186
  Esquema do Cenário: Vizinhas horizontais codificam a mesma parede
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "vizinhas leste-oeste coerentes"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "Your generated data must be coherent: each neighbouring cell must have the"
  # pdf: "same wall if any."
  # md:  "Os dados gerados devem ser coerentes: células vizinhas devem compartilhar a mesma parede, se houver."
  @obrigatorio @derivado @automatizado @pdf-p09-L13-L14 @md-L186
  Esquema do Cenário: Vizinhas verticais codificam a mesma parede
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "vizinhas norte-sul coerentes"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "E.g., it is forbidden to have a first cell with a wall on the"
  # pdf: "east side, and the second cell behind that wall without a wall on the west side."
  # md:  "Ex.: é proibido ter uma primeira célula com parede do lado leste e a célula seguinte, atrás dessa parede, sem parede do lado oeste."
  @obrigatorio @automatizado @pdf-p09-L14-L15 @md-L186
  Esquema do Cenário: O validador distingue paredes coerentes de incoerentes
    Dado o labirinto de teste com a grade "<grade>", entrada "0,0" e saída "<saida>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte relata "<resultado>" em "coerência das paredes"
    E a linha "Wall coherence" do maze_analyzer contém "<analyzer>"

    Exemplos:
      | grade | saida | resultado                      | analyzer                                |
      | F7    | 1,0   | incoerente entre (0,0) e (1,0) | 2 mismatching cell(s) -> (0, 0), (1, 0) |
      | D7    | 1,0   | coerente                       | OK (all shared walls match)             |
      | F / E | 0,1   | incoerente entre (0,0) e (0,1) | 2 mismatching cell(s) -> (0, 0), (0, 1) |
      | B / E | 0,1   | coerente                       | OK (all shared walls match)             |

  # pdf: "Your generated data must be coherent: each neighbouring cell must have the"
  # md:  "Os dados gerados devem ser coerentes: células vizinhas devem compartilhar a mesma parede, se houver."
  @obrigatorio @automatizado @pdf-p09-L13 @md-L186
  Cenário: O maze_analyzer.py confirma a coerência do labirinto gerado
    Dado um labirinto gerado pelo programa com o config base
    Quando eu analiso o labirinto com o maze_analyzer
    Então a linha "Wall coherence" do maze_analyzer contém "OK (all shared walls match)"
