class_name AnimatedEntityRegistry
extends Node2D
## Registro de sprites animados (hero/captive/enemy_cadet/enemy_dev/boss_director).
## Data-driven: lê assets/v1/anim/manifest.json e constrói SpriteFrames por código —
## trocar arte = trocar o arquivo, 0 path hardcoded (RNF-060).
## Mantém a mesma interface pública do EntitySpriteRegistry para substituição transparente.

signal all_done

const _MANIFEST_PATH := "res://assets/v1/anim/manifest.json"
const _ANIM_BASE := "res://assets/v1/anim/"
const _ARROW_TEX := "res://assets/v1/fx_arrow.png"

## Velocidades das animações (frames por segundo).
const _FPS_IDLE := 4.0
const _FPS_WALK := 8.0
const _FPS_ACTION := 10.0
const _FPS_HURT := 10.0
const _FPS_DEATH := 6.0

const _ANIM_FPS: Dictionary = {
	"idle": _FPS_IDLE,
	"walk": _FPS_WALK,
	"attack": _FPS_ACTION,
	"shoot": _FPS_ACTION,
	"cast": _FPS_ACTION,
	"rescue": _FPS_ACTION,
	"hurt": _FPS_HURT,
	"death": _FPS_DEATH,
}

## Mapeamento class_name de domínio → nome no manifest.json.
const _TYPE_TO_MANIFEST: Dictionary = {
	"Warrior": "hero",
	"Captive": "captive",
	"Sludge": "enemy_cadet",
	"ThickSludge": "enemy_cadet",
	"Archer": "enemy_dev",
	"Wizard": "boss_director",
}

## Duração de walk em segundos (equivale à constante ANIM_WALK do registry legado).
const _WALK_S := 0.25

var _sprites: Dictionary = {}
var _frames_cache: Dictionary = {}
var _frame_height: Dictionary = {}
## Referência viva ao sequencer para evitar coleta antecipada (é RefCounted).
var _sequencer: AnimationSequencer = null


func _ready() -> void:
	_build_frames_cache()


# ── API pública ─────────────────────────────────────────────────────────────


func update_from_state(state: LevelState, floor_layer: TileMapLayer) -> void:
	var active: Dictionary = {}

	var stairs_world := _cell_world_2d(state.stairs_position_2d(), floor_layer)
	_ensure_sprite("stairs", stairs_world, "")
	active["stairs"] = true

	for pos: Vector2i in state.unit_positions_2d():
		var key := "unit_%d_%d" % [pos.x, pos.y]
		var unit: Unit = state.unit_at_2d(pos)
		if unit == null:
			continue
		var type_name: String = unit.get_script().get_global_name()
		_ensure_sprite(key, _cell_world_2d(pos, floor_layer), type_name)
		active[key] = true

	var warrior_world := _cell_world_2d(state.warrior_position_2d(), floor_layer)
	_ensure_sprite("warrior", warrior_world, "Warrior")
	_apply_warrior_direction(state)
	active["warrior"] = true

	for key: String in _sprites.keys():
		if not active.has(key):
			_sprites[key].queue_free()
			_sprites.erase(key)


func animate_events(events: Array, floor_layer: TileMapLayer) -> void:
	_sequencer = AnimationSequencer.new()
	for event: TurnEvent in events:
		_sequencer.enqueue_beat(_beat_factories(event, floor_layer))
	_sequencer.all_done.connect(_on_sequence_done, CONNECT_ONE_SHOT)
	_sequencer.play()


func warrior_global_position() -> Vector2:
	var s: Node2D = _sprites.get("warrior") as Node2D
	if s != null:
		return s.global_position
	return Vector2.ZERO


# ── Internos ─────────────────────────────────────────────────────────────────


func _on_sequence_done() -> void:
	all_done.emit()


func _build_frames_cache() -> void:
	var f := FileAccess.open(_MANIFEST_PATH, FileAccess.READ)
	if f == null:
		return
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if not parsed is Array:
		return
	var by_name: Dictionary = {}
	for entry: Dictionary in parsed as Array:
		var name: String = entry.get("name", "")
		if name.is_empty():
			continue
		if not by_name.has(name):
			by_name[name] = []
		(by_name[name] as Array).append(entry)
	for ent_name: String in by_name:
		_frames_cache[ent_name] = _build_sprite_frames(ent_name, by_name[ent_name] as Array)


