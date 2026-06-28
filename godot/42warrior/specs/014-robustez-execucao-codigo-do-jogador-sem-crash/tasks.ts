import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-140 — não-crash p/ runtime + reporte legível ──────────────────────────────
  {
    key: "T-140",
    storyKey: "US-140",
    summary: "Endurecer a execução de play_turn no PlayerScriptRunner para capturar falha de runtime (método inexistente/null/tipo/assert) → estado de erro + no-op do turno, sem crashar, e produzir mensagem legível (causa/linha quando disponível). Mecanismo a critério do dev (GDScript sem try/catch)",
    definitionOfDone:
      "Teste GUT: alimentar o runner com play_turn que dispara erro de runtime — o runner NÃO crasha, fica has_error/no-op e expõe mensagem legível; o caminho de sintaxe (já guardado) permanece verde (RF-140, RF-141, RF-143).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-141 — guarda contra execução que não termina ──────────────────────────────
  {
    key: "T-141",
    storyKey: "US-141",
    summary: "Adicionar guarda contra execução que não termina (loop/recursão) durante um turno — interromper com segurança e reportar como erro, sem travar o jogo",
    definitionOfDone:
      "Teste GUT: play_turn com loop/recursão sem fim — a execução do turno é interrompida com segurança, reportada como erro e o jogo segue responsivo (RF-142).",
    status: "done",
    dependsOn: ["T-140"],
    parallel: false,
    assignee: null,
  },
  // ── US-142 — cobertura dos 3 caminhos + prova por teste ──────────────────────────
  {
    key: "T-142",
    storyKey: "US-142",
    summary: "Garantir que game_controller, replay (009) e sandbox (010) usam o PlayerScriptRunner endurecido e exibem o erro na ErrorView (mesma robustez nos 3 caminhos)",
    definitionOfDone:
      "Nos 3 caminhos que rodam código do jogador, código com erro NÃO crasha e o erro aparece legível na ErrorView; verificação por inspeção + teste cobre que os 3 usam o runner endurecido (RF-144, RF-143).",
    status: "done",
    dependsOn: ["T-140", "T-141"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-143",
    storyKey: "US-142",
    summary: "Suíte GUT de regressão dos 3 caminhos de erro (sintaxe, runtime, loop/recursão), reproduzindo o crash relatado ANTES da correção e provando a correção",
    definitionOfDone:
      "Há teste(s) GUT para (a) sintaxe inválida, (b) runtime, (c) loop/recursão — em todos o runner não crasha (has_error/no-op) e reporta; o crash relatado foi reproduzido por teste antes da correção; a suíte permanece 100% verde (RNF-140).",
    status: "done",
    dependsOn: ["T-140", "T-141"],
    parallel: true,
    assignee: null,
  },
];
