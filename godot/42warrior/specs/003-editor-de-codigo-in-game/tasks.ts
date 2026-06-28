import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-030",
    storyKey: "US-030",
    summary:
      "Criar a cena do editor (CodeEditorPanel) com um CodeEdit configurado para GDScript (syntax highlight, fonte monoespaçada, numeração de linhas), integrada à tela de jogo.",
    definitionOfDone:
      "A cena de jogo exibe um CodeEdit editável com destaque de sintaxe e numeração; digitar altera o texto. gdformat/gdlint sem violações no script da cena.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-031",
    storyKey: "US-031",
    summary:
      "Implementar o botão Rodar: capturar o texto do CodeEdit, enviá-lo ao PlayerScriptRunner (feature 001) e iniciar/reiniciar a simulação do nível com o play_turn do jogador.",
    definitionOfDone:
      "Clicar Rodar com código válido executa a lógica do jogador a cada turno; rodar de novo usa o texto atual. grep confirma 0 referências a LevelState/unidades no script do editor (RNF-030).",
    status: "done",
    dependsOn: ["T-030"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-032",
    storyKey: "US-032",
    summary:
      "Implementar os botões Resetar (volta ao esqueleto do nível, com confirmação) e Ver solução (exibe a solução-referência em leitura, sem sobrescrever o código do jogador).",
    definitionOfDone:
      "Resetar+confirmar recarrega o esqueleto; Ver solução mostra a referência read-only e o código do jogador permanece intacto.",
    status: "done",
    dependsOn: ["T-030", "T-035"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-033",
    storyKey: "US-033",
    summary:
      "Implementar o PlayerCodeStore: salvar o código do jogador por nível em user:// (ao Rodar e ao sair) e recarregá-lo ao abrir o nível.",
    definitionOfDone:
      "Escrever código, sair e reabrir o nível recarrega o código; nível sem save abre com o esqueleto. grep confirma gravação só em user:// (RNF-031).",
    status: "done",
    dependsOn: ["T-030"],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-034",
    storyKey: "US-034",
    summary:
      "Implementar o ErrorView: exibir, junto ao editor, mensagens de erro de compilação/runtime retornadas pelo PlayerScriptRunner, com a linha quando disponível, sem travar o jogo.",
    definitionOfDone:
      "Código com erro de compilação mostra a mensagem e o jogo não trava; exceção em runtime num turno é exibida e a simulação continua.",
    status: "done",
    dependsOn: ["T-031"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-035",
    storyKey: "US-035",
    summary:
      "Implementar o LevelSkeletonProvider: fornecer, por nível, o esqueleto inicial (assinatura play_turn(warrior) + comentário das habilidades/sentidos disponíveis até aquele nível).",
    definitionOfDone:
      "Cada nível, ao abrir sem save, mostra o esqueleto com a assinatura e o comentário das habilidades corretas do nível (paridade com RF-015 da feature 001).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
];
