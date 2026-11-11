# language: pt
Funcionalidade: Bônus
  Tabuleiro sem nenhum beco sem saída, vários algoritmos de geração e animação durante a
  geração. Nenhum é obrigatório.

  # pdf: "You may add various bonuses to your project. Here are possible examples:"
  # md:  "Você pode adicionar vários bônus ao seu projeto. Aqui estão alguns exemplos possíveis:"
  @opcional @manual @pdf-p19-L03 @md-L341
  Cenário: Os bônus são opcionais e os exemplos são sugestões
    Dado o capítulo de bônus
    Quando eu escolho quais bônus implementar
    Então a parte obrigatória continua completa sem nenhum deles
    E bônus diferentes dos exemplos também são possíveis

  # pdf: "You may add various bonuses to your project. Here are possible examples:"
  # md:  "Você pode adicionar vários bônus ao seu projeto. Aqui estão alguns exemplos possíveis:"
  # regua: "The bonuses can only be considered if all the previous questions were successful."
  # regua: "You can validate up to 5 different working bonuses. Each bonus must represent a fair amount of work."
  # regua-md: "Os bônus só podem ser considerados se todas as questões anteriores foram bem-sucedidas."
  # regua-md: "Você pode validar até 5 bônus diferentes que funcionem. Cada bônus deve representar uma quantidade justa de trabalho."
  @informativo @manual @pdf-p19-L03 @md-L341 @regua-p4
  Cenário: Os bônus só contam com a parte obrigatória inteira aprovada
    Dados todos os cenários obrigatórios das funcionalidades 01 a 18 e 21
    Quando algum deles falha
    Então nenhum bônus é considerado na avaliação
    E até 5 bônus que funcionem são validados quando todos passam

  # pdf: "A default (non-perfect) maze with no dead-end at all: a perfectly "braided""
  # pdf: "board, so a chased player is never trapped anywhere (the provided analysis script"
  # pdf: "confirms it with --max-dead-ends 0)."
  # md:  "Um labirinto padrão (não perfeito) sem nenhum beco sem saída: um tabuleiro perfeitamente "trançado" (braided), de modo que um jogador perseguido nunca fique preso em lugar algum (o script de análise fornecido confirma isso com `--max-dead-ends 0`)."
  # md:  "um tabuleiro sem nenhum beco sem saída é o ideal e é recompensado como bônus (veja o capítulo de Bônus)."
  # regua: "A default maze with no dead-end at all (a perfectly braided board). Verify with "python3 maze_analyzer.py <output_file> --max-dead-ends 0": the verdict must stay Pac-Man-USABLE and report it as bonus-grade."
  # regua-md: "Um labirinto padrão sem nenhum beco sem saída (um tabuleiro perfeitamente "trançado"). Verifique com `python3 maze_analyzer.py <output_file> --max-dead-ends 0`: o veredito deve continuar `Pac-Man-USABLE` e reportá-lo como `bonus-grade`."
  @bonus @automatizado @decisao-I06 @pdf-p19-L04-L06 @pdf-p09-L31-L32 @md-L343 @md-L194 @regua-p4
  Esquema do Cenário: O modo Pac-Man não tem nenhum beco sem saída
    Dado o config base com "PERFECT=False", "WIDTH=<largura>", "HEIGHT=<altura>", "EXIT=<saida>" e "SEED=<seed>"
    Quando eu gero o labirinto
    E eu analiso o labirinto com o maze_analyzer.py "--max-dead-ends 0"
    Então a linha "Verdict:" do maze_analyzer.py começa com "Pac-Man-USABLE"
    E a linha "Verdict:" do maze_analyzer.py contém "no real dead-end -> bonus-grade (perfectly braided)"

    Exemplos:
      | largura | altura | saida | seed |
      | 20      | 15     | 19,14 | 1    |
      | 21      | 15     | 20,14 | 2    |
      | 20      | 14     | 19,13 | 3    |
      | 40      | 30     | 39,29 | 4    |

  # pdf: "A default (non-perfect) maze with no dead-end at all: a perfectly "braided""
  # pdf: "The maze can't have large open areas. Corridors can't be wider than 2 cells."
  # md:  "Um labirinto padrão (não perfeito) sem nenhum beco sem saída: um tabuleiro perfeitamente "trançado" (braided)"
  # md:  "O labirinto não pode ter grandes áreas abertas. Corredores não podem ter mais de 2 células de largura."
  # regua: "There is no 3x3 or larger open zone without walls."
  # regua-md: "Não há zona aberta sem paredes de 3x3 ou maior."
  @bonus @derivado @decisao-D11 @automatizado @decisao-I06 @decisao-I07 @pdf-p19-L04 @pdf-p09-L16 @md-L343 @md-L187 @regua-p3
  Cenário: O tabuleiro trançado continua sem áreas 3x3
    Dado o config base com "PERFECT=False"
    Quando eu gero o labirinto com cada seed de 1 a 100
    Então o validador da suíte confirma "sem área aberta 3x3"
    E o validador da suíte confirma "zero becos reais"

  # pdf: "Support multiple maze generation algorithms."
  # pdf: "You may add additional keys (e.g., seed, algorithm, display mode) if useful."
  # md:  "Suportar múltiplos algoritmos de geração de labirinto."
  # md:  "Você pode adicionar chaves extras (ex.: seed, algoritmo, modo de exibição) se for útil."
  @bonus @automatizado @decisao-I19 @pdf-p19-L07 @pdf-p09-L02 @md-L344 @md-L174
  Esquema do Cenário: Cada algoritmo de geração produz labirintos válidos nos dois modos
    Dado o config base com "ALGORITHM=<algoritmo>" e "PERFECT=<perfeito>"
    Quando eu gero o labirinto e o analiso com o maze_analyzer.py
    Então a linha "Verdict:" do maze_analyzer.py começa com "<veredito>"
    E o validador da suíte confirma "labirinto válido conforme o config"
    Quando eu gero o labirinto 2 vezes
    Então os resultados são idênticos em "arquivo de saída"

    Exemplos:
      | algoritmo   | perfeito | veredito       |
      | backtracker | True     | PERFECT maze   |
      | backtracker | False    | Pac-Man-USABLE |
      | kruskal     | True     | PERFECT maze   |
      | kruskal     | False    | Pac-Man-USABLE |
      | prim        | True     | PERFECT maze   |
      | prim        | False    | Pac-Man-USABLE |

  # pdf: "Support multiple maze generation algorithms."
  # md:  "Suportar múltiplos algoritmos de geração de labirinto."
  @bonus @derivado @decisao-D01 @automatizado @decisao-I19 @pdf-p19-L07 @md-L344
  Cenário: Algoritmo desconhecido gera erro
    Dado o config base com "ALGORITHM=inexistente"
    Quando eu executo "python3 a_maze_ing.py cfg.txt"
    Então a mensagem de erro cita "ALGORITHM", "backtracker", "kruskal" e "prim"
    E o código de saída é 1

  # pdf: "Support multiple maze generation algorithms."
  # md:  "Suportar múltiplos algoritmos de geração de labirinto."
  @bonus @derivado @automatizado @decisao-I19 @pdf-p19-L07 @md-L344
  Cenário: Algoritmos diferentes geram labirintos diferentes com a mesma seed
    Dado o config base
    Quando eu gero o labirinto com cada um de "ALGORITHM=backtracker", "ALGORITHM=kruskal" e "ALGORITHM=prim"
    Então os resultados são diferentes entre si em "grade"

  # pdf: "Add animation during maze generation."
  # md:  "Adicionar animação durante a geração do labirinto."
  @bonus @manual @decisao-I19 @pdf-p19-L08 @md-L345
  Cenário: A geração é animada
    Dada a animação ativada
    Quando eu gero um labirinto
    Então eu vejo as paredes sendo abertas passo a passo antes do labirinto final

  # pdf: "Add animation during maze generation."
  # md:  "Adicionar animação durante a geração do labirinto."
  @bonus @derivado @manual @decisao-I19 @pdf-p19-L08 @md-L345
  Cenário: A animação não altera o labirinto final
    Dado o config base
    Quando eu gero o labirinto com a animação ativada e depois desativada
    Então os dois arquivos de saída são idênticos
    E a animação mostra pelo menos um estado intermediário

  # pdf: "You may add additional keys (e.g., seed, algorithm, display mode) if useful."
  # md:  "Você pode adicionar chaves extras (ex.: seed, algoritmo, modo de exibição) se for útil."
  @opcional @manual @decisao-I19 @pdf-p09-L02 @md-L174
  Cenário: Chave extra de modo de exibição
    Dado o config base com uma chave extra de modo de exibição
    Quando eu executo o programa com cada valor aceito dessa chave
    Então cada execução termina sem "Traceback"
    E um valor não aceito gera mensagem de erro citando a chave
