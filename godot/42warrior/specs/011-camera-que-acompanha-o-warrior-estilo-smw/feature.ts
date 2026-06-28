import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "011-camera-que-acompanha-o-warrior-estilo-smw",
  name: "Camera que acompanha o warrior estilo SMW",
  problem:
    "Na tela de jogo (src/presentation/dungeon_view.gd), a câmera só atualiza a posição DEPOIS que a animação do turno termina (_on_animations_done faz _camera.global_position = warrior_global_position()): durante o passo a câmera fica parada e depois corre atrás, gerando solavanco/atraso. _fit_camera() é inconsistente — para nível que cabe no viewport dá zoom para mostrar tudo e centraliza estático, e só para nível mais largo que a tela cola no warrior. Sempre centraliza o warrior no meio exato: 0 dead-zone, 0 lookahead, suavização fixa. O jogador não acompanha o warrior com fluidez nem vê o caminho à frente.",
  productRequirementKeys: ["PR-007"],
  goals: [
    "Acompanhamento contínuo: a câmera segue o warrior DURANTE o movimento (trilha o sprite a cada frame enquanto desliza entre tiles), com interpolação suave — sem snap pós-animação.",
    "Camera window / dead-zone (estilo SMW): faixa central onde o warrior se move sem mover a câmera; ela só rola ao aproximar-se da borda da janela.",
    "Forward focus / lookahead com histerese (estilo SMW): deslocar a câmera à frente na direção em que o warrior anda/encara; ao inverter de direção, manter a âncora atual até cruzar um limiar antes de trocar de lado (evita tremor em idas-e-vindas).",
    "Clamp nas bordas do nível (Camera2D limits): nunca rolar além das extremidades do corredor.",
    "Níveis curtos que cabem na tela: comportamento sensato e consistente, sem o zoom-pra-caber-e-snap atual.",
  ],
  outOfScope: [
    "Alterar o motor de turnos ou a API do warrior.",
    "Alterar o layout de painéis (editor/debug é a feature 012).",
    "Adicionar ou alterar níveis.",
  ],
  productDecisions: [],
  phase: "implementing",
  createdAt: "2026-06-28",
};
