class_name TestApiReferenceTab016
extends GutTest
## T-170 (016) — PROVA DE RENDER: aba Referência da API do editor fiel ao mockup.
## Instancia api_reference_tab.tscn, popula com dados reais via WarriorApiCatalog e
## assere que a lista tem entradas (conteúdo real: SENTIDOS + AÇÕES).

const _SCENE := "res://scenes/api_reference_tab.tscn"


func test_api_reference_tab_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "api_reference_tab.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "api_reference_tab.tscn deve instanciar sem crash")


func test_lista_populada_com_entries_reais() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var entries := WarriorApiCatalog.entries_for_level(9)
	root.populate(entries)
	await get_tree().process_frame
	var list_node := root.find_child("List", true, false)
	assert_not_null(list_node, "VBoxContainer List deve existir em api_reference_tab.tscn")
	assert_true(
		list_node.get_child_count() > 0,
		"Lista da API deve ter entries apos populate() (conteúdo real, nao aba vazia)"
	)


func test_entries_nivel_9_tem_acoes_e_sentidos() -> void:
	var entries := WarriorApiCatalog.entries_for_level(9)
	assert_true(entries.size() > 0, "WarriorApiCatalog.entries_for_level(9) deve retornar entradas")
	var kinds: Array = entries.map(func(e: Dictionary) -> String: return e.get("kind", ""))
	assert_true("action" in kinds, "entries nivel 9 deve ter pelo menos uma ACAO (kind=action)")
	assert_true("sense" in kinds, "entries nivel 9 deve ter pelo menos um SENTIDO (kind=sense)")


func test_entries_nivel_1_tem_walk() -> void:
	var entries := WarriorApiCatalog.entries_for_level(1)
	var names: Array = entries.map(func(e: Dictionary) -> String: return e.get("name", ""))
	assert_true("walk" in names, "nivel 1 deve ter 'walk' desbloqueado (unica ability do nivel 1)")


func test_populate_nivel_1_sem_crash() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var entries := WarriorApiCatalog.entries_for_level(1)
	root.populate(entries)
	await get_tree().process_frame
	var list_node := root.find_child("List", true, false)
	assert_not_null(list_node, "List deve existir")
	assert_true(
		list_node.get_child_count() > 0,
		"Lista deve ter entries do nivel 1 (walk + feel pelo menos)"
	)


func _load_scene() -> ApiReferenceTab:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate() as ApiReferenceTab
	add_child_autoqfree(root)
	return root
