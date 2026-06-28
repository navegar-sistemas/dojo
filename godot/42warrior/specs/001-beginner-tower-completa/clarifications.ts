import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify (1º portão, antes de qualquer requisito/código): perguntas
 * curtas e fáceis feitas ao usuário, as respostas dele, e a confirmação explícita do
 * entendimento. A skill NÃO inventa conteúdo — pergunte e registre só o que o usuário confirmar.
 * O gate (--phase clarify) exige ≥1 registro com status "confirmed" (confirmedBy + confirmedAt);
 * nunca confirme por suposição. Feche com um registro de "resumo do entendimento" ratificado.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Como o jogador fornece a lógica de turno do warrior",
    questions: [
      {
        question:
          "No Ruby Warrior o jogador escreve código (play_turn). Como o jogador vai fornecer essa lógica? (editor de código no jogo / estratégias prontas + visualização / programação por blocos)",
        answer:
          "Inicialmente cogitou-se programação por blocos, mas o usuário decidiu: 'use código normal mesmo, esses blocos vão dar muito trabalho'. Ou seja, o jogador escreve código de verdade (uma classe Player com play_turn(warrior)), como no original.",
      },
      {
        question:
          "Em Godot isso é viável compilando GDScript em runtime (GDScript.source_code + reload(), instanciar e chamar play_turn(warrior)); o jogo embarca soluções-referência por nível. Confirma essa abordagem?",
        answer:
          "Sim — o jogador escreve GDScript que define play_turn(warrior); o jogo compila/executa em runtime contra uma fachada do warrior (só a API pública). Soluções-referência embarcadas para cada nível.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-002",
    topic: "Apresentação em Godot e assets temáticos da 42",
    questions: [
      {
        question: "Qual o estilo de apresentação do nível? (2D top-down em grade / 2D lateral)",
        answer: "2D top-down em grade (corredor de tiles visto de cima, unidades como sprites).",
      },
      {
        question: "Situação dos assets da 42 nesta entrega? (placeholders agora / já tenho os assets)",
        answer:
          "Placeholders agora — implementar com formas/ícones placeholder e deixar os pontos de troca prontos para os assets finais da 42 depois.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-003",
    topic: "Escopo desta entrega além do core (9 níveis + combate)",
    questions: [
      {
        question:
          "Quais funcionalidades extras entram? (pontuação+ace / telas de transição+torre / áudio / menu+créditos)",
        answer:
          "Todas: pontuação com time bonus e ace score; telas de transição/torre com descrição e habilidades; áudio; e menu inicial + créditos.",
      },
      {
        question: "Áudio até onde vai nesta entrega? (SFX placeholder+estrutura / SFX+música completos)",
        answer: "SFX + música completos integrados de verdade nesta entrega.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-004",
    topic: "Fidelidade ao Ruby Warrior beginner (9 níveis e mecânicas)",
    questions: [
      {
        question:
          "O jogo recria a beginner tower de 9 níveis com as mesmas mecânicas (sentidos feel/look/listen, ações walk/attack/rest/rescue/pivot/shoot, saúde 20, descanso 10%, ataque reduzido para trás, sludge/thick sludge/archer/wizard/captive)?",
        answer:
          "Sim — paridade funcional com o Ruby Warrior beginner; customização é só na pele (assets/tema 42), não nas regras, salvo decisão de produto registrada.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-005",
    topic: "Resumo do entendimento (ratificação final)",
    questions: [
      {
        question:
          "Resumo: remake do Ruby Warrior beginner (9 níveis) em Godot/GDScript, com Clean Architecture (Domain puro / Application / Presentation), jogador escrevendo GDScript play_turn(warrior) executado em runtime, apresentação 2D top-down com placeholders 42, pontuação+ace, telas de torre, áudio completo e menu/créditos. Está correto e completo?",
        answer:
          "Sim, entendimento confirmado. Prosseguir para discovery com esse escopo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
];
