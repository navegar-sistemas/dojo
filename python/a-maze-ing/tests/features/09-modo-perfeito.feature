# language: pt
Funcionalidade: Modo perfeito (PERFECT=True)
  Com PERFECT=True o labirinto é perfeito: exatamente um caminho entre entrada e saída,
  nenhum ciclo; as células fora do "42" formam uma árvore geradora.

  Contexto:
    Dado o config base com "PERFECT=True"

  # pdf: "If the PERFECT flag is activated, the maze must contain exactly one path between"
  # pdf: "the entry and the exit"
  # md:  "Se a flag `PERFECT` estiver ativada, o labirinto deve conter exatamente um caminho entre a entrada e a saída"
  # regua: "When 'PERFECT' is set to True, the maze is a perfect maze (exactly one path between entry and exit, no loops)."
  # regua-md: "Quando `PERFECT` é `True`, o labirinto é perfeito (exatamente um caminho entre entrada e saída, sem ciclos)."
  @obrigatorio @automatizado @decisao-I05 @pdf-p09-L20-L21 @md-L189 @regua-p3
  Esquema do Cenário: Existe exatamente um caminho entre entrada e saída
    Dado o config com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "SEED=<seed>"
    Quando eu gero o labirinto
    Então o validador da suíte confirma "árvore geradora fora do 42"
    E o validador da suíte confirma "caminho único entre entrada e saída"

    Exemplos:
      | largura | altura | saida | seed |
      | 20      | 15     | 19,14 | 1    |
      | 21      | 15     | 20,14 | 2    |
      | 9       | 9      | 8,8   | 3    |
      | 40      | 30     | 39,29 | 4    |
      | 2       | 1      | 1,0   | 5    |

  # pdf: "(i.e., it must be a perfect maze: no loops at all)."
  # md:  "(ou seja, deve ser um labirinto perfeito: sem nenhum ciclo)."
  @obrigatorio @automatizado @decisao-I05 @pdf-p09-L21 @md-L189
  Esquema do Cenário: O labirinto perfeito não tem nenhum ciclo
    Dado o config com "SEED=<seed>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então a linha "Independent loops" do maze_analyzer começa com "0 /"
    E o validador da suíte confirma "árvore geradora fora do 42"

    Exemplos:
      | seed |
      | 10   |
      | 20   |
      | 30   |

  # pdf: "perfect mazes (with one unique path between any two points) are directly related to"
  # pdf: "spanning trees in graph theory."
  # md:  "labirintos perfeitos (com um único caminho entre quaisquer dois pontos) estão diretamente relacionados às árvores geradoras (spanning trees) da teoria dos grafos."
  @informativo @derivado @automatizado @pdf-p03-L10-L11 @md-L35
  Cenário: Há caminho único entre quaisquer duas células fora do "42"
    Quando eu gero o labirinto
    Então o validador da suíte confirma "árvore geradora fora do 42"

  # pdf: "PERFECT=True forces a single winding path (every other"
  # pdf: "corridor is a dead-end)"
  # md:  "`PERFECT=True` força um único caminho sinuoso (todos os outros corredores são becos sem saída)"
  @informativo @derivado @automatizado @pdf-p10-L02-L03 @md-L200
  Cenário: Todo corredor fora do caminho da solução termina em beco sem saída
    Quando eu gero o labirinto
    Então o validador da suíte confirma "ramos fora da solução terminam em beco"

  # figura: "one single path · academic / lab maze"
  # md:  "À esquerda, `PERFECT = True` (um único caminho · labirinto acadêmico / de laboratório)"
  @informativo @manual @pdf-p10-figura @md-L198
  Cenário: A figura do subject mostra o modo perfeito como labirinto acadêmico
    - Dada a figura "A-Maze-ing — the two generation modes" do subject
    - Quando eu comparo com o labirinto exibido pelo meu programa com PERFECT=True
    - Então os dois mostram um único caminho sinuoso com o caminho mais curto destacado

  # pdf: "reports whether"
  # pdf: "the maze is perfect (a single path, as required with PERFECT=True) or a playable board"
  # md:  "e informa se o labirinto é perfeito (um único caminho, como exigido com `PERFECT=True`) ou um tabuleiro jogável"
  # regua: "It must report a PERFECT maze for PERFECT=True, and a Pac-Man-USABLE verdict for the default one"
  # regua-md: "Ele deve reportar um labirinto `PERFECT` para `PERFECT=True` e um veredito `Pac-Man-USABLE` para o padrão"
  @informativo @automatizado @pdf-p11-L05-L06 @md-L220 @regua-p3
  Cenário: O maze_analyzer.py classifica o labirinto como perfeito
    Quando eu gero o labirinto
    E eu analiso o labirinto com o maze_analyzer
    Então a linha "Verdict:" do maze_analyzer começa com "PERFECT maze"

  # pdf: "If the PERFECT flag is activated, the maze must contain exactly one path between"
  # md:  "Se a flag `PERFECT` estiver ativada, o labirinto deve conter exatamente um caminho entre a entrada e a saída"
  # regua: "There is the '42' pattern in the maze (except is size does not allow it, then you should have a message on the terminal)."
  # regua-md: "Há o padrão "42" no labirinto (exceto se o tamanho não permitir; nesse caso deve haver uma mensagem no terminal)."
  @obrigatorio @derivado @decisao-D06 @automatizado @pdf-p09-L20 @md-L189 @regua-p3
  Cenário: O labirinto pequeno sem "42" continua perfeito
    Dado o config com "WIDTH=5", "HEIGHT=5" e "EXIT=4,4"
    Quando eu gero o labirinto e o analiso com o maze_analyzer
    Então a linha "Verdict:" do maze_analyzer começa com "PERFECT maze"
    E a linha "Reachable region" do maze_analyzer contém "25 cells"
