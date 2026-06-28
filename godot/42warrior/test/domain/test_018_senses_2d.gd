extends GutTest
## T-182 (018) — Sentidos 2D: feel/look/direction_of_2d/direction_of_stairs_2d
## usando posições Vector2i (NORTH/SOUTH/EAST/WEST). 0-regressão 1D garantida
## pelos testes existentes em test_senses.gd.


func _feel_state() -> LevelState:
	# 4×5, warrior (2,2), sludge (3,2), escada (3,4)
	return LevelState.from_2d(
		4, 5, Vector2i(3, 4), Warrior.new(), Vector2i(2, 2), 1, {Vector2i(3, 2): Sludge.new()}, 0
	)


func test_feel_2d_norte_celula_vazia() -> void:
	var s := Senses.new(_feel_state())
	var space := s.feel_2d(Direction.north())
	assert_false(space.is_wall(), "(1,2) dentro da grade")
	assert_true(space.is_empty(), "(1,2) vazia")


func test_feel_2d_sul_inimigo() -> void:
	var s := Senses.new(_feel_state())
	var space := s.feel_2d(Direction.south())
	assert_true(space.is_enemy(), "(3,2) tem sludge")


func test_feel_2d_leste_escada() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(1, 2), Warrior.new(), Vector2i(1, 1), 1, {}, 0)
	var space := Senses.new(state).feel_2d(Direction.east())
	assert_true(space.is_stairs(), "(1,2) é a escada")


func test_feel_2d_oeste_e_parede_fora_de_bounds() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(2, 0), 1, {}, 0)
	var space := Senses.new(state).feel_2d(Direction.west())
	assert_true(space.is_wall(), "(2,-1) fora da grade é parede")


func test_look_2d_sul_retorna_3_espacos() -> void:
	# warrior (0,2), sem unidades próximas ao sul
	var state := LevelState.from_2d(5, 5, Vector2i(4, 4), Warrior.new(), Vector2i(0, 2), 1, {}, 0)
	var spaces: Array = Senses.new(state).look_2d(Direction.south())
	assert_eq(spaces.size(), 3)
	assert_true(spaces[0].is_empty(), "(1,2) vazia")
	assert_true(spaces[1].is_empty(), "(2,2) vazia")
	assert_true(spaces[2].is_empty(), "(3,2) vazia")


func test_look_2d_leste_com_inimigo_na_segunda_casa() -> void:
	# warrior (0,0), sludge (0,2), escada (0,4): look EAST → (0,1)/(0,2)/(0,3)
	var state := LevelState.from_2d(
		1, 5, Vector2i(0, 4), Warrior.new(), Vector2i(0, 0), 1, {Vector2i(0, 2): Sludge.new()}, 0
	)
	var spaces: Array = Senses.new(state).look_2d(Direction.east())
	assert_eq(spaces.size(), 3)
	assert_true(spaces[0].is_empty(), "(0,1) vazia")
	assert_true(spaces[1].is_enemy(), "(0,2) sludge")
	assert_true(spaces[2].is_empty(), "(0,3) vazia (escada está em (0,4), fora do range)")


func test_look_2d_norte_ate_parede() -> void:
	# warrior (1,2) em grade 2×5: NORTH → (0,2) dentro, (-1,2) parede, (-2,2) parede
	var state := LevelState.from_2d(2, 5, Vector2i(0, 4), Warrior.new(), Vector2i(1, 2), 1, {}, 0)
	var spaces: Array = Senses.new(state).look_2d(Direction.north())
	assert_eq(spaces.size(), 3)
	assert_false(spaces[0].is_wall(), "(0,2) dentro")
	assert_true(spaces[1].is_wall(), "(-1,2) fora = parede")
	assert_true(spaces[2].is_wall(), "(-2,2) fora = parede")


func test_direction_of_2d_norte() -> void:
	var state := LevelState.from_2d(5, 5, Vector2i(4, 4), Warrior.new(), Vector2i(2, 2), 1, {}, 0)
	var dir := Senses.new(state).direction_of_2d(Vector2i(0, 2))
	assert_true(dir.equals(Direction.north()), "alvo ao norte (linha menor)")


func test_direction_of_2d_sul() -> void:
	var state := LevelState.from_2d(5, 5, Vector2i(4, 4), Warrior.new(), Vector2i(0, 2), 1, {}, 0)
	var dir := Senses.new(state).direction_of_2d(Vector2i(3, 2))
	assert_true(dir.equals(Direction.south()), "alvo ao sul (linha maior)")


func test_direction_of_2d_leste() -> void:
	var state := LevelState.from_2d(5, 5, Vector2i(4, 4), Warrior.new(), Vector2i(2, 1), 1, {}, 0)
	var dir := Senses.new(state).direction_of_2d(Vector2i(2, 4))
	assert_true(dir.equals(Direction.east()), "alvo a leste (coluna maior)")


func test_direction_of_2d_oeste() -> void:
	var state := LevelState.from_2d(5, 5, Vector2i(4, 4), Warrior.new(), Vector2i(2, 4), 1, {}, 0)
	var dir := Senses.new(state).direction_of_2d(Vector2i(2, 1))
	assert_true(dir.equals(Direction.west()), "alvo a oeste (coluna menor)")


func test_direction_of_stairs_2d_a_leste() -> void:
	var state := LevelState.from_2d(3, 5, Vector2i(1, 4), Warrior.new(), Vector2i(1, 0), 1, {}, 0)
	var dir := Senses.new(state).direction_of_stairs_2d()
	assert_true(dir.equals(Direction.east()), "escada a leste (col 4, warrior col 0)")


func test_direction_of_stairs_2d_ao_sul() -> void:
	var state := LevelState.from_2d(5, 3, Vector2i(4, 2), Warrior.new(), Vector2i(0, 2), 1, {}, 0)
	var dir := Senses.new(state).direction_of_stairs_2d()
	assert_true(dir.equals(Direction.south()), "escada ao sul (linha 4, warrior linha 0)")
