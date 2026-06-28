class_name TestTelaApiReference016
extends GutTest
## T-170 (016) — PROVA DE RENDER DE CENA: Referência da API fiel ao mockup (man-page).
## Instancia api_reference_tab.tscn + chama populate() com entries de sentidos/ações +
## renderiza >=1 frame + assere que SENTIDOS e AÇÕES aparecem na lista.

const _SCENE := "res://scenes/api_reference_tab.tscn"

const _SENTIDOS: Array = [
	{
		"name": "feel",
		"signature": "feel(direction: Direction = forward()) -> Space",
		"description": "Retorna o espaço adjacente.",
		"kind": "sense"
	},
	{
		"name": "look",
		"signature": "look(direction: Direction = forward()) -> Array[Space]",
		"description": "Retorna os 3 espaços à frente.",
		"kind": "sense"
	},
	{
		"name": "health",
		"signature": "health() -> int",
		"description": "Retorna o HP atual do warrior.",
		"kind": "sense"
	},
	{
		"name": "listen",
		"signature": "listen() -> Array[Space]",
		"description": "Retorna todos os espaços não-vazios do nível.",
		"kind": "sense"
	},
	{
		"name": "direction_of_stairs",
		"signature": "direction_of_stairs() -> Direction",
		"description": "Direção da escada.",
		"kind": "sense"
	},
]

const _ACOES: Array = [
	{
		"name": "walk",
		"signature": "walk(direction: Direction = forward())",
		"description": "Move o warrior.",
		"kind": "action"
	},
	{
		"name": "attack",
		"signature": "attack(direction: Direction = forward())",
		"description": "Ataca a tile adjacente.",
		"kind": "action"
	},
	{
		"name": "rest",
		"signature": "rest()",
		"description": "Descansa e recupera HP.",
		"kind": "action"
	},
	{
		"name": "rescue",
		"signature": "rescue(direction: Direction = forward())",
		"description": "Resgata um cativo.",
		"kind": "action"
	},
	{
		"name": "pivot",
		"signature": "pivot(direction: Direction)",
		"description": "Vira sem mover.",
		"kind": "action"
	},
	{
		"name": "shoot",
		"signature": "shoot(direction: Direction = forward())",
		"description": "Dispara à distância.",
		"kind": "action"
	},
]


func test_api_reference_tab_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "api_reference_tab.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "api_reference_tab.tscn deve instanciar sem crash")


func test_list_container_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var list := root.find_child("List", true, false)
	assert_not_null(list, "VBoxContainer 'List' deve existir em api_reference_tab.tscn")


func test_populate_sentidos_cria_entradas() -> void:
	var root := _load_and_populate(_SENTIDOS)
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir")
	assert_eq(
		list.get_child_count(),
		_SENTIDOS.size(),
		"List deve ter uma entrada por sentido passado a populate()"
	)


func test_populate_acoes_cria_entradas() -> void:
	var root := _load_and_populate(_ACOES)
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir")
	assert_eq(
		list.get_child_count(),
		_ACOES.size(),
		"List deve ter uma entrada por ação passada a populate()"
	)


func test_populate_sentidos_e_acoes_combinados() -> void:
	var all_entries: Array = _SENTIDOS + _ACOES
	var root := _load_and_populate(all_entries)
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_not_null(list, "List deve existir")
	assert_eq(
		list.get_child_count(),
		all_entries.size(),
		"List deve ter uma entrada por cada sentido+ação (man-page completa)"
	)


func test_repopulate_limpa_lista_anterior() -> void:
	var root := _load_and_populate(_SENTIDOS)
	await get_tree().process_frame
	var list := root.find_child("List", true, false) as VBoxContainer
	assert_true(list.get_child_count() > 0, "Lista deve ter entradas após primeiro populate()")
	root.populate([])
	await get_tree().process_frame
	assert_eq(
		list.get_child_count(), 0, "populate([]) deve limpar a lista anterior (sem duplicacao)"
	)


func _load_scene() -> ApiReferenceTab:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate() as ApiReferenceTab
	add_child_autoqfree(root)
	return root


func _load_and_populate(entries: Array) -> ApiReferenceTab:
	var root := _load_scene()
	root.populate(entries)
	return root
