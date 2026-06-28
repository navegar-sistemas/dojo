extends GutTest


func test_ha_nove_niveis() -> void:
	assert_eq(BeginnerTower.definitions().size(), 9)
	assert_eq(BeginnerTower.LEVEL_COUNT, 9)


func test_indice_bate_com_a_posicao() -> void:
	for index in range(1, 10):
		assert_eq(BeginnerTower.definition(index).index, index)


func test_campos_preenchidos_e_positivos() -> void:
	for definition in BeginnerTower.definitions():
		assert_gt(definition.width, 0)
		assert_gt(definition.time_bonus, 0)
		assert_gt(definition.ace_score, 0)
		assert_ne(definition.description, "")
		assert_true(
			definition.stairs_position >= 0 and definition.stairs_position < definition.width
		)
		assert_true(
			definition.warrior_position >= 0 and definition.warrior_position < definition.width
		)


func test_habilidades_introduzidas_na_ordem_canonica() -> void:
	assert_true(BeginnerTower.definition(1).abilities.has("walk"))
	assert_true(BeginnerTower.definition(2).abilities.has("attack"))
	assert_true(BeginnerTower.definition(3).abilities.has("rest"))
	assert_true(BeginnerTower.definition(5).abilities.has("rescue"))
	assert_true(BeginnerTower.definition(7).abilities.has("pivot"))
	assert_true(BeginnerTower.definition(8).abilities.has("shoot"))


func test_time_bonus_e_ace_score_por_nivel() -> void:
	var expected_ace := [10, 26, 71, 90, 123, 105, 50, 46, 100]
	var expected_bonus := [15, 20, 35, 45, 45, 55, 30, 20, 40]
	for index in range(1, 10):
		assert_eq(BeginnerTower.definition(index).ace_score, expected_ace[index - 1])
		assert_eq(BeginnerTower.definition(index).time_bonus, expected_bonus[index - 1])


func test_build_units_devolve_instancias_frescas() -> void:
	var definition := BeginnerTower.definition(2)
	var a: Dictionary = definition.build_units()
	var b: Dictionary = definition.build_units()
	assert_true(a[4] is Sludge)
	assert_ne(a[4], b[4], "instâncias novas a cada carga (sem estado compartilhado)")
