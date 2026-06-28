/**
 * Schema dos artefatos de feature do fluxo de desenvolvimento (skill spec).
 * Este arquivo é a fonte de verdade do formato: cada artefato em specs/NNN-slug/*.ts
 * importa daqui e exporta constantes tipadas. O compilador TypeScript é parte do gate —
 * estrutura inválida não passa; regras semânticas (cobertura, ciclos, keys) são
 * verificadas pelo validate-feature da skill.
 */

/** Versão do schema de specs. Incrementa a cada mudança de schema ou de artefato
 *  obrigatório. v1 = artefatos .ts pré-convenções; v2 = conventions.ts/review.ts e tipos
 *  de convenção/revisão; v3 = fase clarify obrigatória + clarifications.ts; v4 = atual
 *  (proveniência opcional — autor/razão/data — em PR/princípio/convenção/ADR de projeto).
 *  O migrate-spec leva uma spec da versão detectada até esta. */
export const SPEC_SCHEMA_VERSION = 4;

export type TPriority = "lowest" | "low" | "medium" | "high" | "highest";

// ── Nível de projeto (specs/project/) — o contexto do sistema como um todo ───────
// As features derivam daqui: cada feature realiza ≥1 requisito de produto (PR-NNN),
// e a cadeia PR → feature → RF → US → T é verificada pelos gates.

/** Pessoa, papel ou sistema que participa do produto. A lista é a fonte de verdade
 *  para assignee de stories/tasks e from/to do chat. */
export interface IActor {
  name: string;
  description: string;
}

/** Princípio inegociável do projeto (a antiga constitution, em dado tipado). */
export interface IPrinciple {
  name: string;
  rule: string;
  /** O porquê — sem rationale o princípio vira letra morta. */
  rationale: string;
  provenance?: IProvenance;
}

/** Raiz do projeto (specs/project/product.ts). */
export interface IProduct {
  name: string;
  /** O que é o sistema, para quem, por quê — concreto, não slogan. */
  vision: string;
  businessGoals: string[];
  actors: IActor[];
  principles: IPrinciple[];
}

/** Requisito de produto — capacidade/épico de alto nível (specs/project/requirements.ts). */
export interface IProductRequirement {
  /** "PR-NNN" */
  key: string;
  title: string;
  description: string;
  priority: TPriority;
  provenance?: IProvenance;
}

export type TConventionSeverity = "required" | "recommended";
export type TConventionStatus = "accepted" | "superseded";
export type TCheckKind = "lint" | "typecheck" | "test" | "build" | "format" | "security";

/** Alternativa considerada e REJEITADA — memória para não re-propor o que já foi
 *  negado. Vive em convenções (ICodingConvention) e em ADRs (IArchitectureDecision). */
export interface IRejectedAlternative {
  alternative: string;
  reason: string;
}

/** Proveniência de uma mutação durável de projeto (PR-011): quem decidiu, por quê e quando.
 *  Opcional no schema — ausência não reprova (memória durável, não gate de comportamento). */
export interface IProvenance {
  /** Ator declarado no produto, ou "migração"/"legado" para o que veio antes da estampa. */
  author: string;
  /** O porquê da criação/alteração — a memória que evita re-litigar a decisão. */
  reason: string;
  /** YYYY-MM-DD */
  at: string;
}

/** Convenção de código declarada pelo PROJETO (specs/project/conventions.ts).
 *  A skill não traz conteúdo nenhum — cada projeto adequa o seu. */
export interface ICodingConvention {
  /** "CONV-NNN" */
  key: string;
  /** Onde se aplica: camada, tema ou glob (ex.: "camada model", "tratamento de erro", "src/**"). */
  scope: string;
  /** A regra normativa, afirmativa. */
  rule: string;
  /** O porquê — sem rationale a convenção é cargo cult. */
  rationale: string;
  /** Quem manda: "mandato da empresa X", "best practice", "decisão do time". Um mandato
   *  do projeto prevalece sobre best-practice genérica mesmo quando não-ideal. */
  authority: string;
  severity: TConventionSeverity;
  /** Exemplos calibram implementador e revisor (o que segue / o que viola a regra). */
  examples: { good: string; bad: string };
  /** Checagem mecânica que a verifica (comando/regra), ou null se só por revisão de agente. */
  check: string | null;
  status: TConventionStatus;
  /** Alternativas já rejeitadas para esta convenção — não re-propor. */
  rejectedAlternatives?: IRejectedAlternative[];
  provenance?: IProvenance;
}

