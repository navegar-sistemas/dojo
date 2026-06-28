class_name TurnResult
extends RefCounted
## Resultado imutável de um turno: o próximo estado, os eventos observados e o
## desfecho do nível.

enum Outcome { ONGOING, VICTORY, DEFEAT }

var state: LevelState
var events: Array
var outcome: Outcome


func _init(p_state: LevelState, p_events: Array, p_outcome: Outcome) -> void:
	state = p_state
	events = p_events
	outcome = p_outcome


func is_over() -> bool:
	return outcome != Outcome.ONGOING
