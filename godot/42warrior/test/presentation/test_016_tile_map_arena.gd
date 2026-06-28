extends GutTest
## T-161 (016) — PROVA DE RENDER ISOLADA: TileMapArena 32px.
## Instancia TileMapArena sem game.tscn, popula com LevelState minimal
## e assere que floor_layer tem células REALMENTE desenhadas na grade 32px.


func test_floor_layer_exists_after_setup() -> void:
	var state := LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	assert_not_null(arena.get_floor_layer(), "floor_layer deve existir após setup")


func test_floor_layer_has_cells_drawn() -> void:
	var state := LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_gt(cells.size(), 0, "floor_layer deve ter células desenhadas após setup")


func test_floor_cells_cover_full_width() -> void:
	var width := 6
	var state := LevelState.new(width, 5, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	# floor (width) + wall_esq (-1,0) + wall_dir (width,0) + stairs sobrepostos no chão
	assert_gte(cells.size(), width, "deve ter pelo menos width células de chão")


func test_tile_size_is_32px() -> void:
	assert_eq(TileMapArena.TILE_SIZE, 32, "TILE_SIZE deve ser exatamente 32px (sem regredir a 64)")


func test_tile_set_size_is_32x32() -> void:
	var state := LevelState.new(5, 4, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var tile_set := arena.get_floor_layer().tile_set
	assert_not_null(tile_set, "floor_layer deve ter tile_set configurado")
	assert_eq(tile_set.tile_size, Vector2i(32, 32), "tile_set.tile_size deve ser (32, 32)")


func test_stairs_cell_drawn_at_stairs_position() -> void:
	var stairs_pos := 5
	var state := LevelState.new(7, stairs_pos, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_true(
		Vector2i(stairs_pos, 0) in cells,
		"célula de escadas deve estar desenhada em (%d, 0)" % stairs_pos
	)


func test_wall_cells_at_boundaries() -> void:
	var width := 6
	var state := LevelState.new(width, 5, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_true(Vector2i(-1, 0) in cells, "parede esquerda deve estar em (-1, 0)")
	assert_true(Vector2i(width, 0) in cells, "parede direita deve estar em (%d, 0)" % width)


func test_renders_at_least_one_frame() -> void:
	var state := LevelState.new(4, 3, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	assert_true(arena.is_inside_tree(), "arena deve estar na árvore de cena após setup")
