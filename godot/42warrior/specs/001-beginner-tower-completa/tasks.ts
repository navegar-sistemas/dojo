import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-016: base de testes, lint e guarda de arquitetura ─────────────────────
  {
    key: "T-001",
    storyKey: "US-016",
    summary:
      "Instalar o addon GUT e criar a estrutura de pastas (src/domain, src/application, test) com um script headless de execução de testes.",
    definitionOfDone:
      "O comando 'godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://test -gexit' executa e um teste smoke passa (0 falhas).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-002",
    storyKey: "US-016",
    summary:
      "Configurar gdformat/gdlint (gdtoolkit) e um guard de arquitetura (script que falha se algum .gd em src/domain ou src/application usar 'extends Node' ou referenciar tipos de cena/UI).",
    definitionOfDone:
      "gdformat --check e gdlint rodam com 0 violações no esqueleto; o guard de arquitetura retorna 0 (nenhuma violação) e falha propositalmente num arquivo de teste com 'extends Node'.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  // ── US-001: estado do nível e value objects ──────────────────────────────────
  {
    key: "T-003",
    storyKey: "US-001",
    summary:
      "Implementar o VO Direction (enum forward/backward) com offset na grade e direção oposta (para pivot).",
    definitionOfDone:
      "Testes GUT cobrem offset e oposto de cada direção e passam; nenhuma string mágica de direção no código.",
    status: "done",
    dependsOn: ["T-001"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-004",
    storyKey: "US-001",
    summary:
      "Implementar a base Unit e os tipos (Warrior, Sludge, ThickSludge, Archer, Wizard, Captive) com saúde e atributos de combate (HP/dano/alcance), sem IA ainda.",
    definitionOfDone:
      "Testes GUT verificam HP inicial e atributos de cada tipo e passam; cada tipo em seu próprio arquivo (responsabilidade única).",
    status: "done",
    dependsOn: ["T-003"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-005",
    storyKey: "US-001",
    summary:
      "Implementar o VO Space com os predicados empty?/stairs?/enemy?/captive?/wall? e identificação do tipo da unidade contida.",
    definitionOfDone:
      "Testes GUT cobrem cada predicado para espaços vazio/escada/inimigo/cativo/parede e passam.",
    status: "done",
    dependsOn: ["T-004"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-006",
    storyKey: "US-001",
    summary:
      "Implementar LevelState imutável (grade, unidades com posição e direção, número do turno) com consultas puras (space_at, unit_at) que não mutam.",
    definitionOfDone:
      "Testes GUT provam que consultas retornam o Space correto e que o estado original não é mutado após qualquer consulta; passam.",
    status: "done",
    dependsOn: ["T-005"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-004: sentidos ─────────────────────────────────────────────────────────
  {
    key: "T-007",
    storyKey: "US-004",
    summary:
      "Implementar os sentidos sobre um snapshot do LevelState: feel/look/listen/health/direction_of_stairs/direction_of, retornando VOs Space/Direction sem efeito colateral.",
    definitionOfDone:
      "Testes GUT cobrem cada sentido (incl. look com 3 espaços ordenados e direction_of_stairs) e provam que o estado não muda; passam.",
    status: "done",
    dependsOn: ["T-006"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-005 + US-002: ações e resolver ────────────────────────────────────────
  {
    key: "T-008",
    storyKey: "US-005",
    summary:
      "Implementar os objetos de comando Action tipados para Walk, Attack e Rest (cada um com sua direção quando aplicável).",
    definitionOfDone:
      "Testes GUT instanciam cada Action e verificam seu tipo/direção; sem if-cadeia de strings.",
    status: "done",
    dependsOn: ["T-003"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-014",
    storyKey: "US-002",
    summary:
      "Definir os tipos de TurnEvent (moveu, atacou, recebeu_dano, descansou, venceu, morreu) que descrevem o que ocorreu no turno.",
    definitionOfDone:
      "Testes GUT constroem cada evento com seus dados; tipos usados pelo resolver compilam.",
    status: "done",
    dependsOn: ["T-001"],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-010",
    storyKey: "US-002",
    summary:
      "Implementar o TurnResolver: resolve(state, action) com despacho por tipo de Action, retornando TurnResult{ next_state, events }, garantindo determinismo. (A garantia de UMA ação por turno é estrutural — o resolver recebe exatamente uma Action; a regra 'primeira registrada vence entre várias' é da WarriorFacade, US-008/Sprint 2, fronteira CQS.)",
    definitionOfDone:
      "Testes GUT provam: (a) mesmo estado+ação ⇒ mesmo next_state (determinismo); (b) Action base/desconhecida ⇒ no-op (estado inalterado além do turno); passam.",
    status: "done",
    dependsOn: ["T-006", "T-008", "T-014"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-009",
    storyKey: "US-005",
    summary:
      "Implementar os efeitos das ações no resolver: walk move um espaço; attack causa dano ao adjacente (reduzido para trás); rest cura 10% do máximo sem ultrapassar.",
    definitionOfDone:
      "Testes GUT cobrem walk em espaço vazio, attack frente vs trás (dano menor atrás) e rest com clamp no máximo; passam e emitem os TurnEvent corretos.",
    status: "done",
    dependsOn: ["T-010", "T-004"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-003: vitória/derrota ──────────────────────────────────────────────────
  {
    key: "T-011",
    storyKey: "US-003",
    summary:
      "Derivar o desfecho do nível no TurnResult: vitória quando o warrior alcança a escada; derrota quando a saúde do warrior chega a 0.",
    definitionOfDone:
      "Testes GUT cobrem vitória (warrior na escada) e derrota (HP 0) e passam; o desfecho é exposto ao chamador.",
    status: "done",
    dependsOn: ["T-010"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-007: comportamento dos inimigos ───────────────────────────────────────
  {
    key: "T-012",
    storyKey: "US-007",
    summary:
      "Implementar UnitBehavior polimórfico por tipo: sludge/thick atacam adjacente; archer/wizard atacam à distância dentro do alcance; captive é inerte.",
    definitionOfDone:
      "Testes GUT cobrem o comportamento de cada tipo isoladamente e passam; cada comportamento em sua própria classe (sem if-cadeia por tipo).",
    status: "done",
    dependsOn: ["T-004"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-013",
    storyKey: "US-007",
    summary:
      "Integrar a fase de reação dos inimigos ao resolver: após a ação do warrior, cada inimigo vivo age via UnitBehavior, aplicando dano ao warrior e emitindo eventos.",
    definitionOfDone:
      "Testes GUT de combate integrado (warrior adjacente a sludge leva dano; archer à distância acerta; cativo não age) passam.",
    status: "done",
    dependsOn: ["T-010", "T-012"],
    parallel: false,
    assignee: "usuario",
  },

  // ══════════════ SPRINT 2 — execução do jogador, níveis e pontuação ══════════════

  // ── US-006: ações rescue/pivot/shoot ─────────────────────────────────────────
  {
    key: "T-015",
    storyKey: "US-006",
    summary:
      "Criar os objetos de comando RescueAction, PivotAction e ShootAction (tipados, com direção quando aplicável).",
    definitionOfDone:
      "Testes GUT instanciam cada Action e verificam tipo/direção; todas estendem Action.",
    status: "done",
    dependsOn: ["T-008"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-016",
    storyKey: "US-006",
    summary:
      "Implementar os efeitos no ActionApplier: rescue! liberta o cativo adjacente (remove e emite RESCUED); pivot! inverte o facing do warrior; shoot! atinge a primeira unidade até 3 espaços na direção (emite SHOT/ENEMY_DEFEATED).",
    definitionOfDone:
      "Testes GUT cobrem rescue (cativo some, evento RESCUED), pivot (facing invertido, warrior não move) e shoot (primeira unidade na linha perde HP; bloqueio por unidade intermediária) e passam.",
    status: "done",
    dependsOn: ["T-015", "T-010"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-008: WarriorFacade ────────────────────────────────────────────────────
  {
    key: "T-017",
    storyKey: "US-008",
    summary:
      "Implementar a WarriorFacade (Application): expõe os sentidos (delegando a Senses) e as ações (registrando a 1ª Action escolhida; demais ignoradas). Não expõe LevelState nem outras unidades.",
    definitionOfDone:
      "Testes GUT provam: 1ª ação registrada vence; sentidos retornam os valores sobre o snapshot sem mutar; a superfície pública contém só os métodos da API (sentidos+ações).",
    status: "done",
    dependsOn: ["T-015", "T-007"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-009: PlayerScriptRunner ───────────────────────────────────────────────
  {
    key: "T-018",
    storyKey: "US-009",
    summary:
      "Implementar o PlayerScriptRunner (Application): compila o GDScript do jogador em runtime (source_code + reload()), valida que define play_turn, instancia e o invoca por turno contra a WarriorFacade; captura erro de compilação/execução e turno-sem-ação sem travar.",
    definitionOfDone:
      "Testes GUT: código válido com play_turn produz a Action escolhida; código inválido/sem play_turn/sem ação retorna resultado de erro/no-op sem exceção propagada.",
    status: "done",
    dependsOn: ["T-017"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-010: definições dos 9 níveis + loader ─────────────────────────────────
  {
    key: "T-019",
    storyKey: "US-010",
    summary:
      "Definir os 9 níveis da beginner tower como dados declarativos (LevelDefinition): largura, posições de unidades por tipo, posição da escada, facing inicial, descrição, habilidades introduzidas, time_bonus e ace_score, na ordem canônica.",
    definitionOfDone:
      "Testes GUT verificam que há 9 definições, com campos preenchidos e valores (time_bonus/ace_score) coerentes com o original por nível.",
    status: "done",
    dependsOn: ["T-004"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-020",
    storyKey: "US-010",
    summary:
      "Implementar o LevelLoader (Application): monta o LevelState inicial a partir de uma LevelDefinition (warrior, unidades por posição, escada, facing).",
    definitionOfDone:
      "Testes GUT: carregar o nível N produz um LevelState com warrior na posição/facing certos, unidades nas posições da definição e escada correta.",
    status: "done",
    dependsOn: ["T-019", "T-006"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-011: soluções-referência ──────────────────────────────────────────────
  {
    key: "T-021",
    storyKey: "US-011",
    summary:
      "Escrever uma solução-referência (código play_turn) para cada um dos 9 níveis e um teste ponta-a-ponta que roda cada solução pelo runner+resolver até o desfecho.",
    definitionOfDone:
      "Teste GUT ponta-a-ponta: cada um dos 9 níveis é VENCIDO pela sua solução-referência; nenhuma solução ataca cativo.",
    status: "done",
    dependsOn: ["T-018", "T-020", "T-016"],
    parallel: false,
    assignee: "usuario",
  },
  // ── US-012: pontuação e ace ──────────────────────────────────────────────────
  {
    key: "T-022",
    storyKey: "US-012",
    summary:
      "Implementar o ScoringService (Domain): a partir dos TurnEvent e do nº de turnos, calcula pontos (inimigos derrotados + cativos resgatados) + time bonus decrescente, e o veredito de ace contra o ace_score do nível.",
    definitionOfDone:
      "Testes GUT: pontos por inimigo/resgate corretos; time bonus decai por turno e não fica negativo; ace sinalizado quando score ≥ ace_score.",
    status: "done",
    dependsOn: ["T-014", "T-019"],
    parallel: false,
    assignee: "usuario",
  },
];
