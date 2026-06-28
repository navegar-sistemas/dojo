import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-001",
    title: "Fluxo de torre como controlador de telas sobre a progressão",
    context:
      "A torre encadeia menu → transição → nível → resultado → (próximo|créditos) com reinício (RF-050..054), e isso é navegação de apresentação, não regra de domínio (RNF-050).",
    decision:
      "Um TowerFlowController coordena uma pilha de telas (ScreenStack) conforme o desfecho de cada nível e o progresso; o domínio só informa vitória/derrota e score.",
    consequences:
      "Navegação centralizada e testável; níveis e telas evoluem sem tocar o domínio. Custo: definir os estados/transições de tela e os pontos de entrada/saída do LevelRunner.",
    status: "accepted",
    requirementKeys: ["RF-050", "RF-051", "RF-052", "RF-053", "RF-054"],
  },
  {
    key: "ADR-002",
    title: "Áudio via AudioManager acionado por eventos, assíncrono",
    context:
      "SFX por evento de turno e trilha de fundo (RF-056, RF-057) não podem bloquear o loop de turno (RNF-052) nem acoplar o domínio ao áudio (RNF-050).",
    decision:
      "Um AudioManager assina TurnEvents e eventos de tela e toca os AudioStreams correspondentes de forma assíncrona; o domínio apenas emite eventos, sem conhecer áudio.",
    consequences:
      "Som reativo e desacoplado; trocar assets (CC0 → 42) não toca lógica (RF-058). Custo: mapear evento→som e gerir os players/buses de volume.",
    status: "accepted",
    requirementKeys: ["RF-056", "RF-057", "RF-058", "RNF-052"],
  },
  {
    key: "ADR-003",
    title: "Progresso e settings persistidos em user:// por um ProgressStore",
    context:
      "O nível alcançado e o volume precisam sobreviver entre sessões sem poluir o repo (RF-055, RNF-051).",
    decision:
      "Um ProgressStore encapsula ler/gravar progresso e settings em user://; menu e fluxo consultam o store; ausência de save inicia no nível 1.",
    consequences:
      "Persistência isolada e robusta no primeiro start; trocar formato não afeta o fluxo. Custo: versionar o formato do save.",
    status: "accepted",
    requirementKeys: ["RF-055", "RNF-051"],
  },
];

export const components: IComponent[] = [
  {
    name: "TowerFlowController",
    responsibility:
      "Coordena a navegação da torre (menu, transição, nível, resultado, créditos, reinício) conforme desfecho e progresso.",
    dependsOn: ["ScreenStack", "ProgressStore"],
    requirementKeys: ["RF-050", "RF-051", "RF-052", "RF-053", "RF-054"],
  },
  {
    name: "ScreenStack",
    responsibility:
      "Pilha de telas da torre (menu inicial, transição com descrição+habilidades, resultado/score, conclusão+créditos).",
    dependsOn: ["ProgressStore"],
    requirementKeys: ["RF-050", "RF-051", "RF-053", "RF-054"],
  },
  {
    name: "AudioManager",
    responsibility:
      "Assina TurnEvents (domínio) e eventos de tela e toca SFX/trilha assíncronos a partir de assets CC0; expõe controle de volume música/SFX.",
    dependsOn: [],
    requirementKeys: ["RF-056", "RF-057", "RF-058", "RNF-052"],
  },
  {
    name: "ProgressStore",
    responsibility:
      "Lê e grava progresso na torre e settings de volume em user://; trata ausência de save como início no nível 1.",
    dependsOn: [],
    requirementKeys: ["RF-055", "RNF-051"],
  },
];
