import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "021-export-do-jogo-para-o-navegador-web-html5",
  name: "Export do jogo para o navegador Web HTML5",
  problem:
    "O Matheus determinou que o jogo precisa rodar no NAVEGADOR ('o projeto precisa ser exportado em html'). Hoje o projeto é desktop-only: renderer Forward+ (que NÃO roda em browser) e SEM export_presets.cfg (nenhum preset Web). A investigação (cmqxw7jfu) mapeou os bloqueadores (renderer + preset) e os riscos a validar no WASM: o PILAR é o player_script_runner, que compila GDScript em RUNTIME (GDScript.new()+reload()) — se não rodar no WASM, o jogo inteiro não funciona no web; além de glitch shader (hint_screen_texture), áudio com autoplay-block, e persistência user://→IndexedDB. O pré-requisito (robustez P0 do runner contra recursão, feature 020) está FECHADO — um crash no desktop crasharia no web igual. Esta feature produtiza o export web sem perder a experiência desktop.",
  productRequirementKeys: ["PR-014"],
  goals: [
    "Renderer COMPATIBILITY no web (rendering_method.web=gl_compatibility) mantendo Forward+ no desktop — o jogo 2D pixel-art renderiza no WebGL2.",
    "Preset Web no export_presets.cfg + export templates do Godot 4.7, gerando um build HTML5/WASM que abre no navegador.",
    "Áudio inicia/retoma no 1º GESTO do usuário (contorna o autoplay-block dos browsers); persistência user:// (código do jogador + progresso) funcionando no web (IndexedDB), preservada entre reloads.",
    "PILAR provado por SMOKE-TEST WEB: o warrior EXECUTA o código do jogador no WASM (GDScript em runtime) — build roda no browser + o warrior roda o código + salva progresso (smoke real, não só 'compilou').",
    "0 REGRESSÃO da experiência desktop; glitch shader (hint_screen_texture) e performance conferidos no WebGL2.",
  ],
  outOfScope: [
    "Não reescrever a lógica de jogo/domínio — só a camada de config (project.godot/export_presets), ajustes de UI/cena (áudio-gesto) e a validação web.",
    "Sem threads no jogo → NÃO precisa de COOP/COEP/SharedArrayBuffer (simplifica a hospedagem).",
    "Hospedagem/deploy do build (CDN, itch.io, etc.) fora de escopo — a feature entrega o build exportável e validado, não a publicação.",
  ],
  productDecisions: [
    "Produtizado como FEATURE + PR-014 novos (recorte do PO cmqxwb2zw, ratificando a ordem direta do Matheus).",
    "P0-recursão (feature 020) é PRÉ-REQUISITO do smoke web do código do jogador e está FECHADO (a robustez do runner já vale no desktop e, por construção, no WASM).",
    "Config/export (project.godot, export_presets.cfg, áudio-gesto) é implementação do dev/tech-lead (fora de specs/); o spec define RF/RNF/DoD e o smoke como prova.",
  ],
  phase: "done",
  createdAt: "2026-06-28",
};
