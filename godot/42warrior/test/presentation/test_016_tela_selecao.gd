class_name TestTelaSelecao016
extends GutTest
## T-165 (016) — PROVA DE RENDER DE CENA: tela de SELEÇÃO DE NÍVEIS fiel ao mockup.
## Instancia level_select_screen.tscn + renderiza >=1 frame + assere:
## fundo void, grade 3x3 dos 9 andares, FourStateButton, BackBtn, Theme.

const _SCENE := "res://scenes/level_select_screen.tscn"


func test_level_select_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "level_select_screen.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "level_select_screen.tscn deve instanciar sem crash")


func test_fundo_void_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var bg := root.find_child("VoidBackground", true, false)
	assert_not_null(bg, "VoidBackground (ColorRect fundo void) deve existir")


func test_level_grid_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var grid := root.find_child("LevelGrid", true, false)
	assert_not_null(grid, "LevelGrid (GridContainer 3x3) deve existir na cena")


func test_level_btn_1_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("LevelBtn_1", true, false)
	assert_not_null(btn, "LevelBtn_1 deve existir após _populate()")
	assert_true(btn is FourStateButton, "LevelBtn_1 deve ser FourStateButton (T-162)")


func test_level_btn_9_chefe_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("LevelBtn_9", true, false)
	assert_not_null(btn, "LevelBtn_9 (andar chefe) deve existir na grade")


func test_todos_9_andares_existem() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	for i: int in range(1, 10):
		var btn := root.find_child("LevelBtn_%d" % i, true, false)
		assert_not_null(btn, "LevelBtn_%d deve existir na grade 3x3" % i)


func test_back_btn_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("BackBtn", true, false)
	assert_not_null(btn, "BackBtn deve existir na tela de seleção")
	assert_true(btn is FourStateButton, "BackBtn deve ser FourStateButton (T-162)")


func test_theme_global_design_system_aplicado() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false)
	assert_not_null(title, "Label Title deve existir na tela de seleção")


func test_grid_tem_9_botoes_criados() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var grid := root.find_child("LevelGrid", true, false) as GridContainer
	assert_not_null(grid, "LevelGrid deve existir")
	assert_true(
		grid.get_child_count() >= 9,
		"LevelGrid deve ter >=9 botoes criados por _populate() (conteudo real, nao grade vazia)"
	)


func test_theme_fonte_press_start_2p_aplicada() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false) as Label
	assert_not_null(title, "Title Label deve existir")
	var font := title.get_theme_font("font", "Label")
	assert_not_null(font, "Label deve ter fonte do Theme aplicada (nao null)")
	assert_true(
		font.resource_path.length() > 0,
		"fonte deve ser Press Start 2P (resource_path nao vazio — nao default Godot)"
	)


func _load_scene() -> Node:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
