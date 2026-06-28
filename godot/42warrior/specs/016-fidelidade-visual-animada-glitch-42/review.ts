import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

const CHECKS_T160: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture (Domain/Application puros)",
    command: "bash scripts/arch_guard.sh",
    passed: true,
  },
  {
    name: "Formatação + lint GDScript (gdformat/gdlint sobre src e test)",
    command: "bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 212/212 (inclui a prova de render do T-160)",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

const CHECKS_T161_T162: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture + lint GDScript",
    command: "bash scripts/arch_guard.sh && bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 226/226 na main pós-merge (inclui render-proof do TileMapArena e os 4 estados do FourStateButton)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T172: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture + lint GDScript (0 warnings)",
    command: "bash scripts/arch_guard.sh && bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 224/224 (assert HARD heading_font()/body_font()!=null, sem pending; .import das 4 fontes committados @73cfefd)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T163: IReviewCheckOutcome[] = [
  {
    name: "Render-proof COUNT-LEVEL (tela JOGO @d6b6ccf): floor_layer.get_used_cells().size()>0 (arena não-preta) + AnimatedSprite2D posicionado em Entities + get_theme_font().resource_path>0 (fonte real != default)",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 251/251 no sha aceito; código integrado na main (merge 072909d)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T164: IReviewCheckOutcome[] = [
  {
    name: "Render-proof COUNT-LEVEL (tela MENU @b9771c1): KeyArt.texture != null (key_art.png realmente carregada) + get_theme_font().resource_path>0 (fonte real != default); BootLog assere o texto '42warrior'",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 260/260 no sha aceito; código integrado na main (merge e64c3f0)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T165: IReviewCheckOutcome[] = [
  {
    name: "Render-proof COUNT-LEVEL (tela SELEÇÃO @98b1a89): LevelGrid com >=9 botões contados + LevelBtn bloqueado disabled==true (estado visual real — o assert pegou bug real do boss-btn) + fonte real",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 259/259 no sha aceito; código integrado na main (merge c5d42cb)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-160",
    phase: null,
    status: "approved",
    checks: CHECKS_T160,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-161",
    phase: null,
    status: "approved",
    checks: CHECKS_T161_T162,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-162",
    phase: null,
    status: "approved",
    checks: CHECKS_T161_T162,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-172",
    phase: null,
    status: "approved",
    checks: CHECKS_T172,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-163",
    phase: null,
    status: "approved",
    checks: CHECKS_T163,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-164",
    phase: null,
    status: "approved",
    checks: CHECKS_T164,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-165",
    phase: null,
    status: "approved",
    checks: CHECKS_T165,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
