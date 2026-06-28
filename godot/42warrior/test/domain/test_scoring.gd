extends GutTest

var _scoring: ScoringService


func before_each() -> void:
	_scoring = ScoringService.new()


func _definition() -> LevelDefinition:
	return BeginnerTower.definition(3)


func test_pontos_por_inimigo_derrotado_usam_o_hp() -> void:
	var events := [TurnEvent.new(TurnEvent.Kind.ENEMY_DEFEATED, "Sludge", 12, 4)]
	var score := _scoring.score(events, 0, _definition())
	assert_eq(score.total, 12 + _definition().time_bonus)


func test_resgate_vale_pontos_fixos() -> void:
	var events := [
		TurnEvent.new(TurnEvent.Kind.RESCUED, "warrior", 0, 2),
		TurnEvent.new(TurnEvent.Kind.RESCUED, "warrior", 0, 6),
	]
	var score := _scoring.score(events, 0, _definition())
	assert_eq(score.total, 2 * ScoringService.CAPTIVE_POINTS + _definition().time_bonus)


func test_time_bonus_decai_por_turno() -> void:
	var bonus := _definition().time_bonus
	assert_eq(_scoring.score([], 5, _definition()).total, bonus - 5)


func test_time_bonus_nao_fica_negativo() -> void:
	assert_eq(_scoring.score([], 9999, _definition()).total, 0)


func test_ace_quando_atinge_o_ace_score() -> void:
	var definition := BeginnerTower.definition(1)
	var defeats: Array = []
	for i in range(20):
		defeats.append(TurnEvent.new(TurnEvent.Kind.ENEMY_DEFEATED, "Sludge", 12, i))
	assert_true(_scoring.score(defeats, 0, definition).is_ace())


func test_nao_ace_quando_abaixo() -> void:
	assert_false(_scoring.score([], 9999, BeginnerTower.definition(5)).is_ace())
