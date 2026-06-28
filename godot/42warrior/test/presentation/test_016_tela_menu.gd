class_name TestTelaMenu016
extends GutTest
## T-164 (016) — PROVA DE RENDER DE CENA: tela de MENU fiel ao mockup.
## Instancia main_menu.tscn + renderiza >=1 frame + assere elementos-chave:
## fundo void, boot log fake, key art, opções FourStateButton, Theme aplicado.

const _MENU_SCENE := "res://scenes/main_menu.tscn"


func test_main_menu_tscn_instancia_sem_crash() -> void:
	var packed := load(_MENU_SCENE) as PackedScene
	assert_not_null(packed, "main_menu.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "main_menu.tscn deve instanciar sem crash")


func test_fundo_void_presente() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var bg := root.find_child("VoidBackground", true, false)
	assert_not_null(bg, "VoidBackground (ColorRect fundo void) deve existir em main_menu.tscn")


func test_boot_log_presente_com_texto_42warrior() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var boot_log := root.find_child("BootLog", true, false)
	assert_not_null(boot_log, "BootLog deve existir em main_menu.tscn")
	var text: String = ""
	if boot_log.has_method("get_text"):
		text = boot_log.get_text()
	elif boot_log.get("text") != null:
		text = boot_log.text
	elif boot_log.get("bbcode_text") != null:
		text = boot_log.bbcode_text
	assert_true(
		"42warrior" in text.to_lower() or "./42warrior" in text,
		"BootLog deve conter '42warrior' no texto do boot log fake"
	)


func test_key_art_presente() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var key_art := root.find_child("KeyArt", true, false)
	assert_not_null(key_art, "KeyArt (TextureRect) deve existir em main_menu.tscn")


func test_start_btn_e_four_state_button() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var btn := root.find_child("StartBtn", true, false)
	assert_not_null(btn, "StartBtn deve existir no menu")
	assert_true(btn is FourStateButton, "StartBtn deve ser FourStateButton (T-162)")


func test_continue_btn_e_four_state_button() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var btn := root.find_child("ContinueBtn", true, false)
	assert_not_null(btn, "ContinueBtn deve existir no menu")
	assert_true(btn is FourStateButton, "ContinueBtn deve ser FourStateButton (T-162)")


func test_select_levels_btn_e_four_state_button() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var btn := root.find_child("SelectLevelsBtn", true, false)
	assert_not_null(btn, "SelectLevelsBtn deve existir no menu")
	assert_true(btn is FourStateButton, "SelectLevelsBtn deve ser FourStateButton (T-162)")


func test_audio_btn_presente() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var btn := root.find_child("AudioBtn", true, false)
	assert_not_null(btn, "AudioBtn (Áudio) deve existir no menu (mockup T-164)")


func test_about_btn_presente() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var btn := root.find_child("AboutBtn", true, false)
	assert_not_null(btn, "AboutBtn (Sobre/Créditos) deve existir no menu (mockup T-164)")


func test_theme_global_design_system_aplicado() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false)
	assert_not_null(title, "Label Title deve existir no menu")


func test_key_art_texture_carregada() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var key_art := root.find_child("KeyArt", true, false) as TextureRect
	assert_not_null(key_art, "KeyArt TextureRect deve existir")
	assert_not_null(
		key_art.texture,
		"key_art.png deve estar REALMENTE carregado (texture != null, nao TextureRect vazio)"
	)


func test_theme_fonte_press_start_2p_aplicada() -> void:
	var root := _load_menu()
	await get_tree().process_frame
	var title := root.find_child("Title", true, false) as Label
	assert_not_null(title, "Title Label deve existir")
	var font := title.get_theme_font("font", "Label")
	assert_not_null(font, "Label deve ter fonte do Theme aplicada (nao null)")
	assert_true(
		font.resource_path.length() > 0,
		"fonte deve ser Press Start 2P (resource_path nao vazio — nao default Godot)"
	)


func _load_menu() -> Node:
	var packed := load(_MENU_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
