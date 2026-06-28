import type { IArchitectureDecision, IComponent } from "../types.ts";

// Arquitetura do SISTEMA: ADRs e componentes globais. Aqui, requirementKeys
// referenciam requisitos de produto (PR-NNN).
export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-001",
    title: "Clean Architecture em camadas: Domain / Application / Presentation(Godot)",
    context:
      "O dono do produto exige OO, DDD, Clean Code e Clean Architecture, com responsabilidade única por arquivo e método. O jogo precisa de regras testáveis e independentes da engine, e de uma camada Godot para renderizar e orquestrar.",
    decision:
      "Organizar o código em três camadas com dependências apontando para dentro: (1) Domain — entidades, value objects e serviços de regra (GDScript puro, RefCounted, sem tipos de cena); (2) Application — casos de uso/orquestração de turno e progressão (depende só de Domain via interfaces); (3) Presentation — nós Godot (scenes, sprites, UI, input) que adaptam Application ao motor. Domain não conhece Application nem Presentation.",
    consequences:
      "Domain testável de forma isolada e determinística; troca de apresentação sem tocar regras. Custo: mais arquivos e camadas de adaptação (mappers/adapters) entre objetos de domínio e nós Godot.",
    status: "accepted",
    requirementKeys: ["PR-001", "PR-002", "PR-003"],
    rejectedAlternatives: [
      {
        alternative: "Colocar a lógica do jogo direto em scripts de Node/Scene da Godot",
        reason:
          "Acopla regra à engine, impede teste isolado e leva a arquivos gigantes multifunção — viola os princípios do projeto.",
      },
    ],
  },
  {
    key: "ADR-002",
    title: "Turno como transição de estado pura (CQS: sentidos consultam, ações comandam)",
    context:
      "A semântica do Ruby Warrior é: uma ação por turno consome o turno; sentidos são consultas livres sem efeito colateral. Determinismo é necessário para testabilidade e justiça.",
    decision:
      "Modelar a resolução de turno como função de domínio que recebe o estado do nível e a ação escolhida e retorna o próximo estado, sem efeitos colaterais ocultos. Separar explicitamente Sentidos (queries puras sobre um snapshot do nível) de Ações (comandos que produzem novo estado). Validar no Application que no máximo uma ação seja efetivada por turno.",
    consequences:
      "Lógica testável com asserções estado→estado; replays determinísticos; pontuação reproduzível. Custo: snapshots/cópia de estado e disciplina para não vazar mutação nos sentidos.",
    status: "accepted",
    requirementKeys: ["PR-001", "PR-002", "PR-005"],
    rejectedAlternatives: [
      {
        alternative: "Mutação direta e ad-hoc do estado dentro dos próprios métodos de sentido",
        reason:
          "Quebra CQS, torna o turno não-determinístico e dificulta teste e replay.",
      },
    ],
  },
  {
    key: "ADR-003",
    title: "Níveis como dados declarativos carregados por loader",
    context:
      "São 9 níveis com layout, posições de unidades, escada, descrição e habilidades introduzidas. A definição precisa ser fiel ao original e fácil de revisar/ajustar.",
    decision:
      "Representar cada nível como dado declarativo (recurso/estrutura de dados) e ter um LevelLoader no Domain/Application que monta o estado inicial do nível a partir desse dado. Sem lógica de regra embutida na definição do nível.",
    consequences:
      "Adicionar/ajustar níveis é editar dados, não código; paridade com o original verificável item a item. Custo: definir e versionar o formato de dados do nível.",
    status: "accepted",
    requirementKeys: ["PR-004", "PR-008"],
  },
  {
    key: "ADR-004",
    title: "Lógica do jogador via interface PlayerTurnStrategy injetada",
    context:
      "No original o jogador escreve play_turn(warrior). Para a jam, a lógica do jogador deve ser plugável e executar contra a API do warrior sem acessar o estado interno do mundo.",
    decision:
      "Definir uma interface de domínio (PlayerTurnStrategy) com um método play_turn(warrior_facade), onde warrior_facade expõe apenas a API pública (sentidos + ações). A estratégia é injetada no caso de uso de turno. Para os níveis, fornecer estratégias-referência que resolvem cada fase.",
    consequences:
      "Desacopla a inteligência do jogador do motor; permite trocar/testar estratégias. Caminho aberto para, no futuro, aceitar roteiro do usuário em texto. Custo: desenhar uma fachada que não vaze o estado do mundo.",
    status: "accepted",
    requirementKeys: ["PR-002", "PR-005"],
  },
];

export const components: IComponent[] = [
  {
    name: "Domain",
    responsibility:
      "Núcleo de regras: entidades (Warrior, Unit e tipos de inimigo, Captive), value objects (Direction, Health, Position, Space/Tile, Action, Score) e serviços de domínio (resolução de turno, combate, sentidos, IA de inimigo, pontuação). GDScript puro, sem dependência da engine.",
    dependsOn: [],
    requirementKeys: ["PR-001", "PR-002", "PR-003", "PR-006"],
  },
  {
    name: "Application",
    responsibility:
      "Casos de uso e orquestração: executar um turno (obter ação da estratégia do jogador, validar uma-ação-por-turno, aplicar ao Domain, fazer inimigos reagirem), avaliar vitória/derrota, carregar níveis (LevelLoader) e progredir pela torre. Depende de Domain por interfaces.",
    dependsOn: ["Domain"],
    requirementKeys: ["PR-001", "PR-004", "PR-005", "PR-008"],
  },
  {
    name: "Presentation",
    responsibility:
      "Camada Godot: scenes, sprites e animações das unidades e do grid, UI de saúde/turno/descrição/pontuação, telas de transição da torre e input. Adapta o estado do Application para nós e renderiza o feedback de cada turno. Usa assets temáticos da 42.",
    dependsOn: ["Application"],
    requirementKeys: ["PR-007", "PR-008"],
  },
  {
    name: "LevelData",
    responsibility:
      "Definições declarativas dos 9 níveis da beginner tower (layout, unidades, escada, descrição, habilidades introduzidas, time bonus e ace score), consumidas pelo LevelLoader do Application.",
    dependsOn: [],
    requirementKeys: ["PR-004"],
  },
];
