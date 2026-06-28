extends GutTest
## Cobre os sentidos: feel/look/listen/health/direction_of_*, sem mutar estado.


func _state() -> LevelState:
	# warrior em 1 (facing +1), sludge em 3, escada em 5, largura 6.
	return LevelState.new(6, 5, Warrior.new(), 1, 1, {3: Sludge.new()}, 0)


func test_feel_adjacente() -> void:
	var s := Senses.new(_state())
	assert_true(s.feel(Direction.forward()).is_empty(), "posição 2 vazia")
	assert_true(s.feel(Direction.backward()).is_empty(), "posição 0 dentro da grade, vazia")


func test_feel_para_tras_na_borda() -> void:
	# warrior em 0 → feel backward vira parede.
	var state := LevelState.new(6, 5, Warrior.new(), 0, 1, {}, 0)
	assert_true(Senses.new(state).feel(Direction.backward()).is_wall())


func test_look_devolve_tres_espacos_ordenados() -> void:
	var spaces := Senses.new(_state()).look(Direction.forward())
	assert_eq(spaces.size(), 3)
	assert_true(spaces[0].is_empty(), "posição 2 vazia")
	assert_true(spaces[1].is_enemy(), "posição 3 tem sludge")


func test_listen_lista_unidades() -> void:
	var spaces := Senses.new(_state()).listen()
	assert_eq(spaces.size(), 1)
	assert_true(spaces[0].is_enemy())


func test_health_reflete_o_warrior() -> void:
	assert_eq(Senses.new(_state()).health(), 20)


func test_direction_of_stairs_a_frente() -> void:
	# escada em 5, warrior em 1 facing +1 → forward.
	assert_true(Senses.new(_state()).direction_of_stairs().equals(Direction.forward()))


func test_direction_of_stairs_atras_quando_facing_invertido() -> void:
	var state := _state().with_warrior_facing(-1)
	assert_true(Senses.new(state).direction_of_stairs().equals(Direction.backward()))


func test_direction_of_position_a_frente_e_atras() -> void:
	# warrior em 1 (facing +1): posição 3 está à frente, posição 0 atrás.
	var senses := Senses.new(_state())
	assert_true(senses.direction_of_position(3).equals(Direction.forward()))
	assert_true(senses.direction_of_position(0).equals(Direction.backward()))
