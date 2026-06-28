import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Fluxo de torre e progressão (PR-008) ──────────────────────────────────────
  {
    key: "RF-050",
    kind: "functional",
    description:
      "Um menu inicial abre o jogo com as opções iniciar (do nível 1) e continuar (do nível salvo); 'continuar' leva ao nível conforme o progresso persistido.",
    priority: "high",
    rationale: "CLR-002: ponto de entrada da torre; respeita o progresso do jogador.",
  },
  {
    key: "RF-051",
    kind: "functional",
    description:
      "Antes de cada nível, uma tela de transição mostra o nome/descrição do nível e as habilidades novas introduzidas (RF-015 da feature 001).",
    priority: "high",
    rationale: "CLR-002: comunica a progressão didática da beginner tower.",
  },
  {
    key: "RF-052",
    kind: "functional",
    description:
      "Ao vencer um nível, o jogo avança ao próximo; o jogador pode reiniciar o nível atual a qualquer momento, recomeçando-o do estado inicial.",
    priority: "high",
    rationale: "CLR-002: progressão e reinício são parte do laço de jogo do Ruby Warrior.",
  },
  {
    key: "RF-053",
    kind: "functional",
    description:
      "Ao concluir um nível, uma tela de resultado mostra a pontuação do nível e o veredito de ace, consumindo o ScoringService (PR-006/feature 001).",
    priority: "high",
    rationale: "Fecha o laço de otimização: o jogador vê o score e se atingiu o ace.",
  },
  {
    key: "RF-054",
    kind: "functional",
    description:
      "Ao vencer o último nível da torre, uma tela de conclusão + créditos é exibida.",
    priority: "medium",
    rationale: "CLR-002: encerramento da experiência completa da torre exigido pela jam.",
  },
  {
    key: "RF-055",
    kind: "functional",
    description:
      "O progresso na torre (nível alcançado) é persistido em user:// e restaurado entre sessões.",
    priority: "high",
    rationale: "CLR-002: o jogador retoma de onde parou.",
  },
  // ── Áudio (PR-009) ────────────────────────────────────────────────────────────
  {
    key: "RF-056",
    kind: "functional",
    description:
      "Cada evento de turno (andar, atacar, levar dano, descansar, resgatar, atirar, vitória, derrota) dispara um efeito sonoro correspondente, acionado pelos TurnEvents.",
    priority: "medium",
    rationale: "CLR-001: feedback sonoro por ação, confirmado no escopo da entrega.",
  },
  {
    key: "RF-057",
    kind: "functional",
    description:
      "Há trilha sonora de fundo em loop durante o jogo, com controle de volume básico separado para música e efeitos.",
    priority: "medium",
    rationale: "CLR-001: imersão e polimento para a jam.",
  },
  {
    key: "RF-058",
    kind: "functional",
    description:
      "Sons e música vêm de assets de áudio CC0, referenciados por caminhos/recursos padronizados de modo que a troca pela arte sonora da 42 não exija reescrever lógica.",
    priority: "medium",
    rationale: "CLR-001: art swap de áudio sem refactor, espelhando o ponto de troca visual.",
  },
  // ── Não-funcionais ────────────────────────────────────────────────────────────
  {
    key: "RNF-050",
    kind: "non_functional",
    description:
      "O fluxo de torre e o áudio vivem na camada de apresentação/aplicação: 0 imports ou referências a áudio/fluxo de torre dentro de src/domain, verificável por grep.",
    priority: "highest",
    rationale: "CONV-002/ADR-001: domínio independente da engine e do fluxo de UI.",
  },
  {
    key: "RNF-051",
    kind: "non_functional",
    description:
      "Progresso da torre e volume são persistidos em user://: 100% em user:// e 0 escritas no repo; na ausência de save, o jogo inicia no nível 1 sem erro.",
    priority: "high",
    rationale: "Isola estado do jogador dos assets versionados; robustez no primeiro start.",
  },
  {
    key: "RNF-052",
    kind: "non_functional",
    description:
      "A reprodução de áudio disparada por eventos é assíncrona e adiciona 0 ms de latência ao loop de turno e ao TurnResolver: o tempo do ciclo de turno é o mesmo com e sem áudio.",
    priority: "high",
    rationale: "Determinismo (ADR-002): áudio é efeito de apresentação, não pode atrasar o ciclo de turno.",
  },
];
