extends GutTest
## Cobre o GlossaryCatalog: entidades por nível, termos de score, deduplicação.


func test_nivel_1_sem_entidades() -> void:
	var entries: Dictionary = GlossaryCatalog.entries_for_level(1)
	assert_eq(entries["entities"].size(), 0, "nível 1 não tem inimigos nem cativos")


func test_nivel_2_tem_sludge() -> void:
	var entries: Dictionary = GlossaryCatalog.entries_for_level(2)
	var names := _entity_names(entries)
	assert_has(names, "Sludge")


func test_nivel_3_deduplica_sludges() -> void:
	var entries: Dictionary = GlossaryCatalog.entries_for_level(3)
	var names := _entity_names(entries)
	assert_eq(names.count("Sludge"), 1, "múltiplos sludges = 1 entrada no glossário")


func test_nivel_5_tem_cativo_e_arqueiro() -> void:
	var entries: Dictionary = GlossaryCatalog.entries_for_level(5)
	var names := _entity_names(entries)
	assert_has(names, "Arqueiro")
	assert_has(names, "Cativo")


func test_nivel_8_tem_mago() -> void:
	var names := _entity_names(GlossaryCatalog.entries_for_level(8))
	assert_has(names, "Mago")


func test_entity_entry_tem_campos_obrigatorios() -> void:
	var entry: Dictionary = GlossaryCatalog.entries_for_level(2)["entities"][0]
	assert_has(entry, "name")
	assert_has(entry, "description")
	assert_ne(entry["description"], "")


func test_score_terms_sempre_presentes() -> void:
	var terms: Array = GlossaryCatalog.entries_for_level(1)["score_terms"]
	var names := _score_names(terms)
	assert_has(names, "Bônus de tempo")
	assert_has(names, "Meta ACE")


func test_bonus_resgate_so_quando_ha_cativos() -> void:
	var names_1 := _score_names(GlossaryCatalog.entries_for_level(1)["score_terms"])
	assert_false(names_1.has("Bônus de resgate"), "nível 1 não tem cativos")
	var names_5 := _score_names(GlossaryCatalog.entries_for_level(5)["score_terms"])
	assert_has(names_5, "Bônus de resgate")


func test_score_term_tem_campos_obrigatorios() -> void:
	var term: Dictionary = GlossaryCatalog.entries_for_level(1)["score_terms"][0]
	assert_has(term, "name")
	assert_has(term, "definition")
	assert_has(term, "value")


func _entity_names(entries: Dictionary) -> Array:
	var result: Array = []
	for e: Dictionary in entries["entities"]:
		result.append(e["name"])
	return result


func _score_names(terms: Array) -> Array:
	var result: Array = []
	for t: Dictionary in terms:
		result.append(t["name"])
	return result
