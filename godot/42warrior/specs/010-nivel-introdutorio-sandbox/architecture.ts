import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-018",
    title: "Sandbox como LevelData data-driven com campos is_sandbox e hint_text, sem novo subsistema",
    context:
      "O sandbox precisa de: (a) layout próprio (corredor curto + escada + sludge opcional), (b) texto fixo de orientação na tela, (c) progressão que não conta pontuação nem exibe ResultScreen. O motor de turnos, LevelState e entidades existentes já suportam qualquer layout de LevelData. Criar uma nova cena ou novo script para o sandbox violaria RF-005 (sem subsistema novo) e aumentaria a superfície de manutenção.",
    decision:
      "O sandbox é descrito como um LevelData normal com dois campos extras: `is_sandbox: bool = true` e `hint_text: String` (texto de orientação fixo). O campo is_sandbox sinaliza ao fluxo de progressão (ProgressionManager / ScreenManager) que, ao completar o nível, não deve exibir ResultScreen nem registrar score — navegando diretamente ao nível 1. O hint_text é lido pela GameScreen e exibido como Label no HUD enquanto o nível estiver ativo. Nenhum novo script de domínio, nenhuma nova cena de tela.",
    consequences:
      "Todo o motor de turnos, entidades e editor de código reusados sem alteração (RNF-001). O fluxo pós-conclusão diverge apenas num if is_sandbox na camada de progressão (RF-003). A GameScreen precisa de uma Label condicional para hint_text (RF-004). Custo: LevelData ganha dois campos opcionais; progressão ganha a branch de sandbox.",
    status: "accepted",
    requirementKeys: ["RF-002", "RF-003", "RF-004", "RF-005", "RNF-001"],
    rejectedAlternatives: [
      {
        alternative: "Criar uma SandboxScreen separada com cena própria",
        reason:
          "Duplica a lógica da GameScreen (arena, editor, HUD, console de turnos), aumenta superfície de manutenção e viola o requisito de reutilização de sistemas (RNF-001) sem nenhum benefício funcional.",
      },
    ],
  },
  {
    key: "ADR-019",
    title: "Sandbox listado na seleção de níveis (feature 009) como item persistentemente desbloqueado",
    context:
      "CLR-002 definiu que o sandbox é acessível no menu/seleção de níveis a qualquer momento, sem forçar acesso automático. A tela de seleção de níveis (feature 009) controla quais níveis estão desbloqueados via dados de progresso salvos (SaveData). O sandbox não deve depender do progresso da torre para aparecer.",
    decision:
      "O ProgressionManager/SaveData marca o sandbox (level_id = 0) como sempre_desbloqueado=true — valor hardcoded que não é sobrescrito pelo fluxo de progressão normal da torre. A tela de seleção (feature 009) o lista em primeiro, com indicador visual que o distingue como prática (ex.: 'Treinamento'). Ao selecioná-lo, o fluxo de entrada é idêntico ao de qualquer nível: LevelLoader carrega o LevelData do sandbox e GameScreen inicia.",
    consequences:
      "Integração limpa com a feature 009 sem novo componente (RF-001). O LevelRegistry define o sandbox como level_id=0 e o ProgressionManager sabe que level_id=0 nunca é bloqueado — uma exceção de 2 linhas no método de verificação de desbloqueio.",
    status: "accepted",
    requirementKeys: ["RF-001", "RF-005"],
    rejectedAlternatives: [
      {
        alternative: "Botão separado no menu principal fora da tela de seleção",
        reason: "CLR-002 definiu explicitamente integração com a seleção de níveis (feature 009); botão separado duplica o ponto de entrada e quebra a consistência de navegação.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "SandboxLevelData",
    responsibility:
      "Instância LevelData configurada com corredor curto, escada ao final, sludge fraco opcional e campos is_sandbox=true e hint_text fixo. Declarada no LevelRegistry como level_id=0.",
    dependsOn: [],
    requirementKeys: ["RF-002", "RF-004"],
  },
  {
    name: "ProgressionManagerSandboxExtension",
    responsibility:
      "Ao receber conclusão de nível com is_sandbox=true: não registra score, não exibe ResultScreen, navega via ScreenManager diretamente ao nível 1. Mantém level_id=0 permanentemente desbloqueado em SaveData.",
    dependsOn: ["SandboxLevelData"],
    requirementKeys: ["RF-001", "RF-003", "RF-005"],
  },
  {
    name: "GameScreenHintLabel",
    responsibility:
      "Label de orientação no HUD da GameScreen: quando o LevelData ativo tem hint_text não-vazio, exibe o texto durante toda a execução; oculta-se nos demais níveis (compatibilidade retroativa).",
    dependsOn: ["SandboxLevelData"],
    requirementKeys: ["RF-004"],
  },
];
