# language: pt
Funcionalidade: Caminho mais curto
  O gerador calcula um caminho válido mais curto da entrada até a saída, escrito com as
  letras N, E, S e W, e o expõe pela API.

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # pdf: "entry to exit, using the four letters N , E , S , W ."
  # md:  "o caminho válido mais curto da entrada até a saída, usando as quatro letras `N`, `E`, `S`, `W`."
  @obrigatorio @automatizado @decisao-I08 @pdf-p10-L19-L20 @md-L217
  Esquema do Cenário: O caminho usa só as letras N, E, S e W
    Dado um labirinto gerado pelo módulo mazegen com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então a solução casa com a expressão "^[NESW]+$"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "o caminho válido mais curto da entrada até a saída"
  @obrigatorio @automatizado @decisao-I08 @pdf-p10-L19 @md-L217
  Esquema do Cenário: O caminho é válido passo a passo
    Dado um labirinto gerado pelo módulo mazegen com o config base mais "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "solução atravessa só paredes abertas"
    E o validador da suíte confirma "solução não sai da grade"
    E o validador da suíte confirma "solução não entra no 42"
    E o validador da suíte confirma "solução termina na saída"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "o caminho válido mais curto da entrada até a saída"
  @obrigatorio @automatizado @decisao-D15 @decisao-I08 @pdf-p10-L19 @md-L217
  Esquema do Cenário: O caminho tem o comprimento mínimo
    Dado um labirinto gerado pelo módulo mazegen com o config base mais "SEED=<seed>" e "PERFECT=<perfeito>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte confirma "solução mais curta"
    E o validador da suíte confirma "solução sem célula repetida"

    Exemplos:
      | seed | perfeito |
      | 1    | True     |
      | 2    | True     |
      | 1    | False    |
      | 2    | False    |
      | 3    | False    |

  # pdf: "the entry coordinates, the exit coordinates, and the shortest valid path from"
  # md:  "o caminho válido mais curto da entrada até a saída"
  @obrigatorio @derivado @automatizado @decisao-I08 @pdf-p10-L19 @md-L217
  Esquema do Cenário: Entrada e saída em posições variadas
    Dado o config base com "ENTRY=<entrada>", "EXIT=<saida>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto
    Então o validador da suíte confirma "solução válida e mais curta"

    Exemplos:
      | entrada | saida | perfeito |
      | 0,0     | 1,0   | True     |
      | 0,0     | 0,1   | False    |
      | 1,1     | 18,13 | True     |
      | 19,14   | 0,0   | False    |
      | 10,0    | 10,14 | True     |

  # pdf: "Access the generated structure, and access at least a solution."
  # md:  "Acessar a estrutura gerada e acessar pelo menos uma solução."
  @obrigatorio @automatizado @decisao-I08 @decisao-I09 @pdf-p15-L08 @md-L288
  Cenário: A classe geradora expõe pelo menos uma solução
    Dado o gerador "MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42)"
    Quando o gerador gera o labirinto
    Então o módulo mazegen confirma "solution pública e documentada"
    E o validador da suíte confirma "solução válida e mais curta"
