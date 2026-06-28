class_name TileMapArena
extends Node2D
## Componente isolado de arena: TileMapLayer 32px com tiles floor/wall/stairs.
## Cria e gerencia seu próprio TileMapLayer — não depende de game.tscn.
## Fonte de verdade do TILE_SIZE 32px para toda a apresentação (ADR-042).

const TILE_SIZE := 32
const ATLAS_COORD := Vector2i(0, 0)

var _floor_layer: TileMapLayer
var _floor_source_id := 0
var _wall_source_id := 1
var _stairs_source_id := 2


func _init() -> void:
	_floor_layer = TileMapLayer.new()
	_floor_layer.name = "FloorLayer"
	add_child(_floor_layer)


func setup(state: LevelState) -> void:
	_setup_tile_set()
	_update_cells(state)


func get_floor_layer() -> TileMapLayer:
	return _floor_layer


func _setup_tile_set() -> void:
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

	var stairs_src := TileSetAtlasSource.new()
	stairs_src.texture = _load_or_color(EntityAssetRegistry.stairs_tile(), Color(0.8, 0.7, 0.2))
	stairs_src.texture_region_size = Vector2i(TILE_SIZE, TILE_SIZE)
	stairs_src.create_tile(ATLAS_COORD)
	_stairs_source_id = tile_set.add_source(stairs_src)

	_floor_layer.tile_set = tile_set


func _update_cells(state: LevelState) -> void:
	_floor_layer.clear()
	if state.rows() > 1:
		_update_cells_2d(state)
		return
	var width := state.width()
	for col: int in range(width):
		_floor_layer.set_cell(Vector2i(col, 0), _floor_source_id, ATLAS_COORD)
	_floor_layer.set_cell(Vector2i(-1, 0), _wall_source_id, ATLAS_COORD)
	_floor_layer.set_cell(Vector2i(width, 0), _wall_source_id, ATLAS_COORD)
	_floor_layer.set_cell(Vector2i(state.stairs_position(), 0), _stairs_source_id, ATLAS_COORD)


## Grade R×C: itera rows×cols, adiciona paredes ao redor e posiciona a escada.
## Convenção domínio → TileMap: Vector2i(row, col) → TileMap cell (col, row).
func _update_cells_2d(state: LevelState) -> void:
	var r := state.rows()
	var c := state.cols()
	for row: int in range(r):
		for col: int in range(c):
			_floor_layer.set_cell(Vector2i(col, row), _floor_source_id, ATLAS_COORD)
	for row: int in range(r):
		_floor_layer.set_cell(Vector2i(-1, row), _wall_source_id, ATLAS_COORD)
		_floor_layer.set_cell(Vector2i(c, row), _wall_source_id, ATLAS_COORD)
	for col: int in range(-1, c + 1):
		_floor_layer.set_cell(Vector2i(col, -1), _wall_source_id, ATLAS_COORD)
		_floor_layer.set_cell(Vector2i(col, r), _wall_source_id, ATLAS_COORD)
	var stairs := state.stairs_position_2d()
	_floor_layer.set_cell(Vector2i(stairs.y, stairs.x), _stairs_source_id, ATLAS_COORD)


func _load_or_color(path: String, fallback: Color) -> Texture2D:
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	var img := Image.create(TILE_SIZE, TILE_SIZE, false, Image.FORMAT_RGBA8)
	img.fill(fallback)
	return ImageTexture.create_from_image(img)
