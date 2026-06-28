class_name ThemeCatalog
extends RefCounted
## Catálogo data-driven do tema 'Kernel corrompido da 42' (ADR-036, RF-154).
## Fonte única de mensagens Unix/42 e intensidade de corrupção por andar.
## Apresentação e narrativa leem daqui; 0 literal Unix/42 fora deste arquivo.

const _MESSAGES: Dictionary = {
	"error_compile": "syntax error near unexpected token",
	"error_runtime": "segfault (core dumped)",
	"error_loop": "killed: SIGTERM — loop limit exceeded",
	"error_no_method": "command not found: play_turn",
	"error_no_action": "process returned 0",
	"victory": "exit 0  —  processo concluido",
	"defeat": "SIGKILL  —  processo terminado",
	"warrior_damaged": "integrity fault: sector corrupted",
	"warrior_died": "kernel panic — not syncing: fatal exception",
	"floor_heading": "KERNEL/FLOOR_%02d :: INICIANDO DESFRAGMENTACAO",
	"floor_cleared": "sector cleared — corruption removed",
	"ace": "ACE — all sectors clean, bonus allocated",
	"retry": "re-exec: tentando novamente",
	"score_label": "[%d pts] (%d turnos)",
}

## Intensidade de corrupção da UI por andar (índice 1–9).
## Andar 1 = quase limpo; andar 9 = corrupção máxima.
const _CORRUPTION_BY_FLOOR: Array = [0.0, 0.04, 0.08, 0.14, 0.22, 0.32, 0.46, 0.62, 0.78, 1.0]


static func message(key: String, args: Array = []) -> String:
	var msg: String = _MESSAGES.get(key, key)
	if args.is_empty():
		return msg
	return msg % args


static func corruption_for_floor(floor_index: int) -> float:
	if floor_index <= 0 or floor_index >= _CORRUPTION_BY_FLOOR.size():
		return 0.0
	return _CORRUPTION_BY_FLOOR[floor_index]
