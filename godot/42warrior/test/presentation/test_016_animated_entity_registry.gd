extends GutTest
## T-160 (016) — PROVA DE RENDER: AnimatedEntityRegistry em game.tscn headless.
## Assere que, após _ready carregar o nível 1, o warrior tem um AnimatedSprite2D
## ativo com SpriteFrames (idle) e ancoragem bottom-center (offset.y != 0).

const _GAME_SCENE := "res://scenes/game.tscn"


func test_warrior_tem_animated_sprite2d_ativo() -> void:
	var packed: PackedScene = load(_GAME_SCENE)
	var game_view: Node = packed.instantiate()
	add_child_autoqfree(game_view)

	# Aguarda _ready: AnimatedEntityRegistry._ready() + game_controller._load_level(1)
	await get_tree().process_frame
	await get_tree().process_frame

	var registry := game_view.get_node_or_null("DungeonView/Entities")
	assert_not_null(registry, "nó Entities (AnimatedEntityRegistry) deve existir em game.tscn")
	if registry == null:
		return

	var warrior_sprite := _find_animated_sprite2d(registry)
	assert_not_null(
		warrior_sprite, "deve existir ao menos um AnimatedSprite2D (warrior) em Entities"
	)
	if warrior_sprite == null:
		return

	assert_not_null(warrior_sprite.sprite_frames, "SpriteFrames deve estar configurado")
	assert_true(
		warrior_sprite.sprite_frames.has_animation("idle"),
		"animação 'idle' deve existir nos SpriteFrames"
	)
	assert_true(warrior_sprite.is_playing(), "AnimatedSprite2D deve estar tocando uma animação")
	assert_ne(
		warrior_sprite.offset.y, 0.0, "offset.y != 0 confirma ancoragem pelos pés (bottom-center)"
	)


func _find_animated_sprite2d(root: Node) -> AnimatedSprite2D:
	if root is AnimatedSprite2D:
		return root as AnimatedSprite2D
	for child: Node in root.get_children():
		var found := _find_animated_sprite2d(child)
		if found != null:
			return found
	return null
