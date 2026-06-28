import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── Fundação data-driven do tema ─────────────────────────────────────────────────
  {
    key: "T-154",
    storyKey: "US-154",
    summary: "Criar o ThemeCatalog data-driven (linhagem EntityAssetRegistry): vocabulário de mensagens Unix/42 mapeado a eventos/erros + parâmetros de glitch + intensidade de corrupção por andar, com pontos de troca",
    definitionOfDone:
      "O ThemeCatalog existe como fonte única data-driven; mensagens de erro/feedback usam o vocabulário Unix/42 ('segfault (core dumped)', 'command not found', 'exit 0'); a ErrorView/console consomem do catálogo (0 literal Unix/42 hardcoded fora do catálogo); teste cobre o mapeamento evento→mensagem (RF-154).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  // ── US-151 — mecânica erro→glitch determinístico (núcleo) ────────────────────────
  {
    key: "T-151",
    storyKey: "US-151",
    summary: "Implementar o GlitchRule em Domain/Application: dado estado+seed determinístico (nível/andar/turno)+turn_events (incl. erro do código já tratado), produzir o efeito de glitch que afeta regra/mundo, sem RNG",
    definitionOfDone:
      "Quando o script do jogador lança erro, o mundo glitcha (warrior/tela/tile corrompem) além do log; teste de DOMÍNIO confirma que o mesmo estado+seed produz o MESMO resultado (determinístico, 0 RNG) e que a suíte de domínio permanece 100% verde sem regressão das 001–006 (RF-151, RNF-150).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-150 — conceito narrativo Kernel-42 ────────────────────────────────────────
  {
    key: "T-150",
    storyKey: "US-150",
    summary: "Aplicar o fio narrativo 'Kernel corrompido da 42' nos textos de menu/transição/resultado (via ScreenManager 006), lendo os textos do ThemeCatalog",
    definitionOfDone:
      "O menu e as telas de transição apresentam o conceito (torre = mainframe da 42 infectado; warrior = processo de debug) nos textos vindos do ThemeCatalog; verificação por inspeção das telas/textos (RF-150).",
    status: "done",
    dependsOn: ["T-154"],
    parallel: false,
    assignee: null,
  },
  // ── US-152 — pós-processo glitch escalando ───────────────────────────────────────
  {
    key: "T-152",
    storyKey: "US-152",
    summary: "Implementar o GlitchPostProcess (shader na câmera: RGB split/aberração/scanlines) com intensidade função dos turn_events (DAMAGED/DIED/erro) e do andar — só apresentação",
    definitionOfDone:
      "Em dano/morte/erro o pós-processo intensifica e depois relaxa; a intensidade é função determinística do estado/evento (mesmo estado → mesma intensidade); o efeito não toca regra (RF-152).",
    status: "done",
    dependsOn: ["T-151"],
    parallel: false,
    assignee: null,
  },
  // ── US-153 — corrupção progressiva da UI ─────────────────────────────────────────
  {
    key: "T-153",
    storyKey: "US-153",
    summary: "Implementar o UiCorruption: degradar a UI (scanlines/texto embaralhado/RGB split) de forma determinística conforme o andar, lendo a intensidade por andar do ThemeCatalog",
    definitionOfDone:
      "Andar mais alto → UI mais corrompida, de forma determinística por andar (mesma intensidade para o mesmo andar); verificação por inspeção em andares distintos; não regride a legibilidade essencial dos controles (RF-153).",
    status: "done",
    dependsOn: ["T-154"],
    parallel: true,
    assignee: null,
  },
];
