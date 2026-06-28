import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "003-editor-de-codigo-in-game",
  name: "Editor de codigo in-game",
  problem: `O jogador nao tem onde escrever o codigo. Hoje a logica play_turn vem embutida em reference_solutions.gd e o jogo roda sozinho — o jogador nunca programa nada. Num remake do Ruby Warrior, escrever a logica de turno E o jogo; sem a interface onde o jogador digita, roda e corrige sua propria logica, o produto nao e jogavel como foi concebido. Prioridade numero 2 da correcao de rumo.`,
  productRequirementKeys: ["PR-010"],
  goals: [
    "Painel de edicao in-game (CodeEdit) com syntax highlight de GDScript, fonte monoespacada e numeracao de linhas.",
    "Botoes Rodar (compila e executa o codigo contra a fachada do warrior via PlayerScriptRunner ja existente), Resetar (volta ao esqueleto inicial do nivel) e Ver solucao de referencia.",
    "Persistir o codigo do jogador por nivel em user:// para nao se perder entre sessoes.",
    "Exibir erros de compilacao e de runtime de forma legivel junto ao editor, sem travar o jogo (consome o tratamento de erro de RF-012 da feature 001).",
    "Esqueleto inicial por nivel: assinatura play_turn(warrior) com as habilidades disponiveis ate aquele nivel sinalizadas.",
  ],
  outOfScope: [
    "Autocomplete, lint em tempo real, multiplos arquivos ou breakpoints de linha.",
    "A execucao/compilacao do codigo em si — ja existe no PlayerScriptRunner (feature 001); aqui e a UI que a aciona.",
    "Sandbox alem da fachada ja existente (RNF-005 da feature 001).",
    "Renderizacao grafica (002), inspecao passo-a-passo (004) e audio (005).",
  ],
  productDecisions: [
    "Jogador escreve GDScript real (play_turn), nao blocos (ratificado em CLR-001 da feature 001).",
    "O editor liga no PlayerScriptRunner existente, que ja compila GDScript em runtime.",
    "Codigo do jogador persistido localmente por nivel em user://.",
  ],
  phase: "done",
  createdAt: "2026-06-27",
};
