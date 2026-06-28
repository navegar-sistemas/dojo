import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-200",
    kind: "functional",
    description:
      "DEPTH-GUARD DE RECURSÃO: o runner do código do jogador (player_script_runner) instrumenta a execução com um BOUND DE PROFUNDIDADE — na entrada de cada chamada de função do jogador, conta a profundidade da pilha de chamadas do jogador e, ao exceder um teto seguro, INTERROMPE o turno (no-op) e reporta erro legível, SEM crash/Stack-overflow. Corrige a PREMISSA FALSA atual ('recursão aborta nativamente'): o runner NÃO pode depender de abort nativo da engine — o guard é explícito e determinístico.",
    priority: "highest",
    rationale: "CLR-001/002 (PO cmqxwb2yr): recursão infinita estoura a pilha hoje; o depth-guard é o mecanismo que falta (o loop-guard só cobre while).",
  },
  {
    key: "RF-201",
    kind: "functional",
    description:
      "PARIDADE E COBERTURA: recursão infinita recebe o MESMO tratamento comportamental do while-infinito da 014 (RF-142) — turno interrompido com segurança + mensagem legível na ErrorView (reusa RF-143) — e vale em TODAS as superfícies que executam código do jogador: tela de jogo (game_controller), seleção/replay (009) e sandbox (010) (reusa RF-144). Não reescreve a robustez de while/sintaxe/runtime da 014; estende-a à recursão.",
    priority: "high",
    rationale: "CLR-001/003: a promessa de robustez da 014 deve valer para recursão em todas as superfícies, sem duplicar o que já existe.",
  },
  {
    key: "RNF-200",
    kind: "non_functional",
    description:
      "PROVADO POR TESTE, SEM MÁSCARA: há ≥1 teste GUT que REPRODUZ o crash de recursão infinita ANTES da correção e, após o fix, verifica no-op real (has_error/reporte) — 0 uso de pending/skip para mascarar; e ≥1 teste de SINTAXE-INVÁLIDA preenchendo o gap histórico. check.sh permanece 100% verde, com 0 regressão da 014 (RF-140..144) e das demais features (001–019).",
    priority: "highest",
    rationale: "CLR-002 (PO): o gap que deixou o defeito passar verde foi teste inadequado; o critério exige reprodução real do crash + cobertura de sintaxe, sem pending/skip.",
  },
];
