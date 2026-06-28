class_name TestTelaResultado016
extends GutTest
## T-166 (016) — PROVA DE RENDER DE CENA: tela de RESULTADO fiel ao mockup.
## Instancia level_result.tscn + renderiza >=1 frame + assere elementos-chave
## (Title, ScoreLabel, AceLabel, NextBtn, RetryBtn) sem depender de TowerFlow.

const _SCENE := "res://scenes/level_result.tscn"


func test_level_result_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "level_result.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "level_result.tscn deve instanciar sem crash")


func test_title_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false)
	assert_not_null(title, "Label Title deve existir em level_result.tscn")


func test_score_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var lbl := root.find_child("ScoreLabel", true, false)
	assert_not_null(lbl, "Label ScoreLabel deve existir em level_result.tscn")


func test_ace_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var lbl := root.find_child("AceLabel", true, false)
	assert_not_null(lbl, "Label AceLabel deve existir em level_result.tscn")


func test_next_btn_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("NextBtn", true, false)
	assert_not_null(btn, "NextBtn (Próximo Nível) deve existir em level_result.tscn")


func test_retry_btn_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("RetryBtn", true, false)
	assert_not_null(btn, "RetryBtn (Tentar Novamente) deve existir em level_result.tscn")


func test_menu_btn_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("MenuBtn", true, false)
	assert_not_null(btn, "MenuBtn (Menu) deve existir em level_result.tscn")


func test_sem_tower_flow_nao_crasha() -> void:
	# TowerFlow ausente no contexto de teste — _ready() deve ser tolerante
	var root := _load_scene()
	await get_tree().process_frame
	assert_not_null(root, "level_result deve renderizar sem crash mesmo sem TowerFlow")


func test_fundo_void_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var bg := root.find_child("VoidBackground", true, false)
	assert_not_null(bg, "VoidBackground (fundo void) deve existir em level_result.tscn")


func test_next_btn_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("NextBtn", true, false)
	assert_not_null(btn, "NextBtn deve existir")
	assert_true(
		btn is FourStateButton, "NextBtn deve ser FourStateButton (T-162) — nao Button base"
	)


func test_retry_btn_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("RetryBtn", true, false)
	assert_not_null(btn, "RetryBtn deve existir")
	assert_true(
		btn is FourStateButton, "RetryBtn deve ser FourStateButton (T-162) — nao Button base"
	)


func test_menu_btn_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("MenuBtn", true, false)
	assert_not_null(btn, "MenuBtn deve existir")
	assert_true(
		btn is FourStateButton, "MenuBtn deve ser FourStateButton (T-162) — nao Button base"
	)


func test_theme_fonte_real_aplicada() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false) as Label
	assert_not_null(title, "Title Label deve existir")
	var font := title.get_theme_font("font", "Label")
	assert_not_null(font, "Label deve ter fonte do Theme aplicada (nao null)")
	assert_true(
		font.resource_path.length() > 0,
		"fonte deve ser real do GlobalDesignSystem (resource_path nao vazio — nao default Godot)"
	)


func _load_scene() -> Node:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
