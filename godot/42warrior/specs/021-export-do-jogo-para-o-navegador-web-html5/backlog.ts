import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-210",
    asA: "Jogador",
    iWant: "abrir e jogar o 42warrior diretamente no navegador",
    soThat: "eu jogue sem instalar nada, a partir de um link (incl. para a Game Jam)",
    acceptanceCriteria: [
      "Dado o build Web exportado, quando abro o index.html no navegador, então o jogo inicia e renderiza (menu/arena) via WebGL2 (renderer Compatibility), sem tela preta.",
      "Dado o project.godot, quando inspeciono a configuração, então rendering_method.web=gl_compatibility está definido e o desktop permanece Forward+ (override por plataforma).",
      "Dado o export_presets.cfg, quando rodo o export, então existe o preset Web e o build HTML5/WASM (index.html + .wasm + .pck) é gerado.",
    ],
    requirementKeys: ["RF-210", "RF-211"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
  {
    key: "US-211",
    asA: "Jogador",
    iWant: "ouvir o áudio e manter meu código/progresso ao jogar no navegador",
    soThat: "a experiência web não perca som nem zere meu avanço a cada reload",
    acceptanceCriteria: [
      "Dado o jogo no navegador, quando faço o primeiro gesto (clique/tecla), então o áudio (música/SFX) inicia — não fica mudo pelo autoplay-block; no desktop o áudio segue como hoje.",
      "Dado que escrevi código e avancei níveis no navegador, quando recarrego a página, então o código do jogador e o progresso persistem (user://→IndexedDB).",
    ],
    requirementKeys: ["RF-212", "RF-213"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
  {
    key: "US-212",
    asA: "Jurado da Jam",
    iWant: "confiar que o jogo realmente funciona no navegador (o warrior roda o código do jogador) sem degradar o desktop",
    soThat: "eu avalie a versão web como um jogo jogável de verdade, não só um build que abriu",
    acceptanceCriteria: [
      "Dado o build web, quando o smoke-test roda, então o warrior EXECUTA ≥1 turno do código do jogador no WASM (runtime GDScript) e o progresso é salvo — prova real, sem pending/máscara.",
      "Dado os overrides web, quando rodo a suíte desktop (check.sh), então fica 100% verde com 0 regressão das features 001–020.",
      "Dado o glitch shader (hint_screen_texture), quando o build roda no WebGL2, então o efeito renderiza corretamente e a performance fica jogável (alvo ≥ 30 fps em hardware comum).",
    ],
    requirementKeys: ["RNF-210", "RNF-211", "RNF-212"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
];
