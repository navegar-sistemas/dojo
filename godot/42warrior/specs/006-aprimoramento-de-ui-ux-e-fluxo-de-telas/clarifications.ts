import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify (1º portão). Registrados a partir das decisões que o usuario
 * ratificou nesta sessão (2026-06-28), ao apontar que a UI/UX está "completamente diferente da
 * referência" e que a tela de jogo aparece sobreposta por outras telas (bug de navegação), e ao
 * escolher escopo, grau de fidelidade e layout via perguntas estruturadas.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Escopo: fidelidade visual + correção das telas sobrepostas numa feature; áudio fora; apresentação data-driven",
    questions: [
      {
        question:
          "A feature 006 de UI/UX deve cobrir o quê: (a) fidelidade visual + corrigir as telas sobrepostas juntos, (b) só as telas, ou (c) só o visual?",
        answer:
          "Opção (a): os dois juntos numa feature — elevar o visual E corrigir a sobreposição de telas. Áudio (feature 005 / PR-009) fica totalmente fora. Adicional do usuário: manter o código e os assets organizados de forma que alterações futuras sejam fáceis (apresentação data-driven / registro de assets), e criar animações de ataque, cura, defesa etc.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Grau de fidelidade: inspirado no Ruby Warrior, com adaptação livre",
    questions: [
      {
        question:
          "Quão fiel à referência do Ruby Warrior o visual deve ser: réplica fiel do original, ou inspirado com adaptação livre?",
        answer:
          "Inspirado, com adaptação livre: usar o Ruby Warrior como base, mas com liberdade de estilo e de layout e mais cara da 42 — não precisa ser réplica pixel-perfect. O alvo é um jogo visualmente coeso e bom, não uma cópia exata.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Layout da tela de jogo: arena em destaque, editor de código retrátil, console com controles",
    questions: [
      {
        question:
          "Como deve ser a tela de jogo (arena + editor de código + console de turnos): tela única integrada, arena em destaque com editor retrátil, ou telas separadas em fluxo?",
        answer:
          "Arena em destaque: o corredor da masmorra ocupa a tela; HUD no topo (nível/HP/turno); o editor de código fica RETRÁTIL e desliza por cima/lateral apenas quando aberto (botão '</> Código'); console de turnos embaixo com controles play/pause/passo. Escolhido para imersão na batalha, sem o editor ocupando espaço fixo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Bug de navegação: telas do jogo renderizam sobrepostas; alvo é uma-tela-por-vez",
    questions: [
      {
        question:
          "O sintoma mostrado é que a tela de jogo aparece sobreposta por outras telas (menu / editor / arena / resultado empilhados ao mesmo tempo). A correção é garantir uma única tela ativa por vez, com a anterior removida ou ocultada na troca?",
        answer:
          "Sim. O bug é que as telas se sobrepõem em vez de trocar. A feature deve introduzir um fluxo de navegação que mantém exatamente uma tela ativa por vez (menu, jogo, transição, resultado, conclusão), liberando ou escondendo a anterior na transição — nada de telas empilhadas.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-005",
    topic: "Origem dos assets e ratificação do escopo",
    questions: [
      {
        question:
          "Os assets gráficos podem vir da internet sem preocupação com licença (o jogo não é comercial)? E o resumo do escopo da 006 — visual inspirado e coeso + animações por ação + correção da sobreposição + arena em destaque com editor retrátil + apresentação data-driven, com áudio fora — está correto?",
        answer:
          "Sim para os dois. Pode usar quaisquer assets da internet, a licença não importa pois não é jogo para vender. O resumo do escopo está confirmado — seguir para discovery com ele.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
