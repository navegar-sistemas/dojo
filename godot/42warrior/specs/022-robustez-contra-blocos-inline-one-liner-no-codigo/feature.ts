import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "022-robustez-contra-blocos-inline-one-liner-no-codigo",
  name: "Robustez contra blocos inline one-liner no codigo do jogador",
  problem:
    "A 020 fechou a recursão infinita, mas restou um BURACO no escopo declarado do T-200/RF-143 ('recursão infinita NÃO crasha, idêntico nas superfícies'): código do jogador com corpo INLINE/one-liner (ex.: `func play_turn(w): while true: pass`, ou statements inline) ESCAPAVA do loop/depth-guard — a instrumentação só cobria corpos MULTI-LINHA → Stack overflow → CRASH. Ou seja, o T-200 estava done com um buraco. O Matheus reportou o crash (P0) e commitou o fix de produção (branch fix-020-oneliner-guard @4b3f920, JÁ na main): `_normalize_inline_blocks()` quebra corpos inline em multi-linha ANTES da instrumentação, +4 testes de regressão (347/347). Esta fix-feature dá RASTRO a esse fix (pedido do PO cmqy0fd2g): sem US/T, as 81 linhas de produção + 4 testes ficam órfãs e quebram a cadeia PR→RF→US→T. Precedente exato: a 020 nasceu assim para um buraco da 014, sem reabrir a 014.",
  productRequirementKeys: ["PR-010"],
  goals: [
    "Código do jogador com corpo INLINE/one-liner (while/recursão inline) recebe o MESMO tratamento robusto do multi-linha — no-op + erro reportado, SEM crash/Stack overflow — porque o runner NORMALIZA blocos inline para multi-linha antes de instrumentar os guards.",
    "Provado pelos testes do fix do Matheus: ≥4 testes de regressão (recursão one-liner + while inline) verdes nas superfícies aplicáveis, sem máscara/pending; 0-regressão (347/347).",
    "Traceability (pedido do PO cmqy0fd2g): a cadeia PR-010→RF→US→T cobre o caso inline/one-liner, espelhando o fix já na main; nenhuma linha de produção fica órfã.",
  ],
  outOfScope: [
    "Não reescrever a robustez de multi-linha (while/recursão/sintaxe) já entregue na 014/020; estende-a ao caso inline.",
    "O mecanismo/heurística de normalização inline é decisão de IMPLEMENTAÇÃO (já feita no 4b3f920); o spec exige apenas que o caso inline NÃO escape do guard.",
  ],
  productDecisions: [
    "Mecanismo = FIX-FEATURE (precedente 020←014: novo número p/ um buraco de feature done, sem reabrir a 020 done/closed) tracando o mesmo PR-010.",
    "O código JÁ está na main (4b3f920, autor Matheus, P0) + o PO aceita (cmqy0fd2g: 'não é bloqueio, o fix é do Usuário'); a feature dá o rastro e marca done=integrado.",
  ],
  phase: "done",
  createdAt: "2026-06-28",
};
