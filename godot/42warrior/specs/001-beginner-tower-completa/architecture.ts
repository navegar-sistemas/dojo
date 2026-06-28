import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-001",
    title: "LevelState imutável + TurnResolver puro que retorna (novo estado, eventos)",
    context:
      "O turno precisa ser determinístico e testável (RF-003), com vitória/derrota derivadas do estado (RF-004), e a apresentação precisa saber o que aconteceu para animar.",
    decision:
      "LevelState é um value object imutável (grade, unidades, posições/direções, turno atual). TurnResolver.resolve(state, action) -> TurnResult{ next_state, events } não muta a entrada: produz um novo LevelState e uma lista de TurnEvent descrevendo o que ocorreu (moveu, atacou, levou dano, descansou, resgatou, atirou, venceu, morreu). Inimigos reagem dentro do resolve, após a ação do warrior.",
    consequences:
      "Testes asseguram estado→estado; replay e pontuação reproduzíveis; presentation consome eventos sem ler o domínio. Custo: cópia de estado a cada turno (irrelevante numa grade 1×N pequena).",
    status: "accepted",
    requirementKeys: ["RF-001", "RF-002", "RF-003", "RF-004"],
    rejectedAlternatives: [
      {
        alternative: "Mutar LevelState in-place e disparar sinais Godot direto do domínio",
        reason: "Acopla domínio à engine (viola RNF-001) e quebra determinismo/replay.",
      },
    ],
  },
  {
    key: "ADR-002",
    title: "Direction e Action como value objects/enums; ataque-para-trás reduzido modelado no VO",
    context:
      "A API aceita direção forward/backward e cada ação tem semântica própria; strings mágicas são proibidas (RNF-004).",
    decision:
      "Direction é um enum/VO com forward/backward e a operação de resolver o offset e o oposto (para pivot). Action é modelada como objeto de comando tipado (Walk/Attack/Rest/Rescue/Pivot/Shoot, cada um com sua direção), consumido pelo TurnResolver via despacho por tipo — não por if-cadeia de strings.",
    consequences:
      "Sem strings mágicas; adicionar ação é adicionar um tipo. Despacho explícito e testável. Custo: uma classe pequena por ação.",
    status: "accepted",
    requirementKeys: ["RF-002", "RF-006"],
  },
  {
    key: "ADR-003",
    title: "WarriorFacade: única superfície da API exposta ao código do jogador",
    context:
      "O código do jogador deve sentir e agir sem acessar o estado interno do mundo (RNF-005); e no máximo uma ação efetiva por turno (RF-002).",
    decision:
      "WarriorFacade recebe um snapshot somente-leitura do LevelState (para os sentidos) e registra a ação escolhida. Sentidos (feel/look/listen/health/direction_of_*) leem o snapshot e retornam VOs Space/Direction. Ações (walk!/attack!/...) apenas REGISTRAM a Action pretendida; a primeira chamada de ação vence e as demais no mesmo turno são ignoradas. A fachada não expõe LevelState nem outras unidades.",
    consequences:
      "Isolamento e uma-ação-por-turno garantidos na fronteira; superfície auditável por allowlist de métodos. Custo: a fachada é reconstruída por turno com o snapshot atual.",
    status: "accepted",
    requirementKeys: ["RF-002", "RF-005", "RF-007", "RF-011", "RNF-005"],
  },
  {
    key: "ADR-004",
    title: "Execução do código do jogador via compilação de GDScript em runtime, com captura de erro",
    context:
      "O jogador escreve código real (RF-011) e código é entrada não confiável que não pode travar o jogo (RF-012).",
    decision:
      "PlayerScriptRunner recebe o texto, cria um GDScript com source_code e reload(), valida que ele define play_turn, instancia e o invoca passando a WarriorFacade. Falha de compilação, exceção em runtime ou turno sem ação são capturadas e transformadas em um resultado de erro/turno-sem-ação, sem efeito no mundo.",
    consequences:
      "Fidelidade ao original com risco controlado; mensagens de erro ao jogador. Custo: depende de API da engine para compilar em runtime; tratar como detalhe de Application (não Domain).",
    status: "accepted",
    requirementKeys: ["RF-011", "RF-012", "RF-013"],
    rejectedAlternatives: [
      {
        alternative: "Usar a classe Expression da Godot para avaliar o código do jogador",
        reason: "Expression não suporta definição de classe/método com fluxo de controle como play_turn exige.",
      },
    ],
  },
  {
    key: "ADR-005",
    title: "Comportamento de inimigo por polimorfismo (uma estratégia por tipo de unidade)",
    context:
      "Sludge/thick atacam adjacente; archer/wizard atacam à distância; cativo não age (RF-008, RF-009). Strings/condicionais por tipo violam responsabilidade única.",
    decision:
      "Cada tipo de unidade conhece seu próprio comportamento de turno (UnitBehavior.act(state, self_pos) -> events/efeitos), despachado polimorficamente pelo TurnResolver na fase de reação dos inimigos. Atributos (HP, alcance, dano) ficam na própria unidade.",
    consequences:
      "Adicionar inimigo = nova classe; combate testável por tipo. Custo: pequena hierarquia de unidades.",
    status: "accepted",
    requirementKeys: ["RF-008", "RF-009", "RF-010"],
  },
  {
    key: "ADR-006",
    title: "Níveis declarativos (Resource) + LevelLoader; habilidades por nível como dado",
    context:
      "9 níveis com layout, unidades, escada, descrição, habilidades introduzidas, time bonus e ace score, fiéis ao original (RF-014, RF-015).",
    decision:
      "Cada nível é uma definição declarativa (LevelDefinition, Resource) com os dados do nível; LevelLoader.build(definition) -> LevelState monta o estado inicial. As habilidades introduzidas são dado do nível (usadas pela UI e, se desejado, para restringir a API exibida).",
    consequences:
      "Ajustar/balancear nível é editar dado; paridade verificável item a item. Custo: definir e versionar o formato.",
    status: "accepted",
    requirementKeys: ["RF-014", "RF-015"],
  },
  {
    key: "ADR-007",
    title: "Pontuação como serviço de domínio dirigido por eventos",
    context:
      "Pontos por inimigo/resgate + time bonus decrescente + comparação com ace score (RF-016).",
    decision:
      "ScoringService consome os TurnEvent acumulados e o número de turnos para computar o Score do nível (componentes + time bonus) e o veredito de ace contra o ace score da LevelDefinition. Puro, sem dependência da engine.",
    consequences:
      "Pontuação determinística e testável; desacoplada da renderização. Custo: garantir que todos os eventos pontuáveis sejam emitidos pelo resolver.",
    status: "accepted",
    requirementKeys: ["RF-016"],
  },
  {
    key: "ADR-008",
    title: "GameFlow como máquina de estados na Application; Presentation renderiza eventos e estado",
    context:
      "Menu, torre, transições, vitória/reinício, resultado, créditos e persistência de progresso (RF-018); renderização 2D e áudio dirigidos por estado/eventos (RF-017, RF-019).",
    decision:
      "Um GameFlowController (Application) modela os estados de jogo (menu, briefing de nível, jogando, resultado, créditos) e a progressão na torre, persistindo o progresso em user:// via um repositório. A Presentation (autoloads/scenes Godot) observa o estado e os TurnEvent para renderizar a grade, o HUD, as telas de transição e disparar SFX/música via um AudioManager.",
    consequences:
      "Fluxo testável separado do desenho; troca de telas sem tocar regra. Custo: mapear estado→cena e eventos→animação/áudio na borda.",
    status: "accepted",
    requirementKeys: ["RF-017", "RF-018", "RF-019"],
  },
];

