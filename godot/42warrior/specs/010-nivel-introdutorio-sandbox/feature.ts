import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "010-nivel-introdutorio-sandbox",
  name: "Nível introdutório sandbox",
  problem:
    "O jogador iniciante entra direto no nível 1 da beginner tower sem um espaço de baixo risco para experimentar a API (walk!, feel, attack!) e o editor in-game. Falta um 'nível 0' de prática antes da torre valer pontuação — o que torna a curva inicial mais íngreme e o primeiro contato com o loop (escrever código → rodar → ver turnos) mais intimidante.",
  productRequirementKeys: ["PR-004"],
  goals: [
    "Adicionar um único nível introdutório/sandbox ANTES do nível 1: corredor curto, 0 ou 1 inimigo fraco, objetivo trivial (andar até a escada ou um ataque), sem contar pontuação na torre.",
    "Reusar o motor de turnos, o ScreenManager (feature 006) e o editor in-game existentes — sem novo subsistema.",
    "Exibir um texto curto de orientação na própria tela do sandbox (não overlay interativo passo-a-passo).",
  ],
  outOfScope: [
    "Tutorial interativo guiado com overlays/setas passo-a-passo.",
    "Alterar os 9 níveis existentes da beginner tower.",
    "Mudar mecânica de combate ou regras de pontuação.",
  ],
  productDecisions: [],
  phase: "implementing",
  createdAt: "2026-06-28",
};
