extends GutTest
## T-173 (016 Sprint 4 delta-A) — animações rescue/captive no AnimatedEntityRegistry.
## DoD count-level: hero_rescue (6f), captive_idle (4f), captive_rescue (5f) carregados;
## Captive usa AnimatedSprite2D; RESCUED aciona hero_rescue no warrior. 0-regressão.


func _make_registry_ready() -> AnimatedEntityRegistry:
	var reg := AnimatedEntityRegistry.new()
	add_child_autoqfree(reg)
	await get_tree().process_frame
	return reg


func _make_floor() -> TileMapLayer:
	var floor := TileMapLayer.new()
	var tile_set := TileSet.new()
	tile_set.tile_size = Vector2i(32, 32)
	floor.tile_set = tile_set
	add_child_autoqfree(floor)
	return floor


# ── Manifest data-driven: 3 entradas obrigatórias ────────────────────────────


func test_manifest_hero_tem_animacao_rescue_6_frames() -> void:
	var reg := await _make_registry_ready()
	var cache: Dictionary = reg.get("_frames_cache")
	assert_true(cache.has("hero"), "hero deve estar no frames_cache")
	if not cache.has("hero"):
		return
	var sf: SpriteFrames = cache["hero"]
	assert_true(sf.has_animation("rescue"), "hero deve ter animação rescue")
	assert_eq(sf.get_frame_count("rescue"), 6, "hero_rescue deve ter 6 frames")


func test_manifest_captive_tem_animacao_idle_4_frames() -> void:
	var reg := await _make_registry_ready()
	var cache: Dictionary = reg.get("_frames_cache")
	assert_true(cache.has("captive"), "captive deve estar no frames_cache")
	if not cache.has("captive"):
		return
	var sf: SpriteFrames = cache["captive"]
	assert_true(sf.has_animation("idle"), "captive deve ter animação idle")
	assert_eq(sf.get_frame_count("idle"), 4, "captive_idle deve ter 4 frames")


func test_manifest_captive_tem_animacao_rescue_5_frames() -> void:
	var reg := await _make_registry_ready()
	var cache: Dictionary = reg.get("_frames_cache")
	assert_true(cache.has("captive"), "captive deve estar no frames_cache")
	if not cache.has("captive"):
		return
	var sf: SpriteFrames = cache["captive"]
	assert_true(sf.has_animation("rescue"), "captive deve ter animação rescue")
	assert_eq(sf.get_frame_count("rescue"), 5, "captive_rescue deve ter 5 frames")


# ── Captive renderiza como AnimatedSprite2D ───────────────────────────────────


func test_captive_renderiza_como_animated_sprite2d() -> void:
	var units := {1: Captive.new()}
	var state := LevelState.new(5, 5, Warrior.new(), 1, 1, units, 0)
	var floor := _make_floor()
	var reg := await _make_registry_ready()
	reg.update_from_state(state, floor)
	await get_tree().process_frame

	var animated_count := 0
	for child: Node in reg.get_children():
		if child is AnimatedSprite2D:
			animated_count += 1
	# warrior + captive = pelo menos 2 AnimatedSprite2D
	assert_gte(animated_count, 2, "captive deve ser AnimatedSprite2D (junto ao warrior: >=2)")


func test_captive_sprite_toca_idle_ao_renderizar() -> void:
	var units := {1: Captive.new()}
	var state := LevelState.new(5, 5, Warrior.new(), 1, 1, units, 0)
	var floor := _make_floor()
	var reg := await _make_registry_ready()
	reg.update_from_state(state, floor)
	await get_tree().process_frame

	var idle_anims := 0
	for child: Node in reg.get_children():
		if child is AnimatedSprite2D:
			var asp := child as AnimatedSprite2D
			if asp.sprite_frames != null and asp.sprite_frames.has_animation("idle"):
				if asp.animation == "idle":
					idle_anims += 1
	assert_gte(idle_anims, 2, "warrior e captive devem estar tocando idle ao renderizar")


# ── RESCUED aciona hero_rescue no warrior ─────────────────────────────────────


func test_rescued_event_aciona_rescue_no_warrior() -> void:
	var state := LevelState.new(5, 5, Warrior.new(), 1, 1, {1: Captive.new()}, 0)
	var floor := _make_floor()
	var reg := await _make_registry_ready()
	reg.update_from_state(state, floor)
	await get_tree().process_frame

	# Acessa o sprite interno do warrior diretamente via reflexividade do GDScript.
	var sprites: Dictionary = reg.get("_sprites")
	var warrior_asp := sprites.get("warrior") as AnimatedSprite2D

	assert_not_null(warrior_asp, "warrior deve ter AnimatedSprite2D com animação rescue disponível")
	if warrior_asp == null:
		return

	# animate_events dispara factories síncronamente até o primeiro await interno;
	# _play_anim é chamado antes de qualquer await → animação fica "rescue" imediatamente.
	var event := TurnEvent.new(TurnEvent.Kind.RESCUED, "warrior", 0, 1)
	reg.animate_events([event], floor)

	assert_eq(
		warrior_asp.animation,
		"rescue",
		"RESCUED deve acionar animação rescue no warrior imediatamente"
	)
