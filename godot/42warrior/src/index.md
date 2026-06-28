# `src/` — Código-fonte

Código do jogo, organizado em camadas de **Clean Architecture**. As dependências apontam
sempre para dentro: `presentation → application → domain`.

| Pasta | Camada | Status |
|---|---|---|
| [`domain/`](domain/index.md) | Regras puras do jogo (sem dependência da Godot) | ✅ Sprint 1 |
| `application/` | Casos de uso: rodar código do jogador, carregar nível, progressão | ⬜ Sprint 2 |
| `presentation/` | Camada Godot: telas, sprites, input, áudio | ⬜ Sprint 3 |

> Hoje só existe `domain/`. As pastas `application/` e `presentation/` nascem nos
> próximos sprints. A regra de arquitetura é verificada por `scripts/arch_guard.sh`.
