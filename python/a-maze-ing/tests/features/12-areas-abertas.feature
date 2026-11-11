# language: pt
Funcionalidade: Sem grandes áreas abertas
  Corredores têm no máximo 2 células de largura: áreas abertas 2x3 e 3x2 são permitidas,
  3x3 nunca. Vale nos dois modos.

  # pdf: "The maze can't have large open areas. Corridors can't be wider than 2 cells."
  # pdf: "For example, you can have 2x3 or 3x2 open area, but never a 3x3 open area."
  # md:  "O labirinto não pode ter grandes áreas abertas. Corredores não podem ter mais de 2 células de largura. Por exemplo, você pode ter uma área aberta 2x3 ou 3x2, mas nunca uma área aberta 3x3."
  # regua: "There is no 3x3 or larger open zone without walls. Ask how this was implemented or verified in the code."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior. Pergunte como isso foi implementado ou verificado no código."
  @obrigatorio @automatizado @decisao-D11 @pdf-p09-L16-L17 @md-L187 @regua-p3
  Esquema do Cenário: O validador da suíte classifica áreas abertas
    Dado o labirinto de teste com a grade "<grade>", entrada "0,0" e saída "<saida>"
    Quando o validador da suíte lê o labirinto
    Então a grade do labirinto tem <largura> colunas e <altura> linhas
    E o validador da suíte relata "<resultado>" em "áreas abertas"

    Exemplos:
      | grade           | largura | altura | saida | resultado          |
      | 93 / c6         | 2       | 2      | 1,1   | aceito             |
      | 93 / 82 / c6    | 2       | 3      | 1,2   | aceito             |
      | 913 / c46       | 3       | 2      | 2,1   | aceito             |
      | 913 / 802 / c46 | 3       | 3      | 2,2   | recusado: área 3x3 |

  # pdf: "Corridors can't be wider than 2 cells."
  # md:  "Corredores não podem ter mais de 2 células de largura."
  # regua: "There is no 3x3 or larger open zone without walls. Ask how this was implemented or verified in the code."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior. Pergunte como isso foi implementado ou verificado no código."
  @obrigatorio @automatizado @decisao-D11 @decisao-I07 @pdf-p09-L16 @md-L187 @regua-p3
  Esquema do Cenário: Nenhum labirinto gerado tem área aberta 3x3
    Dado o config base com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>", "SEED=<seed>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto
    E o validador da suíte lê o labirinto
    Então o validador da suíte confirma "sem área aberta 3x3"

    Exemplos:
      | largura | altura | saida | seed | perfeito |
      | 20      | 15     | 19,14 | 1    | True     |
      | 20      | 15     | 19,14 | 1    | False    |
      | 40      | 30     | 39,29 | 2    | False    |
      | 9       | 9      | 8,8   | 3    | False    |
      | 21      | 14     | 20,13 | 4    | False    |

  # pdf: "The maze can't have large open areas."
  # md:  "O labirinto não pode ter grandes áreas abertas."
  # regua: "There is no 3x3 or larger open zone without walls."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior."
  @obrigatorio @automatizado @decisao-D11 @decisao-I07 @pdf-p09-L16 @md-L187 @regua-p3
  Cenário: A regra vale para muitas seeds no modo Pac-Man
    Dado o config base com "PERFECT=False"
    Quando eu gero o labirinto com cada seed de 1 a 100
    Então o validador da suíte confirma "sem área aberta 3x3"

  # pdf: "For example, you can have 2x3 or 3x2 open area, but never a 3x3 open area."
  # md:  "Por exemplo, você pode ter uma área aberta 2x3 ou 3x2, mas nunca uma área aberta 3x3."
  # regua: "There is no 3x3 or larger open zone without walls."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior."
  @opcional @automatizado @decisao-D11 @pdf-p09-L17 @md-L187 @regua-p3
  Cenário: Áreas 2x2, 2x3 e 3x2 abertas são permitidas no labirinto gerado
    Dado um labirinto gerado pelo programa com o config base mais "PERFECT=False"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "blocos 2x2, 2x3 e 3x2 abertos aceitos"

  # figura: "user@42:~/a_maze_ing$ cat output_maze.txt"
  # md:  "9139551111555515515395153"
  # md:  "c44556c6c555455546c446c46"
  # regua: "There is no 3x3 or larger open zone without walls."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior."
  @informativo @derivado @automatizado @decisao-D11 @pdf-p11-figura @md-L226-L245 @regua-p3
  Cenário: O exemplo do subject tem blocos 2x2 abertos e nenhum 3x3
    Dado o labirinto de teste "exemplo do subject"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte conta 35 "janelas 2x2 abertas"
    E o validador da suíte confirma "sem área aberta 3x3"
