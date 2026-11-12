# language: pt
Funcionalidade: Uso de IA (Capítulo II)
  A IA é usada com cautela, só no que eu entendo e consigo defender, com verificação
  sistemática e revisão por pares.

  # pdf: "During your learning journey, AI can assist with many different tasks. Take the time to"
  # pdf: "explore the various capabilities of AI tools and how they can support your work."
  # md:  "Durante sua jornada de aprendizado, a IA pode ajudar em muitas tarefas diferentes. Reserve um tempo para explorar as diversas capacidades das ferramentas de IA e como elas podem apoiar seu trabalho."
  @recomendado @manual @pdf-p04-L03-L05 @md-L45-L47
  Cenário: Explorar o que as ferramentas de IA fazem
    - Dado que vou usar uma ferramenta de IA no projeto
    - Quando eu começo a usá-la
    - Então eu sei descrever onde ela ajuda e onde costuma errar

  # pdf: "However, always approach them with caution and critically assess the results."
  # md:  "No entanto, aborde-as sempre com cautela e avalie criticamente os resultados."
  @recomendado @manual @pdf-p04-L05-L06 @md-L47
  Cenário: Avaliar criticamente toda resposta da IA
    - Dada uma resposta gerada por IA
    - Quando eu a considero para o projeto
    - Então eu confiro a resposta contra o subject, a documentação e os testes antes de usá-la

  # pdf: "you can never be completely sure"
  # pdf: "that your question was well-formed or that the generated content is accurate."
  # md:  "você nunca pode ter certeza absoluta de que sua pergunta foi bem formulada ou de que o conteúdo gerado está correto."
  @informativo @manual @pdf-p04-L06-L08 @md-L47
  Cenário: Nenhuma resposta da IA é tratada como certa
    - Dada uma resposta gerada por IA
    - Quando ela parece correta
    - Então eu ainda a trato como hipótese até verificá-la

  # pdf: "Your peers"
  # pdf: "are a valuable resource to help you avoid mistakes and blind spots."
  # md:  "Seus colegas são um recurso valioso para ajudá-lo a evitar erros e pontos cegos."
  @informativo @manual @pdf-p04-L08-L09 @md-L47
  Cenário: Os colegas ajudam a achar erros e pontos cegos
    - Dada uma parte do projeto que eu considero pronta
    - Quando eu a mostro a um colega
    - Então eu registro os erros e pontos cegos que ele encontrar

  # pdf: "Main message"
  # pdf: "Use AI to reduce repetitive or tedious tasks."
  # md:  "Mensagem principal"
  # md:  "Use a IA para reduzir tarefas repetitivas ou tediosas."
  @recomendado @manual @pdf-p04-L10-L11 @md-L49-L51
  Cenário: A IA reduz tarefas repetitivas
    - Dada uma tarefa repetitiva (ex.: gerar casos de teste parecidos)
    - Quando eu peço ajuda à IA
    - Então o resultado é revisado por mim antes de entrar no projeto

  # pdf: "Develop prompting skills — both coding and non-coding — that will benefit your"
  # pdf: "future career."
  # md:  "Desenvolva habilidades de prompting — tanto para código quanto fora dele — que beneficiarão sua carreira futura."
  @recomendado @manual @pdf-p04-L12-L13 @md-L52
  Cenário: Praticar a escrita de prompts
    - Dada uma dúvida de código ou de outro assunto
    - Quando eu escrevo o prompt
    - Então ele traz contexto, objetivo e restrições com vocabulário preciso

  # pdf: "Learn how AI systems work to better anticipate and avoid common risks, biases,"
  # pdf: "and ethical issues."
  # md:  "Aprenda como os sistemas de IA funcionam para antecipar e evitar melhor riscos comuns, vieses e questões éticas."
  @recomendado @manual @pdf-p04-L14-L15 @md-L53
  Cenário: Conhecer riscos, vieses e questões éticas da IA
    - Dado o uso de IA no projeto
    - Quando eu explico como a ferramenta funciona
    - Então eu cito pelo menos um risco, um viés e uma questão ética e como os evitei

  # pdf: "Continue building both technical and power skills by working with your peers."
  # md:  "Continue desenvolvendo habilidades técnicas e comportamentais trabalhando com seus colegas."
  @recomendado @manual @pdf-p04-L16 @md-L54
  Cenário: Desenvolver habilidades técnicas e interpessoais com os colegas
    - Dado o andamento do projeto
    - Quando eu trabalho com colegas
    - Então eu discuto decisões técnicas com eles em vez de só consultar a IA

  # pdf: "Only use AI-generated content that you fully understand and can take responsibility"
  # pdf: "for."
  # pdf: "evaluation, I can't explain what it does or why. I lose credibility — and I fail my"
  # md:  "Use apenas conteúdo gerado por IA que você entenda por completo e pelo qual possa assumir responsabilidade."
  # md:  "Durante a avaliação entre pares, não consigo explicar o que ela faz nem por quê. Perco credibilidade — e reprovo no projeto."
  @obrigatorio @derivado @manual @pdf-p04-L17-L18 @pdf-p05-L20-L23 @md-L55 @md-L81-L83
  Cenário: Só entra no projeto o que eu entendo por completo
    - Dado um trecho gerado por IA
    - Quando eu decido mantê-lo no projeto
    - Então eu explico linha a linha o que ele faz e por quê
    - E eu assumo a responsabilidade por ele

  # pdf: "Learner rules:"
  # pdf: "You should take the time to explore AI tools and understand how they work, so"
  # pdf: "you can use them ethically and reduce potential biases."
  # md:  "Regras do aprendiz"
  # md:  "Você deve reservar um tempo para explorar ferramentas de IA e entender como funcionam, para usá-las de forma ética e reduzir vieses potenciais."
  @recomendado @manual @pdf-p04-L19-L21 @md-L57-L59
  Cenário: Entender as ferramentas para usá-las com ética e menos viés
    - Dadas as ferramentas de IA disponíveis
    - Quando eu escolho uma
    - Então eu sei como ela gera respostas e quais vieses isso traz

  # pdf: "You should reflect on your problem before prompting — this helps you write clearer,"
  # pdf: "more detailed, and more relevant prompts using accurate vocabulary."
  # md:  "Você deve refletir sobre o seu problema antes de escrever o prompt — isso ajuda a escrever prompts mais claros, detalhados e relevantes, usando vocabulário preciso."
  @recomendado @manual @pdf-p04-L22-L23 @md-L60
  Cenário: Refletir sobre o problema antes do prompt
    - Dado um problema do projeto
    - Quando eu vou perguntar à IA
    - Então eu já escrevi o que sei, o que quero e o que já tentei

  # pdf: "You should develop the habit of systematically checking, reviewing, questioning,"
  # pdf: "and testing anything generated by AI."
  # md:  "Você deve desenvolver o hábito de verificar, revisar, questionar e testar sistematicamente tudo o que for gerado por IA."
  @recomendado @manual @pdf-p04-L24-L25 @md-L61
  Cenário: Todo código gerado por IA é verificado e testado
    - Dado um trecho de código gerado por IA no projeto
    - Quando eu o incorporo
    - Então ele tem testes na suíte
    - E "make lint" e a suíte passam com ele

  # pdf: "You should always seek peer review — don't rely solely on your own validation."
  # md:  "Você deve sempre buscar revisão por pares — não confie apenas na sua própria validação."
  @recomendado @manual @pdf-p04-L26 @md-L62
  Cenário: Buscar revisão por pares
    - Dada uma parte do projeto validada só por mim
    - Quando eu a considero pronta
    - Então um colega revisou essa parte

  # pdf: "Phase outcomes:"
  # pdf: "Develop both general-purpose and domain-specific prompting skills."
  # pdf: "Boost your productivity with effective use of AI tools."
  # pdf: "Continue strengthening computational thinking, problem-solving, adaptability, and"
  # pdf: "collaboration."
  # md:  "Resultados da fase"
  # md:  "Desenvolver habilidades de prompting tanto genéricas quanto específicas de domínio."
  # md:  "Aumentar sua produtividade com o uso eficaz de ferramentas de IA."
  # md:  "Continuar fortalecendo pensamento computacional, resolução de problemas, adaptabilidade e colaboração."
  @informativo @manual @pdf-p05-L02-L06 @md-L64-L68
  Cenário: Os resultados esperados da fase
    - Dado o fim do projeto
    - Quando eu reviso o que aprendi
    - Então eu sei escrever prompts gerais e de domínio
    - E eu fui mais produtivo com a IA sem perder compreensão
    - E eu exercitei pensamento computacional, resolução de problemas, adaptabilidade e colaboração

  # pdf: "You'll regularly encounter situations — exams, evaluations, and more — where"
  # pdf: "you must demonstrate real understanding."
  # md:  "Você encontrará regularmente situações — exames, avaliações e outras — em que precisará demonstrar compreensão real."
  @obrigatorio @manual @pdf-p05-L07-L09 @md-L70-L72
  Cenário: Demonstrar compreensão real na avaliação
    - Dada a defesa do projeto
    - Quando o avaliador pergunta sobre qualquer parte do código
    - Então eu respondo sem consultar a IA

  # pdf: "Be prepared, keep building both your"
  # pdf: "technical and interpersonal skills."
  # md:  "Esteja preparado; continue desenvolvendo suas habilidades técnicas e interpessoais."
  @recomendado @manual @pdf-p05-L09-L10 @md-L72
  Cenário: Estar preparado para exames e avaliações
    - Dada a proximidade da defesa
    - Quando eu me preparo
    - Então eu ensaio explicações técnicas em voz alta, como faria com o avaliador

  # pdf: "Explaining your reasoning and debating with peers often reveals gaps in your un-"
  # pdf: "derstanding. Make peer learning a priority."
  # md:  "Explicar seu raciocínio e debater com colegas frequentemente revela lacunas no seu entendimento. Faça do aprendizado entre pares uma prioridade."
  @recomendado @manual @pdf-p05-L11-L12 @md-L73
  Cenário: Priorizar o aprendizado entre pares
    - Dada uma decisão do projeto
    - Quando eu a explico a um colega
    - Então eu anoto as lacunas que a explicação revelou e as estudo

  # pdf: "AI tools often lack your specific context and tend to provide generic responses. Your"
  # pdf: "peers, who share your environment, can offer more relevant and accurate insights."
  # md:  "Ferramentas de IA geralmente não têm o seu contexto específico e tendem a dar respostas genéricas. Seus colegas, que compartilham o seu ambiente, podem oferecer percepções mais relevantes e precisas."
  @informativo @manual @pdf-p05-L13-L14 @md-L74
  Cenário: A IA não conhece o meu contexto
    - Dada uma resposta genérica da IA
    - Quando ela não considera o subject ou o ambiente da 42
    - Então eu consulto um colega que compartilha esse contexto

  # pdf: "Where AI tends to generate the most likely answer, your peers can provide alter-"
  # pdf: "native perspectives and valuable nuance. Rely on them as a quality checkpoint."
  # md:  "Enquanto a IA tende a gerar a resposta mais provável, seus colegas podem oferecer perspectivas alternativas e nuances valiosas. Conte com eles como ponto de controle de qualidade."
  @recomendado @manual @pdf-p05-L15-L16 @md-L75
  Cenário: Colegas como ponto de controle de qualidade
    - Dada uma solução sugerida pela IA
    - Quando eu a comparo com a visão de um colega
    - Então eu considero a alternativa dele antes de decidir

  # pdf: "I ask AI: "How do I test a sorting function?" It gives me a few ideas. I try them out"
  # pdf: "and review the results with a peer. We refine the approach together."
  # md:  "Pergunto à IA: "Como testo uma função de ordenação?". Ela me dá algumas ideias. Eu as experimento e reviso os resultados com um colega. Refinamos a abordagem juntos."
  @informativo @manual @pdf-p05-L17-L19 @md-L77-L79
  Cenário: Boa prática — pedir ideias, experimentar e revisar com um colega
    - Dada uma dúvida sobre como testar uma parte do labirinto
    - Quando eu peço ideias à IA
    - Então eu as experimento e reviso o resultado com um colega

  # pdf: "I ask AI to write a whole function, copy-paste it into my project. During peer-"
  # pdf: "evaluation, I can't explain what it does or why. I lose credibility — and I fail my"
  # pdf: "project."
  # md:  "Peço à IA para escrever uma função inteira e colo no meu projeto. Durante a avaliação entre pares, não consigo explicar o que ela faz nem por quê. Perco credibilidade — e reprovo no projeto."
  @obrigatorio @derivado @manual @pdf-p05-L20-L23 @md-L81-L83
  Cenário: Má prática — colar função gerada sem entender
    - Dada qualquer função do projeto
    - Quando o avaliador pede para eu explicar o que ela faz e por quê
    - Então eu explico sem hesitar
    - E nenhuma função do projeto foi colada da IA sem compreensão

  # pdf: "I use AI to help design a parser. Then I walk through the logic with a peer. We catch"
  # pdf: "two bugs and rewrite it together — better, cleaner, and fully understood."
  # md:  "Uso a IA para ajudar a projetar um parser. Depois, percorro a lógica com um colega. Encontramos dois bugs e reescrevemos juntos — melhor, mais limpo e totalmente compreendido."
  @informativo @manual @pdf-p05-L24-L26 @md-L85-L87
  Cenário: Boa prática — projetar com a IA e percorrer a lógica com um colega
    - Dado o parser do arquivo de configuração
    - Quando eu o projeto com ajuda da IA
    - Então eu percorro a lógica com um colega e corrijo os erros encontrados

  # pdf: "I let Copilot generate my code for a key part of my project. It compiles, but I can't"
  # pdf: "explain how it handles pipes. During the evaluation, I fail to justify and I fail my"
  # pdf: "project."
  # md:  "Deixo o Copilot gerar o código de uma parte-chave do meu projeto. Compila, mas não consigo explicar como ele lida com pipes. Durante a avaliação, não consigo justificar e reprovo no projeto."
  @obrigatorio @derivado @manual @pdf-p05-L27-L30 @md-L89-L91
  Cenário: Má prática — parte-chave gerada que eu não sei justificar
    - Dadas as partes-chave do projeto (geração, "42", solução, arquivo de saída, exibição)
    - Quando o avaliador pede a justificativa de cada uma
    - Então eu justifico cada decisão de implementação
