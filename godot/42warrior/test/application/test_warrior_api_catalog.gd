extends GutTest
## Cobre o WarriorApiCatalog: acúmulo de habilidades por nível, shape dos entries.


func test_nivel_1_expoe_so_walk() -> void:
	var entries: Array = WarriorApiCatalog.entries_for_level(1)
	assert_eq(entries.size(), 1)
	assert_eq(entries[0]["name"], "walk")


func test_nivel_2_acumula_feel_e_attack() -> void:
	var entries: Array = WarriorApiCatalog.entries_for_level(2)
	var names := _names(entries)
	assert_eq(entries.size(), 3)
	assert_has(names, "walk")
	assert_has(names, "feel")
	assert_has(names, "attack")


func test_nivel_3_acumula_health_e_rest() -> void:
	var entries: Array = WarriorApiCatalog.entries_for_level(3)
	assert_eq(entries.size(), 5)
	assert_has(_names(entries), "health")
	assert_has(_names(entries), "rest")


func test_nivel_4_identico_ao_3_nenhuma_habilidade_nova() -> void:
	assert_eq(
		WarriorApiCatalog.entries_for_level(4).size(), WarriorApiCatalog.entries_for_level(3).size()
	)


func test_nivel_5_adiciona_rescue() -> void:
	assert_has(_names(WarriorApiCatalog.entries_for_level(5)), "rescue")


func test_nivel_7_adiciona_pivot() -> void:
	assert_has(_names(WarriorApiCatalog.entries_for_level(7)), "pivot")


func test_nivel_8_adiciona_look_e_shoot() -> void:
	var names := _names(WarriorApiCatalog.entries_for_level(8))
	assert_has(names, "look")
	assert_has(names, "shoot")


func test_nivel_9_identico_ao_8() -> void:
	assert_eq(
		WarriorApiCatalog.entries_for_level(9).size(), WarriorApiCatalog.entries_for_level(8).size()
	)


func test_entry_tem_campos_obrigatorios() -> void:
	var entry: Dictionary = WarriorApiCatalog.entries_for_level(1)[0]
	assert_has(entry, "name")
	assert_has(entry, "signature")
	assert_has(entry, "description")
	assert_has(entry, "kind")


func test_kind_e_action_ou_sense() -> void:
	for entry: Dictionary in WarriorApiCatalog.entries_for_level(9):
		assert_true(
			entry["kind"] == "action" or entry["kind"] == "sense",
			"kind deve ser action ou sense, obteve: %s" % entry["kind"]
		)


func _names(entries: Array) -> Array:
	var result: Array = []
	for e: Dictionary in entries:
		result.append(e["name"])
	return result
