import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-210",
    title: "Renderer Compatibility via override .web (não trocar o projeto inteiro)",
    context:
      "O projeto é Forward+ (config/features), que não roda em browser. Trocar o projeto inteiro para Compatibility degradaria o desktop sem necessidade.",
    decision:
      "Usar o override por plataforma rendering/renderer/rendering_method.web=\"gl_compatibility\", mantendo Forward+ no desktop. O jogo é 2D pixel-art e não usa recursos exclusivos de Forward+, então Compatibility/WebGL2 atende sem perda visual.",
    consequences:
      "Web roda no WebGL2; desktop intocado (0-regressão). Custo: validar que nada visual depende de Forward+ (conferido no smoke web, junto do shader).",
    status: "accepted",
    requirementKeys: ["RF-210", "RNF-211"],
    rejectedAlternatives: [
      {
        alternative: "Trocar o projeto inteiro para Compatibility",
        reason: "Degradaria o desktop sem ganho — o override por plataforma preserva Forward+ no desktop.",
      },
    ],
  },
  {
    key: "ADR-211",
    title: "Preset Web + export templates 4.7 → build HTML5/WASM",
    context:
      "Não existe export_presets.cfg; sem preset Web + templates não há build exportável para o navegador.",
    decision:
      "Criar o preset \"Web\" no export_presets.cfg e instalar os export templates do Godot 4.7 no ambiente de build, gerando o artefato HTML5/WASM (index.html + .wasm + .pck) que abre o jogo no navegador.",
    consequences:
      "Pipeline de export web reprodutível. Custo: o ambiente de build precisa dos templates 4.7 (mecânica do tech-lead, fora de specs/).",
    status: "accepted",
    requirementKeys: ["RF-211"],
    rejectedAlternatives: [],
  },
  {
    key: "ADR-212",
    title: "Áudio diferido ao 1º gesto (contorna autoplay-block) sem regredir desktop",
    context:
      "audio_manager.gd dá _music.play() no boot; navegadores bloqueiam autoplay até um gesto do usuário, então a música ficaria muda no web.",
    decision:
      "Iniciar/retomar o áudio no PRIMEIRO gesto do usuário (clique/tecla), em vez de no boot. No desktop, manter o comportamento atual (sem regressão) — o gating só ativa o áudio na primeira interação, que no desktop acontece naturalmente.",
    consequences:
      "Áudio toca no web após a 1ª interação; desktop inalterado. Custo: ajustar o AudioManager para diferir o play ao gesto.",
    status: "accepted",
    requirementKeys: ["RF-212", "RNF-211"],
    rejectedAlternatives: [],
  },
  {
    key: "ADR-213",
    title: "Smoke web do runtime GDScript como prova do PILAR (não confiar em 'compilou')",
    context:
      "O player_script_runner compila GDScript em runtime (GDScript.new()+reload()). É o pilar do jogo; runtime GDScript geralmente funciona no WASM mas DEVE ser provado. O glitch shader (hint_screen_texture) e a persistência user://→IndexedDB também têm nuances web.",
    decision:
      "Provar o web por um SMOKE real: o build abre no navegador, o warrior EXECUTA ≥1 turno do código do jogador no WASM, o progresso é salvo (user://→IndexedDB persiste em reload) e o glitch shader renderiza no WebGL2 com perf jogável. Sem pending/máscara — se o runtime GDScript falhar no WASM, o smoke falha (não há fallback que esconda).",
    consequences:
      "O risco #1 (runtime no WASM) é validado de verdade; o web só é aceito com o jogo realmente jogável. Custo: montar o harness de smoke web (mecânica do dev/tech-lead).",
    status: "accepted",
    requirementKeys: ["RNF-210", "RF-213", "RNF-212"],
    rejectedAlternatives: [
      {
        alternative: "Aceitar o web só por 'o build compilou/abriu'",
        reason: "Não prova o pilar — runtime GDScript pode falhar no WASM e o jogo não funcionaria, exatamente o risco a cobrir.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "WebRendererConfig",
    responsibility:
      "Config (project.godot): override rendering_method.web=gl_compatibility mantendo Forward+ no desktop; garante que o 2D renderiza no WebGL2 sem recursos Forward+-only.",
    dependsOn: [],
    requirementKeys: ["RF-210", "RNF-211"],
  },
  {
    name: "WebExportPreset",
    responsibility:
      "Preset \"Web\" no export_presets.cfg + export templates 4.7; produz o build HTML5/WASM que abre no navegador.",
    dependsOn: [],
    requirementKeys: ["RF-211"],
  },
  {
    name: "AudioGestureGate",
    responsibility:
      "Ajuste no AudioManager: inicia/retoma o áudio no 1º gesto do usuário (autoplay-block), preservando o comportamento desktop.",
    dependsOn: [],
    requirementKeys: ["RF-212", "RNF-211"],
  },
  {
    name: "WebPersistenceAdapter",
    responsibility:
      "Garantia de que user:// (código do jogador + progresso) persiste no web (IndexedDB) entre reloads; validação do flush, sem alterar o desktop.",
    dependsOn: [],
    requirementKeys: ["RF-213"],
  },
  {
    name: "WebSmokeHarness",
    responsibility:
      "Harness de smoke web: abre o build no navegador, executa ≥1 turno do código do jogador no WASM (runtime GDScript), confere a persistência user://, e valida o glitch shader (WebGL2) + perf — prova real, sem pending.",
    dependsOn: ["WebRendererConfig", "WebExportPreset"],
    requirementKeys: ["RNF-210", "RNF-212"],
  },
];
