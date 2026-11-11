# language: pt
Funcionalidade: Submissão e avaliação entre pares (Capítulo IX)
  Só o que está no repositório Git é avaliado; os nomes dos arquivos estão corretos; eu estou
  pronto para uma modificação breve durante a defesa.

  # pdf: "Submit your assignment in your Git repository as usual."
  # md:  "Submeta sua tarefa no seu repositório Git como de costume."
  @obrigatorio @manual @pdf-p20-L03 @md-L351
  Cenário: O trabalho está submetido no repositório Git
    Dado o repositório de entrega da 42, clonado à parte (não o monorepo dojo)
    Quando eu executo "git fetch", "git status --porcelain" e comparo "git rev-parse HEAD" com "git rev-parse @{u}"
    Então "git status --porcelain" não imprime nada
    E HEAD é igual ao upstream

  # pdf: "Only the work inside your repos-"
  # pdf: "itory will be evaluated during the defense."
  # md:  "Apenas o trabalho dentro do seu repositório será avaliado durante a defesa."
  @informativo @automatizado @pdf-p20-L03-L04 @md-L351
  Cenário: Um clone limpo tem tudo o que a avaliação usa
    Dado o repositório no estado "clone do remoto"
    Quando eu executo "make install" e "make lint"
    Então todos os comandos terminam com código 0
    Quando eu executo "make run" com a entrada "4"
    Então o código de saída é 0

  # pdf: "Don't hesitate to double-check the names of"
  # pdf: "your files to ensure they are correct."
  # md:  "Não hesite em conferir duas vezes os nomes dos seus arquivos para garantir que estão corretos."
  # regua: "Check if all expected files are present in the Git repository:"
  # regua: "If any of the required elements is missing, the grade is 0."
  # regua-md: "Verifique se todos os arquivos esperados estão presentes no repositório Git:"
  # regua-md: "Se qualquer um dos elementos obrigatórios estiver faltando, a nota é 0."
  @obrigatorio @automatizado @decisao-I11 @pdf-p20-L04-L05 @md-L351 @regua-p1
  Esquema do Cenário: Os arquivos exigidos estão versionados com o nome exato
    Dado o repositório no estado "clone limpo"
    Quando eu executo "git ls-files '<arquivo>'"
    Então o código de saída é 0
    E a saída padrão não contém "/"
    E o caminho "<arquivo>" está versionado no git
    E o caminho "tests" não existe

    Exemplos:
      | arquivo        |
      | a_maze_ing.py  |
      | config.txt     |
      | Makefile       |
      | README.md      |
      | LICENSE.md     |
      | .gitignore     |
      | mazegen-*      |
      | pyproject.toml |

  # pdf: "During the evaluation, a brief modification of the project may occasionally be re-"
  # pdf: "quested. This could involve a minor behaviour change, a few lines of code to write or"
  # pdf: "rewrite, or an easy-to-add feature."
  # md:  "Durante a avaliação, uma breve modificação do projeto poderá ocasionalmente ser solicitada. Isso pode envolver uma pequena mudança de comportamento, algumas linhas de código a escrever ou reescrever, ou uma funcionalidade fácil de adicionar."
  @informativo @manual @pdf-p20-L06-L08 @md-L353
  Cenário: A avaliação pode pedir uma modificação breve
    Dada a defesa do projeto
    Quando o avaliador pede uma pequena mudança de comportamento, poucas linhas ou uma funcionalidade fácil
    Então eu entendo o pedido como parte normal da avaliação

  # pdf: "While this step may not be applicable to every project, you must be prepared for it"
  # pdf: "if it is mentioned in the evaluation guidelines."
  # md:  "Embora esta etapa possa não se aplicar a todo projeto, você deve estar preparado para ela caso seja mencionada nas diretrizes de avaliação."
  @obrigatorio @manual @pdf-p20-L09-L10 @md-L355
  Cenário: Estar preparado para a modificação
    Dada a ficha de avaliação do A-Maze-ing
    Quando ela menciona a modificação
    Então eu conheço o código o suficiente para alterá-lo sem consultar a IA

  # pdf: "This step is meant to verify your actual understanding of a specific part of the project."
  # md:  "Esta etapa visa verificar sua compreensão real de uma parte específica do projeto."
  @informativo @manual @pdf-p20-L11 @md-L357
  Cenário: A modificação verifica a compreensão real de uma parte
    Dada qualquer parte do projeto escolhida pelo avaliador
    Quando ele pede uma mudança nela
    Então eu localizo o código responsável e explico o impacto da mudança

  # pdf: "The modification can be performed in any development environment you choose (e.g.,"
  # pdf: "your usual setup)"
  # md:  "A modificação pode ser realizada em qualquer ambiente de desenvolvimento de sua escolha (ex.: sua configuração habitual)"
  @opcional @manual @pdf-p20-L12-L13 @md-L357
  Cenário: A modificação pode ser feita no meu ambiente habitual
    Dado o meu editor e o meu terminal de sempre
    Quando eu faço a modificação
    Então eu rodo "make lint" e a suíte de testes nesse mesmo ambiente

  # pdf: "and it should be feasible within a few minutes — unless a specific time"
  # pdf: "frame is defined as part of the evaluation."
  # md:  "e deve ser viável em poucos minutos — a menos que um prazo específico seja definido como parte da avaliação."
  @informativo @manual @pdf-p20-L13-L14 @md-L357
  Cenário: A modificação cabe em poucos minutos
    Dado um pedido de modificação simples
    Quando eu cronometro a mudança, o lint e os testes
    Então tudo fica pronto em poucos minutos, ou no prazo definido pela avaliação

  # pdf: "You can, for example, be asked to make a small update to a function or script, modify a"
  # pdf: "display, or adjust a data structure to store new information, etc."
  # md:  "Você pode, por exemplo, ser solicitado a fazer uma pequena atualização em uma função ou script, modificar uma exibição ou ajustar uma estrutura de dados para armazenar novas informações etc."
  @informativo @manual @pdf-p20-L15-L16 @md-L359
  Esquema do Cenário: Ensaios de modificação antes da defesa
    Dado o projeto com "make lint" e a suíte verdes
    Quando eu faço o ensaio "<modificacao>"
    Então "make lint" e a suíte continuam verdes
    E eu desfaço o ensaio

    Exemplos:
      | modificacao                                           |
      | aceitar uma nova chave no config                      |
      | trocar o caractere usado para desenhar as paredes     |
      | mostrar o comprimento do caminho mais curto na tela   |
      | guardar em cada célula quantas vezes ela foi visitada |
      | mudar a posição do "42"                               |

  # pdf: "The details (scope, target, etc.) will be specified in the evaluation guidelines and may"
  # pdf: "vary from one evaluation to another for the same project."
  # md:  "Os detalhes (escopo, alvo etc.) serão especificados nas diretrizes de avaliação e podem variar de uma avaliação para outra para o mesmo projeto."
  @informativo @manual @pdf-p20-L17-L18 @md-L361
  Cenário: Os detalhes da modificação variam entre avaliações
    Dadas as diretrizes de avaliação
    Quando eu me preparo para a defesa
    Então eu me preparo para qualquer parte do projeto, não só para um pedido específico
