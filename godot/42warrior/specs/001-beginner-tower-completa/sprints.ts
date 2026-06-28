import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Núcleo de domínio jogável",
    goal: "Ter o motor de turnos determinístico do Domain funcionando: estado do nível, sentidos, ações básicas (walk/attack/rest), unidades e combate com IA, vitória/derrota, e a base de testes/lint/arquitetura — tudo coberto por testes GUT.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-001", "US-002", "US-003", "US-004", "US-005", "US-007", "US-016"],
  },
  {
    id: 2,
    name: "Execução do jogador, níveis e pontuação",
    goal: "Permitir que o jogador escreva e rode código (play_turn) com isolamento e tratamento de erro, carregar os 9 níveis declarativos com soluções-referência, completar as ações restantes (rescue/pivot/shoot) e calcular pontuação/ace.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-006", "US-008", "US-009", "US-010", "US-011", "US-012"],
  },
  {
    id: 3,
    name: "Apresentação, fluxo de torre e áudio",
    goal: "Entregar a camada Godot jogável: renderização 2D top-down com HUD, fluxo de menu/torre/transições/resultado/créditos com progresso persistido, e áudio (SFX+música). [SUPERSEDED: US-013/014/015 foram planejadas na 001 mas NÃO executadas por ela — entregues pelas features irmãs 002 (UI/render+HUD), 006 (ScreenManager/arena/transições) e 005 (áudio/créditos). Sprint #3 fica future-superseded; status 'done' significaria entrega pela 001, que não ocorreu, por isso as stories seguem em backlog.]",
    state: "future",
    startDate: "",
    endDate: "",
    storyKeys: ["US-013", "US-014", "US-015"],
  },
];
