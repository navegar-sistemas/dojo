import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Editor in-game (PR-010) ───────────────────────────────────────────────────
  {
    key: "RF-030",
    kind: "functional",
    description:
      "A tela de jogo exibe um painel de edição de código (CodeEdit) editável pelo jogador, com destaque de sintaxe de GDScript, fonte monoespaçada e numeração de linhas.",
    priority: "highest",
    rationale: "CLR-002: é a superfície onde o jogador escreve a lógica do warrior; sem ela o jogo não é de programação.",
  },
  {
    key: "RF-031",
    kind: "functional",
    description:
      "Um botão Rodar pega o texto atual do editor, compila via PlayerScriptRunner (já existente) e, se compilar, inicia/reinicia a simulação do nível executando o play_turn do jogador a cada turno.",
    priority: "highest",
    rationale: "CLR-001/CLR-002: liga a entrada do jogador ao motor de execução existente.",
  },
  {
    key: "RF-032",
    kind: "functional",
    description:
      "Um botão Resetar restaura o conteúdo do editor ao esqueleto inicial do nível, descartando as edições do jogador após confirmação.",
    priority: "high",
    rationale: "Permite recomeçar do zero sem fechar o jogo.",
  },
  {
    key: "RF-033",
    kind: "functional",
    description:
      "Um botão Ver solução exibe a solução-referência do nível (RF-013 da feature 001) em modo leitura, sem sobrescrever silenciosamente o código que o jogador escreveu.",
    priority: "medium",
    rationale: "Apoio ao aprendizado sem destruir o trabalho do jogador.",
  },
  {
    key: "RF-034",
    kind: "functional",
    description:
      "O código do jogador é persistido por nível em user:// (salvo ao Rodar e ao sair) e recarregado ao abrir o nível; um nível sem código salvo abre com o esqueleto inicial.",
    priority: "high",
    rationale: "CLR-002: o jogador não perde sua lógica entre sessões.",
  },
  {
    key: "RF-035",
    kind: "functional",
    description:
      "Falha de compilação ou exceção em runtime no código do jogador é exibida de forma legível (mensagem e, quando disponível, a linha) num painel junto ao editor, sem travar o jogo (consome o tratamento de erro de RF-012 da feature 001).",
    priority: "highest",
    rationale: "Robustez: o código do jogador é entrada não confiável; o erro precisa ser comunicado, não engolido.",
  },
  {
    key: "RF-036",
    kind: "functional",
    description:
      "Cada nível fornece um esqueleto inicial para o editor: a assinatura de play_turn(warrior) e um comentário listando as habilidades/sentidos disponíveis até aquele nível.",
    priority: "high",
    rationale: "Reduz a barreira de entrada e guia o jogador na API introduzida por nível (RF-015 da feature 001).",
  },
  // ── Não-funcionais ────────────────────────────────────────────────────────────
  {
    key: "RNF-030",
    kind: "non_functional",
    description:
      "O editor não acessa o LevelState, as unidades nem nós internos do jogo: envia apenas o texto-fonte ao PlayerScriptRunner (Application) e recebe resultado/erros. Limite: 0 referências a tipos de domínio ou nós internos no script do editor, verificável por grep.",
    priority: "highest",
    rationale: "CONV-002: separação de camadas preservada; o editor é um adaptador de entrada.",
  },
  {
    key: "RNF-031",
    kind: "non_functional",
    description:
      "A persistência do código do jogador ocorre exclusivamente em user://: 100% das gravações em user:// e 0 escritas em res:// ou em arquivos versionados do projeto, verificável por grep dos caminhos de save.",
    priority: "high",
    rationale: "Isola dados do jogador dos assets do jogo; evita poluir o repositório.",
  },
  {
    key: "RNF-032",
    kind: "non_functional",
    description:
      "Os scripts do editor seguem o GDScript style guide com tipagem estática (CONV-004/005): gdformat sem diffs e gdlint sem violações.",
    priority: "high",
    rationale: "Qualidade verificável mecanicamente, consistente com o projeto.",
  },
];
