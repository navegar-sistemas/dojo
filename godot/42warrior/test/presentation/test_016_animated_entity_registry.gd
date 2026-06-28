extends GutTest
## T-160 (016) — PROVA DE RENDER ISOLADA: AnimatedEntityRegistry como componente standalone.
## Instancia o registro diretamente (sem game.tscn), injeta um LevelState mínimo e assere
## que o warrior tem AnimatedSprite2D ativo com SpriteFrames+idle e ancoragem pelos pés.

const _MANIFEST_PATH := "res://assets/v1/anim/manifest.json"


func test_warrior_tem_animated_sprite2d_ativo() -> void:
	if not FileAccess.file_exists(_MANIFEST_PATH):
		pending("manifest.json ausente — prova de render de sprite pulada (sem assets de arte)")
		return

	var registry := AnimatedEntityRegistry.new()
	add_child_autoqfree(registry)
	await get_tree().process_frame

	var floor_layer := TileMapLayer.new()
	add_child_autoqfree(floor_layer)

	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {}, 0)
	registry.update_from_state(state, floor_layer)

	var warrior_sprite := _find_animated_sprite2d(registry)
	assert_not_null(warrior_sprite, "deve existir ao menos um AnimatedSprite2D (warrior)")
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
