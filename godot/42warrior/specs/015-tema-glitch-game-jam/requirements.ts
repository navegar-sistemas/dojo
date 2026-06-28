import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── P0 — combo mínimo (essencial) ────────────────────────────────────────────────
  {
    key: "RF-150",
    kind: "functional",
    description:
      "CONCEITO 'Kernel corrompido da 42': um fio narrativo apresenta a torre como um mainframe da 42 infectado e o warrior como um processo de debug que sobe limpando a corrupção, presente nas telas, transições e textos do jogo.",
    priority: "highest",
    rationale: "CLR-001: tema perceptível em CONCEITO, casando Ruby Warrior + glitch + identidade 42.",
  },
  {
    key: "RF-151",
    kind: "functional",
    description:
      "MECÂNICA (obrigatória): quando o script do jogador lança erro/exceção (tratamento já existente), o mundo glitcha DE VERDADE de forma DETERMINÍSTICA (warrior/tela/tile corrompem) além do log no console; o mesmo erro no mesmo estado produz o mesmo glitch (scriptado/seedado), reproduzível por teste.",
    priority: "highest",
    rationale: "CLR-002/003: liga o tema ao núcleo (programar); glitch na jogabilidade, determinístico.",
  },
  {
    key: "RF-152",
    kind: "functional",
    description:
      "ESTÉTICA: há pós-processo de glitch na câmera (RGB split / aberração cromática / scanlines) cuja intensidade ESCALA com eventos de turno — intensificando em dano, morte e erro do código — e relaxando fora desses eventos.",
    priority: "highest",
    rationale: "CLR-001: estética glitch reativa ao estado, acionada pelos turn_events.",
  },
  {
    key: "RF-153",
    kind: "functional",
    description:
      "CORRUPÇÃO PROGRESSIVA DA UI: quanto mais alto o andar na torre, mais a interface degrada de forma determinística por andar (scanlines, texto embaralhado, RGB split), comunicando a corrupção crescente do kernel.",
    priority: "high",
    rationale: "CLR-001: o tema escala com o progresso; determinístico por andar.",
  },
  {
    key: "RF-154",
    kind: "functional",
    description:
      "IDENTIDADE 42/Unix: as mensagens de erro e feedback usam a língua Unix/42 (ex.: 'segfault (core dumped)', 'command not found', 'exit 0'), reforçando a identidade terminal/hacker da 42.",
    priority: "high",
    rationale: "CLR-001: identidade 42 perceptível na linguagem do jogo.",
  },
  // ── P1 — reforço (se couber no tempo) ────────────────────────────────────────────
  {
    key: "RF-155",
    kind: "functional",
    description:
      "Há ao menos uma mecânica de glitch DETERMINÍSTICA por andar que o jogador contorna no código: entidades cintilantes que existem em turnos alternados num padrão fixo OU uma ação corrompida scriptada (ex.: corredor que altera walk!/feel de forma fixa) — sempre seedada/reproduzível.",
    priority: "medium",
    rationale: "P1/CLR-003: aprofunda o glitch na jogabilidade sem RNG.",
  },
  {
    key: "RF-156",
    kind: "functional",
    description:
      "O sprite do warrior/entidades corrompe visualmente em dano/morte (pixel-sort/static), acionado pelos turn_events existentes (DAMAGED/DIED), sem duplicar regra na cena.",
    priority: "medium",
    rationale: "P1: reforço estético acoplado aos eventos de turno.",
  },
  {
    key: "RF-157",
    kind: "functional",
    description:
      "As transições entre telas/níveis usam um efeito datamosh (corrupção de quadro), coerente com o tema glitch.",
    priority: "low",
    rationale: "P1: polish de transição temática.",
  },
  {
    key: "RF-158",
    kind: "functional",
    description:
      "O áudio corrompe com o estado (bit-crush/distorção) quando o HP está baixo ou o código falha, reforçando o tema pelo som.",
    priority: "low",
    rationale: "P1: camada de áudio do tema, reativa ao estado.",
  },
  // ── P2 — nice-to-have (backlog) ──────────────────────────────────────────────────
  {
    key: "RF-159",
    kind: "functional",
    description:
      "Backlog de aprofundamento (nice-to-have): glitch-through-walls como puzzle de 1 nível; um 'falso crash' encenado em momento-chave; e/ou a variação narrativa 'o warrior é o glitch' — qualquer um determinístico e contido, registrado como candidato futuro.",
    priority: "low",
    rationale: "P2: ideias de maior risco/escopo, mantidas no backlog sem comprometer o P0.",
  },
  // ── RNF — determinismo e não-regressão ───────────────────────────────────────────
  {
    key: "RNF-150",
    kind: "non_functional",
    description:
      "Determinismo sagrado: toda regra de glitch (que afete o turno/estado) é scriptada/seedada — 0 uso de RNG injusto — e o mesmo estado+seed produz o mesmo resultado, coberto por teste de domínio; efeitos puramente visuais/áudio ficam na apresentação; nada das features 001–006 regride (suíte de domínio permanece 100% verde).",
    priority: "highest",
    rationale: "CLR-003/006: determinismo do turno + domínio independente da engine + tema aditivo.",
  },
];
