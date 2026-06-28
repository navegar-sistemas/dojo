import type { IProduct } from "../types.ts";

export const product: IProduct = {
  name: "42 Warrior",
  vision: `Um remake do jogo de programação Ruby Warrior, reambientado no universo da 42 (a escola/comunidade 42 São Paulo), construído em Godot com GDScript para uma game jam da 42SP. O jogador não controla o herói diretamente: ele escreve, em uma linguagem/API de roteiro exposta pelo jogo, a lógica que o "warrior" executa a cada turno. O objetivo de cada fase é levar o warrior do início até a escada (saída), sobrevivendo a inimigos, resgatando cativos e — idealmente — limpando o nível de forma ótima. O produto recria fielmente a "beginner tower" de 9 níveis do original, com mecânica de turnos, sentidos (feel/look/listen), ações (walk/attack/rest/rescue/pivot/shoot), saúde/dano/descanso e pontuação com time bonus e ace score, porém com assets visuais e narrativos customizados na temática 42.`,
  businessGoals: [
    "Entregar um jogo jogável e completo (9 níveis da beginner tower) dentro do prazo da game jam da 42SP.",
    "Demonstrar excelência técnica: código GDScript orientado a objetos, com responsabilidade única por arquivo e por método, aplicando DDD, Clean Code e Clean Architecture.",
    "Recriar fielmente as mecânicas e a curva de aprendizado do Ruby Warrior original, validando paridade de funcionalidades nível a nível.",
    "Diferenciar pela identidade visual e narrativa da 42 (assets customizados na temática da escola).",
  ],
  actors: [
    {
      name: "Jogador",
      description:
        "Usuário final do jogo. Aprendiz de programação que escreve a lógica de turno do warrior e progride pela torre. Fonte de verdade dos requisitos de experiência (UX, dificuldade, feedback).",
    },
    {
      name: "usuario",
      description:
        "Desenvolvedor e dono do produto nesta game jam. Implementa o jogo em Godot/GDScript, decide arquitetura e ratifica esclarecimentos, revisões e convenções. Assignee padrão de stories e tasks.",
    },
    {
      name: "Jurado da Jam",
      description:
        "Avaliador da game jam da 42SP. Sistema/papel externo que joga e julga o resultado; influencia critérios de completude, polimento e fidelidade à temática.",
    },
  ],
  principles: [
    {
      name: "Responsabilidade única em arquivo e método",
      rule: "Cada script GDScript tem uma única responsabilidade coesa; cada método faz uma só coisa. Nada de arquivos gigantescos ou métodos multifunção.",
      rationale:
        "Requisito explícito do dono do produto. Arquivos e métodos pequenos e coesos são testáveis, legíveis e evoluíveis sob a pressão de prazo de uma jam, e evitam o acoplamento que torna mudanças arriscadas.",
    },
    {
      name: "Domínio independente da engine",
      rule: "A lógica de domínio do jogo (regras de turno, combate, sentidos, pontuação, estado do nível) não depende de tipos da Godot (Node, Scene, sinais de UI). A camada Godot orquestra e renderiza; o domínio é GDScript puro (RefCounted/objetos simples).",
      rationale:
        "Clean Architecture: a regra de negócio é o núcleo estável e o framework é um detalhe. Permite testar o domínio de forma isolada e determinística, e trocar/renderizar a apresentação sem tocar nas regras.",
    },
    {
      name: "Orientação a objetos com modelagem de domínio (DDD)",
      rule: "Modelar o jogo com entidades e value objects do domínio (Warrior, Unit, Level, Tile/Space, Direction, Health, Position, Action) e linguagem ubíqua alinhada ao Ruby Warrior. Regras vivem nas entidades/serviços de domínio, não em controllers de UI.",
      rationale:
        "DDD dá vocabulário comum e coloca o comportamento junto dos dados que ele governa, reduzindo lógica anêmica espalhada e tornando a paridade com o jogo de referência verificável conceito a conceito.",
    },
    {
      name: "Turno determinístico",
      rule: "A resolução de um turno é uma transição de estado pura e determinística: dado o estado do nível e a ação escolhida, o próximo estado é sempre o mesmo. Sentidos são consultas sem efeito colateral; apenas ações (terminadas em '!') consomem o turno.",
      rationale:
        "Determinismo torna o jogo testável e justo (mesmo input → mesmo resultado), espelha a semântica do original (uma ação por turno; sentidos livres) e separa consulta de comando (CQS).",
    },
    {
      name: "Fidelidade ao Ruby Warrior beginner",
      rule: "As mecânicas, a API, as entidades e os 9 níveis seguem o comportamento do Ruby Warrior beginner tower; divergências só por decisão de produto registrada.",
      rationale:
        "É um remake: a paridade funcional com a referência é o critério de sucesso. Customização é na pele (assets/tema 42), não nas regras, salvo decisão explícita.",
    },
  ],
};
