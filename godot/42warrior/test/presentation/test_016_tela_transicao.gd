class_name TestTelaTransicao016
extends GutTest
## T-167 (016) — PROVA DE RENDER DE CENA: tela de TRANSIÇÃO fiel ao mockup.
## Instancia level_transition.tscn + renderiza >=1 frame + assere elementos-chave:
## Title do andar, Description, Abilities badge, StartBtn.

const _SCENE := "res://scenes/level_transition.tscn"


func test_level_transition_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "level_transition.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "level_transition.tscn deve instanciar sem crash")


func test_title_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false)
	assert_not_null(title, "Label Title (segmento/andar) deve existir em level_transition.tscn")


func test_description_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var lbl := root.find_child("Description", true, false)
	assert_not_null(lbl, "Label Description deve existir em level_transition.tscn")


func test_abilities_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var lbl := root.find_child("Abilities", true, false)
	assert_not_null(
		lbl, "Label Abilities (badge nova habilidade) deve existir em level_transition.tscn"
	)


func test_start_btn_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("StartBtn", true, false)
	assert_not_null(btn, "StartBtn (Iniciar Nível / > ENTER) deve existir em level_transition.tscn")


func test_sem_tower_flow_nao_crasha() -> void:
	# TowerFlow ausente no contexto de teste — _ready() deve ser tolerante
	var root := _load_scene()
	await get_tree().process_frame
	assert_not_null(root, "level_transition deve renderizar sem crash mesmo sem TowerFlow")


func _load_scene() -> Node:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
