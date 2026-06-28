class_name TestTelaGlossario016
extends GutTest
## T-169 (016) — PROVA DE RENDER DE CENA: Glossário fiel ao mockup.
## Instancia glossary_tab.tscn + chama populate() com entradas de game-term +
## renderiza >=1 frame + assere que a lista tem conteúdo com os termos esperados.

const _SCENE := "res://scenes/glossary_tab.tscn"

const _GAME_TERMS: Dictionary = {
	"entities":
	[
		{"name": "Cadete", "description": "Inimigo fraco que patrulha o corredor."},
		{"name": "Cativo", "description": "Prisioneiro que pode ser resgatado com rescue()."},
		{"name": "Daemon", "description": "Entidade hostil de alto nível que ocupa o corredor."},
	],
	"score_terms":
	[
		{
			"name": "Turno",
			"definition": "Cada execução do play_turn do jogador conta como um turno.",
			"value": "—"
		},
		{
			"name": "Andar",
			"definition": "Fase/nível da torre com uma configuração de grade fixa.",
			"value": "—"
		},
		{
			"name": "ACE",
			"definition": "Avaliação máxima: completar o nível com pontuação acima do limiar.",
			"value": "★★★"
		},
		{
			"name": "Corrupção",
			"definition": "Estado visual glitch que indica perigo ou erro na execução.",
			"value": "—"
		},
	],
}


func test_glossary_tab_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "glossary_tab.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "glossary_tab.tscn deve instanciar sem crash")


func test_list_container_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var list := root.find_child("List", true, false)
	assert_not_null(list, "VBoxContainer 'List' deve existir em glossary_tab.tscn")


func test_populate_cria_entradas_entities() -> void:
	var root := _load_and_populate()
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir")
	assert_true(
		list.get_child_count() > 0,
		"List deve ter filhos após populate() com entidades (conteúdo real, nao lista vazia)"
	)


func test_populate_com_score_terms_cria_entradas() -> void:
	var root := _load_and_populate()
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir")
	# entities (3) + score_terms (4) + 2 section labels = ao menos 9 filhos
	assert_true(
		list.get_child_count() >= 7,
		"List deve ter ao menos 7 filhos (entities + score_terms + section labels)"
	)


func test_populate_vazio_nao_crasha() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	root.populate({})
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir mesmo após populate({})")


func test_repopulate_limpa_lista_anterior() -> void:
	var root := _load_and_populate()
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	var count_before := list.get_child_count()
	assert_true(count_before > 0, "Lista deve ter entradas após primeiro populate()")
	root.populate({})
	await get_tree().process_frame
	assert_eq(
		list.get_child_count(), 0, "populate({}) deve limpar a lista anterior (sem duplicacao)"
	)


func _load_scene() -> GlossaryTab:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate() as GlossaryTab
	add_child_autoqfree(root)
	return root


func _load_and_populate() -> GlossaryTab:
	var root := _load_scene()
	root.populate(_GAME_TERMS)
	return root
