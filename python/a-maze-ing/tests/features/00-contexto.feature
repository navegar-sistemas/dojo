# language: pt
Funcionalidade: Contexto do subject
  O subject A-Maze-ing v2.3 é a fonte de todos os requisitos desta suíte.

  # pdf: "A-Maze-ing"
  # pdf: "This is the way"
  # pdf: "Summary: Create your own maze generator and display its result!"
  # md:  "A-Maze-ing"
  # md:  "This is the way"
  # md:  "Resumo: Crie seu próprio gerador de labirintos e exiba o resultado!"
  @informativo @manual @pdf-p01-L01-L03 @md-L1-L5
  Cenário: O projeto é um gerador de labirintos que exibe o resultado
    - Dado o subject "A-Maze-ing"
    - Quando eu leio o resumo da capa
    - Então o projeto entregue gera um labirinto
    - E o projeto entregue exibe o labirinto gerado

  # pdf: "Version: 2.3"
  # md:  "Versão: 2.3"
  @informativo @manual @pdf-p01-L04 @md-L7
  Cenário: Os requisitos seguem a versão 2.3 do subject
    - Dado o PDF "en.subject.pdf" e a tradução "pt_br.subject.md"
    - Quando eu confiro a versão impressa na capa
    - Então a versão é "2.3"
    - E a implementação é conferida contra essa versão

  # pdf: "Contents"
  # pdf: "Mandatory part"
  # md:  "Sumário"
  # md:  "Capítulo IV — Parte Obrigatória"
  @informativo @manual @pdf-p02-L01-L18 @md-L11-L29
  Cenário: O subject tem nove capítulos e a parte obrigatória tem cinco seções
    - Dado o sumário do subject
    - Quando eu listo os capítulos
    - Então existem os capítulos I a IX
    - E as Instruções Comuns têm as seções III.1 a III.3
    - E a Parte Obrigatória tem as seções IV.1 a IV.5

  # pdf: "Some famous algorithms used for maze generation, like Prim's, Kruskal's, or the recursive backtracker"
  # md:  "Alguns algoritmos famosos usados para gerar labirintos, como o de Prim, o de Kruskal ou o recursive backtracker"
  @informativo @manual @pdf-p03-L03-L09 @md-L35
  Cenário: O prefácio cita algoritmos clássicos de geração
    - Dado o prefácio do subject
    - Quando eu escolho o algoritmo de geração
    - Então eu conheço Prim, Kruskal e recursive backtracker como referências
    - E o algoritmo escolhido usa aleatoriedade e teoria dos grafos

  # pdf: "Building a maze, especially one you can visualize and share"
  # md:  "Construir um labirinto, especialmente um que você possa visualizar e compartilhar"
  @informativo @manual @pdf-p03-L11-L13 @md-L35
  Cenário: O labirinto pode ser visualizado e compartilhado
    - Dado o prefácio do subject
    - Quando eu leio o objetivo do projeto
    - Então o labirinto gerado é visualizável no programa
    - E o labirinto gerado é compartilhável por meio do arquivo de saída

  # pdf: "A labyrinth is not a place to be lost, but a path to be found."
  # md:  "Um labirinto não é um lugar para se perder, mas um caminho a ser encontrado."
  @informativo @manual @pdf-p03-L14-L15 @md-L37-L39
  Cenário: A epígrafe não gera requisito
    - Dada a epígrafe do prefácio
    - Quando eu procuro uma exigência nela
    - Então nenhum comportamento do programa depende da epígrafe
