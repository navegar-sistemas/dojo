class_name CameraFollowController
extends Node

## Dead-zone half-width in pixels: camera doesn't scroll while warrior is within this distance.
@export var dead_zone_half_w: float = 32.0
## How far (px) the camera leads in the direction of movement.
@export var lookahead_px: float = 96.0
## Warrior must move this far (px) in the opposite direction before lookahead side flips.
@export var hysteresis_px: float = 32.0
## Camera lerp speed toward desired position (higher = snappier follow).
@export var smooth_speed: float = 6.0

## Exposed for tests: warrior position tracked last frame.
var target_position: Vector2 = Vector2.ZERO
## Exposed for tests: current committed lookahead direction (-1, 0 or +1).
var current_lookahead_dir: float = 0.0

var _camera: Camera2D
var _get_warrior_pos: Callable
var _static_mode: bool = true
## Segue Y somente quando o nível é maior que o viewport verticalmente.
var _static_mode_y: bool = true
var _lookahead_dir: float = 0.0
var _anchor_x: float = 0.0


func initialize(
	camera: Camera2D,
	level_width_px: float,
	viewport_size: Vector2,
	get_warrior_pos: Callable,
	level_height_px: float = 0.0
) -> void:
	_camera = camera
	_get_warrior_pos = get_warrior_pos
	_static_mode = level_width_px <= viewport_size.x
	_static_mode_y = level_height_px <= 0.0 or level_height_px <= viewport_size.y

	camera.zoom = Vector2.ONE
	camera.position_smoothing_enabled = false
	camera.limit_left = 0
	camera.limit_right = int(level_width_px)
	camera.limit_top = -int(viewport_size.y)
	camera.limit_bottom = int(viewport_size.y + maxf(0.0, level_height_px))

	var initial_x: float
	if _static_mode:
		initial_x = level_width_px * 0.5
	else:
		var wp: Vector2 = get_warrior_pos.call()
		initial_x = wp.x

	var initial_y: float = 0.0
	if not _static_mode_y:
		initial_y = get_warrior_pos.call().y

	camera.global_position = Vector2(initial_x, initial_y)
	target_position = camera.global_position
	_anchor_x = initial_x
	_lookahead_dir = 0.0
	current_lookahead_dir = 0.0


func _process(delta: float) -> void:
	if _camera == null or _static_mode:
		return
	var warrior_pos: Vector2 = _get_warrior_pos.call()
	if warrior_pos == Vector2.ZERO:
		return
	_follow(warrior_pos, delta)


func _follow(warrior_pos: Vector2, delta: float) -> void:
	target_position = warrior_pos

	var dx := warrior_pos.x - _anchor_x
	if absf(dx) > hysteresis_px:
		_lookahead_dir = signf(dx)
		_anchor_x = warrior_pos.x
	current_lookahead_dir = _lookahead_dir

	var cam_x := _camera.global_position.x
	var warrior_dist := warrior_pos.x - cam_x
	var new_x := cam_x
	if absf(warrior_dist) > dead_zone_half_w:
		var target_x := warrior_pos.x + _lookahead_dir * lookahead_px
		new_x = lerpf(cam_x, target_x, minf(1.0, delta * smooth_speed))

	var new_y := _camera.global_position.y
	if not _static_mode_y:
		var cam_y := _camera.global_position.y
		var dy := warrior_pos.y - cam_y
		if absf(dy) > dead_zone_half_w:
			new_y = lerpf(cam_y, warrior_pos.y, minf(1.0, delta * smooth_speed))

	_camera.global_position = Vector2(new_x, new_y)
