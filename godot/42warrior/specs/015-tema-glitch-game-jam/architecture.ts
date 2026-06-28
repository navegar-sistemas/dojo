import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-034",
    title: "Regra de glitch DETERMINÍSTICA em Domain/Application, separada dos efeitos visuais",
    context:
      "O tema exige glitch na MECÂNICA (RF-151) e por andar (RF-155), mas o determinismo do turno é sagrado (RNF-150) e o domínio é independente da engine. Glitch que afeta REGRA não pode ser RNG nem viver na cena.",
    decision:
      "Introduzir um GlitchRule na camada Domain/Application: dado o estado do nível + um seed determinístico (derivado do nível/andar/turno, não aleatório) + os turn_events (incl. o erro/exceção do código do jogador já tratado), decide os efeitos de glitch que afetam REGRA (ex.: entidade cintilante presente em turnos alternados por padrão fixo; ação corrompida scriptada). É puro/determinístico e coberto por teste de domínio; a apresentação apenas LÊ o resultado. Erros do código do jogador entram como um TurnEvent/sinal de glitch consumido pela regra e pela apresentação.",
    consequences:
      "Glitch mecânico reproduzível e testável (mesmo estado+seed → mesmo resultado); domínio independente da engine preservado; o jogador contorna o glitch no código de forma justa. Custo: modelar o seed e o efeito de glitch no domínio + testes.",
    status: "accepted",
    requirementKeys: ["RF-151", "RF-155", "RF-159", "RNF-150"],
    rejectedAlternatives: [
      {
        alternative: "Glitch mecânico via RNG na cena (presentation) tocando regra",
        reason: "Viola RNF-150 (determinismo) e o domínio-independente-da-engine; glitch injusto/não-testável.",
      },
    ],
  },
  {
    key: "ADR-035",
    title: "Pós-processo de glitch e corrupção de sprite/UI/áudio na APRESENTAÇÃO, reagindo aos turn_events",
    context:
      "A estética glitch (RF-152), a corrupção da UI por andar (RF-153), o sprite que corrompe em dano/morte (RF-156) e o áudio que corrompe com o estado (RF-158) são efeitos puramente visuais/sonoros — devem ficar SÓ na apresentação, sem duplicar regra.",
    decision:
      "Camada de apresentação: um GlitchPostProcess (shader na câmera: RGB split/aberração/scanlines) cuja intensidade é função dos turn_events (DAMAGED/DIED/erro) e do andar; um UiCorruption que degrada a UI por andar de forma determinística; corrupção de sprite (pixel-sort/static) acionada por DAMAGED/DIED; e um GlitchAudio (bit-crush/distorção) função de HP baixo/erro. Todos CONSOMEM os turn_events existentes e o estado/andar — nenhum decide regra.",
    consequences:
      "Estética rica e reativa sem tocar o domínio; reaproveita o mapa de turn_events da 006. Custo: shader + fiação dos efeitos aos eventos/estado. Intensidade derivada de estado é determinística (mesmo estado → mesma intensidade).",
    status: "accepted",
    requirementKeys: ["RF-152", "RF-153", "RF-156", "RF-158"],
    rejectedAlternatives: [
      {
        alternative: "Efeitos visuais embutidos no domínio/regra",
        reason: "Quebra domínio-independente-da-engine; mistura render com regra.",
      },
    ],
  },
  {
    key: "ADR-036",
    title: "Catálogo data-driven do tema (mensagens Unix/42, assets de glitch, intensidade por andar) via registro análogo ao EntityAssetRegistry",
    context:
      "Mensagens Unix/42 (RF-154), assets/efeitos de glitch e a curva de intensidade por andar devem ser data-driven com pontos de troca (invariante), não hardcoded espalhados.",
    decision:
      "Um ThemeCatalog data-driven (na linhagem do EntityAssetRegistry/asset_paths da 006) centraliza: o vocabulário de mensagens Unix/42 mapeado a eventos/erros, os assets/parâmetros de glitch e a intensidade de corrupção por andar. Apresentação e (quando aplicável) a regra leem do catálogo; pontos de troca documentados.",
    consequences:
      "Tema ajustável sem caça a literais; coerente com o padrão data-driven do projeto. Custo: definir o esquema do catálogo e os pontos de troca.",
    status: "accepted",
    requirementKeys: ["RF-154"],
    rejectedAlternatives: [
      {
        alternative: "Mensagens e parâmetros de glitch hardcoded nas cenas/scripts",
        reason: "Viola o invariante data-driven e a coesão (mesmo antipadrão do RNF-063 da 006).",
      },
    ],
  },
  {
    key: "ADR-037",
    title: "Fio narrativo 'Kernel corrompido da 42' nas telas/transições (reuso do ScreenManager 006) + transições datamosh",
    context:
      "O conceito (RF-150) precisa de um fio narrativo nas telas/transições/textos, e as transições entre telas/níveis ganham datamosh (RF-157). Ambos vivem na navegação já entregue pela 006.",
    decision:
      "Reusar o ScreenManager da 006 para conduzir o fio 'Kernel corrompido da 42' (textos de menu/transição/resultado apresentando torre=mainframe infectado, warrior=processo de debug) e aplicar o efeito datamosh nas transições entre telas/níveis. Textos vêm do ThemeCatalog (ADR-036).",
    consequences:
      "Narrativa e transições coesas com a navegação existente, sem nova infraestrutura de telas. Custo: redação dos textos temáticos + efeito de transição.",
    status: "accepted",
    requirementKeys: ["RF-150", "RF-157"],
    rejectedAlternatives: [
      {
        alternative: "Nova camada de telas dedicada ao tema",
        reason: "Duplicaria o ScreenManager da 006; desnecessário e churn.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "GlitchRule",
    responsibility:
      "Domain/Application: dado estado do nível + seed determinístico (nível/andar/turno) + turn_events (incl. erro do código do jogador), decide os efeitos de glitch que afetam REGRA (entidade cintilante por padrão fixo, ação corrompida scriptada). Puro/determinístico, coberto por teste de domínio; 0 RNG injusto.",
    dependsOn: [],
    requirementKeys: ["RF-151", "RF-155", "RF-159", "RNF-150"],
  },
  {
    name: "GlitchPostProcess",
    responsibility:
      "Apresentação: shader de glitch na câmera (RGB split/aberração/scanlines) e corrupção de sprite (pixel-sort/static), com intensidade função dos turn_events (DAMAGED/DIED/erro) e do andar. Consome eventos/estado; não decide regra.",
    dependsOn: [],
    requirementKeys: ["RF-152", "RF-156"],
  },
  {
    name: "UiCorruption",
    responsibility:
      "Apresentação: degrada a UI (scanlines, texto embaralhado, RGB split) de forma determinística conforme o andar na torre, lendo a intensidade por andar do ThemeCatalog.",
    dependsOn: [],
    requirementKeys: ["RF-153"],
  },
  {
    name: "GlitchAudio",
    responsibility:
      "Apresentação: corrompe o áudio (bit-crush/distorção) em função do estado (HP baixo, erro do código), consumindo o estado/eventos; não decide regra.",
    dependsOn: [],
    requirementKeys: ["RF-158"],
  },
  {
    name: "ThemeCatalog",
    responsibility:
      "Data-driven (linhagem EntityAssetRegistry): catálogo do tema — mensagens Unix/42 por evento/erro, assets/parâmetros de glitch e intensidade de corrupção por andar; fonte única com pontos de troca, lida pela apresentação e pela narrativa.",
    dependsOn: [],
    requirementKeys: ["RF-154", "RF-150", "RF-157"],
  },
];
