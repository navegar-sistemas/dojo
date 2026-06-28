class_name TestSandboxScreen016
extends GutTest
## T-168 (016) — PROVA DE RENDER DE CENA: tela Sandbox/Tutorial fiel ao mockup.
## Instancia sandbox_screen.tscn + renderiza >=1 frame + assere:
## fundo void, badge MODO SANDBOX, grade com tiles (T-161), sprites (T-160), tooltips.

const _SCENE := "res://scenes/sandbox_screen.tscn"


func test_sandbox_screen_instancia_sem_crash() -> void:
	var packed := load(_SCENE) as PackedScene
	assert_not_null(packed, "sandbox_screen.tscn deve existir e ser carregável")
	var root := packed.instantiate()
	add_child_autoqfree(root)
	await get_tree().process_frame
	assert_not_null(root, "sandbox_screen.tscn deve instanciar sem crash")


func test_fundo_void_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var bg := root.find_child("VoidBackground", true, false)
	assert_not_null(bg, "VoidBackground (ColorRect fundo void) deve existir em sandbox_screen.tscn")


func test_badge_modo_sandbox_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var badge := root.find_child("SandboxBadge", true, false)
	assert_not_null(badge, "SandboxBadge (Label 'MODO SANDBOX') deve existir (mockup T-168)")
	var text: String = ""
	if badge.get("text") != null:
		text = badge.text
	assert_true("SANDBOX" in text.to_upper(), "SandboxBadge deve conter 'SANDBOX' no texto")


func test_dungeon_view_com_floor_tiles() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	await get_tree().process_frame
	var floor_layer := root.find_child("Floor", true, false) as TileMapLayer
	assert_not_null(floor_layer, "Floor TileMapLayer deve existir (reusa T-161 TileMapArena)")
	assert_true(
		floor_layer.get_used_cells().size() > 0,
		"Floor deve ter tiles REALMENTE desenhados (grade nao preta) — reusa T-161"
	)


func test_dungeon_view_entities_presente() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	await get_tree().process_frame
	var entities := root.find_child("Entities", true, false)
	assert_not_null(entities, "Entities (AnimatedEntityRegistry) deve existir — reusa T-160")


func test_tooltips_presentes() -> void:
	var root := _load_scene()
	await get_tree().process_frame
	var tooltip_list := root.find_child("TooltipList", true, false)
	assert_not_null(tooltip_list, "TooltipList deve existir em sandbox_screen.tscn")
	assert_true(
		tooltip_list.get_child_count() >= 2,
		"TooltipList deve ter >=2 tooltips passo a passo (mockup T-168)"
	)


func _load_scene() -> Node:
	var packed := load(_SCENE) as PackedScene
	var root := packed.instantiate()
	add_child_autoqfree(root)
	return root
