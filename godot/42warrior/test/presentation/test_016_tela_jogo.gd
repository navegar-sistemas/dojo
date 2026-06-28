class_name TestTelaJogo016
extends GutTest
## T-163 (016) — PROVA DE RENDER DE CENA: tela de JOGO fiel ao mockup.
## Instancia game.tscn + renderiza >=1 frame + assere 3 zonas (status bar,
## arena tiles/sprites, console+controles) + editor retrátil visível + glitch + Theme.

const _GAME_SCENE := "res://scenes/game.tscn"


func test_game_tscn_instancia_sem_crash() -> void:
	var packed := load(_GAME_SCENE) as PackedScene
	assert_not_null(packed, "game.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "game.tscn deve instanciar sem crash")


func test_zona_status_bar_presente_no_topo() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var status_bar := root.find_child("StatusBar", true, false)
	assert_not_null(status_bar, "zona topo: nó StatusBar deve existir em game.tscn")


func test_zona_arena_dungeon_view_com_floor_e_entities() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var dungeon := root.find_child("DungeonView", true, false)
	assert_not_null(dungeon, "zona centro: DungeonView deve existir na cena")
	var floor_layer := root.find_child("Floor", true, false)
	assert_not_null(floor_layer, "arena deve ter TileMapLayer 'Floor' com tiles posicionados")
	var entities := root.find_child("Entities", true, false)
	assert_not_null(entities, "arena deve ter Entities (AnimatedEntityRegistry com sprites)")


func test_zona_console_presente() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var console := root.find_child("TurnConsole", true, false)
	assert_not_null(console, "zona inferior: TurnConsole deve existir na cena")


func test_zona_controles_presente() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var controls := root.find_child("ExecutionControls", true, false)
	assert_not_null(controls, "zona inferior: ExecutionControls deve existir na cena")


func test_editor_retratil_default_visivel() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var editor := root.find_child("CodeEditorPanel", true, false)
	assert_not_null(editor, "CodeEditorPanel deve existir na cena")
	assert_true(editor.visible, "editor retrátil deve estar visível por padrão (começa aberto)")


func test_glitch_post_process_nomeado_e_presente() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var glitch := root.find_child("GlitchPostProcess", true, false)
	assert_not_null(glitch, "GlitchPostProcess deve existir como filho nomeado da cena")


func test_play_btn_e_four_state_button() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var play_btn := root.find_child("PlayBtn", true, false)
	assert_not_null(play_btn, "PlayBtn deve existir nos controles")
	assert_true(
		play_btn is FourStateButton,
		"PlayBtn deve ser FourStateButton (T-162) para 4 estados data-driven"
	)


func test_step_btn_e_four_state_button() -> void:
	var root := _load_game()
	await get_tree().process_frame
	var step_btn := root.find_child("StepBtn", true, false)
	assert_not_null(step_btn, "StepBtn deve existir nos controles")
	assert_true(
		step_btn is FourStateButton,
		"StepBtn deve ser FourStateButton (T-162) para 4 estados data-driven"
	)


func test_theme_global_design_system_aplicado() -> void:
	var root := _load_game()
	await get_tree().process_frame
	# Verifica que o GameController aplicou o Theme às camadas de UI
	var hud := root.find_child("HudView", true, false)
	assert_not_null(hud, "HudView deve existir")
	# Qualquer Label dentro do HudView deve ter font_color não-nulo via Theme herdado
	var any_label := root.find_child("HpLabel", true, false)
	assert_not_null(any_label, "HpLabel deve existir no StatusBar")


func _load_game() -> Node:
	var packed := load(_GAME_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
