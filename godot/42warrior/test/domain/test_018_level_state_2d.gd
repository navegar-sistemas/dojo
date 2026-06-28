extends GutTest
## T-180 (018) — LevelState 2D: grade R×C, posição (linha,coluna), 1×N = R=1.
## Cobre: bounds 2D ([0,R-1]×[0,C-1]), grade R×C com unidades, compat 1D.


func test_grade_3x5_dentro_nao_e_parede() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_false(state.space_at_2d(Vector2i(0, 0)).is_wall())
	assert_false(state.space_at_2d(Vector2i(2, 4)).is_wall())
	assert_false(state.space_at_2d(Vector2i(1, 2)).is_wall())


func test_grade_3x5_linha_negativa_e_parede() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(state.space_at_2d(Vector2i(-1, 0)).is_wall())


func test_grade_3x5_linha_igual_rows_e_parede() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(state.space_at_2d(Vector2i(3, 0)).is_wall())


func test_grade_3x5_coluna_negativa_e_parede() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(state.space_at_2d(Vector2i(0, -1)).is_wall())


func test_grade_3x5_coluna_igual_cols_e_parede() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(state.space_at_2d(Vector2i(0, 5)).is_wall())


func test_corredor_1xn_compat_com_api_1d() -> void:
	# Grade 1×6, warrior col 1, facing +1, sludge col 3, escada col 5.
	var units_2d := {Vector2i(0, 3): Sludge.new()}
	var state_2d := LevelState.from_2d(
		1, 6, Vector2i(0, 5), Warrior.new(), Vector2i(0, 1), 1, units_2d, 0
	)
	# Equivalente 1D
	var state_1d := LevelState.new(6, 5, Warrior.new(), 1, 1, {3: Sludge.new()}, 0)

	assert_false(state_2d.space_at_2d(Vector2i(0, 2)).is_enemy(), "col 2 vazia")
	assert_true(state_2d.space_at_2d(Vector2i(0, 3)).is_enemy(), "col 3 = sludge")
	assert_true(state_2d.space_at_2d(Vector2i(0, 5)).is_stairs(), "col 5 = escada")
	assert_true(state_2d.space_at_2d(Vector2i(0, 6)).is_wall(), "col 6 fora = parede")
	# 1D legado ainda funciona identicamente
	assert_false(state_1d.space_at(2).is_enemy())
	assert_true(state_1d.space_at(3).is_enemy())
	assert_true(state_1d.space_at(5).is_stairs())
	assert_true(state_1d.space_at(6).is_wall())


func test_rows_e_cols_acessiveis() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(0, 0), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_eq(state.rows(), 3)
	assert_eq(state.cols(), 5)


func test_warrior_position_2d_acessivel() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(1, 2), 1, {}, 0)
	assert_eq(state.warrior_position_2d(), Vector2i(1, 2))


func test_stairs_position_2d_acessivel() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_eq(state.stairs_position_2d(), Vector2i(2, 4))


func test_with_warrior_position_2d_imutavel() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	var moved := state.with_warrior_position_2d(Vector2i(1, 3))
	assert_eq(state.warrior_position_2d(), Vector2i(0, 0), "original imutável")
	assert_eq(moved.warrior_position_2d(), Vector2i(1, 3))


func test_unidade_2d_em_espaco_correto() -> void:
	var sludge := Sludge.new()
	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {Vector2i(1, 2): sludge}, 0
	)
	assert_true(state.space_at_2d(Vector2i(1, 2)).is_enemy())
	assert_true(state.space_at_2d(Vector2i(1, 3)).is_empty())


func test_escada_2d_detectada() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 3), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(state.space_at_2d(Vector2i(2, 3)).is_stairs())
	assert_false(state.space_at_2d(Vector2i(1, 3)).is_stairs())
