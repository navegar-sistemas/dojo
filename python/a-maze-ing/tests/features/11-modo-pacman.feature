# language: pt
Funcionalidade: Modo Pac-Man (PERFECT=False, o padrão)
  Com PERFECT=False o labirinto é um tabuleiro de Pac-Man: conectado, com cantos e centro
  abertos, pelo menos duas rotas independentes e no máximo dois becos sem saída reais.

  Contexto:
    Dado o config base com "PERFECT=False"

  # pdf: "If the PERFECT flag is not activated (the default), the maze must instead be a board"
  # pdf: "directly usable by a Pac-Man-like game."
  # md:  "Se a flag `PERFECT` não estiver ativada (o padrão), o labirinto deve ser um tabuleiro diretamente utilizável por um jogo estilo Pac-Man."
  @obrigatorio @automatizado @decisao-I06 @pdf-p09-L22-L23 @md-L190
  Esquema do Cenário: O labirinto é um tabuleiro utilizável por um jogo tipo Pac-Man
    Dado o config com "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "SEED=<seed>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "Pac-Man-USABLE"

    Exemplos:
      | largura | altura | saida | seed |
      | 20      | 15     | 19,14 | 1    |
      | 21      | 15     | 20,14 | 2    |
      | 20      | 14     | 19,13 | 3    |
      | 9       | 9      | 8,8   | 4    |
      | 40      | 30     | 39,29 | 5    |

  # pdf: "If the PERFECT flag is not activated (the default), the maze must instead be a board"
  # md:  "Se a flag `PERFECT` não estiver ativada (o padrão), o labirinto deve ser um tabuleiro"
  # regua: "When 'PERFECT' is set to False (the default), the maze is a board usable by a Pac-Man-like game"
  # regua-md: "Quando `PERFECT` é `False` (o padrão), o labirinto é um tabuleiro utilizável por um jogo estilo Pac-Man"
  @obrigatorio @decisao-D03 @automatizado @decisao-I20 @pdf-p09-L22 @md-L190 @regua-p3
  Cenário: O modo Pac-Man é o modo padrão do projeto
    Dado o config do repositório
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "Pac-Man-USABLE"

  # pdf: "every corridor is reachable (full connectivity), so the whole board can be filled"
  # pdf: "with pac-gums and remains winnable"
  # md:  "todo corredor é alcançável (conectividade total), de modo que o tabuleiro inteiro pode ser preenchido com pac-gums e continua vencível;"
  @obrigatorio @automatizado @pdf-p09-L24-L25 @md-L191
  Cenário: Todo corredor é alcançável
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Reachable region" do maze_analyzer.py contém "(0 corridor(s) unreachable)"
    E o validador da suíte confirma "toda célula fora do 42 alcançável"

  # pdf: "the four corners and the centre are open corridors (the ghosts and super-pac-"
  # pdf: "gums sit in the corners, the player starts in the centre)"
  # md:  "os quatro cantos e o centro são corredores abertos (os fantasmas e as super-pac-gums ficam nos cantos; o jogador começa no centro);"
  @obrigatorio @automatizado @pdf-p09-L26-L27 @md-L192
  Esquema do Cenário: Os quatro cantos são corredores abertos
    Quando eu gero o labirinto
    Então a célula "<canto>" não tem valor F
    E a célula "<canto>" é alcançável a partir da entrada

    Exemplos:
      | canto |
      | 0,0   |
      | 19,0  |
      | 0,14  |
      | 19,14 |

  # pdf: "the four corners and the centre are open corridors (the ghosts and super-pac-"
  # pdf: "gums sit in the corners, the player starts in the centre)"
  # md:  "os quatro cantos e o centro são corredores abertos (os fantasmas e as super-pac-gums ficam nos cantos; o jogador começa no centro);"
  # regua: "the 4 corners and the centre are open corridors"
  # regua-md: "os 4 cantos e o centro são corredores abertos"
  @obrigatorio @automatizado @decisao-D08 @pdf-p09-L26-L27 @md-L192 @regua-p3
  Esquema do Cenário: O centro é corredor aberto, com dimensão par ou ímpar
    Dado o config com "WIDTH=<largura>", "HEIGHT=<altura>" e "EXIT=<saida>"
    Quando eu gero o labirinto
    Então pelo menos uma das células <candidatas> é alcançável a partir da entrada
    E a linha "Corners + centre" do maze_analyzer.py contém "all reachable"

    Exemplos:
      | largura | altura | saida | candidatas                    |
      | 21      | 15     | 20,14 | "10,7"                        |
      | 20      | 15     | 19,14 | "9,7" e "10,7"                |
      | 21      | 14     | 20,13 | "10,6" e "10,7"               |
      | 20      | 14     | 19,13 | "9,6", "10,6", "9,7" e "10,7" |

  # pdf: "it offers at least two independent routes (loops), so that a chased player"
  # pdf: "always has an alternative"
  # md:  "oferece pelo menos duas rotas independentes (ciclos), para que um jogador perseguido sempre tenha uma alternativa"
  # regua: "and at least two independent routes."
  # regua: "(the script also prints the loop count and the dead-end count against their thresholds)"
  # regua-md: "e pelo menos duas rotas independentes."
  # regua-md: "(o script também imprime a contagem de ciclos e de becos sem saída contra seus limiares)"
  @obrigatorio @automatizado @decisao-D10 @decisao-I06 @pdf-p09-L28-L29 @md-L193 @regua-p3
  Esquema do Cenário: Há pelo menos duas rotas independentes
    Dado o config com "SEED=<seed>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então o número na linha "Independent loops" do maze_analyzer.py é pelo menos 2
    E o validador da suíte confirma "pelo menos 2 rotas independentes"

    Exemplos:
      | seed |
      | 11   |
      | 12   |
      | 13   |

  # pdf: "(a perfect maze, or a perfect maze with merely one"
  # pdf: "wall removed (a single loop), is therefore not acceptable in this mode)"
  # md:  "(um labirinto perfeito, ou um labirinto perfeito com apenas uma parede removida — um único ciclo — não é aceitável neste modo);"
  # regua: "and at least two independent routes."
  # regua-md: "e pelo menos duas rotas independentes."
  @obrigatorio @automatizado @decisao-D10 @pdf-p09-L29-L30 @md-L193 @regua-p3
  Esquema do Cenário: Perfeito ou perfeito com uma parede removida não é aceito
    Dado o labirinto de teste "<modelo>"
    Quando o validador da suíte lê o labirinto
    Então o validador da suíte relata "recusado: <loops> rota(s) independente(s)" em "modo Pac-Man"
    E a linha "Verdict:" do maze_analyzer.py começa com "<veredito>"

    Exemplos:
      | modelo                                                | loops | veredito          |
      | perfeito do config base                               | 0     | PERFECT maze      |
      | perfeito do config base com uma parede interna aberta | 1     | Not Pac-Man-ready |

  # pdf: "dead-ends should stay rare (a couple are tolerated)"
  # md:  "becos sem saída devem ser raros (um ou dois são tolerados);"
  # regua: "A few dead-ends are tolerated."
  # regua: "(the script also prints the loop count and the dead-end count against their thresholds)"
  # regua-md: "Alguns becos sem saída são tolerados."
  # regua-md: "(o script também imprime a contagem de ciclos e de becos sem saída contra seus limiares)"
  @recomendado @automatizado @decisao-D09 @decisao-I06 @pdf-p09-L31 @md-L194 @regua-p3
  Esquema do Cenário: Becos sem saída são raros
    Dado o config com "SEED=<seed>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então o número na linha "Dead-ends" do maze_analyzer.py é no máximo 2
    E o validador da suíte confirma "no máximo 2 becos reais"

    Exemplos:
      | seed |
      | 21   |
      | 22   |
      | 23   |

  # pdf: "a board with no dead-end"
  # pdf: "at all is the ideal and is rewarded as a bonus (see the Bonuses chapter)."
  # md:  "um tabuleiro sem nenhum beco sem saída é o ideal e é recompensado como bônus (veja o capítulo de Bônus)."
  @bonus @automatizado @decisao-I06 @pdf-p09-L31-L32 @md-L194
  Cenário: O ideal é nenhum beco sem saída
    Quando eu gero o labirinto
    E eu analiso o labirinto com o maze_analyzer.py "--max-dead-ends 0"
    Então a linha "Verdict:" do maze_analyzer.py contém "no real dead-end -> bonus-grade"

  # pdf: "while the default PERFECT=False keeps at least two independent routes open so"
  # pdf: "a chased player always has an alternative."
  # md:  "enquanto o padrão `PERFECT=False` mantém pelo menos duas rotas independentes abertas, para que um jogador perseguido sempre tenha uma alternativa."
  # regua: "and at least two independent routes."
  # regua-md: "e pelo menos duas rotas independentes."
  @informativo @derivado @automatizado @decisao-D10 @pdf-p10-L03-L04 @md-L200 @regua-p3
  Cenário: A legenda da figura confirma ao menos duas rotas abertas
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então o número na linha "Independent loops" do maze_analyzer.py é pelo menos 2

  # figura: "playable board · loops, no dead-ends · Pac-Man"
  # md:  "à direita, `PERFECT = False (default)` (tabuleiro jogável · ciclos, sem becos sem saída · Pac-Man)."
  @informativo @manual @pdf-p10-figura @md-L198
  Cenário: A figura do subject mostra o modo Pac-Man como tabuleiro jogável
    Dada a figura "A-Maze-ing — the two generation modes" do subject
    Quando eu comparo com o labirinto exibido pelo meu programa com PERFECT=False
    Então os dois mostram ciclos, quase nenhum beco e o caminho mais curto destacado

  # pdf: "or a playable board"
  # pdf: "(no dead-ends besides the "42" pattern and several independent routes, as required by"
  # pdf: "default)."
  # md:  "ou um tabuleiro jogável (sem becos sem saída além do padrão "42" e várias rotas independentes, como exigido por padrão)."
  # regua: "It must report a PERFECT maze for PERFECT=True, and a Pac-Man-USABLE verdict for the default one"
  # regua-md: "Ele deve reportar um labirinto `PERFECT` para `PERFECT=True` e um veredito `Pac-Man-USABLE` para o padrão"
  @informativo @automatizado @pdf-p11-L06-L08 @md-L220 @regua-p3
  Cenário: O maze_analyzer.py classifica o labirinto como tabuleiro jogável
    Quando eu gero o labirinto
    E eu analiso o labirinto com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "Pac-Man-USABLE"

  # pdf: "the four corners and the centre are open corridors (the ghosts and super-pac-"
  # md:  "os quatro cantos e o centro são corredores abertos"
  @obrigatorio @derivado @automatizado @pdf-p09-L26 @md-L192
  Esquema do Cenário: Entrada e saída podem ficar em canto ou no centro
    Dado o config com "WIDTH=<largura>", "HEIGHT=<altura>", "ENTRY=<entrada>" e "EXIT=<saida>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "Pac-Man-USABLE"

    Exemplos:
      | largura | altura | entrada | saida |
      | 20      | 15     | 0,0     | 19,14 |
      | 20      | 15     | 19,0    | 0,14  |
      | 21      | 15     | 10,7    | 0,0   |
      | 21      | 15     | 20,14   | 10,7  |
