import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "020-robustez-contra-recursao-infinita-no-codigo-do-jog",
  name: "Robustez contra recursao infinita no codigo do jogador",
  problem:
    "A feature 014 prometeu robustez contra código ruim do jogador, mas a RECURSÃO INFINITA NÃO é tratada: o RF-142 diz 'loop/recursão' porém a implementação (loop-guard) só cobre o caso `while`; recursão infinita estoura a pilha e CRASHA o motor (Stack overflow/underflow). A premissa de que 'recursão aborta nativamente' (comentário em player_script_runner.gd) é FALSA. O Matheus reportou o crash e o tech-lead reproduziu — defeito P0 real (cmqxwb2yr): quebra o fluxo CORE (o jogador escreve código e a mecânica central), supera as telas P1 e é PRÉ-REQUISITO do web export (o smoke do código do jogador no WASM exige o runner robusto — um crash no desktop crasha no web igual). Esta fix-feature dá rastro ao fix: nomeia recursão-depth explicitamente e preenche o gap de teste que deixou isso passar verde.",
  productRequirementKeys: ["PR-010"],
  goals: [
    "Recursão infinita no código do jogador → o processo SOBREVIVE (vira no-op + erro legível reportado ao jogador), NUNCA crash/Stack-overflow — igual ao tratamento do while-infinito da 014, estendendo o loop-guard à recursão via bound de profundidade (depth-guard).",
    "Corrigir a PREMISSA FALSA: o runner não pode depender de abort nativo de recursão; precisa de um depth-guard explícito na entrada de cada chamada do código do jogador, com teto seguro.",
    "Preencher o gap histórico de TESTE: teste real de recursão infinita (no-op verificado, sem máscara/pending) + teste de SINTAXE-INVÁLIDA; check.sh 100% verde sem pending/skip.",
    "Traceability (pedido do PO cmqxwb2yr): RF nomeando recursão-depth; cadeia íntegra — o RF-142 da 014 ficou sem rastro do mecanismo de recursão, esta feature o supre.",
  ],
  outOfScope: [
    "Não reescrever a robustez de while/sintaxe/runtime já entregue na 014 (RF-140..144); reusa/estende, não duplica.",
    "O valor exato do teto de profundidade é decisão de IMPLEMENTAÇÃO (dev), não prescrita no spec — o spec exige apenas que exista um bound seguro e determinístico.",
    "Não otimizar performance do runner além do depth-guard necessário.",
  ],
  productDecisions: [
    "Mecanismo = FIX-FEATURE curta (a 014 está phase=done com sprint fechado; precedente 017) tracando o mesmo PR-010, em vez de reabrir a 014.",
    "Robustez contra 'código ruim' do produto INCLUI recursão, não só while — decisão do PO (cmqxwb2yr) ratificando o report do Matheus.",
    "É PRÉ-REQUISITO do web export (cmqxwb2zw): o smoke web do código do jogador só vale após este fix.",
  ],
  phase: "implementing",
  createdAt: "2026-06-28",
};
