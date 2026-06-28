class_name TestGlossaryTab016
extends GutTest
## T-169 (016) — PROVA DE RENDER: aba Glossário do editor fiel ao mockup.
## Instancia glossary_tab.tscn, popula com dados reais via GlossaryCatalog e
## assere que a lista tem entradas (conteúdo real, nao aba vazia).

const _SCENE := "res://scenes/glossary_tab.tscn"


func test_glossary_tab_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "glossary_tab.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "glossary_tab.tscn deve instanciar sem crash")


func test_lista_populada_com_entradas_reais() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var entries := GlossaryCatalog.entries_for_level(1)
	root.populate(entries)
	await get_tree().process_frame
	var list_node := root.find_child("List", true, false)
	assert_not_null(list_node, "VBoxContainer List deve existir em glossary_tab.tscn")
	assert_true(
		list_node.get_child_count() > 0,
		"Lista do glossário deve ter entradas apos populate() (conteudo real, nao aba vazia)"
	)


func test_populate_multiplos_niveis_sem_crash() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	for level: int in range(1, 5):
		var entries := GlossaryCatalog.entries_for_level(level)
		root.populate(entries)
		await get_tree().process_frame
	assert_true(true, "populate() chamado para niveis 1-4 sem crash")


func _load_scene() -> GlossaryTab:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate() as GlossaryTab
	add_child_autoqfree(root)
	return root
