class_name EntitySpriteRegistry
extends Node2D

signal all_done

const TILE_SIZE := 64
const ANIM_WALK := 0.25
const ANIM_ATTACK := 0.20
const ANIM_HURT := 0.20
const ANIM_DIE := 0.30
const ANIM_REST := 0.20

var _sprites: Dictionary = {}
var _pending := 0


func update_from_state(state: LevelState, floor_layer: TileMapLayer) -> void:
	var active: Dictionary = {}

	var stairs_world := _cell_world(state.stairs_position(), floor_layer)
	_ensure_sprite("stairs", stairs_world, AssetPaths.STAIRS_SPRITE)
	active["stairs"] = true

	for pos: int in state.unit_positions():
		var key := "unit_%d" % pos
		var type_name: String = state.unit_at(pos).get_script().get_global_name()
		_ensure_sprite(key, _cell_world(pos, floor_layer), EntityAssetRegistry.sprite_for_type(type_name))
		active[key] = true

	var warrior_world := _cell_world(state.warrior_position(), floor_layer)
	_ensure_sprite("warrior", warrior_world, AssetPaths.WARRIOR_SPRITE)
	active["warrior"] = true

	for key: String in _sprites.keys():
		if not active.has(key):
			_sprites[key].queue_free()
			_sprites.erase(key)


func animate_events(events: Array, floor_layer: TileMapLayer) -> void:
	_pending = 0
	for event: TurnEvent in events:
		if _animate_event(event, floor_layer):
			_pending += 1
	if _pending == 0:
		all_done.emit()


func warrior_global_position() -> Vector2:
	if _sprites.has("warrior"):
		return (_sprites["warrior"] as Sprite2D).global_position
	return Vector2.ZERO


func _animate_event(event: TurnEvent, floor_layer: TileMapLayer) -> bool:
	match event.kind:
		TurnEvent.Kind.MOVED:
			return _tween_move("warrior", _cell_world(event.position, floor_layer))
		TurnEvent.Kind.ATTACKED, TurnEvent.Kind.SHOT:
			_tween_scale_pulse("warrior")
			return _tween_hurt("unit_%d" % event.position)
		TurnEvent.Kind.DAMAGED:
			return _tween_hurt("warrior")
		TurnEvent.Kind.ENEMY_DEFEATED, TurnEvent.Kind.RESCUED, TurnEvent.Kind.DIED:
			return _tween_die(_entity_key(event))
		TurnEvent.Kind.RESTED, TurnEvent.Kind.WON:
			return _tween_scale_pulse("warrior")
	return false


func _entity_key(event: TurnEvent) -> String:
	if event.kind == TurnEvent.Kind.DIED:
		return "warrior"
	return "unit_%d" % event.position


func _tween_move(key: String, target_world: Vector2) -> bool:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return false
	var tween := create_tween()
	tween.tween_property(sprite, "global_position", target_world, ANIM_WALK).set_ease(
		Tween.EASE_IN_OUT
	)
	tween.finished.connect(_on_tween_done, CONNECT_ONE_SHOT)
	return true


func _tween_scale_pulse(key: String) -> bool:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return false
	var tween := create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.3, 1.3), ANIM_ATTACK * 0.5)
	tween.tween_property(sprite, "scale", Vector2.ONE, ANIM_ATTACK * 0.5)
	tween.finished.connect(_on_tween_done, CONNECT_ONE_SHOT)
	return true


func _tween_hurt(key: String) -> bool:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return false
	var tween := create_tween()
	tween.tween_property(sprite, "modulate", Color.RED, ANIM_HURT * 0.4)
	tween.tween_property(sprite, "modulate", Color.WHITE, ANIM_HURT * 0.6)
	tween.finished.connect(_on_tween_done, CONNECT_ONE_SHOT)
	return true


func _tween_die(key: String) -> bool:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return false
	var tween := create_tween()
	tween.tween_property(sprite, "modulate:a", 0.0, ANIM_DIE)
	tween.finished.connect(_on_tween_done, CONNECT_ONE_SHOT)
	return true


func _on_tween_done() -> void:
	_pending -= 1
	if _pending <= 0:
		all_done.emit()


func _cell_world(col: int, floor_layer: TileMapLayer) -> Vector2:
	return floor_layer.to_global(floor_layer.map_to_local(Vector2i(col, 0)))


func _ensure_sprite(key: String, world_pos: Vector2, tex_path: String) -> void:
	if not _sprites.has(key):
		var sprite := Sprite2D.new()
		sprite.texture = _load_or_placeholder(tex_path)
		add_child(sprite)
		_sprites[key] = sprite
	(_sprites[key] as Sprite2D).global_position = world_pos
	(_sprites[key] as Sprite2D).modulate = Color.WHITE
	(_sprites[key] as Sprite2D).scale = Vector2.ONE


func _load_or_placeholder(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	var img := Image.create(TILE_SIZE, TILE_SIZE, false, Image.FORMAT_RGBA8)
	img.fill(Color.MAGENTA)
	return ImageTexture.create_from_image(img)
