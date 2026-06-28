extends GutTest
## T-185 (018 Sprint 3) — LevelLoader aceita layout 2D RxC.
## DoD: níveis RxC carregam; 1xN lido como R=1 (RETROCOMPAT); LevelState 2D correto.

# ── T-185: Retrocompat (1xN = rows=1) ────────────────────────────────────────


func test_load_definition_1d_retrocompat_rows_e_1() -> void:
	var state := LevelLoader.new().load_level(1)
	assert_eq(state.rows(), 1, "nível 1D deve ter rows()=1 (retrocompat)")


func test_load_definition_1d_retrocompat_cols_igual_a_width() -> void:
	var state := LevelLoader.new().load_level(1)
	var loader := LevelLoader.new()
	var def := BeginnerTower.definition(1)
	assert_eq(state.cols(), def.width, "nível 1D deve ter cols()=width")


func test_load_definition_1d_retrocompat_suite_referencia_continua_verde() -> void:
	var loader := LevelLoader.new()
	var runner := LevelRunner.new()
	for index: int in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
		var state := loader.load_level(index)
		var result: Dictionary = runner.run(state, ReferenceSolutions.for_level(index))
		assert_eq(
			result["outcome"],
			TurnResult.Outcome.VICTORY,
			"nível %d deve ser vencido pela solução de referência (retrocompat 1D)" % index
		)


# ── T-185: Layout 2D RxC ─────────────────────────────────────────────────────


func test_load_definition_2d_retorna_level_state_com_rows_correto() -> void:
	var def := (
		LevelDefinition
		. new(
			{
				"index": 99,
				"width": 5,
				"rows": 3,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 4,
				"warrior_position_2d": Vector2i(0, 0),
				"stairs_position_2d": Vector2i(2, 4),
				"description": "test 2D",
				"abilities": [],
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": {},
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.rows(), 3, "LevelState 2D deve ter rows()=3")
	assert_eq(state.cols(), 5, "LevelState 2D deve ter cols()=5 (width)")


func test_load_definition_2d_warrior_position_2d_correto() -> void:
	var def := (
		LevelDefinition
		. new(
			{
				"index": 99,
				"width": 7,
				"rows": 4,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 6,
				"warrior_position_2d": Vector2i(1, 2),
				"stairs_position_2d": Vector2i(3, 6),
				"description": "test 2D pos",
				"abilities": [],
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": {},
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(
		state.warrior_position_2d(), Vector2i(1, 2), "warrior_position_2d deve ser Vector2i(1,2)"
	)


func test_load_definition_2d_stairs_position_2d_correto() -> void:
	var def := (
		LevelDefinition
		. new(
			{
				"index": 99,
				"width": 7,
				"rows": 4,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 6,
				"warrior_position_2d": Vector2i(1, 2),
				"stairs_position_2d": Vector2i(3, 6),
				"description": "test 2D escada",
				"abilities": [],
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": {},
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(
		state.stairs_position_2d(), Vector2i(3, 6), "stairs_position_2d deve ser Vector2i(3,6)"
	)


func test_load_definition_2d_build_units_2d_instancia_frescos() -> void:
	var units_2d := {Vector2i(1, 2): func() -> Unit: return Sludge.new()}
	var def := (
		LevelDefinition
		. new(
			{
				"index": 99,
				"width": 5,
				"rows": 3,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 4,
				"warrior_position_2d": Vector2i(0, 0),
				"stairs_position_2d": Vector2i(2, 4),
				"description": "test 2D units",
				"abilities": [],
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
				"units_2d": units_2d,
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	var unit: Unit = state.unit_at_2d(Vector2i(1, 2))
	assert_not_null(unit, "unidade 2D deve existir na posição Vector2i(1,2)")
	assert_true(unit is Sludge, "unidade deve ser Sludge")


func test_load_definition_rows_1_usa_caminho_1d() -> void:
	var def := (
		LevelDefinition
		. new(
			{
				"index": 99,
				"width": 5,
				"rows": 1,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 4,
				"description": "test 1D explícito",
				"abilities": [],
				"time_bonus": 0,
				"ace_score": 0,
				"units": {},
			}
		)
	)
	var state := LevelLoader.new().load_definition(def)
	assert_eq(state.rows(), 1, "rows=1 explícito deve usar caminho 1D (rows()=1)")
	assert_eq(state.cols(), 5, "cols deve ser 5 (width)")
