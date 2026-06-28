class_name TestTelaConclusao016
extends GutTest
## T-171 (016) — PROVA DE RENDER DE CENA: tela de CONCLUSÃO/CRÉDITOS fiel ao mockup.
## Instancia tower_complete.tscn + renderiza >=1 frame + assere:
## terminal SYSTEM RESTORED, exit 0 verde, créditos SEM freesound/opengameart.

const _SCENE := "res://scenes/tower_complete.tscn"


func test_tower_complete_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "tower_complete.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "tower_complete.tscn deve instanciar sem crash")


func test_title_system_restored() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false) as Label
	assert_not_null(title, "Label Title deve existir em tower_complete.tscn")
	assert_true(
		"SYSTEM RESTORED" in title.text,
		"Title deve conter 'SYSTEM RESTORED' (terminal style, mockup T-171)"
	)


func test_exit_code_label_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var exit_lbl := root.find_child("ExitCode", true, false) as Label
	assert_not_null(exit_lbl, "ExitCode Label deve existir em tower_complete.tscn")
	assert_true(
		"exit 0" in exit_lbl.text, "ExitCode deve conter 'exit 0' (saída de sucesso, mockup T-171)"
	)


func test_credits_sem_freesound_opengameart() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var credits := root.find_child("Credits", true, false) as Label
	assert_not_null(credits, "Label Credits deve existir em tower_complete.tscn")
	assert_false(
		"freesound" in credits.text.to_lower(),
		"Credits NAO deve conter 'freesound' — atribuicao FALSA removida (T-171 must-fix)"
	)
	assert_false(
		"opengameart" in credits.text.to_lower(),
		"Credits NAO deve conter 'opengameart' — atribuicao FALSA removida (T-171 must-fix)"
	)


func test_credits_contem_atribuicao_correta() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var credits := root.find_child("Credits", true, false) as Label
	assert_not_null(credits, "Label Credits deve existir")
	assert_true(
		"Arte e áudio originais" in credits.text,
		"Credits deve conter 'Arte e áudio originais' (correcao factual T-171)"
	)
	assert_true(
		"Inspired by Ruby Warrior" in credits.text,
		"Credits deve manter 'Inspired by Ruby Warrior (Ryan Bates)'"
	)
	assert_true("Godot" in credits.text, "Credits deve manter 'Built with Godot 4 + GDScript'")


func test_menu_btn_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("MenuBtn", true, false)
	assert_not_null(btn, "MenuBtn deve existir em tower_complete.tscn")


func test_fundo_void_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var bg := root.find_child("VoidBackground", true, false)
	assert_not_null(bg, "VoidBackground (fundo void) deve existir em tower_complete.tscn")


func test_menu_btn_e_four_state_button() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var btn := root.find_child("MenuBtn", true, false)
	assert_not_null(btn, "MenuBtn deve existir")
	assert_true(
		btn is FourStateButton, "MenuBtn deve ser FourStateButton (T-162) — nao Button base"
	)


func _load_scene() -> Node:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
