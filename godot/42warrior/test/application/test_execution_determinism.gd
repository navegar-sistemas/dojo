extends GutTest
## RNF-041: o estado final do nível deve ser idêntico entre execução contínua
## (LevelRunner.run) e execução passo-a-passo (TurnResolver chamado turno a turno).

const MAX_TURNS := 200


func _run_continuous(state: LevelState, source: String) -> Dictionary:
	return LevelRunner.new().run(state, source)


func _run_step_by_step(state: LevelState, source: String) -> Dictionary:
	var runner := PlayerScriptRunner.new()
	var compiled := runner.compile(source)
	if compiled == null:
		return {"outcome": TurnResult.Outcome.DEFEAT, "turns": 0, "state": state}
	var resolver := TurnResolver.new()
	var current := state
	var turns := 0
	var outcome := TurnResult.Outcome.ONGOING
	while turns < MAX_TURNS:
		var facade := WarriorFacade.new(current)
		var action := runner.play_turn(compiled, facade)
		var result := resolver.resolve(current, action)
		current = result.state
		turns += 1
		if result.outcome != TurnResult.Outcome.ONGOING:
			outcome = result.outcome
			break
	return {"outcome": outcome, "turns": turns, "state": current}


func _initial_state(level: int) -> LevelState:
	return LevelLoader.new().load_definition(BeginnerTower.definition(level))


func _solution(level: int) -> String:
	return ReferenceSolutions.for_level(level)


func test_nivel_1_resultado_identico() -> void:
	var state := _initial_state(1)
	var source := _solution(1)
	var continuous := _run_continuous(state, source)
	var step_by_step := _run_step_by_step(state, source)
	assert_eq(continuous["outcome"], step_by_step["outcome"], "outcome idêntico")
	assert_eq(continuous["turns"], step_by_step["turns"], "turnos idênticos")


func test_nivel_3_resultado_identico() -> void:
	var state := _initial_state(3)
	var source := _solution(3)
	var continuous := _run_continuous(state, source)
	var step_by_step := _run_step_by_step(state, source)
	assert_eq(continuous["outcome"], step_by_step["outcome"], "outcome idêntico")
	assert_eq(continuous["turns"], step_by_step["turns"], "turnos idênticos")


func test_nivel_5_resultado_identico() -> void:
	var state := _initial_state(5)
	var source := _solution(5)
	var continuous := _run_continuous(state, source)
	var step_by_step := _run_step_by_step(state, source)
	assert_eq(continuous["outcome"], step_by_step["outcome"], "outcome idêntico")
	assert_eq(continuous["turns"], step_by_step["turns"], "turnos idênticos")
