import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-210",
    kind: "functional",
    description:
      "RENDERER COMPATIBILITY NO WEB: o project.godot define rendering/renderer/rendering_method.web=\"gl_compatibility\" (override por plataforma), mantendo Forward+ no desktop. O jogo 2D pixel-art (TileMap, sprites, HUD) renderiza no WebGL2 sem depender de recursos exclusivos de Forward+. Sem este override o build web não roda no navegador.",
    priority: "highest",
    rationale: "Investigação cmqxw7jfu + recorte PO cmqxwb2zw(a): Forward+ não roda em browser; Compatibility é o bloqueador #1.",
  },
  {
    key: "RF-211",
    kind: "functional",
    description:
      "PRESET WEB + BUILD HTML5: há um preset \"Web\" no export_presets.cfg e os export templates do Godot 4.7 instalados, produzindo um artefato HTML5/WASM (index.html + .wasm + .pck) que ABRE e inicia o jogo no navegador. Hoje não existe export_presets.cfg.",
    priority: "highest",
    rationale: "Recorte PO cmqxwb2zw(b): sem preset Web + templates não há build exportável.",
  },
  {
    key: "RF-212",
    kind: "functional",
    description:
      "ÁUDIO NO 1º GESTO: como os navegadores BLOQUEIAM autoplay até uma interação do usuário, o AudioManager inicia/retoma o áudio (música/SFX) no PRIMEIRO gesto (clique/tecla), em vez de no boot. No desktop o comportamento permanece o atual (sem regressão).",
    priority: "high",
    rationale: "Investigação cmqxw7jfu + recorte PO cmqxwb2zw(c): _music.play() no boot é silenciado pelo browser até o gesto.",
  },
  {
    key: "RF-213",
    kind: "functional",
    description:
      "PERSISTÊNCIA user:// NO WEB: o código do jogador (player_code_store) e o progresso (level_progress_store/progress_store), gravados em user:// via FileAccess/ConfigFile, persistem no web (Godot mapeia user:// para IndexedDB) e SOBREVIVEM a reload da página. No desktop a persistência permanece a atual.",
    priority: "high",
    rationale: "Recorte PO cmqxwb2zw(d): user:// no web é IndexedDB assíncrono; precisa persistir entre sessões.",
  },
  {
    key: "RNF-210",
    kind: "non_functional",
    description:
      "SMOKE-TEST WEB (o PILAR): há ≥1 smoke-test do build web que prova que o warrior EXECUTA o código do jogador no WASM (player_script_runner: GDScript.new()+reload() em runtime) — o build abre no navegador, o warrior roda ≥1 turno do código do jogador e o progresso é salvo. Smoke REAL (não só 'compilou'), sem máscara/pending.",
    priority: "highest",
    rationale: "Recorte PO cmqxwb2zw(e): runtime GDScript no WASM é o risco #1; se falhar, o jogo não funciona no web.",
  },
  {
    key: "RNF-211",
    kind: "non_functional",
    description:
      "ZERO REGRESSÃO DESKTOP: a suíte desktop (check.sh) permanece 100% verde, com 0 regressão das features 001–020; os overrides web (renderer, áudio-gesto) não alteram o comportamento desktop.",
    priority: "highest",
    rationale: "Recorte PO cmqxwb2zw(f): o web não pode degradar a experiência desktop já entregue.",
  },
  {
    key: "RNF-212",
    kind: "non_functional",
    description:
      "GLITCH SHADER + PERF NO WEBGL2: o glitch shader (hint_screen_texture / back-buffer copy) renderiza corretamente no WebGL2 (Compatibility) e o build mantém performance jogável (alvo ≥ 30 fps em hardware comum no smoke web). Conferido como parte do smoke, sem pending.",
    priority: "high",
    rationale: "Recorte PO cmqxwb2zw(g): screen-read shader + perf têm nuances no WebGL2 que precisam ser validadas.",
  },
];
