import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-024",
    title: "Tela de seleção de níveis como nova tela no ScreenManager (006), acessada pelo menu principal",
    context:
      "A seleção/replay é navegação de 1ª classe (CLR-001/009): uma tela nova no ScreenManager da 006, acessada SÓ pelo menu principal (sem replay pelo pause), listando os níveis com status e a melhor pontuação com breakdown (RF-090/091/094).",
    decision:
      "LevelSelectScreen é uma nova tela registrada no ScreenManager (006), montada uma-tela-por-vez a partir do menu principal. Lista os níveis com status (bloqueado/desbloqueado/vencido) e, por nível vencido, a melhor pontuação + breakdown (time/rescue/ace) lidos do LevelProgressStore. Selecionar um nível vencido aciona o re-entry no nível.",
    consequences:
      "Replay como navegação coesa com a 006 (1 tela de topo, sem vazar); acesso restrito ao menu principal mantém o escopo contido (sem pause-replay). RF-090/091/094 atendidos. Custo: registrar a nova tela e o ponto de entrada no menu principal.",
    status: "accepted",
    requirementKeys: ["RF-090", "RF-091", "RF-094"],
    rejectedAlternatives: [
      {
        alternative: "Modal/seção dentro da tela de resultado, ou acesso também pelo menu de pause",
        reason:
          "CLR-001 (009) definiu tela nova de 1ª classe pelo menu principal e descartou o pause-replay por ora (escopo contido).",
      },
    ],
  },
  {
    key: "ADR-025",
    title: "Código por nível (user://code_level_N.gd) + score máximo preservado, via LevelProgressStore em user://",
    context:
      "Re-jogar para otimizar exige preservar a solução POR NÍVEL (RF-092) e o score MÁXIMO do nível, atualizando só se melhorar (RF-093); tudo persistido em user:// sem escrever em res:// (RNF-090).",
    decision:
      "Um LevelProgressStore (na linhagem do ProgressStore/PlayerCodeStore já existentes, camada Application/persistência) guarda, por nível, o código (user://code_level_N.gd), o status e a melhor pontuação + breakdown. Ao re-entrar num nível, carrega o código daquele nível; ao concluir uma run, atualiza o score máximo somente se a nova pontuação for melhor. Toda escrita é em user://; 0 escrita em res://.",
    consequences:
      "Solução por nível preservada e otimização de score sem punir exploração (RF-092/093); persistência local robusta (RNF-090). Custo: esquema de armazenamento por nível (código + score) e a regra 'atualiza só se melhorar'.",
    status: "accepted",
    requirementKeys: ["RF-092", "RF-093", "RNF-090"],
    rejectedAlternatives: [
      {
        alternative: "Um único arquivo de código compartilhado entre níveis e score sempre sobrescrito",
        reason:
          "Quebra RF-092 (re-jogar perderia a solução de outro nível) e RF-093 (sobrescrever score puniria o jogador que explora uma run pior).",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "LevelSelectScreen",
    responsibility:
      "Nova tela (ScreenManager da 006) acessada pelo menu principal: lista os níveis com status e, por nível vencido, a melhor pontuação + breakdown (do LevelProgressStore); aciona o re-entry num nível vencido. Uma-tela-por-vez.",
    dependsOn: ["LevelProgressStore"],
    requirementKeys: ["RF-090", "RF-091", "RF-094"],
  },
  {
    name: "LevelProgressStore",
    responsibility:
      "Persistência (camada Application, user://) por nível: código (user://code_level_N.gd), status e melhor pontuação + breakdown. Carrega o código do nível no re-entry e atualiza o score máximo só se a nova run melhorar. 0 escrita em res://.",
    dependsOn: [],
    requirementKeys: ["RF-091", "RF-092", "RF-093", "RNF-090"],
  },
];
