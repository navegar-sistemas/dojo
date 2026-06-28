import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify (1º portão). Registrados a partir das decisões que o usuario
 * ratificou diretamente na sessão de correção de rumo (2026-06-27), quando apontou que a
 * apresentação atual (render procedural/ASCII) "não tem nada a ver" com a referência do Ruby
 * Warrior e definiu a UI gráfica como prioridade número 1.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Alvo visual: jogo gráfico fiel à referência, não render procedural",
    questions: [
      {
        question:
          "A apresentação atual é desenhada por código (_draw: círculos/retângulos) e não se parece com o Ruby Warrior de referência (cavaleiro de armadura, slime verde, escada dourada, masmorra de pedra). O alvo é esse visual gráfico de verdade?",
        answer:
          "Sim. A UI gráfica fiel à referência é a prioridade máxima. Render procedural por formas geométricas é insuficiente e deve ser substituído por sprites e tiles reais.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-002",
    topic: "Origem dos assets gráficos",
    questions: [
      {
        question:
          "De onde vêm os sprites (cavaleiro, inimigos, escada, tiles de masmorra)? (asset pack CC0 / pixel art própria tema 42 / você fornece)",
        answer:
          "Asset pack de pixel-art CC0 (licença livre, ex.: Kenney/0x72): visual decente imediato, sem custo de licença, integrado com pontos de troca para a arte definitiva da 42 depois.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-003",
    topic: "Estilo de cena e respeito à arquitetura",
    questions: [
      {
        question:
          "Mantém 2D top-down em grade (como já confirmado para o projeto) e a apresentação apenas consome o estado/eventos do domínio (Clean Architecture), sem regra de jogo na cena?",
        answer:
          "Sim — 2D top-down em grade; a camada Godot adapta o estado da Application e os turn_events do domínio para sprites/animações, sem mover regra de jogo para a apresentação.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question:
          "Resumo: feature 002 entrega a UI gráfica do jogo — TileMap de masmorra + sprites de todas as unidades e da escada + animações de feedback por turno (a partir dos turn_events) + HUD (HP coração, turno, descrição, score), com asset pack CC0 trocável pela arte 42, substituindo o game_view.gd procedural. Correto?",
        answer:
          "Sim, entendimento confirmado. É a prioridade 1; seguir para discovery com esse escopo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
];
