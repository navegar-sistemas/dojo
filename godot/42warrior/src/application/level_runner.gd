class_name LevelRunner
extends RefCounted
## Executa um nível: compila a lógica do jogador e roda o loop de turnos até o
## desfecho (ou MAX_TURNS). Reutilizável pela apresentação (Sprint 3) e pelos testes.

const MAX_TURNS := 200


## Retorna { "outcome": TurnResult.Outcome, "turns": int, "events": Array }.
func run(state: LevelState, solution_source: String) -> Dictionary:
	var script_runner := PlayerScriptRunner.new()
	var instance := script_runner.compile(solution_source)
	if instance == null:
		return {"outcome": TurnResult.Outcome.DEFEAT, "turns": 0, "events": []}

	var resolver := TurnResolver.new()
	var current := state
	var events: Array = []
	var turns := 0
	while turns < MAX_TURNS:
		var facade := WarriorFacade.new(current)
		var action := script_runner.play_turn(instance, facade)
		var result := resolver.resolve(current, action)
		current = result.state
		events.append_array(result.events)
		turns += 1
		if result.outcome != TurnResult.Outcome.ONGOING:
			return {"outcome": result.outcome, "turns": turns, "events": events}
	return {"outcome": TurnResult.Outcome.ONGOING, "turns": turns, "events": events}
