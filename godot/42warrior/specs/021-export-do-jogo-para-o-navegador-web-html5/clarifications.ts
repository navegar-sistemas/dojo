import type { IClarification } from "../types.ts";

/**
 * Feature de DIREÇÃO DO USUÁRIO: o Matheus ordenou diretamente ("o projeto precisa ser exportado
 * em html"). O agente-spec investigou (cmqxw7jfu) e o agente-po deu o recorte/GO (cmqxwb2zw),
 * produtizando como feature + PR-014. O entendimento confirmado vem da ordem do Matheus + o
 * recorte explícito do PO (autoridade de produto neste canal).
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Objetivo e escopo do export web",
    questions: [
      {
        question: "O que a feature precisa entregar para o jogo rodar no navegador?",
        answer:
          "Um build Web/HTML5 (Godot 4 WASM) jogável no navegador: (a) renderer Compatibility no web (gl_compatibility) mantendo Forward+ no desktop; (b) preset Web no export_presets.cfg + export templates 4.7; (c) áudio iniciando no 1º gesto do usuário (autoplay-block); (d) persistência user:// (código do jogador + progresso) no web via IndexedDB. Tudo sem perder a experiência desktop.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "O PILAR e o critério de aceite (DoD = smoke web real)",
    questions: [
      {
        question: "Qual é o risco crítico e como se prova o aceite?",
        answer:
          "O PILAR é o player_script_runner, que compila GDScript em RUNTIME (GDScript.new()+reload()) — se não rodar no WASM, o jogo inteiro não funciona no web. DoD = SMOKE-TEST WEB REAL: o build roda no navegador + o warrior EXECUTA o código do jogador (não só 'compilou') + o progresso é salvo. Além disso: 0 regressão da experiência desktop; o glitch shader (hint_screen_texture) e a performance conferidos no WebGL2.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Pré-requisito e simplificações",
    questions: [
      {
        question: "Que dependências e simplificações existem?",
        answer:
          "PRÉ-REQUISITO: a robustez P0 do runner contra recursão (feature 020) — um crash no desktop crasharia no web igual; a 020 está FECHADA (integrada + aceita), então o smoke web do código do jogador é válido agora. SIMPLIFICAÇÃO: o jogo NÃO usa Thread/WorkerThreadPool/OS.execute → NÃO precisa de COOP/COEP/SharedArrayBuffer, o que facilita a hospedagem.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question: "O entendimento está correto?",
        answer:
          "Sim. A 021 entrega o build Web/HTML5 jogável no navegador (renderer Compatibility no web + preset Web + áudio-gesto + persistência user://-IndexedDB), com o PILAR provado por smoke-test web (o warrior roda o código do jogador no WASM + salva progresso) e 0 regressão desktop. Rastreia PR-014 (ordem do Matheus, recorte do PO cmqxwb2zw). Config/export é implementação do dev/tech-lead; o spec define RF/RNF/DoD. P0-recursão (020) já fechada habilita o smoke.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
];
