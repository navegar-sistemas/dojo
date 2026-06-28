class_name DungeonView
extends Node2D

signal animations_finished

const TILE_SIZE := 64
const ATLAS_COORD := Vector2i(0, 0)

var _floor_source_id := 0
var _wall_source_id := 1
var _pending_state: LevelState
var _cam_controller: CameraFollowController

@onready var _floor_layer: TileMapLayer = $Floor
@onready var _entities: EntitySpriteRegistry = $Entities
@onready var _camera: Camera2D = $Camera


func _ready() -> void:
	_setup_tiles()
	_entities.all_done.connect(_on_animations_done)
	_cam_controller = CameraFollowController.new()
	add_child(_cam_controller)


func refresh_level(state: LevelState) -> void:
	_update_floor(state)
	_entities.update_from_state(state, _floor_layer)
	_init_camera(state)


func on_turn_result(result: TurnResult, state: LevelState) -> void:
	_pending_state = state
	_entities.animate_events(result.events, _floor_layer)


func _on_animations_done() -> void:
	if _pending_state != null:
		_entities.update_from_state(_pending_state, _floor_layer)
	animations_finished.emit()


func _init_camera(state: LevelState) -> void:
	var level_w := float(state.width() * TILE_SIZE)
	var vp_size := get_viewport_rect().size
	_cam_controller.initialize(_camera, level_w, vp_size, _entities.warrior_global_position)


func _update_floor(state: LevelState) -> void:
	_floor_layer.clear()
	var width := state.width()
	for col: int in range(width):
		_floor_layer.set_cell(Vector2i(col, 0), _floor_source_id, ATLAS_COORD)
	_floor_layer.set_cell(Vector2i(-1, 0), _wall_source_id, ATLAS_COORD)
	_floor_layer.set_cell(Vector2i(width, 0), _wall_source_id, ATLAS_COORD)


func _setup_tiles() -> void:
	var tile_set := TileSet.new()
	tile_set.tile_size = Vector2i(TILE_SIZE, TILE_SIZE)

	var floor_src := TileSetAtlasSource.new()
	floor_src.texture = _load_or_color(EntityAssetRegistry.floor_tile(), Color(0.137, 0.169, 0.212))
	floor_src.texture_region_size = Vector2i(TILE_SIZE, TILE_SIZE)
	floor_src.create_tile(ATLAS_COORD)
	_floor_source_id = tile_set.add_source(floor_src)

	var wall_src := TileSetAtlasSource.new()
	wall_src.texture = _load_or_color(EntityAssetRegistry.wall_tile(), Color(0.227, 0.176, 0.290))
	wall_src.texture_region_size = Vector2i(TILE_SIZE, TILE_SIZE)
	wall_src.create_tile(ATLAS_COORD)
	_wall_source_id = tile_set.add_source(wall_src)

	_floor_layer.tile_set = tile_set


func _load_or_color(path: String, fallback: Color) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	var img := Image.create(TILE_SIZE, TILE_SIZE, false, Image.FORMAT_RGBA8)
	img.fill(fallback)
	return ImageTexture.create_from_image(img)
