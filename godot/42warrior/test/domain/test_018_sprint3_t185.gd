extends GutTest
## T-185 (018 Sprint 3) — LevelLoader aceita layout 2D RxC.
## Cobre: carga de nível RxC; 1xN como R=1 (retrocompat); posições 2D corretas.


func _make_def_2d(r: int, c: int, warrior_pos: Vector2i, stairs_pos: Vector2i) -> LevelDefinition:
	return (
		LevelDefinition
		. new(
			{
				"index": 0,
				"width": c,
				"rows": r,
				"warrior_position": warrior_pos.y,
				"warrior_facing": 1,
				"stairs_position": stairs_pos.y,
				"warrior_position_2d": warrior_pos,
				"stairs_position_2d": stairs_pos,
				"description": "test_2d",
				"abilities": PackedStringArray([]),
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": {},
			}
		)
	)


func _make_def_1d(width: int) -> LevelDefinition:
	return (
		LevelDefinition
		. new(
			{
				"index": 0,
				"width": width,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": width - 1,
				"description": "test_1d",
				"abilities": PackedStringArray([]),
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
			}
		)
	)


# ── Carga de nível 2D ────────────────────────────────────────────────────────


func test_nivel_3x5_carrega_com_rows_cols_corretos() -> void:
	var def := _make_def_2d(3, 5, Vector2i(0, 0), Vector2i(2, 4))
	var loader := LevelLoader.new()
	var state := loader.load_definition(def)
	assert_eq(state.rows(), 3, "rows() deve ser 3")
	assert_eq(state.cols(), 5, "cols() deve ser 5")


func test_warrior_position_2d_correto() -> void:
	var warrior_pos := Vector2i(1, 2)
	var def := _make_def_2d(3, 5, warrior_pos, Vector2i(2, 4))
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.warrior_position_2d(), warrior_pos, "warrior_position_2d deve coincidir")


func test_stairs_position_2d_correto() -> void:
	var stairs_pos := Vector2i(2, 4)
	var def := _make_def_2d(3, 5, Vector2i(0, 0), stairs_pos)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.stairs_position_2d(), stairs_pos, "stairs_position_2d deve coincidir")


func test_nivel_2d_space_at_dentro_da_grade_e_passavel() -> void:
	var def := _make_def_2d(3, 5, Vector2i(0, 0), Vector2i(2, 4))
	var state := LevelLoader.new().load_definition(def)
	var space := state.space_at_2d(Vector2i(1, 2))
	assert_false(space.is_wall(), "posição interna não deve ser parede")


func test_nivel_2d_space_fora_da_grade_e_parede() -> void:
	var def := _make_def_2d(3, 5, Vector2i(0, 0), Vector2i(2, 4))
	var state := LevelLoader.new().load_definition(def)
	var space := state.space_at_2d(Vector2i(5, 0))
	assert_true(space.is_wall(), "posição fora da grade deve ser parede")


func test_nivel_2d_com_unidade() -> void:
	var def := LevelDefinition.new(
		{
			"index": 0,
			"width": 4,
			"rows": 3,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 3,
			"warrior_position_2d": Vector2i(0, 0),
			"stairs_position_2d": Vector2i(2, 3),
			"description": "2d_unit",
			"abilities": PackedStringArray([]),
			"time_bonus": 0,
			"ace_score": 0,
			"units": {},
			"units_2d": {Vector2i(1, 2): func() -> Unit: return Sludge.new()},
		}
	)
	var state := LevelLoader.new().load_definition(def)
	var unit := state.unit_at_2d(Vector2i(1, 2))
	assert_not_null(unit, "deve haver unidade em (1,2)")
	assert_true(unit is Sludge, "unidade deve ser Sludge")


# ── Retrocompat 1×N ─────────────────────────────────────────────────────────


func test_nivel_1xn_retrocompat_rows_e_1() -> void:
	var def := _make_def_1d(6)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.rows(), 1, "1xN deve retornar rows()==1")


func test_nivel_1xn_retrocompat_cols_igual_width() -> void:
	var def := _make_def_1d(6)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.cols(), 6, "1xN cols() deve ser igual a width")


func test_nivel_1xn_retrocompat_api_1d_funciona() -> void:
	var def := _make_def_1d(6)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.width(), 6, "API 1D deve funcionar: width()==6")
	assert_eq(state.warrior_position(), 0, "warrior_position() 1D deve ser 0")


func test_todos_9_niveis_beginner_carregam_sem_erro() -> void:
	var loader := LevelLoader.new()
	for i in range(1, 10):
		var state := loader.load_level(i)
		assert_not_null(state, "nível %d deve carregar" % i)
		assert_gt(state.width(), 0, "nível %d width > 0" % i)


# ── warrior_4dir default ──────────────────────────────────────────────────────


func test_nivel_2d_warrior_4dir_default_east_quando_facing_positivo() -> void:
	var def := _make_def_2d(3, 5, Vector2i(0, 0), Vector2i(2, 4))
	var state := LevelLoader.new().load_definition(def)
	var dir := state.warrior_4dir()
	assert_not_null(dir, "warrior_4dir não deve ser null em estado 2D")
	assert_true(dir.equals(Direction.east()), "facing=+1 deve gerar Direction.east()")


func test_nivel_2d_warrior_4dir_explicito_respeita_config() -> void:
	var def := (
		LevelDefinition
		. new(
			{
				"index": 0,
				"width": 4,
				"rows": 3,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 3,
				"warrior_position_2d": Vector2i(0, 0),
				"stairs_position_2d": Vector2i(2, 3),
				"warrior_direction": Direction.north(),
				"description": "dir_north",
				"abilities": PackedStringArray([]),
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": {},
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	assert_true(
		state.warrior_4dir().equals(Direction.north()), "warrior_direction explícita deve ser north"
	)