func _build_sprite_frames(ent_name: String, entries: Array) -> SpriteFrames:
	var sf := SpriteFrames.new()
	if sf.has_animation("default"):
		sf.remove_animation("default")
	var fh_last := 48
	for entry: Dictionary in entries:
		var anim_name: String = entry.get("anim", "")
		var frame_count: int = entry.get("frames", 1)
		var fw: int = entry.get("fw", 48)
		fh_last = entry.get("fh", 48)
		var fps: float = _ANIM_FPS.get(anim_name, 8.0)
		var path: String = _ANIM_BASE + "%s_%s.png" % [ent_name, anim_name]
		var tex: Texture2D = _load_tex(path)
		sf.add_animation(anim_name)
		sf.set_animation_speed(anim_name, fps)
		sf.set_animation_loop(anim_name, anim_name != "death")
		for i: int in frame_count:
			var at := AtlasTexture.new()
			at.atlas = tex
			at.region = Rect2(i * fw, 0, fw, fh_last)
			sf.add_frame(anim_name, at)
	if not sf.has_animation("idle"):
		sf.add_animation("idle")
	_frame_height[ent_name] = fh_last
	return sf


func _ensure_sprite(key: String, world_pos: Vector2, type_name: String) -> void:
	var manifest_name: String = _TYPE_TO_MANIFEST.get(type_name, "")
	var is_animated := manifest_name != "" and _frames_cache.has(manifest_name)
	if not _sprites.has(key):
		if is_animated:
			var asp := AnimatedSprite2D.new()
			asp.sprite_frames = _frames_cache[manifest_name]
			# Ancoragem pelos pés: desloca o sprite para cima em metade da altura do frame.
			asp.offset = Vector2(0.0, -float(_frame_height.get(manifest_name, 48)) * 0.5)
			asp.play("idle")
			add_child(asp)
			_sprites[key] = asp
		else:
			var sp := Sprite2D.new()
			sp.texture = _load_tex(EntityAssetRegistry.sprite_for_type(type_name))
			add_child(sp)
			_sprites[key] = sp
	var node: Node2D = _sprites[key] as Node2D
	node.global_position = world_pos
	node.modulate = Color.WHITE
	node.scale = Vector2.ONE


func _beat_factories(event: TurnEvent, floor_layer: TileMapLayer) -> Array:
	var result: Array = []
	match event.kind:
		TurnEvent.Kind.MOVED:
			var target := _cell_world(event.position, floor_layer)
			result = [func() -> Tween: return _tween_walk("warrior", target)]
		TurnEvent.Kind.ATTACKED:
			var tk := "unit_%d" % event.position
			result = [
				func() -> Tween: return _tween_anim("warrior", "attack"),
				func() -> Tween: return _tween_anim(tk, "hurt"),
			]
		TurnEvent.Kind.SHOT:
			# Warrior dispara; fx_arrow é spawnado no frame de release (~40% da anim).
			var tk := "unit_%d" % event.position
			var wnode: Node2D = _sprites.get("warrior") as Node2D
			var wpos := wnode.global_position if wnode != null else Vector2.ZERO
			var tnode: Node2D = _sprites.get(tk) as Node2D
			var tpos := tnode.global_position if tnode != null else wpos
			result = [
				func() -> Tween: return _tween_shot("warrior", wpos, tpos),
				func() -> Tween: return _tween_anim(tk, "hurt"),
			]
		TurnEvent.Kind.DAMAGED:
			result = [func() -> Tween: return _tween_anim("warrior", "hurt")]
		TurnEvent.Kind.RESCUED:
			var ck := "unit_%d" % event.position
			result = [
				func() -> Tween: return _tween_anim("warrior", "rescue"),
				func() -> Tween: return _tween_die(ck),
			]
		TurnEvent.Kind.ENEMY_DEFEATED:
			var dk := "unit_%d" % event.position
			result = [func() -> Tween: return _tween_die(dk)]
		TurnEvent.Kind.DIED:
			result = [func() -> Tween: return _tween_die("warrior")]
		TurnEvent.Kind.RESTED, TurnEvent.Kind.WON:
			result = [func() -> Tween: return _tween_pulse("warrior")]
	return result


func _tween_walk(key: String, target_world: Vector2) -> Tween:
	var node: Node2D = _sprites.get(key) as Node2D
	if node == null:
		return null
	_play_anim(node, "walk")
	var tween := create_tween()
	tween.tween_property(node, "global_position", target_world, _WALK_S).set_ease(Tween.EASE_IN_OUT)
	tween.finished.connect(func() -> void: _play_anim(node, "idle"))
	return tween


func _tween_anim(key: String, anim_name: String) -> Tween:
	var node: Node2D = _sprites.get(key) as Node2D
	if node == null:
		return null
	_play_anim(node, anim_name)
	var dur := _anim_duration(node, anim_name)
	if dur <= 0.0:
		return null
	var tween := create_tween()
	tween.tween_interval(dur)
	if anim_name != "death":
		tween.finished.connect(func() -> void: _play_anim(node, "idle"))
	return tween


