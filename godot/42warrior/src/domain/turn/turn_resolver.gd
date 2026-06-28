class_name TurnResolver
extends RefCounted
## Resolve um turno de forma pura e determinística: aplica a ação do warrior,
## checa vitória, deixa os inimigos reagirem e checa derrota. Não muta a entrada.

var _applier: ActionApplier
var _enemy_phase: EnemyPhase


func _init() -> void:
	_applier = ActionApplier.new()
	_enemy_phase = EnemyPhase.new()


func resolve(state: LevelState, action: Action) -> TurnResult:
	var after_action: Dictionary = _applier.apply(state, action)
	var current: LevelState = after_action.state
	var events: Array = (after_action.events as Array).duplicate()

	if _reached_stairs(current):
		events.append(TurnEvent.new(TurnEvent.Kind.WON, "warrior"))
		return TurnResult.new(_advanced(current), events, TurnResult.Outcome.VICTORY)

	# Percepção dos inimigos: warrior na posição CORRENTE (recuo tira do alcance), mas
	# bloqueadores de linha do INÍCIO do turno (um inimigo morto/cativo resgatado neste
	# turno ainda bloqueava a linha quando os inimigos decidiram). Dano aplicado em `current`.
	var perception: LevelState = current.with_units(state.units_snapshot())
	var after_enemies: Dictionary = _enemy_phase.react(perception, current)
	current = after_enemies.state
	events.append_array(after_enemies.events as Array)

	if not current.warrior().is_alive():
		events.append(TurnEvent.new(TurnEvent.Kind.DIED, "warrior"))
		return TurnResult.new(_advanced(current), events, TurnResult.Outcome.DEFEAT)

	return TurnResult.new(_advanced(current), events, TurnResult.Outcome.ONGOING)


func _reached_stairs(state: LevelState) -> bool:
	return state.warrior_position() == state.stairs_position()


func _advanced(state: LevelState) -> LevelState:
	return state.with_turn(state.turn() + 1)