/** Checagem executável declarada pelo projeto — a skill RODA a do projeto, nunca traz a sua. */
export interface IProjectCheck {
  name: string;
  /** Comando do projeto (ex.: "npm run typecheck", "ruff check ."). */
  command: string;
  kind: TCheckKind;
}

/** Fase corrente da feature no fluxo: clarifying → discovery → planning → backlog → sprinting → implementing → done. */
export type TPhase = "clarifying" | "discovery" | "planning" | "backlog" | "sprinting" | "implementing" | "done";

export type TRequirementKind = "functional" | "non_functional";
export type TStoryStatus = "backlog" | "todo" | "in_progress" | "review" | "done";
export type TTaskStatus = "todo" | "in_progress" | "review" | "done";
export type TSprintState = "future" | "active" | "closed";
export type TAdrStatus = "proposed" | "accepted" | "superseded";

/** Raiz da feature (feature.ts). Prosa longa em template literals. */
export interface IFeature {
  /** "NNN-slug" — igual ao nome da pasta. */
  key: string;
  name: string;
  /** O problema que justifica a feature — por que ela existe, para quem. */
  problem: string;
  /** Requisitos de produto (PR-NNN) que esta feature realiza — a feature é o elo
   *  entre o contexto do sistema e a execução; ≥1 obrigatório (gate). */
  productRequirementKeys: string[];
  goals: string[];
  outOfScope: string[];
  /** Decisões de produto registradas com o usuário durante o discovery. */
  productDecisions: string[];
  phase: TPhase;
  /** YYYY-MM-DD */
  createdAt: string;
}

/** Um par pergunta→resposta registrado na clarify (clarifications.ts). */
export interface IClarificationQA {
  question: string;
  answer: string;
}

/** Esclarecimento ratificado pelo usuário na fase clarify (clarifications.ts) — antes de
 *  qualquer requisito/código. O gate exige status "confirmed" com confirmador e data: o
 *  artefato prova que o entendimento foi VALIDADO com o usuário, não presumido pelo agente.
 *  Espelha o padrão de registro ratificado do IReviewRecord (status + ator + data). */
export interface IClarification {
  /** "CLR-NNN" */
  key: string;
  /** Assunto esclarecido (escopo, atores, dados, exceções, limites, tempo, resumo do entendimento...). */
  topic: string;
  /** Perguntas feitas ao usuário e as respostas dele — sem Q&A respondido não há confirmação. */
  questions: IClarificationQA[];
  status: "pending" | "confirmed";
  /** Quem confirmou — o usuário/PO que validou o entendimento (não necessariamente um ator de implementação). */
  confirmedBy: string | null;
  /** YYYY-MM-DD */
  confirmedAt: string | null;
}

/** Requisito levantado no discovery (requirements.ts). */
export interface IRequirement {
  /** "RF-001" (functional) | "RNF-001" (non_functional). */
  key: string;
  kind: TRequirementKind;
  /** Comportamento testável — dá para provar verdadeiro/falso. */
  description: string;
  priority: TPriority;
  rationale?: string;
}

/** Decisão de arquitetura no formato ADR (architecture.ts). */
export interface IArchitectureDecision {
  /** "ADR-001" */
  key: string;
  title: string;
  /** Situação/forças que motivam a decisão. */
  context: string;
  decision: string;
  consequences: string;
  status: TAdrStatus;
  /** Requisitos que esta decisão atende (rastreabilidade). */
  requirementKeys: string[];
  /** Alternativas consideradas e rejeitadas — memória para não re-propor em sessões futuras. */
  rejectedAlternatives?: IRejectedAlternative[];
  provenance?: IProvenance;
}

/** Componente da visão de arquitetura (architecture.ts) — nível container/módulo. */
export interface IComponent {
  name: string;
  responsibility: string;
  /** Nomes de outros componentes dos quais depende. */
  dependsOn: string[];
  requirementKeys: string[];
}

/** User story do backlog (backlog.ts). */
export interface IUserStory {
  /** "US-001" */
  key: string;
  asA: string;
  iWant: string;
  soThat: string;
  /** Critérios Dado/Quando/Então — observáveis. */
  acceptanceCriteria: string[];
  /** Requisitos que a story cobre (≥1). */
  requirementKeys: string[];
  priority: TPriority;
  storyPoints: number;
  status: TStoryStatus;
  assignee: string | null;
}

