import type { ICodingConvention, IProjectCheck } from "../types.ts";

/**
 * Convenções de código DESTE projeto e suas checagens executáveis (fase 0 — inception).
 * A skill NÃO impõe conteúdo: preencha conforme o projeto. Uma convenção pode ser um
 * mandato que prevalece sobre "best practice" genérica mesmo quando não-ideal — grave
 * isso em `authority`. Decisões já rejeitadas vão em `rejectedAlternatives` (não re-propor).
 *
 * Cada convenção: key "CONV-NNN", scope, rule, rationale, authority, severity
 * ("required" | "recommended"), examples { good, bad }, check (comando) | null, status.
 */
export const conventions: ICodingConvention[] = [
  {
    key: "CONV-001",
    scope: "todos os scripts (.gd)",
    rule: "Um arquivo .gd tem uma única responsabilidade e declara class_name quando é uma classe reutilizável do domínio/aplicação. O nome do arquivo (snake_case) reflete a classe (PascalCase).",
    rationale:
      "Responsabilidade única e nomes previsíveis tornam o código navegável e evitam scripts gigantes multifunção — princípio central do projeto.",
    authority: "mandato do projeto (princípio: responsabilidade única em arquivo e método)",
    severity: "required",
    examples: {
      good: "warrior.gd → class_name Warrior extends RefCounted (só estado e comportamento do warrior)",
      bad: "game.gd com warrior, inimigos, render, input e pontuação no mesmo arquivo",
    },
    check: null,
    status: "accepted",
  },
  {
    key: "CONV-002",
    scope: "camada Domain e Application",
    rule: "Scripts de Domain e Application NÃO podem fazer 'extends Node'/'extends Node2D' nem referenciar tipos de cena/UI; estendem RefCounted (ou Resource para dados). A direção de dependência aponta para dentro: Presentation→Application→Domain, nunca o contrário.",
    rationale:
      "Clean Architecture: o domínio é independente da engine, testável isoladamente e estável frente a mudanças de apresentação (ADR-001).",
    authority: "mandato do projeto (ADR-001, princípio: domínio independente da engine)",
    severity: "required",
    examples: {
      good: "class_name TurnResolver extends RefCounted; recebe LevelState e Action, retorna novo LevelState",
      bad: "class_name TurnResolver extends Node; chama get_node('../Sprite') dentro da regra de turno",
    },
    check: null,
    status: "accepted",
  },
  {
    key: "CONV-003",
    scope: "métodos",
    rule: "Cada método faz uma só coisa e separa consulta de comando (CQS): sentidos retornam valor sem mutar estado; ações retornam novo estado/efeito. Métodos curtos; sem flags booleanas que façam o método ramificar em duas responsabilidades.",
    rationale:
      "Métodos de responsabilidade única são testáveis e legíveis; CQS preserva o determinismo do turno (ADR-002).",
    authority: "mandato do projeto (princípio: turno determinístico; método responsabilidade única)",
    severity: "required",
    examples: {
      good: "func feel(direction) -> Space (puro); func walk(direction) -> LevelState (novo estado)",
      bad: "func act(direction, do_attack: bool) que ora anda ora ataca conforme a flag",
    },
    check: null,
    status: "accepted",
  },
  {
    key: "CONV-004",
    scope: "tipagem GDScript",
    rule: "Tipagem estática obrigatória: parâmetros, retornos e variáveis tipados; nada de Variant implícito em APIs públicas. Usar enums/constantes nomeadas para direções e tipos, não strings mágicas.",
    rationale:
      "Tipos estáticos capturam erros em tempo de parse e documentam contratos; constantes nomeadas evitam typos e dão refatoração segura.",
    authority: "best practice (GDScript style guide) reforçada pelo projeto",
    severity: "required",
    examples: {
      good: "func attack(direction: Direction.Value) -> CombatResult:",
      bad: "func attack(direction):  # sem tipo; direction == 'forward' espalhado em strings",
    },
    check: null,
    status: "accepted",
  },
  {
    key: "CONV-005",
    scope: "estilo e nomenclatura",
    rule: "Seguir o GDScript style guide: snake_case para funções/variáveis, PascalCase para classes, UPPER_SNAKE para constantes/enum values; formatação via gdformat e zero violações de gdlint. Comentários só explicam o porquê (decisão/invariante), nunca o óbvio.",
    rationale:
      "Estilo consistente e verificável mecanicamente reduz ruído de revisão e mantém o codebase coeso na pressão da jam.",
    authority: "best practice (Godot style guide) com checagem mecânica do projeto",
    severity: "required",
    examples: {
      good: "const MAX_HEALTH := 20  # com gdformat aplicado",
      bad: "var MaxHealth = 20  # comentário: 'saude maxima' (redundante)",
    },
    check: "bash scripts/lint.sh",
    status: "accepted",
  },
  {
    key: "CONV-006",
    scope: "testes de domínio",
    rule: "Toda regra de Domain/Application tem teste unitário (GUT) determinístico, sem dependência de cena/render. Comportamento novo ou correção exige teste rodado e verde antes de concluir a task.",
    rationale:
      "O domínio é puro e determinístico justamente para ser testável; testes provam paridade com o Ruby Warrior e protegem contra regressão.",
    authority: "mandato do projeto (regra de operação: rodar testes antes de concluir)",
    severity: "required",
    examples: {
      good: "test_attack_backward_does_reduced_damage() compara dano forward vs backward",
      bad: "validar a regra 'por inspeção' sem teste executado",
    },
    check: "bash scripts/test.sh",
    status: "accepted",
  },
  {
    key: "CONV-007",
    scope: "comentários no código (todos os .gd)",
    rule: "Comentário é último recurso, não default. Só é permitido quando o código é genuinamente difícil e o comentário explica o PORQUÊ não-óbvio (decisão arquitetural, invariante sutil, workaround de bug específico, restrição oculta, fidelidade a um comportamento do Ruby Warrior que o código sozinho não revela). É PROIBIDO comentário que apenas reafirma o que o código já diz (nome de função/variável, tipo, passo trivial), comentário-narração de IA ('agora fazemos X', 'aqui criamos Y', 'loop pelos inimigos'), TODO/placeholder genérico e cabeçalho decorativo. Teste antes de escrever: se removendo o comentário um dev profissional não perde nenhuma informação, NÃO escreva. O código deve se explicar por nomes e estrutura; comentário cobre só o que o código não consegue carregar.",
    rationale: "Comentários redundantes ou narrativos são ruído: envelhecem, mentem quando o código muda, poluem o diff e sinalizam código gerado por IA sem cuidado — exatamente o que o dono do produto não quer no projeto. Reservar comentário para o porquê não-óbvio mantém o sinal alto e o codebase profissional.",
    authority: "mandato do dono do produto (usuario) — prevalece sobre qualquer hábito de comentar gerado por ferramenta de IA",
    severity: "required",
    examples: { good: "# backward causa só metade do dano: paridade com Ruby Warrior (Warrior#attack!)\nfunc attack(direction: Direction.Value) -> CombatResult:", bad: "# função que ataca na direção\nfunc attack(direction): # ataca  ->  var inimigos = [] # lista de inimigos" },
    check: null,
    status: "accepted",
    provenance: { author: "usuario", reason: "Dono do produto exige proibir comentários estúpidos/narrativos de IA; comentar só em última instância para código complexo explicando o porquê não-óbvio.", at: "2026-06-27" },
  },
];

/** Comandos de checagem que a skill executa no gate de revisão (lint/type/test/build/...). */
export const checks: IProjectCheck[] = [
  {
    name: "Formatação + lint GDScript (gdformat/gdlint sobre src e test)",
    command: "bash scripts/lint.sh",
    kind: "lint",
  },
  {
    name: "Guard de Clean Architecture (Domain/Application puros)",
    command: "bash scripts/arch_guard.sh",
    kind: "lint",
  },
  {
    name: "Testes unitários de domínio (GUT, headless)",
    command: "bash scripts/test.sh",
    kind: "test",
  },
];
