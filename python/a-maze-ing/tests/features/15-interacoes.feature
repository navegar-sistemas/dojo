# language: pt
Funcionalidade: Interações do usuário
  Enquanto o programa roda, o usuário regenera o labirinto, mostra ou oculta o caminho mais
  curto, troca a cor das paredes e sai, sem que nada trave.

  Contexto:
    Dado o config base salvo em "cfg.txt"

  # pdf: "User interactions must be available while the program is running, and must include, at"
  # pdf: "least, the following tasks:"
  # md:  "Interações do usuário devem estar disponíveis enquanto o programa está em execução e devem incluir, no mínimo, as seguintes tarefas:"
  @obrigatorio @automatizado @decisao-I03 @pdf-p12-L07-L08 @md-L263
  Cenário: O programa aguarda comandos depois de exibir o labirinto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando o evento "1 segundo sem entrada" acontece no menu
    Então o programa continua em execução
    E o programa aguarda no prompt "Choice? (1-4): "
    E a renderização confirma "cada renderização seguida do menu"

  # pdf: "Re-generate a new maze and display it."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  # regua: "Re-generate a new maze."
  # regua-md: "Regenerar um novo labirinto."
  @obrigatorio @automatizado @decisao-D02 @decisao-D16 @decisao-I03 @pdf-p12-L09 @md-L265 @regua-p2
  Cenário: Regenerar cria um novo labirinto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "1"
    E o validador da suíte lê o labirinto
    Então a renderização confirma "labirinto diferente do da renderização anterior"
    E o validador da suíte confirma "labirinto válido conforme o config"

  # pdf: "Re-generate a new maze and display it."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  @obrigatorio @automatizado @decisao-I02 @decisao-I03 @pdf-p12-L09 @md-L265
  Cenário: O labirinto regenerado é exibido
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "1"
    Então a renderização confirma "nova renderização abaixo da anterior, seguida do menu"

  # pdf: "Re-generate a new maze and display it."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  @obrigatorio @derivado @decisao-D13 @decisao-D16 @automatizado @decisao-I03 @pdf-p12-L09 @md-L265
  Cenário: Regenerar regrava o arquivo de saída
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "1"
    E o validador da suíte lê o labirinto
    Então a renderização confirma "labirinto diferente do da renderização anterior"
    E a renderização confirma "paredes iguais às do arquivo de saída"
    E a renderização confirma "entrada e saída iguais às do rodapé"
    E o validador da suíte confirma "solução válida e mais curta"

  # pdf: "The maze must be randomly generated, but reproducibility via a seed is required."
  # pdf: "Re-generate a new maze and display it."
  # md:  "O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  @obrigatorio @derivado @decisao-D02 @decisao-D16 @automatizado @decisao-I03 @pdf-p09-L05 @pdf-p12-L09 @md-L180 @md-L265
  Cenário: Com SEED, a sequência de regenerações é reproduzível
    Quando eu executo "python3 a_maze_ing.py cfg.txt" 2 vezes com a entrada "1", "1" e "4"
    Então os resultados são idênticos em "saída exibida"

  # pdf: "Show/Hide a valid shortest path from the entrance to the exit."
  # md:  "Mostrar/Ocultar um caminho mais curto válido da entrada até a saída."
  # regua: "A toggle button to show and hide the shortest path from entry to exit."
  # regua-md: "Um botão de alternância para mostrar e ocultar o caminho mais curto da entrada até a saída."
  @obrigatorio @automatizado @decisao-I02 @decisao-I03 @decisao-I21 @pdf-p12-L10 @md-L266 @regua-p2
  Cenário: Mostrar o caminho mais curto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt", com o caminho oculto
    Quando eu envio ao menu "2"
    Então na última renderização, as posições de "células do caminho" têm a cor "ciano"
    E a renderização confirma "caminho do arquivo marcado em ciano"
    E a renderização confirma "espaço fora das paredes, dos cantos e do caminho"

  # pdf: "Show/Hide a valid shortest path from the entrance to the exit."
  # md:  "Mostrar/Ocultar um caminho mais curto válido da entrada até a saída."
  # regua: "A toggle button to show and hide the shortest path from entry to exit."
  # regua-md: "Um botão de alternância para mostrar e ocultar o caminho mais curto da entrada até a saída."
  @obrigatorio @automatizado @decisao-I02 @decisao-I03 @decisao-I21 @pdf-p12-L10 @md-L266 @regua-p2
  Cenário: Ocultar o caminho mais curto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt", com o caminho visível
    Quando eu envio ao menu "2"
    Então na última renderização, nenhuma posição tem a cor "ciano"
    E a renderização confirma "espaço fora das paredes, dos cantos e do caminho"

  # pdf: "Show/Hide a valid shortest path from the entrance to the exit."
  # md:  "Mostrar/Ocultar um caminho mais curto válido da entrada até a saída."
  @obrigatorio @automatizado @decisao-D15 @decisao-I03 @decisao-I08 @pdf-p12-L10 @md-L266
  Cenário: O caminho exibido é válido e mais curto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "2"
    Então a renderização confirma "caminho marcado liga entrada e saída por paredes abertas"
    E a renderização confirma "caminho marcado com o comprimento da busca em largura"

  # pdf: "Show/Hide a valid shortest path from the entrance to the exit."
  # md:  "Mostrar/Ocultar um caminho mais curto válido da entrada até a saída."
  # regua: "Control that the shortest path sequence in the output file matches its visual representation. Any error will mark this question as failed."
  # regua-md: "Verifique que a sequência do caminho mais curto no arquivo de saída corresponde à sua representação visual. Qualquer erro marca esta questão como reprovada."
  @obrigatorio @automatizado @decisao-D15 @decisao-D16 @decisao-I02 @decisao-I03 @decisao-I21 @pdf-p12-L10 @md-L266 @regua-p3
  Esquema do Cenário: O caminho exibido é o mesmo gravado no arquivo de saída
    Dado o config com "PERFECT=<perfeito>"
    E o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "2"
    Então a renderização confirma "caminho do arquivo marcado em ciano"
    Quando eu envio ao menu "1"
    Então a renderização confirma "labirinto diferente do da renderização anterior"
    E a renderização confirma "caminho do arquivo marcado em ciano"

    Exemplos:
      | perfeito |
      | True     |
      | False    |

  # pdf: "Re-generate a new maze and display it."
  # pdf: "Show/Hide a valid shortest path from the entrance to the exit."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  # md:  "Mostrar/Ocultar um caminho mais curto válido da entrada até a saída."
  @obrigatorio @derivado @decisao-D16 @decisao-I03 @automatizado @decisao-I21 @pdf-p12-L09-L10 @md-L265-L266
  Cenário: Depois de regenerar, o caminho continua visível e é o do novo labirinto
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt", com o caminho visível
    Quando eu envio ao menu "1"
    Então a renderização confirma "labirinto diferente do da renderização anterior"
    E na última renderização, as posições de "células do caminho" têm a cor "ciano"
    E a renderização confirma "caminho do arquivo marcado em ciano"

  # pdf: "Change maze wall colours."
  # md:  "Alterar as cores das paredes do labirinto."
  # regua: "A button to change the colours of the walls."
  # regua-md: "Um botão para mudar as cores das paredes."
  @obrigatorio @automatizado @decisao-I03 @decisao-I04 @decisao-I21 @pdf-p12-L11 @md-L267 @regua-p2
  Cenário: Trocar a cor das paredes
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt", com o caminho visível
    Então na última renderização, as posições de "paredes" têm a cor "grafite"
    Quando eu envio ao menu "3"
    Então na última renderização, as posições de "paredes" têm a cor "laranja"
    E na última renderização, as posições de "entrada" têm a cor "magenta"
    E na última renderização, as posições de "saída" têm a cor "vermelho"
    E na última renderização, as posições de "células do caminho" têm a cor "ciano"
    E na última renderização, as posições de "42" têm a cor "cinza"

  # pdf: "Change maze wall colours."
  # md:  "Alterar as cores das paredes do labirinto."
  @obrigatorio @derivado @decisao-I04 @automatizado @decisao-I03 @decisao-I21 @pdf-p12-L11 @md-L267
  Cenário: Trocar a cor várias vezes percorre a paleta e volta ao início
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "3", "3", "3" e "3"
    Então a renderização confirma "paredes em rodízio grafite, laranja, verde, azul"
    E na última renderização, as posições de "paredes" têm a cor "grafite"

  # pdf: "Change maze wall colours."
  # md:  "Alterar as cores das paredes do labirinto."
  @recomendado @derivado @decisao-I04 @manual @pdf-p12-L11 @md-L267
  Cenário: Toda cor da paleta é visível no terminal
    - Dado o programa aberto num terminal de fundo claro e depois num de fundo escuro
    - Quando eu percorro as cores das paredes
    - Então em todas as cores as paredes ficam visíveis contra o fundo branco do desenho, nos dois terminais

  # pdf: "Re-generate a new maze and display it."
  # pdf: "Change maze wall colours."
  # md:  "Regenerar um novo labirinto e exibi-lo."
  # md:  "Alterar as cores das paredes do labirinto."
  @obrigatorio @derivado @decisao-D16 @decisao-I04 @automatizado @decisao-I03 @decisao-I21 @pdf-p12-L09 @pdf-p12-L11 @md-L265 @md-L267
  Cenário: A cor escolhida das paredes se mantém ao regenerar
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "3" e "1"
    Então a renderização confirma "labirinto diferente do da renderização anterior"
    E na última renderização, as posições de "paredes" têm a cor "laranja"

  # pdf: "Optional: set specific colours to display the "42" pattern."
  # md:  "Opcional: definir cores específicas para exibir o padrão "42"."
  # regua: "Extra interactions are possible (e.g., changing the colour of the '42' pattern, quitting the program, ...)."
  # regua-md: "Interações extras são possíveis (ex.: mudar a cor do padrão "42", sair do programa, ...)."
  @opcional @manual @decisao-I19 @pdf-p12-L12 @md-L268 @regua-p2
  Cenário: Cor própria para o "42"
    - Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    - Quando eu escolho a opção de trocar a cor do "42"
    - Então as células do "42" são desenhadas com uma cor diferente da anterior
    - E a cor das paredes não muda

  # pdf: "You can add extra user interactions."
  # md:  "Você pode adicionar interações extras."
  @opcional @manual @pdf-p12-L13 @md-L270
  Cenário: Interações extras são permitidas
    - Dada uma interação extra implementada
    - Quando eu a uso
    - Então ela não quebra as três interações obrigatórias
    - E ela está descrita no README

  # figura: "=== A-Maze-ing ===" "1. Re-generate a new maze" "2. Show / Hide the shortest path"
  # figura: "3. Rotate the wall colours" "4. Quit" "Choice? (1-4): "
  # md:  "Figura: Renderização padrão do labirinto no terminal."
  @informativo @manual @decisao-I03 @pdf-p13-figura @md-L272
  Cenário: O menu da figura do subject
    - Dada a figura "Terminal default rendering of the maze"
    - Quando eu comparo com o menu do meu programa
    - Então o meu menu oferece regenerar, mostrar/ocultar o caminho, trocar a cor das paredes e sair

  # figura: "3. Rotate the wall colours"
  # md:  "Figura: Renderização padrão do labirinto no terminal."
  @informativo @manual @decisao-I04 @pdf-p13-figura @md-L272
  Cenário: "Rotate" sugere alternar entre cores predefinidas
    - Dada a opção "Rotate the wall colours" da figura
    - Quando eu implemento a troca de cor
    - Então alternar por uma paleta fixa atende ao requisito

  # figura: "4. Quit" / "4: quit"
  # md:  "Figura: Renderização padrão do labirinto no terminal."
  # md:  "Figura: Renderização do labirinto usando Mlx."
  # regua: "Extra interactions are possible (e.g., changing the colour of the '42' pattern, quitting the program, ...)."
  # regua-md: "Interações extras são possíveis (ex.: mudar a cor do padrão "42", sair do programa, ...)."
  @opcional @derivado @decisao-I03 @automatizado @pdf-p13-figura @pdf-p14-figura @md-L272 @md-L276 @regua-p2
  Cenário: Sair encerra o programa sem erro
    Quando eu executo "python3 a_maze_ing.py cfg.txt" com a entrada "4"
    Então o código de saída é 0
    E a saída não contém "Traceback"
    E a renderização confirma "última sequência ANSI é o reset"

  # pdf: "It must never crash unexpectedly, and must"
  # md:  "Ele nunca deve travar inesperadamente"
  @obrigatorio @derivado @decisao-I03 @automatizado @pdf-p08-L15 @md-L155
  Esquema do Cenário: Opção inválida no menu não derruba o programa
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando eu envio ao menu "<entrada>"
    Então a saída contém "Invalid choice"
    E o programa continua em execução
    E o programa aguarda no prompt "Choice? (1-4): "
    E a saída não contém "Traceback"

    Exemplos:
      | entrada |
      | 9       |
      | abc     |
      |         |
      | -1      |

  # pdf: "It must never crash unexpectedly, and must"
  # md:  "Ele nunca deve travar inesperadamente"
  @obrigatorio @derivado @decisao-D17 @automatizado @decisao-I03 @pdf-p08-L15 @md-L155
  Esquema do Cenário: Fim da entrada ou interrupção encerram limpo
    Dado o programa iniciado com "python3 a_maze_ing.py cfg.txt"
    Quando o evento "<evento>" acontece no menu
    Então o código de saída é 0
    E a saída não contém "Traceback"
    E a renderização confirma "última sequência ANSI é o reset"

    Exemplos:
      | evento |
      | EOF    |
      | SIGINT |
