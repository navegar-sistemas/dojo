class_name ScoringService
extends RefCounted

const CAPTIVE_POINTS := 20


func score(events: Array, turns_taken: int, definition: LevelDefinition) -> Score:
	var total := _unit_points(events) + _time_bonus(definition, turns_taken)
	return Score.new(total, definition.ace_score)


func _unit_points(events: Array) -> int:
	var points := 0
	for event in events:
		if event.kind == TurnEvent.Kind.ENEMY_DEFEATED:
			points += event.amount
		elif event.kind == TurnEvent.Kind.RESCUED:
			points += CAPTIVE_POINTS
	return points


## Decresce 1 por turno gasto, sem ficar negativo. Modelo aproximado do Ruby
## Warrior (a curva exata do original ainda não foi confirmada).
func _time_bonus(definition: LevelDefinition, turns_taken: int) -> int:
	return maxi(0, definition.time_bonus - turns_taken)
