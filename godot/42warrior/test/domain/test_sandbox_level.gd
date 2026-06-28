extends GutTest
## Cobre sandbox_definition(): is_sandbox, hint_text e layout mínimo.


func test_sandbox_e_marcado_como_sandbox() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_true(def.is_sandbox, "is_sandbox deve ser true")


func test_sandbox_tem_hint_text_nao_vazio() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_false(def.hint_text.is_empty(), "hint_text nao pode estar vazio")


func test_sandbox_index_e_zero() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_eq(def.index, 0, "sandbox usa index 0")


func test_sandbox_tem_layout_valido() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_gt(def.width, 0, "width deve ser positivo")
	assert_true(def.warrior_position >= 0 and def.warrior_position < def.width)
	assert_true(def.stairs_position >= 0 and def.stairs_position < def.width)
	assert_ne(def.warrior_position, def.stairs_position, "warrior e escada nao podem coincidir")


func test_sandbox_time_bonus_e_zero() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_eq(def.time_bonus, 0, "sandbox nao tem time_bonus")


func test_sandbox_ace_score_e_zero() -> void:
	var def := BeginnerTower.sandbox_definition()
	assert_eq(def.ace_score, 0, "sandbox nao tem ace_score")


func test_sandbox_pode_ser_carregado_pelo_level_loader() -> void:
	var def := BeginnerTower.sandbox_definition()
	var state := LevelLoader.new().load_definition(def)
	assert_not_null(state, "loader deve retornar um LevelState valido")
	assert_not_null(state.warrior(), "LevelState deve ter warrior")
