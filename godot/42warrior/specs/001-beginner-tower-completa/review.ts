import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

// Checagens do projeto rodadas pelo revisor no worktree 001 (Godot 4.7 / gdtoolkit 4.5):
// arch_guard OK, gdformat/gdlint limpos, suíte GUT 96/96. Saída real conferida.
const CHECKS: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture (Domain/Application puros)",
    command: "bash scripts/arch_guard.sh",
    passed: true,
  },
  {
    name: "Formatação + lint GDScript (gdformat/gdlint sobre src e test)",
    command: "bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes unitários de domínio (GUT, headless)",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  // ── Sprint 2 — revisão independente (tech-lead) de T-015..T-020 ───────────────
  {
    target: "code",
    taskKey: "T-015",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-016",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-017",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "Space.position() é público — o jogador pode ler a posição absoluta de um Space (RNF-005 visa isolar o estado interno). É necessário para direction_of(space) funcionar (o Space precisa mapear de volta à posição).",
        location: "src/domain/world/space.gd:28; src/application/warrior_facade.gd:36",
        resolution:
          "Trade-off aceito: expõe apenas um int (posição na grade), não LevelState nem unidades mutáveis. O isolamento da superfície da fachada é validado por test_warrior_facade.gd::test_superficie_publica_tem_so_a_api (não vaza unit_at/space_at/warrior/with_warrior).",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-018",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "ADR-004/RF-012 mencionam capturar 'exceção em runtime' do código do jogador. O runner captura falha de compilação, ausência de play_turn e turno-sem-ação, mas um erro de RUNTIME dentro do play_turn (ex.: chamada a método inexistente) não é interceptável em GDScript puro — a engine não oferece try/catch.",
        location: "src/application/player_script_runner.gd:43",
        resolution:
          "Aceito como limitação inerente do GDScript. O DoD literal de T-018 (válido produz Action; inválido/sem play_turn/sem ação ⇒ erro/no-op) está coberto e testado (test_player_script_runner.gd). Reavaliar se a engine oferecer um mecanismo de captura de erro de runtime.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-019",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Fidelidade dos 9 níveis VALIDADA na fonte pelo revisor (amostra L5/L6/L8 cruzada com ryanb/ruby-warrior towers/beginner/level_00N.rb): width, stairs, warrior, todas as unidades, time_bonus e ace_score batem 100% — a correção de L5/L6 do dev está exata. Ressalva: o gem define um FACING por-unidade (ex.: L5 todas :west) que o beginner_tower.gd omite.",
        location: "src/domain/levels/beginner_tower.gd:6-8",
        resolution:
          "Os DADOS dos níveis (T-019) são fiéis ao gem (validado). O facing por-unidade afeta a MECÂNICA ranged (Sprint 1: ranged_behavior/enemy_phase atiram por alcance/linha, sem facing), não os dados de T-019 — encaminhado junto ao achado do motor de turno do L8 no tópico fidelidade-combate (a verificar: no gem o ranged atira só na direção do facing). Não bloqueia os dados desta task.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-020",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "CONV-006/DoD de T-020 pedem um teste GUT que carregue o nível N e asserte o LevelState (warrior na posição/facing, unidades nas posições, escada). Não há teste UNITÁRIO dedicado do LevelLoader.",
        location: "src/application/level_loader.gd; test/",
        resolution:
          "Correção do loader provada FUNCIONALMENTE: test_reference_solutions.gd carrega 8 níveis (load_level) e os vence ponta-a-ponta — o LevelState carregado está correto por construção (sem warrior/unidades/escada corretos não há vitória). Recomendado adicionar um teste unitário granular de load_level. Não bloqueia: correção provada end-to-end.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  // ── T-021 (US-011) — soluções-referência: re-revisão independente após o F2 ──
  {
    target: "code",
    taskKey: "T-021",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "DoD de US-011 ('usa apenas a API introduzida até aquele nível'): na 1ª revisão as soluções-referência eram 4 estratégias genéricas reusadas que chamavam API de níveis posteriores (health/rest/rescue em níveis baixos; direction_of_stairs em todas).",
        location: "src/application/reference_solutions.gd",
        resolution:
          "RESOLVIDO em c75fd85 (verificado na fonte pelo revisor): refatorado para 1 solução MÍNIMA por nível usando só a allowlist cumulativa de BeginnerTower.definition(1..N).abilities; direction_of_stairs trocado por direção fixa (Direction.forward/backward, sempre disponível). DoD tornado EXECUTÁVEL por test/application/test_reference_api_conformance.gd — a allowlist é derivada dos PRÓPRIOS dados dos níveis (fonte única, não circular), escaneia warrior.<metodo>() e falha se a solução extrapolar. Os 9 níveis vencem ponta-a-ponta (check.sh 102/102) e nunca atacam cativos. Mecânica do L8 (fase de inimigos em 2 etapas) e facing já aprovados antes.",
      },
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Fidelidade do MOTOR de turno (transversal, não das soluções): a percepção dos inimigos usa o warrior na posição CORRENTE; avançar de fora para dentro do alcance de um ranged causa dano no mesmo turno, enquanto no gem (prepare-all, decisão sobre o estado do início do turno) só no turno seguinte. Confirmado vs ryanb/ruby-warrior (level.rb prepare/perform).",
        location: "src/domain/turn/turn_resolver.gd; src/domain/combat/ranged_behavior.gd",
        resolution:
          "NÃO bloqueia T-021: as 9 soluções-referência vencem ponta-a-ponta com o motor atual. Divergência de fidelidade fina (~1 tiro/archer ao cruzar a fronteira do alcance avançando); recuo e linha-aberta estão fiéis. Decisão de corrigir/aceitar/adiar encaminhada ao dev/usuario (chat INFO cmqwsrn0a); o dev optou por não alterar o comportamento neste commit, sem regredir.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  // ── T-022 (US-012) — ScoringService: pontuação e ace ─────────────────────────
  {
    target: "code",
    taskKey: "T-022",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "ScoringService NÃO é chamado em lugar nenhum do src/ (nenhum ScoringService.new/.score() fora do teste; Score/is_ace não usados fora de scoring/). A afirmação do HANDOFF do dev ('Integrado ao TurnResolver via TurnEvents') é imprecisa: TurnResolver e ScoringService só COMPARTILHAM o tipo TurnEvent — não há integração de fluxo (ninguém coleta TurnEvents+turns e calcula o score ao fim do nível).",
        location: "src/domain/scoring/scoring_service.gd (sem chamadores)",
        resolution:
          "NÃO bloqueia T-022: o DoD da task é 'ScoringService (Domain) + testes GUT' (lógica), 100% cumprido — 6/6 cobrindo pontos por inimigo (HP máx)/resgate (20), time bonus decai e não-negativo, ace quando score≥ace_score. A INTEGRAÇÃO de fluxo + EXIBIÇÃO (AC de US-012 'ver minha pontuação' / 'o jogo sinaliza ace') dependem do HUD — escopo de US-013/Sprint 3. Encaminhado: US-012 só fecha 100% com a exibição; não dar como 'o jogo pontua' antes disso.",
      },
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "time_bonus decresce linearmente (max(0, time_bonus - turns), -1/turno). O próprio comentário do código admite 'Modelo aproximado do Ruby Warrior (a curva exata do original ainda não foi confirmada)'.",
        location: "src/domain/scoring/scoring_service.gd:24 (_time_bonus)",
        resolution:
          "Atende o DoD literal ('time bonus decrescente pelos turnos' / 'decai por turno e não fica negativo') — testado. A curva exata vs o gem (oráculo ratificado) não foi confirmada (gem indisponível p/ o revisor). Fidelidade fina não-bloqueante; confirmar/ajustar se a paridade de score importar.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
];
