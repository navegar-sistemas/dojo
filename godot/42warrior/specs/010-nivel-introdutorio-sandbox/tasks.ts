import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-076",
    storyKey: "US-070",
    summary: "Adicionar campos is_sandbox: bool e hint_text: String a LevelData e definir o LevelData do sandbox no LevelRegistry (level_id=0, corredor 3–5 tiles, escada, 1 sludge fraco opcional)",
    definitionOfDone: "LevelData aceita is_sandbox e hint_text sem erros de tipo; LevelRegistry expõe level_id=0 com layout correto; teste de domínio verifica que o sandbox tem is_sandbox=true e hint_text não-vazio.",
    status: "todo",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-077",
    storyKey: "US-071",
    summary: "Adicionar Label de hint_text no HUD da GameScreen: visível quando LevelData.is_sandbox=true, oculta nos demais níveis",
    definitionOfDone: "Label exibe o hint_text do sandbox durante toda a execução; Label está oculta em níveis normais; nenhum teste de nível existente regride.",
    status: "todo",
    dependsOn: ["T-076"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-078",
    storyKey: "US-072",
    summary: "Implementar branch is_sandbox no ProgressionManager: ao concluir sandbox pular ResultScreen e navegar via ScreenManager direto ao nível 1, sem registrar score",
    definitionOfDone: "Ao concluir sandbox nenhuma ResultScreen é exibida; score da torre não é alterado; jogador vai para nível 1; teste de domínio cobre os dois caminhos (sandbox vs. nível normal).",
    status: "todo",
    dependsOn: ["T-076"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-079",
    storyKey: "US-069",
    summary: "Integrar sandbox na tela de seleção de níveis (feature 009): listado em primeiro, sempre desbloqueado em SaveData (level_id=0 nunca é bloqueado)",
    definitionOfDone: "Sandbox aparece como primeiro item na seleção; desbloqueado independente do progresso; ao selecionar carrega o LevelData do sandbox; teste de desbloqueio valida que level_id=0 é imune ao bloqueio de progressão.",
    status: "todo",
    dependsOn: ["T-076"],
    parallel: true,
    assignee: null,
  },
];
