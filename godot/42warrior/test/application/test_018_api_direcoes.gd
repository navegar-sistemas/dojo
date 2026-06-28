extends GutTest
## T-183: WarriorApiCatalog.direction_entries() e GlossaryCatalog.directions descrevem
## as 4 direções absolutas (N/S/E/W), relativas (forward/backward) e o pivot 4-dir.
## DoD: catálogo + glossário cobrem as direções; facade expõe os métodos 2D;
## suite beginner 1xN permanece verde sem tocar no código do jogador.

# ─── WarriorApiCatalog.direction_entries() ────────────────────────────────────


func test_direction_entries_retorna_array_nao_vazio() -> void:
	var entries: Array = WarriorApiCatalog.direction_entries()
	assert_true(entries.size() > 0, "direction_entries() deve retornar pelo menos 1 entrada")


func test_direction_entries_contem_4_cardinais() -> void:
	var names := _entry_names(WarriorApiCatalog.direction_entries())
	assert_has(names, "north")
	assert_has(names, "south")
	assert_has(names, "east")
	assert_has(names, "west")


func test_direction_entries_contem_relativas() -> void:
	var names := _entry_names(WarriorApiCatalog.direction_entries())
	assert_has(names, "forward")
	assert_has(names, "backward")


func test_direction_entries_contem_pivot_direcao() -> void:
	var names := _entry_names(WarriorApiCatalog.direction_entries())
	assert_has(names, "pivot_dir")


func test_direction_entry_tem_campos_obrigatorios() -> void:
	for entry: Dictionary in WarriorApiCatalog.direction_entries():
		assert_has(entry, "name", "entry %s falta 'name'" % str(entry))
		assert_has(entry, "signature", "entry %s falta 'signature'" % str(entry))
		assert_has(entry, "description", "entry %s falta 'description'" % str(entry))
		assert_has(entry, "kind", "entry %s falta 'kind'" % str(entry))


func test_direction_entry_kind_e_direction() -> void:
	for entry: Dictionary in WarriorApiCatalog.direction_entries():
		assert_eq(
			entry["kind"], "direction", "kind de %s deve ser 'direction'" % entry.get("name", "?")
		)


func test_direction_entries_nao_aparece_em_entries_for_level() -> void:
	# Direções não são "habilidades" — não poluem o catálogo de ações/sentidos.
	for i in range(1, 10):
		for e: Dictionary in WarriorApiCatalog.entries_for_level(i):
			assert_ne(
				e.get("kind", ""), "direction", "entries_for_level não deve conter kind=direction"
			)


# ─── GlossaryCatalog: chave "directions" ─────────────────────────────────────


func test_glossary_tem_chave_directions() -> void:
	var g: Dictionary = GlossaryCatalog.entries_for_level(1)
	assert_has(g, "directions")


func test_glossary_directions_tem_4_cardinais() -> void:
	var dirs: Array = GlossaryCatalog.entries_for_level(1)["directions"]
	var names := _dir_names(dirs)
	assert_has(names, "Norte")
	assert_has(names, "Sul")
	assert_has(names, "Leste")
	assert_has(names, "Oeste")


func test_glossary_directions_tem_relativas() -> void:
	var dirs: Array = GlossaryCatalog.entries_for_level(1)["directions"]
	var names := _dir_names(dirs)
	assert_has(names, "Frente")
	assert_has(names, "Trás")


func test_glossary_directions_tem_pivot() -> void:
	var dirs: Array = GlossaryCatalog.entries_for_level(1)["directions"]
	var names := _dir_names(dirs)
	assert_has(names, "Pivot")


func test_glossary_direction_entry_tem_campos_obrigatorios() -> void:
	var dirs: Array = GlossaryCatalog.entries_for_level(1)["directions"]
	assert_true(dirs.size() > 0, "deve haver pelo menos 1 entrada de direção")
	for entry: Dictionary in dirs:
		assert_has(entry, "name", "entry falta 'name'")
		assert_has(entry, "description", "entry falta 'description'")
		assert_ne(entry.get("description", ""), "", "description não pode ser vazia")


func test_glossary_directions_estavel_entre_niveis() -> void:
	# As direções não variam por nível (são sempre as mesmas 4 + 2 relativas + pivot).
	var d1: Array = GlossaryCatalog.entries_for_level(1)["directions"]
	var d9: Array = GlossaryCatalog.entries_for_level(9)["directions"]
	assert_eq(d1.size(), d9.size(), "direções não variam por nível")


# ─── WarriorFacade: métodos 2D acessíveis ────────────────────────────────────


func test_facade_expoe_metodos_2d() -> void:
	var state := LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0)
	var facade := WarriorFacade.new(state)
	for m: String in ["feel_2d", "look_2d", "direction_of_2d", "direction_of_stairs_2d"]:
		assert_true(facade.has_method(m), "facade deve expor %s" % m)


# ─── Retrocompat beginner: forward/backward ainda funcionam no R=1 ────────────


func test_direction_forward_semantica_preservada() -> void:
	assert_eq(Direction.forward().relative_sign(), 1)


func test_direction_backward_semantica_preservada() -> void:
	assert_eq(Direction.backward().relative_sign(), -1)


func test_pivot_4dir_horario() -> void:
	assert_true(Direction.north().pivot().equals(Direction.east()))
	assert_true(Direction.east().pivot().equals(Direction.south()))
	assert_true(Direction.south().pivot().equals(Direction.west()))
	assert_true(Direction.west().pivot().equals(Direction.north()))


# ─── helpers ─────────────────────────────────────────────────────────────────


func _entry_names(entries: Array) -> Array:
	var r: Array = []
	for e: Dictionary in entries:
		r.append(e.get("name", ""))
	return r


func _dir_names(dirs: Array) -> Array:
	var r: Array = []
	for d: Dictionary in dirs:
		r.append(d.get("name", ""))
	return r