/** Tarefa técnica derivada de uma story (tasks.ts). */
export interface ITask {
  /** "T-001" */
  key: string;
  /** Story à qual pertence ("US-NNN"). */
  storyKey: string;
  summary: string;
  /** Critério verificável de conclusão. */
  definitionOfDone: string;
  status: TTaskStatus;
  /** Keys de tasks que precisam concluir antes ("T-NNN"). */
  dependsOn: string[];
  /** Pode rodar em paralelo com outras tasks paralelas (sem dependência mútua). */
  parallel: boolean;
  assignee: string | null;
}

/** Sprint/iteração (sprints.ts) — aloca stories do backlog. */
export interface ISprint {
  id: number;
  name: string;
  goal: string;
  state: TSprintState;
  /** YYYY-MM-DD; "" enquanto aberto/não definido. */
  startDate: string;
  endDate: string;
  /** Stories alocadas ("US-NNN"). */
  storyKeys: string[];
}

// ── Chat de coordenação (chat.ts) ─────────────────────────────────────────────
// Mensagens discriminadas por `type`: cada tipo carrega o próprio workflow de status.
// Escreva no chat apenas o que tem impacto externo (bloqueio, pergunta, handoff,
// informação relevante a outros) — progresso interno não entra.

export interface IMessageBloqueio {
  type: "BLOQUEIO";
  /** Descrição do impedimento, impacto e o que é preciso para destravar. */
  data: string;
  status: "pendente" | "resolvido";
}

export interface IMessagePergunta {
  type: "PERGUNTA";
  data: string;
  status: "pendente" | "respondida";
}

export interface IMessageHandoff {
  type: "HANDOFF";
  /** O que está sendo entregue/transferido e o que o destinatário deve fazer. */
  data: string;
  status: "pendente" | "concluido";
}

export interface IMessageInfo {
  type: "INFO";
  data: string;
}

export type TMessage = IMessageBloqueio | IMessagePergunta | IMessageHandoff | IMessageInfo;

export interface IChatEntry {
  /** Quem escreve (agente/pessoa/sistema). */
  from: string;
  /** Destinatários; ["all"] para broadcast. */
  to: string[];
  message: TMessage;
  /** YYYY-MM-DD */
  at: string;
}

/** Tópico de conversa — um assunto por tópico; crie novo só para assunto novo. */
export interface IChatTopic {
  name: string;
  entries: IChatEntry[];
}

// ── Revisão de código e conformidade (review.ts) ──────────────────────────────
// Registro vivo da revisão por task/fase: confronta implementação × spec × convenções.
// O gate review-feature.ts consome estes registros; o doctor os agrega.

export type TReviewTarget = "spec" | "code";
export type TReviewStatus = "approved" | "changes_requested" | "pending";
export type TFindingKind =
  | "conformidade_spec"
  | "desvio_convencao"
  | "uso_de_padrao_rejeitado"
  | "padrao_candidato_nao_documentado";
export type TFindingSeverity = "blocker" | "warning";

/** Resultado registrado de uma checagem executável do projeto naquela revisão. */
export interface IReviewCheckOutcome {
  name: string;
  command: string;
  passed: boolean;
}

/** Achado da revisão; resolution null = pendente (impede o status approved). */
export interface IReviewFinding {
  kind: TFindingKind;
  severity: TFindingSeverity;
  detail: string;
  /** Arquivo/símbolo onde ocorre (diff-scoped), quando aplicável. */
  location: string | null;
  /** Como foi resolvido (refatorado, convenção CONV-NNN criada, alternativa rejeitada) — null enquanto pendente. */
  resolution: string | null;
}

/** Registro de uma revisão (review.ts) — alvo spec (qualidade da fase) ou code (task). */
export interface IReviewRecord {
  target: TReviewTarget;
  /** Task revisada ("T-NNN") quando target=code; null quando target=spec. */
  taskKey: string | null;
  /** Fase revisada (ex.: "backlog") quando target=spec; null quando target=code. */
  phase: string | null;
  status: TReviewStatus;
  /** Checagens do projeto rodadas nesta revisão (resultado registrado). */
  checks: IReviewCheckOutcome[];
  findings: IReviewFinding[];
  /** Ator revisor (deve ser ator declarado no produto). */
  reviewer: string;
  /** YYYY-MM-DD */
  reviewedAt: string;
}
