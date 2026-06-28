extends GutTest
## Cobre o VO Space e as consultas imutáveis do LevelState.


func _build_state() -> LevelState:
	# Grade 0..5, warrior em 1 olhando +1, sludge em 3, escada em 5.
	var units := {3: Sludge.new()}
	return LevelState.new(6, 5, Warrior.new(), 1, 1, units, 0)


func test_space_fora_da_grade_e_parede() -> void:
	var state := _build_state()
	assert_true(state.space_at(-1).is_wall())
	assert_true(state.space_at(6).is_wall())


func test_space_vazio() -> void:
	var space := _build_state().space_at(2)
	assert_true(space.is_empty())
	assert_false(space.is_enemy())


func test_space_com_inimigo() -> void:
	var space := _build_state().space_at(3)
	assert_true(space.is_enemy())
	assert_false(space.is_empty())
	assert_eq(space.unit_type(), "Sludge")


func test_space_com_cativo() -> void:
	var state := LevelState.new(6, 5, Warrior.new(), 1, 1, {2: Captive.new()}, 0)
	var space := state.space_at(2)
	assert_true(space.is_captive())
	assert_false(space.is_enemy())
	assert_eq(space.unit_type(), "Captive")


func test_space_da_escada() -> void:
	var space := _build_state().space_at(5)
	assert_true(space.is_stairs())
	assert_true(space.is_empty(), "escada sem unidade ainda é vazia de unidades")


func test_step_e_posicao_por_direcao() -> void:
	var state := _build_state()
	assert_eq(state._step_of(Direction.forward()), 1)
	assert_eq(state._step_of(Direction.backward()), -1)
	assert_eq(state.position_toward(Direction.forward(), 2), 3)


func test_facing_invertido_inverte_o_step() -> void:
	var state := _build_state().with_warrior_facing(-1)
	assert_eq(state._step_of(Direction.forward()), -1)


func test_with_warrior_position_nao_muta_original() -> void:
	var state := _build_state()
	var moved := state.with_warrior_position(2)
	assert_eq(state.warrior_position(), 1, "original imutável")
	assert_eq(moved.warrior_position(), 2)


func test_with_unit_at_remove_e_substitui_sem_mutar() -> void:
	var state := _build_state()
	var cleared := state.with_unit_at(3, null)
	assert_true(state.space_at(3).is_enemy(), "original imutável")
	assert_true(cleared.space_at(3).is_empty())
