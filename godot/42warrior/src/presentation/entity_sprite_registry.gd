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
## Mantém a referência viva enquanto a sequência toca (play() é assíncrono e o
## sequencer é RefCounted — sem isto ele poderia ser coletado durante o await).
var _sequencer: AnimationSequencer = null


func update_from_state(state: LevelState, floor_layer: TileMapLayer) -> void:
	var active: Dictionary = {}

	var stairs_world := _cell_world(state.stairs_position(), floor_layer)
	_ensure_sprite("stairs", stairs_world, EntityAssetRegistry.sprite_for_type("stairs"))
	active["stairs"] = true

	for pos: int in state.unit_positions():
		var key := "unit_%d" % pos
		var type_name: String = state.unit_at(pos).get_script().get_global_name()
		_ensure_sprite(
			key, _cell_world(pos, floor_layer), EntityAssetRegistry.sprite_for_type(type_name)
		)
		active[key] = true

	var warrior_world := _cell_world(state.warrior_position(), floor_layer)
	_ensure_sprite("warrior", warrior_world, EntityAssetRegistry.sprite_for_type("Warrior"))
	active["warrior"] = true

	for key: String in _sprites.keys():
		if not active.has(key):
			_sprites[key].queue_free()
			_sprites.erase(key)


## Anima os eventos do turno em ordem causal (RF-130): cada TurnEvent é um beat
## da fila; o beat N+1 só inicia depois que o N concluir. Pares causa-efeito do
## mesmo instante (ATTACKED = pulse+hurt) formam UM beat concorrente (RF-131).
func animate_events(events: Array, floor_layer: TileMapLayer) -> void:
	_sequencer = AnimationSequencer.new()
	for event: TurnEvent in events:
		_sequencer.enqueue_beat(_beat_factories(event, floor_layer))
	_sequencer.all_done.connect(_on_sequence_done, CONNECT_ONE_SHOT)
	_sequencer.play()


func warrior_global_position() -> Vector2:
	if _sprites.has("warrior"):
		return (_sprites["warrior"] as Sprite2D).global_position
	return Vector2.ZERO


func _on_sequence_done() -> void:
	all_done.emit()


## Traduz um TurnEvent no conjunto de factories (Callables que criam tweens) do
## seu beat. Um beat com >1 factory é concorrente (tocado junto); a serialização
## acontece ENTRE beats, no AnimationSequencer.
func _beat_factories(event: TurnEvent, floor_layer: TileMapLayer) -> Array:
	match event.kind:
		TurnEvent.Kind.MOVED:
			var target := _cell_world(event.position, floor_layer)
			return [func() -> Tween: return _tween_move("warrior", target)]
		TurnEvent.Kind.ATTACKED, TurnEvent.Kind.SHOT:
			var target_key := "unit_%d" % event.position
			return [
				func() -> Tween: return _tween_scale_pulse("warrior"),
				func() -> Tween: return _tween_hurt(target_key),
			]
		TurnEvent.Kind.DAMAGED:
			return [func() -> Tween: return _tween_hurt("warrior")]
		TurnEvent.Kind.ENEMY_DEFEATED, TurnEvent.Kind.RESCUED, TurnEvent.Kind.DIED:
			var die_key := _entity_key(event)
			return [func() -> Tween: return _tween_die(die_key)]
		TurnEvent.Kind.RESTED, TurnEvent.Kind.WON:
			return [func() -> Tween: return _tween_scale_pulse("warrior")]
	return []


func _entity_key(event: TurnEvent) -> String:
	if event.kind == TurnEvent.Kind.DIED:
		return "warrior"
	return "unit_%d" % event.position


func _tween_move(key: String, target_world: Vector2) -> Tween:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return null
	var tween := create_tween()
	tween.tween_property(sprite, "global_position", target_world, ANIM_WALK).set_ease(
		Tween.EASE_IN_OUT
	)
	return tween


func _tween_scale_pulse(key: String) -> Tween:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return null
	var tween := create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.3, 1.3), ANIM_ATTACK * 0.5)
	tween.tween_property(sprite, "scale", Vector2.ONE, ANIM_ATTACK * 0.5)
	return tween


func _tween_hurt(key: String) -> Tween:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return null
	var tween := create_tween()
	tween.tween_property(sprite, "modulate", Color.RED, ANIM_HURT * 0.4)
	tween.tween_property(sprite, "modulate", Color.WHITE, ANIM_HURT * 0.6)
	return tween


func _tween_die(key: String) -> Tween:
	var sprite := _sprites.get(key) as Sprite2D
	if sprite == null:
		return null
	var tween := create_tween()
	tween.tween_property(sprite, "modulate:a", 0.0, ANIM_DIE)
	return tween


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