func _tween_shot(key: String, from: Vector2, to: Vector2) -> Tween:
	var node: Node2D = _sprites.get(key) as Node2D
	if node == null:
		return null
	_play_anim(node, "attack")
	var dur := _anim_duration(node, "attack")
	if dur <= 0.0:
		dur = 0.25
	var release_delay := dur * 0.4
	var tween := create_tween()
	# Aguarda o frame de "release" antes de spawnar a flecha.
	tween.tween_interval(release_delay)
	tween.tween_callback(func() -> void: _spawn_arrow(from, to))
	tween.tween_interval(dur * 0.6)
	tween.finished.connect(func() -> void: _play_anim(node, "idle"))
	return tween


func _tween_pulse(key: String) -> Tween:
	var node: Node2D = _sprites.get(key) as Node2D
	if node == null:
		return null
	var tween := create_tween()
	tween.tween_property(node, "scale", Vector2(1.3, 1.3), 0.10)
	tween.tween_property(node, "scale", Vector2.ONE, 0.10)
	return tween


func _tween_die(key: String) -> Tween:
	var node: Node2D = _sprites.get(key) as Node2D
	if node == null:
		return null
	_play_anim(node, "death")
	var dur := _anim_duration(node, "death")
	if dur <= 0.0:
		dur = 0.30
	var tween := create_tween()
	tween.tween_interval(dur)
	tween.finished.connect(func() -> void: node.modulate.a = 0.0)
	return tween


func _spawn_arrow(from: Vector2, to: Vector2) -> void:
	var arrow := Sprite2D.new()
	arrow.texture = _load_tex(_ARROW_TEX)
	arrow.global_position = from
	if not from.is_equal_approx(to):
		arrow.rotation = (to - from).angle()
	add_child(arrow)
	var tween := create_tween()
	tween.tween_property(arrow, "global_position", to, 0.15).set_ease(Tween.EASE_IN)
	tween.finished.connect(func() -> void: arrow.queue_free())


func _play_anim(node: Node2D, anim_name: String) -> void:
	if not node is AnimatedSprite2D:
		return
	var asp := node as AnimatedSprite2D
	if asp.sprite_frames != null and asp.sprite_frames.has_animation(anim_name):
		asp.play(anim_name)


func _anim_duration(node: Node2D, anim_name: String) -> float:
	if not node is AnimatedSprite2D:
		return 0.0
	var asp := node as AnimatedSprite2D
	if asp.sprite_frames == null or not asp.sprite_frames.has_animation(anim_name):
		return 0.0
	var count := asp.sprite_frames.get_frame_count(anim_name)
	var fps := asp.sprite_frames.get_animation_speed(anim_name)
	if fps <= 0.0:
		return 0.0
	return count / fps


func _cell_world(col: int, floor_layer: TileMapLayer) -> Vector2:
	return floor_layer.to_global(floor_layer.map_to_local(Vector2i(col, 0)))


## Converte posição domínio (row, col) → posição mundo via TileMap (col, row).
func _cell_world_2d(grid_pos: Vector2i, floor_layer: TileMapLayer) -> Vector2:
	return floor_layer.to_global(floor_layer.map_to_local(Vector2i(grid_pos.y, grid_pos.x)))


## Aplica flip_h/flip_v no sprite do warrior conforme a direção 4-dir do estado.
## Leste: flip_h=false. Oeste: flip_h=true.
## Norte: flip_h=false, flip_v=false, rotation=-PI/2.
## Sul: flip_h=false, flip_v=false, rotation=PI/2.
## Preserva comportamento 1D (warrior_4dir=null → usa warrior_facing).
func _apply_warrior_direction(state: LevelState) -> void:
	var node: Node2D = _sprites.get("warrior") as Node2D
	if not node is AnimatedSprite2D:
		return
	var asp := node as AnimatedSprite2D
	var dir: Direction = state.warrior_4dir()
	if dir == null:
		asp.flip_h = state.warrior_facing() < 0
		asp.flip_v = false
		asp.rotation = 0.0
		return
	var delta := dir.delta()
	if delta == Vector2i(0, 1):  # East
		asp.flip_h = false
		asp.flip_v = false
		asp.rotation = 0.0
	elif delta == Vector2i(0, -1):  # West
		asp.flip_h = true
		asp.flip_v = false
		asp.rotation = 0.0
	elif delta == Vector2i(-1, 0):  # North (row diminui)
		asp.flip_h = false
		asp.flip_v = false
		asp.rotation = -PI / 2.0
	else:  # South (row aumenta)
		asp.flip_h = false
		asp.flip_v = false
		asp.rotation = PI / 2.0


func _load_tex(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	var img := Image.create(48, 48, false, Image.FORMAT_RGBA8)
	img.fill(Color.MAGENTA)
	return ImageTexture.create_from_image(img)