export const components: IComponent[] = [
  {
    name: "LevelState",
    responsibility:
      "Value object imutável do estado do nível: grade de espaços, unidades com posição e direção, número do turno. Oferece consultas puras (espaço em uma posição/direção, unidade em posição) sem mutar.",
    dependsOn: ["Direction", "Unit"],
    requirementKeys: ["RF-001", "RF-007"],
  },
  {
    name: "Direction",
    responsibility:
      "VO/enum de direção (forward/backward) com offset na grade e direção oposta (para pivot). Fonte única de direção, sem strings mágicas.",
    dependsOn: [],
    requirementKeys: ["RF-002", "RF-006"],
  },
  {
    name: "Unit",
    responsibility:
      "Hierarquia de unidades (Warrior, Sludge, ThickSludge, Archer, Wizard, Captive) com saúde, atributos de combate e o próprio UnitBehavior de turno (polimórfico).",
    dependsOn: ["Direction"],
    requirementKeys: ["RF-008", "RF-009", "RF-010"],
  },
  {
    name: "Action",
    responsibility:
      "Objetos de comando tipados (Walk/Attack/Rest/Rescue/Pivot/Shoot) com sua direção, despachados pelo TurnResolver — sem if-cadeia de strings.",
    dependsOn: ["Direction"],
    requirementKeys: ["RF-002", "RF-006"],
  },
  {
    name: "TurnResolver",
    responsibility:
      "Serviço de domínio puro: resolve(state, action) aplica a ação do warrior, faz os inimigos reagirem e retorna TurnResult{ next_state, events }, incluindo o desfecho de vitória/derrota.",
    dependsOn: ["LevelState", "Action", "Unit", "TurnEvents"],
    requirementKeys: ["RF-002", "RF-003", "RF-004", "RF-009", "RF-010"],
  },
  {
    name: "TurnEvents",
    responsibility:
      "Tipos de evento de turno (moveu, atacou, dano, descansou, resgatou, atirou, venceu, morreu) que descrevem o que ocorreu — consumidos por pontuação e apresentação.",
    dependsOn: [],
    requirementKeys: ["RF-003", "RF-016", "RF-017"],
  },
  {
    name: "WarriorFacade",
    responsibility:
      "Superfície única exposta ao código do jogador: sentidos (consultas sobre snapshot) e ações (registram a Action; primeira vence). Não vaza LevelState nem outras unidades.",
    dependsOn: ["LevelState", "Action", "Direction"],
    requirementKeys: ["RF-005", "RF-007", "RF-011", "RNF-005"],
  },
  {
    name: "ScoringService",
    responsibility:
      "Calcula o Score do nível a partir dos TurnEvents e do número de turnos (pontos por inimigo/resgate + time bonus decrescente) e o veredito de ace contra o ace score do nível.",
    dependsOn: ["TurnEvents", "LevelDefinition"],
    requirementKeys: ["RF-016"],
  },
  {
    name: "LevelDefinition",
    responsibility:
      "Definição declarativa de um nível (layout, unidades e posições, escada, direção inicial, descrição, habilidades introduzidas, time bonus, ace score) — os 9 níveis da beginner tower.",
    dependsOn: [],
    requirementKeys: ["RF-014", "RF-015"],
  },
  {
    name: "LevelLoader",
    responsibility:
      "Monta o LevelState inicial a partir de uma LevelDefinition (Application). Sem regra de combate embutida.",
    dependsOn: ["LevelDefinition", "LevelState", "Unit"],
    requirementKeys: ["RF-014"],
  },
  {
    name: "PlayerScriptRunner",
    responsibility:
      "Compila o código GDScript do jogador em runtime, valida play_turn, executa-o por turno contra a WarriorFacade e captura erros/turno-sem-ação sem travar o jogo (Application).",
    dependsOn: ["WarriorFacade"],
    requirementKeys: ["RF-011", "RF-012", "RF-013"],
  },
  {
    name: "GameFlowController",
    responsibility:
      "Máquina de estados do jogo (menu → briefing → jogando → resultado → próximo/repetir → créditos) e progressão na torre, executando o loop de turnos e persistindo o progresso em user:// (Application).",
    dependsOn: ["LevelLoader", "TurnResolver", "PlayerScriptRunner", "ScoringService"],
    requirementKeys: ["RF-013", "RF-018"],
  },
  {
    name: "Presentation",
    responsibility:
      "Camada Godot: GridRenderer (grade 2D top-down + sprites placeholder), HUD (saúde/turno/descrição/pontuação), telas de transição/menu/créditos e AudioManager (SFX+música). Observa o estado do GameFlowController e os TurnEvents para renderizar e tocar áudio.",
    dependsOn: ["GameFlowController", "TurnEvents"],
    requirementKeys: ["RF-017", "RF-018", "RF-019"],
  },
];
