extends GutTest
## T-182 (018) — Sentidos 2D: feel_2d/look_2d inspecionam grade R×C via Direction
## absoluta (NORTH/SOUTH/EAST/WEST). direction_of_2d/_stairs_2d retornam cardinal.
## step_of_2d/position_toward_2d calculam deslocamento Vector2i.
## Sentidos são CQS: não alteram estado nem turno.


func _state_3x5(warrior_pos: Vector2i, units: Dictionary = {}) -> LevelState:
	return LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), warrior_pos, 1, units, 0)


func _facade(warrior_pos: Vector2i, units: Dictionary = {}) -> WarriorFacade:
	return WarriorFacade.new(_state_3x5(warrior_pos, units))


# ── feel_2d ──────────────────────────────────────────────────────────────────


func test_feel_2d_north_celula_vazia() -> void:
	var facade := _facade(Vector2i(1, 2))
	var space := facade.feel_2d(Direction.north())
	assert_false(space.is_wall())
	assert_true(space.is_empty())


func test_feel_2d_north_parede_fora_da_grade() -> void:
	# warrior na linha 0; north => linha -1 = parede
	var facade := _facade(Vector2i(0, 2))
	assert_true(facade.feel_2d(Direction.north()).is_wall())


func test_feel_2d_east_inimigo() -> void:
	var facade := _facade(Vector2i(1, 2), {Vector2i(1, 3): Sludge.new()})
	assert_true(facade.feel_2d(Direction.east()).is_enemy())


func test_feel_2d_south_escada() -> void:
	# warrior at (1,4); south = (2,4) = escada
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(1, 4), 1, {}, 0)
	assert_true(WarriorFacade.new(state).feel_2d(Direction.south()).is_stairs())


func test_feel_2d_west_parede_coluna_negativa() -> void:
	# warrior na coluna 0; west => coluna -1 = parede
	var facade := _facade(Vector2i(1, 0))
	assert_true(facade.feel_2d(Direction.west()).is_wall())


# ── look_2d ──────────────────────────────────────────────────────────────────


func test_look_2d_retorna_tres_espacos() -> void:
	assert_eq(_facade(Vector2i(1, 0)).look_2d(Direction.east()).size(), 3)


func test_look_2d_east_conteudo_correto() -> void:
	# warrior at (0,0); east -> cols 1,2,3; col 1 = inimigo
	var units := {Vector2i(0, 1): Sludge.new()}
	var spaces := _facade(Vector2i(0, 0), units).look_2d(Direction.east())
	assert_true(spaces[0].is_enemy(), "col 1 = inimigo")
	assert_true(spaces[1].is_empty(), "col 2 = vazio")
	assert_true(spaces[2].is_empty(), "col 3 = vazio")


func test_look_2d_north_fora_da_grade_vira_parede() -> void:
	# warrior at (1,2); north -> (0,2),(-1,2),(-2,2)
	var spaces := _facade(Vector2i(1, 2)).look_2d(Direction.north())
	assert_false(spaces[0].is_wall(), "(0,2) dentro")
	assert_true(spaces[1].is_wall(), "(-1,2) fora")
	assert_true(spaces[2].is_wall(), "(-2,2) fora")


# ── direction_of_stairs_2d ───────────────────────────────────────────────────


func test_direction_of_stairs_2d_north() -> void:
	# warrior at (2,2), stairs at (0,2) -> NORTH
	var state := LevelState.from_2d(3, 5, Vector2i(0, 2), Warrior.new(), Vector2i(2, 2), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.north()))


func test_direction_of_stairs_2d_south() -> void:
	# warrior at (0,2), stairs at (2,2) -> SOUTH
	var state := LevelState.from_2d(3, 5, Vector2i(2, 2), Warrior.new(), Vector2i(0, 2), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.south()))


func test_direction_of_stairs_2d_east() -> void:
	# warrior at (1,1), stairs at (1,4) -> EAST
	var state := LevelState.from_2d(3, 5, Vector2i(1, 4), Warrior.new(), Vector2i(1, 1), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.east()))


func test_direction_of_stairs_2d_west() -> void:
	# warrior at (1,3), stairs at (1,0) -> WEST
	var state := LevelState.from_2d(3, 5, Vector2i(1, 0), Warrior.new(), Vector2i(1, 3), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.west()))


# ── direction_of_2d (via feel_2d) ───────────────────────────────────────────


