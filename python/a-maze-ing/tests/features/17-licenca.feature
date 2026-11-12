# language: pt
Funcionalidade: Licença do gerador
  O LICENSE.md na raiz declara uma licença que permite explicitamente reutilizar e distribuir
  o gerador em projetos posteriores.

  # pdf: "Because this maze generator is meant to be reused in a later project, you must include a"
  # pdf: "LICENSE.md file at the root of your repository"
  # md:  "Como este gerador de labirintos se destina a ser reutilizado em um projeto posterior, você deve incluir um arquivo `LICENSE.md` na raiz do seu repositório"
  @obrigatorio @automatizado @pdf-p15-L21-L22 @md-L302
  Cenário: LICENSE.md existe na raiz do repositório
    Dado o repositório no estado "clone limpo"
    Quando eu executo "git ls-files LICENSE.md"
    Então a saída padrão é "LICENSE.md"
    E o caminho "LICENSE.md" não está vazio

  # pdf: "stating the license under which your code"
  # pdf: "may be reused."
  # md:  "declarando a licença sob a qual seu código pode ser reutilizado."
  @obrigatorio @automatizado @decisao-I17 @pdf-p15-L22-L23 @md-L302
  Cenário: O LICENSE.md declara qual é a licença
    Dado o arquivo "LICENSE.md" na raiz do repositório
    Quando eu leio "LICENSE.md"
    Então o arquivo "LICENSE.md" contém "MIT License"
    E o arquivo "LICENSE.md" tem uma linha que casa com a expressão "^Copyright (\(c\) )?\d{4}(-\d{4})?,? \S"

  # pdf: "Choosing and writing this license is part of the assignment: it is your"
  # pdf: "first contact with software licensing and intellectual property."
  # md:  "Escolher e escrever essa licença faz parte da tarefa: é o seu primeiro contato com licenciamento de software e propriedade intelectual."
  @informativo @manual @pdf-p15-L23-L24 @md-L302
  Cenário: A escolha da licença é justificável na defesa
    - Dada a licença escolhida
    - Quando o avaliador pergunta por que ela foi escolhida
    - Então eu explico o que ela permite, o que exige de quem reutiliza e por que serve ao projeto

  # pdf: "The license you pick must"
  # pdf: "explicitly allow the reuse and distribution of your maze generator by the later project(s)"
  # pdf: "that build on it."
  # md:  "A licença escolhida deve permitir explicitamente a reutilização e distribuição do seu gerador de labirintos pelo(s) projeto(s) posterior(es) que se basearem nele."
  @obrigatorio @manual @decisao-I17 @pdf-p15-L24-L25 @pdf-p16-L02 @md-L302
  Esquema do Cenário: A licença permite explicitamente <permissao>
    - Dado o texto do "LICENSE.md", com a licença MIT
    - Quando eu procuro a concessão de <permissao>
    - Então o texto concede "<termo>" de forma explícita

    Exemplos:
      | permissao                    | termo      |
      | uso, parte da reutilização   | use        |
      | cópia, parte da reutilização | copy       |
      | modificação                  | modify     |
      | distribuição                 | distribute |

  # pdf: "explicitly allow the reuse and distribution of your maze generator by the later project(s)"
  # md:  "permitir explicitamente a reutilização e distribuição do seu gerador de labirintos pelo(s) projeto(s) posterior(es)"
  @obrigatorio @derivado @automatizado @decisao-I13 @decisao-I17 @pdf-p15-L25 @md-L302
  Cenário: O pacote distribuído carrega a mesma licença
    Dado o arquivo "mazegen-*" na raiz do repositório
    Quando eu leio "mazegen-*"
    Então o metadado "License-Expression" do pacote "mazegen-*" é "MIT"
    E o arquivo "LICENSE.md" contém "MIT License"
    E o pacote "mazegen-*" confirma "LICENSE.md incluído"
