import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-001",
    kind: "functional",
    description:
      "O nível sandbox deve estar listado no menu/tela de seleção de níveis (feature 009) como o primeiro item da lista, sempre desbloqueado independente do progresso do jogador na torre.",
    priority: "high",
    rationale: "Integrado à feature 009 (seleção de níveis); não força acesso automático na 1ª run — respeita quem já conhece o jogo.",
  },
  {
    key: "RF-002",
    kind: "functional",
    description:
      "O nível sandbox deve ter layout fixo: corredor horizontal curto (3–5 tiles), 1 escada ao final e, opcionalmente, 1 sludge fraco (configurável no LevelData). O objetivo é chegar à escada; havendo o sludge, um único ataque deve ser suficiente para eliminá-lo.",
    priority: "highest",
  },
  {
    key: "RF-003",
    kind: "functional",
    description:
      "Ao concluir o sandbox (warrior sobe a escada), o jogo deve transitar imediatamente para o nível 1 da beginner tower, sem exibir tela de resultado, pontuação ou resumo intermediário.",
    priority: "highest",
    rationale: "Decisão confirmada na clarify: sandbox não pontua nem exibe tela de transição.",
  },
  {
    key: "RF-004",
    kind: "functional",
    description:
      "O sandbox deve exibir, na tela de jogo, um texto de orientação fixo e genérico de 1–2 linhas (ex.: 'Use walk!, feel e attack! para chegar à escada.') visível durante toda a duração do nível, não adaptativo.",
    priority: "high",
  },
  {
    key: "RF-005",
    kind: "functional",
    description:
      "O sandbox NÃO deve registrar nem exibir pontuação (time bonus, rescue bonus, ace/clear bonus) e o resultado não deve afetar a progressão nem o score acumulado da beginner tower.",
    priority: "highest",
    rationale: "Sandbox é espaço de prática sem consequências de pontuação.",
  },
  {
    key: "RNF-001",
    kind: "non_functional",
    description:
      "A implementação do sandbox deve reutilizar exclusivamente os sistemas existentes (motor de turnos, LevelState, entidades sludge, ScreenManager da feature 006, editor de código da feature 003) sem adicionar novo subsistema ou nova camada de domínio.",
    priority: "high",
    rationale: "Requisito explícito do feature.ts: escopo contido, sem novo subsistema.",
  },
];

