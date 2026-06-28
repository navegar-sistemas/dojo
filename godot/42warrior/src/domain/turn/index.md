# `src/domain/turn/` — Resolução do turno

O mecanismo central do jogo: pegar a ação do warrior, aplicá-la, deixar os inimigos
reagirem e decidir o desfecho. Tudo puro e determinístico.

| Arquivo | Classe | Responsabilidade |
|---|---|---|
| `turn_resolver.gd` | `TurnResolver` | **Orquestra o turno**: aplica a ação → checa vitória → inimigos reagem → checa derrota → incrementa o turno. ⭐ |
| `action_applier.gd` | `ActionApplier` | Aplica a ação **do warrior** (despacho por tipo): walk, attack (metade para trás), rest (cura 10%). |
| `turn_result.gd` | `TurnResult` | Resultado imutável: novo estado, eventos e desfecho (`ONGOING`/`VICTORY`/`DEFEAT`). |
| `turn_event.gd` | `TurnEvent` | Evento observável (`MOVED`, `ATTACKED`, `DAMAGED`, `RESTED`, `RESCUED`, `SHOT`, `ENEMY_DEFEATED`, `WON`, `DIED`). |
| [`actions/`](actions/index.md) | — | Os objetos de comando do warrior. |

## Ordem do turno (importa!)

1. Aplica a ação do warrior.
2. **Chegou na escada? → VITÓRIA** (antes de os inimigos agirem).
3. Inimigos reagem ([`../combat/`](../combat/index.md)).
4. Vida do warrior zerou? → DERROTA.
5. Incrementa o turno.

Os **eventos** são a ponte para a futura camada visual (Sprint 3): ela lê `MOVED`,
`DAMAGED` etc. para animar e tocar áudio.