func test_direction_of_2d_via_feel_east() -> void:
	# warrior at (1,2); inimigo at (1,3); feel_2d(east) -> Space; direction_of_2d -> EAST
	var units := {Vector2i(1, 3): Sludge.new()}
	var facade := _facade(Vector2i(1, 2), units)
	var space := facade.feel_2d(Direction.east())
	assert_true(facade.direction_of_2d(space).equals(Direction.east()))


func test_direction_of_2d_via_feel_north() -> void:
	# warrior at (2,2); inimigo at (1,2); feel_2d(north) -> Space; direction_of_2d -> NORTH
	var units := {Vector2i(1, 2): Sludge.new()}
	var facade := _facade(Vector2i(2, 2), units)
	var space := facade.feel_2d(Direction.north())
	assert_true(facade.direction_of_2d(space).equals(Direction.north()))


# ── direction.delta() / position_toward_2d ───────────────────────────────────


func test_direction_delta_north() -> void:
	assert_eq(Direction.north().delta(), Vector2i(-1, 0))


func test_direction_delta_south() -> void:
	assert_eq(Direction.south().delta(), Vector2i(1, 0))


func test_direction_delta_east() -> void:
	assert_eq(Direction.east().delta(), Vector2i(0, 1))


func test_direction_delta_west() -> void:
	assert_eq(Direction.west().delta(), Vector2i(0, -1))


func test_position_toward_2d_dois_passos_east() -> void:
	assert_eq(_state_3x5(Vector2i(1, 1)).position_toward_2d(Direction.east(), 2), Vector2i(1, 3))


func test_position_toward_2d_um_passo_north() -> void:
	assert_eq(_state_3x5(Vector2i(2, 2)).position_toward_2d(Direction.north(), 1), Vector2i(1, 2))


# ── direction_of_2d: casos edge (zero-delta, diagonal tie-break, S/W via feel) ──


func test_direction_of_2d_zero_delta_retorna_north() -> void:
	# warrior NA escada → delta = ZERO → NORTH por convenção
	var state := LevelState.from_2d(3, 5, Vector2i(1, 2), Warrior.new(), Vector2i(1, 2), 1, {}, 0)
	var facade := WarriorFacade.new(state)
	assert_true(facade.direction_of_stairs_2d().equals(Direction.north()))


func test_direction_of_2d_diagonal_tie_sul() -> void:
	# warrior (0,0), escada (2,2): |Δrow|==|Δcol|==2, tie → N/S, Δrow>0 → SOUTH
	var state := LevelState.from_2d(3, 5, Vector2i(2, 2), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.south()))


func test_direction_of_2d_diagonal_tie_norte() -> void:
	# warrior (2,0), escada (0,2): |Δrow|==|Δcol|==2, tie → N/S, Δrow<0 → NORTH
	var state := LevelState.from_2d(3, 5, Vector2i(0, 2), Warrior.new(), Vector2i(2, 0), 1, {}, 0)
	assert_true(WarriorFacade.new(state).direction_of_stairs_2d().equals(Direction.north()))


func test_direction_of_2d_via_feel_south() -> void:
	# warrior (0,2); inimigo em (1,2); feel_2d(south) → Space; direction_of_2d → SOUTH
	var units := {Vector2i(1, 2): Sludge.new()}
	var facade := _facade(Vector2i(0, 2), units)
	var space := facade.feel_2d(Direction.south())
	assert_true(facade.direction_of_2d(space).equals(Direction.south()))


func test_direction_of_2d_via_feel_west() -> void:
	# warrior (1,3); inimigo em (1,2); feel_2d(west) → Space; direction_of_2d → WEST
	var units := {Vector2i(1, 2): Sludge.new()}
	var facade := _facade(Vector2i(1, 3), units)
	var space := facade.feel_2d(Direction.west())
	assert_true(facade.direction_of_2d(space).equals(Direction.west()))


# ── CQS: sentidos não alteram estado nem turno ──────────────────────────────


func test_sentidos_2d_nao_alteram_estado() -> void:
	var state := _state_3x5(Vector2i(1, 2))
	var facade := WarriorFacade.new(state)
	var turn_antes := state.turn()
	@warning_ignore("return_value_discarded")
	facade.feel_2d(Direction.north())
	@warning_ignore("return_value_discarded")
	facade.look_2d(Direction.east())
	@warning_ignore("return_value_discarded")
	facade.direction_of_stairs_2d()
	assert_eq(state.turn(), turn_antes, "sentidos nao consomem turno")
	assert_null(facade.chosen_action(), "sentidos nao registram acao")
