# language: pt
Funcionalidade: README.md
  O README.md da raiz apresenta o projeto a quem não o conhece: primeira linha obrigatória,
  Description, Instructions, Resources e as seções extras exigidas pelo A-Maze-ing.

  Contexto:
    Dado o arquivo "README.md" na raiz do repositório

  # pdf: "A README.md file must be provided at the root of your Git repository."
  # md:  "Um arquivo `README.md` deve ser fornecido na raiz do seu repositório Git."
  @obrigatorio @automatizado @pdf-p17-L03 @md-L310
  Cenário: README.md existe na raiz do repositório
    Quando eu executo "git ls-files README.md"
    Então a saída padrão é "README.md"

  # pdf: "Its purpose is"
  # pdf: "to allow anyone unfamiliar with the project (peers, staff, recruiters, etc.) to quickly"
  # pdf: "understand what the project is about, how to run it, and where to find more information"
  # pdf: "on the topic."
  # md:  "Seu propósito é permitir que qualquer pessoa não familiarizada com o projeto (colegas, staff, recrutadores etc.) entenda rapidamente do que se trata o projeto, como executá-lo e onde encontrar mais informações sobre o tema."
  @informativo @manual @pdf-p17-L03-L06 @md-L310
  Cenário: Uma pessoa de fora entende o projeto pelo README
    Quando um colega que não conhece o projeto lê o README por poucos minutos
    Então ele sabe o que o projeto faz
    E ele sabe como executá-lo
    E ele sabe onde aprender mais sobre geração de labirintos

  # pdf: "The very first line must be italicized and read: This project has been created as part"
  # pdf: "of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]]."
  # md:  "A primeiríssima linha deve estar em itálico e dizer: This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]]."
  # regua: "The first line is italicized and formatted exactly as: This project has been created as part of the 42 curriculum by <login>, <login>."
  # regua-md: "A primeira linha está em itálico e formatada exatamente como: This project has been created as part of the 42 curriculum by <login>, <login>."
  @obrigatorio @automatizado @decisao-D21 @pdf-p17-L07-L09 @md-L312-L314 @regua-p1
  Cenário: A primeira linha é a frase obrigatória em itálico
    Quando eu leio "README.md"
    Então a primeira linha do README casa com a expressão "^\*This project has been created as part of the 42 curriculum by [a-z0-9-]+(, [a-z0-9-]+)*\.\*$"

  # pdf: "A "Description" section that clearly presents the project, including its goal and a"
  # pdf: "brief overview."
  # md:  "Uma seção "Description" que apresente claramente o projeto, incluindo seu objetivo e uma breve visão geral."
  # regua: "A "Description" section explaining the project's purpose and providing a brief overview."
  # regua-md: "Uma seção "Description" explicando o propósito do projeto e dando uma breve visão geral."
  @obrigatorio @automatizado @decisao-D22 @pdf-p17-L10-L11 @md-L315 @regua-p1
  Cenário: Existe a seção Description
    Quando eu leio "README.md"
    Então o arquivo "README.md" tem uma linha que casa com a expressão "^#+ Description\s*$"

  # pdf: "A "Description" section that clearly presents the project, including its goal and a"
  # md:  "Uma seção "Description" que apresente claramente o projeto, incluindo seu objetivo"
  @obrigatorio @manual @pdf-p17-L10 @md-L315
  Cenário: Description apresenta o objetivo do projeto
    Quando eu leio a seção "Description"
    Então ela diz que o projeto gera labirintos a partir de um arquivo de configuração e os exibe

  # pdf: "brief overview."
  # md:  "e uma breve visão geral."
  @obrigatorio @manual @pdf-p17-L11 @md-L315
  Cenário: Description traz uma visão geral breve
    Quando eu leio a seção "Description"
    Então ela resume os modos perfeito e Pac-Man, o arquivo de saída, a exibição e o módulo reutilizável

  # pdf: "An "Instructions" section containing any relevant information about compilation,"
  # pdf: "installation, and/or execution."
  # md:  "Uma seção "Instructions" contendo qualquer informação relevante sobre compilação, instalação e/ou execução."
  # regua: "An "Instructions" section with relevant details about compilation, installation, and/or execution."
  # regua-md: "Uma seção "Instructions" com detalhes relevantes sobre compilação, instalação e/ou execução."
  @obrigatorio @automatizado @decisao-D22 @pdf-p17-L12-L13 @md-L316 @regua-p1
  Cenário: Existe a seção Instructions com instalação e execução
    Quando eu leio "README.md"
    Então a seção "Instructions" do README contém "make install", "python3 a_maze_ing.py config.txt" e "make run"

  # pdf: "A "Resources" section listing classic references related to the topic (documen-"
  # pdf: "tation, articles, tutorials, etc.)"
  # md:  "Uma seção "Resources" listando referências clássicas relacionadas ao tema (documentação, artigos, tutoriais etc.)"
  # regua: "A "Resources" section listing external references (documentation, tutorials, etc.) and explaining how AI was used, specifying for which tasks and which parts of the project."
  # regua-md: "Uma seção "Resources" listando referências externas (documentação, tutoriais etc.) e explicando como a IA foi usada, especificando para quais tarefas e quais partes do projeto."
  @obrigatorio @automatizado @decisao-D22 @pdf-p17-L14-L15 @md-L317 @regua-p1
  Cenário: Existe a seção Resources com referências clássicas
    Quando eu leio "README.md"
    Então a seção "Resources" do README contém "http"

  # pdf: "A "Resources" section listing classic references related to the topic (documen-"
  # pdf: "tation, articles, tutorials, etc.)"
  # md:  "Uma seção "Resources" listando referências clássicas relacionadas ao tema (documentação, artigos, tutoriais etc.)"
  @obrigatorio @manual @pdf-p17-L14-L15 @md-L317
  Cenário: As referências de Resources tratam do tema do projeto
    Quando eu leio cada referência da seção "Resources"
    Então ela trata de geração ou resolução de labirintos, de grafos ou das ferramentas usadas no projeto
    E cada referência tem título e link ou autor

  # pdf: "as well as a description of how AI was used"
  # md:  "bem como uma descrição de como a IA foi usada"
  @obrigatorio @manual @pdf-p17-L15 @md-L317
  Cenário: Resources descreve como a IA foi usada
    Quando eu leio a seção "Resources"
    Então ela tem uma parte sobre o uso de IA

  # pdf: "specifying for which tasks and which parts of the project."
  # md:  "especificando para quais tarefas e quais partes do projeto."
  @obrigatorio @manual @pdf-p17-L16 @md-L317
  Cenário: O uso de IA cita tarefas e partes do projeto
    Quando eu leio a parte sobre o uso de IA
    Então ela nomeia as tarefas em que a IA ajudou
    E ela nomeia os arquivos ou partes do projeto afetados

  # pdf: "Additional sections may be required depending on the project (e.g., usage"
  # pdf: "examples, feature list, technical choices, etc.)."
  # pdf: "Any required additions will be explicitly listed below."
  # md:  "Seções adicionais podem ser exigidas dependendo do projeto (ex.: exemplos de uso, lista de funcionalidades, escolhas técnicas etc.)."
  # md:  "Quaisquer adições exigidas serão listadas explicitamente abaixo."
  @informativo @manual @pdf-p17-L17-L19 @md-L319-L321
  Cenário: As seções extras exigidas são as listadas pelo subject
    Quando eu confiro as seções extras do README
    Então elas incluem todas as listadas nos cenários seguintes

  # pdf: "The complete structure and format of your config file."
  # md:  "A estrutura e o formato completos do seu arquivo de configuração."
  @obrigatorio @automatizado @pdf-p17-L20 @md-L323
  Cenário: O README documenta o formato completo do config
    Quando eu leio "README.md"
    Então o arquivo "README.md" contém "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE" e "PERFECT"
    E o arquivo "README.md" contém "SEED"
    E o arquivo "README.md" contém "KEY=VALUE" e "x,y"
    E o arquivo "README.md" tem uma linha que casa com a expressão "^#"
    E o arquivo "README.md" tem uma linha que casa com a expressão "^WIDTH=\d+$"

  # pdf: "The complete structure and format of your config file."
  # md:  "A estrutura e o formato completos do seu arquivo de configuração."
  @obrigatorio @manual @pdf-p17-L20 @md-L323
  Cenário: O README explica as regras de leitura do config
    Quando eu leio a parte do README sobre o arquivo de configuração
    Então o README explica as regras de leitura de D03, D04 e D05: chaves e booleanos em qualquer caixa, chave desconhecida ignorada, chave repetida valendo a última, "SEED" opcional e WIDTH e HEIGHT entre 1 e 100

  # pdf: "The maze generation algorithm you chose."
  # md:  "O algoritmo de geração de labirinto que você escolheu."
  @obrigatorio @manual @pdf-p17-L21 @md-L324
  Cenário: O README diz qual algoritmo de geração foi escolhido
    Quando eu leio o README
    Então ele nomeia o algoritmo de geração usado

  # pdf: "Why you chose this algorithm."
  # md:  "Por que você escolheu esse algoritmo."
  @obrigatorio @manual @pdf-p17-L22 @md-L325
  Cenário: O README justifica a escolha do algoritmo
    Quando eu leio o README
    Então ele explica por que esse algoritmo foi escolhido

  # pdf: "What part of your code is reusable, and how."
  # md:  "Qual parte do seu código é reutilizável, e como."
  @obrigatorio @manual @pdf-p17-L23 @md-L326
  Cenário: O README diz o que é reutilizável e como reutilizar
    Quando eu leio o README
    Então ele aponta o módulo "mazegen" como a parte reutilizável
    E ele mostra como instalá-lo e usá-lo

  # pdf: "Your team and project management with:"
  # pdf: "The roles of each team member."
  # md:  "Sua equipe e gestão do projeto, com:"
  # md:  "Os papéis de cada membro da equipe."
  @obrigatorio @manual @pdf-p17-L24-L25 @md-L327-L328
  Cenário: O README descreve a equipe e o papel de cada membro
    Quando eu leio a seção de equipe e gestão
    Então cada membro aparece com o seu papel

  # pdf: "Your anticipated planning and how it evolved until the end"
  # md:  "Seu planejamento previsto e como ele evoluiu até o fim."
  @obrigatorio @manual @pdf-p18-L02 @md-L329
  Cenário: O README descreve o planejamento previsto e como ele evoluiu
    Quando eu leio a seção de equipe e gestão
    Então ela mostra o planejamento inicial
    E ela mostra o que mudou até o fim

  # pdf: "What worked well and what could be improved"
  # md:  "O que funcionou bem e o que poderia ser melhorado."
  @obrigatorio @manual @pdf-p18-L03 @md-L330
  Cenário: O README diz o que funcionou bem e o que pode melhorar
    Quando eu leio a seção de equipe e gestão
    Então ela lista o que funcionou bem
    E ela lista o que poderia melhorar

  # pdf: "Have you used any specific tools? Which ones?"
  # md:  "Vocês usaram alguma ferramenta específica? Quais?"
  @obrigatorio @manual @pdf-p18-L04 @md-L331
  Cenário: O README cita as ferramentas usadas
    Quando eu leio a seção de equipe e gestão
    Então ela diz se ferramentas específicas foram usadas e quais

  # pdf: "If you implement advanced features (multiple algorithms, display options), describe them"
  # pdf: "in this README.md file."
  # md:  "Se você implementar funcionalidades avançadas (múltiplos algoritmos, opções de exibição), descreva-as neste `README.md`."
  @obrigatorio @manual @pdf-p18-L05-L06 @md-L333
  Cenário: Funcionalidades avançadas estão descritas no README
    Dado que o projeto implementa funcionalidades além do obrigatório
    Quando eu leio o README
    Então cada uma está descrita, com a forma de ativá-la

  # pdf: "English is recommended; alternatively, you may use the main language"
  # md:  "Inglês é recomendado"
  @recomendado @manual @decisao-I18 @pdf-p18-L07 @md-L335
  Cenário: O README está em inglês
    Quando eu leio o README
    Então ele está escrito em inglês

  # pdf: "alternatively, you may use the main language"
  # pdf: "of your campus."
  # md:  "alternativamente, você pode usar o idioma principal do seu campus."
  @opcional @manual @decisao-I18 @pdf-p18-L07-L08 @md-L335
  Cenário: O README pode estar no idioma principal do campus
    Dado que o README não está em inglês
    Quando eu confiro o idioma
    Então ele está no idioma principal do campus
