import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Motor de turnos e estado (PR-001) ────────────────────────────────────────
  {
    key: "RF-001",
    kind: "functional",
    description:
      "O nível é representado por uma grade 1×N de espaços; cada espaço está vazio, contém uma unidade (warrior/inimigo/cativo), é a escada ou é parede. O estado do nível conhece a posição e a direção de cada unidade.",
    priority: "highest",
    rationale: "Base de todo o jogo; espelha o formato de corredor da beginner tower.",
  },
  {
    key: "RF-002",
    kind: "functional",
    description:
      "A cada turno o warrior executa no máximo UMA ação. Tentar efetivar mais de uma ação no mesmo turno é ignorado após a primeira, e isso é detectável/registrável.",
    priority: "highest",
    rationale: "Regra nuclear do Ruby Warrior (uma ação por turno).",
  },
  {
    key: "RF-003",
    kind: "functional",
    description:
      "A resolução de um turno é determinística: dado o mesmo estado do nível e a mesma ação, o próximo estado é sempre idêntico. Após a ação do warrior, cada inimigo vivo reage segundo sua IA.",
    priority: "highest",
    rationale: "Determinismo (ADR-002) garante testabilidade, justiça e replay.",
  },
  {
    key: "RF-004",
    kind: "functional",
    description:
      "O nível termina em vitória quando o warrior alcança a escada, e em derrota quando a saúde do warrior chega a 0. O resultado é exposto ao fluxo de jogo.",
    priority: "highest",
    rationale: "Condições de fim de nível.",
  },
  // ── API do warrior: sentidos e ações (PR-002) ────────────────────────────────
  {
    key: "RF-005",
    kind: "functional",
    description:
      "Sentidos do warrior são consultas sem efeito colateral e não consomem o turno: feel(direction)→Space, look(direction)→[Space×3], listen→[Space], health→int, direction_of_stairs→Direction, direction_of(space)→Direction. Podem ser chamados quantas vezes quiser por turno.",
    priority: "highest",
    rationale: "CQS: sentidos consultam; necessários para a lógica do jogador decidir.",
  },
  {
    key: "RF-006",
    kind: "functional",
    description:
      "Ações do warrior consomem o turno e aceitam direção (forward/backward) onde aplicável: walk!(dir) move um espaço; attack!(dir) ataca corpo-a-corpo a unidade adjacente (dano reduzido para trás); rest! recupera 10% da saúde máxima; rescue!(dir) liberta um cativo adjacente; pivot!(dir) gira o warrior; shoot!(dir) dispara atingindo a primeira unidade até 3 espaços.",
    priority: "highest",
    rationale: "Conjunto de ações da beginner tower; cada ação introduzida em seu nível.",
  },
  {
    key: "RF-007",
    kind: "functional",
    description:
      "Um objeto Space responde a consultas de predicado: empty?, stairs?, enemy?, captive?, wall?, e identifica o tipo da unidade que contém. Space é o que sentidos retornam, nunca a unidade mutável diretamente.",
    priority: "highest",
    rationale: "Encapsula o que o jogador pode saber de um espaço sem vazar estado interno.",
  },
  // ── Entidades e combate (PR-003) ─────────────────────────────────────────────
  {
    key: "RF-008",
    kind: "functional",
    description:
      "As unidades têm saúde e comportamento próprios: warrior (20 HP, dano de ataque, dano reduzido para trás), sludge (12 HP), thick sludge (24 HP), archer (7 HP, ataque à distância), wizard (3 HP, ataque à distância letal), captive (1 HP, não-hostil, só pode ser resgatado).",
    priority: "highest",
    rationale: "Paridade de unidades com o original (valores podem ser confirmados na implementação).",
  },
  {
    key: "RF-009",
    kind: "functional",
    description:
      "IA dos inimigos por turno: sludge/thick sludge atacam corpo-a-corpo quando o warrior está adjacente; archer e wizard atacam à distância dentro do alcance; cativo nunca ataca. Atacar um cativo é uma jogada inválida do ponto de vista do objetivo (não deve ser feito pela solução-referência).",
    priority: "highest",
    rationale: "Define a ameaça de cada nível e a estratégia de solução.",
  },
  {
    key: "RF-010",
    kind: "functional",
    description:
      "rest! recupera 10% da saúde máxima por turno e nunca ultrapassa o máximo; o warrior não regenera sozinho sem descansar. A saúde reinicia ao máximo no começo de cada nível.",
    priority: "high",
    rationale: "Mecânica de cura do original; base da estratégia de descansar quando seguro.",
  },
  // ── Roteiro do jogador (PR-005) ──────────────────────────────────────────────
  {
    key: "RF-011",
    kind: "functional",
    description:
      "O jogador fornece código GDScript que define uma classe com play_turn(warrior); o jogo compila esse código em runtime, instancia e chama play_turn a cada turno, passando uma fachada do warrior que expõe apenas a API pública (sentidos + ações).",
    priority: "highest",
    rationale: "Fidelidade ao modelo de jogo do Ruby Warrior; decisão do usuário por código real.",
  },
  {
    key: "RF-012",
    kind: "functional",
    description:
      "Erro no código do jogador (falha de compilação, exceção em runtime, ou nenhuma ação escolhida no turno) é capturado e comunicado ao jogador sem travar o jogo; o turno sem ação não altera o mundo (warrior fica parado).",
    priority: "high",
    rationale: "Robustez: código do jogador é entrada não confiável.",
  },
  {
    key: "RF-013",
    kind: "functional",
    description:
      "O jogo embarca uma solução-referência (código play_turn) para cada um dos 9 níveis, que resolve o nível ao ser executada.",
    priority: "medium",
    rationale: "Permite demonstrar o jogo e serve de teste de paridade ponta-a-ponta.",
  },
  // ── Beginner tower: 9 níveis (PR-004) ────────────────────────────────────────
  {
    key: "RF-014",
    kind: "functional",
    description:
      "Os 9 níveis da beginner tower são definidos como dados declarativos (layout, posições de unidades, posição da escada, direção inicial do warrior, descrição, habilidades introduzidas, time bonus e ace score) e montados por um LevelLoader.",
    priority: "highest",
    rationale: "ADR-003; reproduz a curva de dificuldade do original.",
  },
  {
    key: "RF-015",
    kind: "functional",
    description:
      "Cada nível introduz exatamente as habilidades/sentidos do original na ordem canônica (L1 walk; L2 feel+attack; L3 health+rest; L5 rescue; L7 pivot; L8 look+shoot) e contém as unidades e posições correspondentes.",
    priority: "high",
    rationale: "Progressão didática fiel é o coração do jogo.",
  },
  // ── Pontuação (PR-006) ───────────────────────────────────────────────────────
  {
    key: "RF-016",
    kind: "functional",
    description:
      "Ao concluir um nível, calcula-se a pontuação: pontos por inimigos derrotados e cativos resgatados, mais um time bonus que decai a cada turno gasto; compara-se com o ace score do nível e sinaliza-se 'ace' quando atingido ou superado.",
    priority: "high",
    rationale: "Sistema de pontuação do original; dá objetivo de otimização.",
  },
  // ── Apresentação e fluxo (PR-007, PR-008) ────────────────────────────────────
  {
    key: "RF-017",
    kind: "functional",
    description:
      "A camada Godot renderiza a grade 2D top-down, as unidades como sprites, a escada e o feedback de cada turno (movimento, ataque, dano, descanso, resgate, tiro), além de HUD com saúde, número do turno, descrição do nível e pontuação. Assets são placeholders com pontos de troca definidos.",
    priority: "high",
    rationale: "Torna o jogo jogável e legível; identidade 42 entra pelos assets.",
  },
  {
    key: "RF-018",
    kind: "functional",
    description:
      "O fluxo de jogo cobre: menu inicial, início da torre, telas de transição entre níveis (descrição + habilidades novas + narrativa), avanço ao próximo nível na vitória, reinício do nível, tela de resultado/pontuação, conclusão da torre e créditos. O progresso na torre é persistido localmente.",
    priority: "high",
    rationale: "Experiência completa de torre exigida para a entrega da jam.",
  },
  {
    key: "RF-019",
    kind: "functional",
    description:
      "O jogo reproduz áudio: efeitos sonoros para as ações/eventos (andar, atacar, levar dano, descansar, resgatar, atirar, vitória, derrota) e trilha sonora de fundo, com controle de volume básico.",
    priority: "medium",
    rationale: "Áudio completo (SFX+música) confirmado no escopo; eleva o polimento na jam.",
  },
  // ── Não-funcionais ───────────────────────────────────────────────────────────
  {
    key: "RNF-001",
    kind: "non_functional",
    description:
      "A camada Domain e Application é GDScript puro (RefCounted/Resource): 0 ocorrências de 'extends Node'/'Node2D' e 0 referências a tipos de cena/UI nesses diretórios; a dependência aponta sempre para dentro (Presentation→Application→Domain), com 0 imports de Application/Presentation dentro do Domain. Verificável por grep/lint.",
    priority: "highest",
    rationale: "Clean Architecture (ADR-001, CONV-002): domínio testável e independente da engine.",
  },
  {
    key: "RNF-002",
    kind: "non_functional",
    description:
      "Cada arquivo .gd define no máximo 1 classe com responsabilidade única e cada método faz uma só coisa (CQS); como limites objetivos de revisão: ≤ ~150 linhas por arquivo de domínio e ≤ ~20 linhas por método, com 0 métodos de ação que também consultem-e-mutem no mesmo corpo. Sem flags booleanas que ramifiquem responsabilidade.",
    priority: "highest",
    rationale: "Princípio central do projeto (CONV-001, CONV-003).",
  },
  {
    key: "RNF-003",
    kind: "non_functional",
    description:
      "100% das regras de Domain/Application (resolução de turno, combate, sentidos, IA de inimigo, pontuação, level loader) têm teste unitário determinístico (GUT) sem dependência de cena; o gate de testes roda com 0 falhas antes de qualquer task ser concluída, e cada teste produz o mesmo resultado em execuções repetidas.",
    priority: "high",
    rationale: "Determinismo + cobertura de regras provam paridade e evitam regressão (CONV-006).",
  },
  {
    key: "RNF-004",
    kind: "non_functional",
    description:
      "O código adere ao GDScript style guide com tipagem estática: gdformat reporta 0 arquivos a reformatar e gdlint reporta 0 violações em todo o projeto; 0 strings mágicas para direções/tipos (uso obrigatório de enums/constantes nomeadas).",
    priority: "high",
    rationale: "Qualidade verificável mecanicamente (CONV-004, CONV-005).",
  },
  {
    key: "RNF-005",
    kind: "non_functional",
    description:
      "A execução do código do jogador é isolada do estado interno: a fachada do warrior expõe exatamente os métodos públicos da API (os sentidos e ações de RF-005/RF-006 e nada além); o código do jogador tem 0 referências acessíveis ao LevelState, a outras unidades ou a nós de cena. Verificável por revisão da superfície da fachada (allowlist de métodos).",
    priority: "high",
    rationale: "Integridade das regras e da pontuação; evita trapaça e acoplamento.",
  },
];
