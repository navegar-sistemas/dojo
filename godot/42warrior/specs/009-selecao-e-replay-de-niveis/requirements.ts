import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Funcionais (PR-008 Fluxo/progressão + PR-006 Pontuação) ──────────────────────
  {
    key: "RF-090",
    kind: "functional",
    description:
      "Uma tela de seleção de níveis (tela nova no ScreenManager da feature 006), acessada pelo MENU PRINCIPAL, lista os níveis da tower com seu status (bloqueado / desbloqueado / vencido). Verificável: pelo menu principal, abre-se a tela de seleção listando os níveis com o status correto de cada um.",
    priority: "highest",
    rationale: "CLR-001 (009): tela nova no ScreenManager via menu principal (navegação de 1ª classe); base do replay (PR-008).",
  },
  {
    key: "RF-091",
    kind: "functional",
    description:
      "A tela de seleção exibe, por nível vencido, a MELHOR PONTUAÇÃO com o breakdown (time bonus, rescue bonus, ace/clear bonus). Verificável: cada nível vencido mostra a melhor pontuação e seu breakdown; níveis não vencidos não exibem pontuação.",
    priority: "highest",
    rationale: "CLR-003 (009) + PR-006: o breakdown é o que motiva o replay (otimização de score).",
  },
  {
    key: "RF-092",
    kind: "functional",
    description:
      "O jogador pode RE-ENTRAR num nível já vencido a partir da seleção, e o editor carrega o código salvo DAQUELE nível (arquivo separado por nível, ex.: user://code_level_N.gd), não o código compartilhado do fluxo normal. Verificável: re-entrar num nível N carrega o código de user://code_level_N.gd.",
    priority: "highest",
    rationale: "CLR-002 (009): re-jogar para otimizar exige preservar a solução por nível.",
  },
  {
    key: "RF-093",
    kind: "functional",
    description:
      "Ao re-jogar um nível, o score MÁXIMO daquele nível é preservado — atualiza somente se a nova run melhorar. Verificável: re-jogar com pontuação pior mantém o score máximo anterior; re-jogar melhor atualiza o máximo.",
    priority: "high",
    rationale: "CLR-002 (009) + PR-006: o objetivo do replay é otimizar; sobrescrever puniria a exploração.",
  },
  {
    key: "RF-094",
    kind: "functional",
    description:
      "A seleção integra-se ao fluxo de navegação do ScreenManager (006), uma-tela-por-vez, e o acesso à seleção/replay se dá SÓ pelo menu principal (sem replay pelo menu de pause). Verificável: a tela de seleção é montada via ScreenManager (1 tela de topo); busca por acesso à seleção pelo pause retorna 0 ocorrências.",
    priority: "high",
    rationale: "CLR-001 (009): só menu principal (sem pause-replay); coeso com a navegação uma-tela-por-vez da 006.",
  },
  // ── Não-funcional ────────────────────────────────────────────────────────────────
  {
    key: "RNF-090",
    kind: "non_functional",
    description:
      "O código por nível e o score máximo são persistidos em user:// (0 escrita em res://); a tela de seleção lê o progresso e os scores do armazenamento de progresso, sem caminho hardcoded. Verificável: 0 ocorrências de escrita em res:// para código/score; persistência confirmada em user://.",
    priority: "high",
    rationale: "CONV/persistência: estado do jogador vive em user:// (como ProgressStore/PlayerCodeStore já existentes), não em res:// (read-only do build).",
  },
];
