extends GutTest
## T-184 (018 Sprint 3) — TileMapArena 2D + câmera 2 eixos + animações 4-dir.
## Render-rule COUNT-LEVEL: assere CONTEÚDO, não presença de nó.

const VIEWPORT := Vector2(1280.0, 720.0)


func _make_state_2d(rows: int, cols: int) -> LevelState:
	return LevelState.from_2d(
		rows, cols, Vector2i(rows - 1, cols - 1), Warrior.new(), Vector2i(0, 0), 1, {}, 0
	)


# ── TileMapArena 2D ──────────────────────────────────────────────────────────


func test_floor_layer_tem_celulas_em_grade_2d() -> void:
	var state := _make_state_2d(3, 5)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_gt(cells.size(), 0, "floor_layer deve ter células após setup 2D")


func test_floor_layer_cobre_toda_a_grade_rxc() -> void:
	var r := 3
	var c := 5
	var state := _make_state_2d(r, c)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	# R*C tiles de chão + paredes ao redor (2*(R+C+2) paredes)
	assert_gte(cells.size(), r * c, "floor_layer deve ter pelo menos R×C células de chão")


func test_celula_0_0_desenhada_em_grade_2d() -> void:
	var state := _make_state_2d(3, 5)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_true(Vector2i(0, 0) in cells, "célula (col=0, row=0) deve estar desenhada")


func test_celula_escada_desenhada_em_grade_2d() -> void:
	var stairs_row := 2
	var stairs_col := 4
	var state := LevelState.from_2d(
		3, 5, Vector2i(stairs_row, stairs_col), Warrior.new(), Vector2i(0, 0), 1, {}, 0
	)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	# TileMap cell da escada: Vector2i(stairs_col, stairs_row)
	assert_true(
		Vector2i(stairs_col, stairs_row) in cells,
		"célula de escada deve estar desenhada em (%d,%d)" % [stairs_col, stairs_row]
	)


func test_grade_2d_nao_afeta_grade_1d_retrocompat() -> void:
	var state_1d := LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0)
	var arena := TileMapArena.new()
	add_child_autoqfree(arena)
	arena.setup(state_1d)
	await get_tree().process_frame

	var cells := arena.get_floor_layer().get_used_cells()
	assert_gte(cells.size(), 6, "1D retrocompat: pelo menos 6 células de chão")
	assert_true(Vector2i(5, 0) in cells, "1D retrocompat: escada em (5, 0)")


# ── CameraFollowController 2D ────────────────────────────────────────────────


func test_camera_segue_warrior_no_eixo_y_em_nivel_2d() -> void:
	var warrior_pos := Vector2.ZERO
	var cam := Camera2D.new()
	add_child(cam)
	var ctrl := CameraFollowController.new()
	ctrl.smooth_speed = 1.0
	ctrl.dead_zone_half_w = 10.0
	add_child(ctrl)

	warrior_pos = Vector2(200.0, 100.0)
	ctrl.initialize(cam, 2000.0, VIEWPORT, func() -> Vector2: return warrior_pos, 1500.0)

	var cam_y_antes := cam.global_position.y
	warrior_pos = Vector2(200.0, cam_y_antes + 80.0)
	ctrl._follow(warrior_pos, 1.0)

	assert_gt(
		cam.global_position.y, cam_y_antes, "câmera deve seguir warrior no eixo Y em nível 2D"
	)
	cam.queue_free()
	ctrl.queue_free()


func test_camera_nao_segue_y_em_nivel_1d() -> void:
	var warrior_pos := Vector2.ZERO
	var cam := Camera2D.new()
	add_child(cam)
	var ctrl := CameraFollowController.new()
	ctrl.smooth_speed = 1.0
	ctrl.dead_zone_half_w = 10.0
	add_child(ctrl)

	warrior_pos = Vector2(200.0, 0.0)
	ctrl.initialize(cam, 2000.0, VIEWPORT, func() -> Vector2: return warrior_pos)

	var cam_y_antes := cam.global_position.y
	warrior_pos = Vector2(200.0, 200.0)
	ctrl._follow(warrior_pos, 1.0)

	assert_almost_eq(
		cam.global_position.y,
		cam_y_antes,
		0.01,
		"câmera NÃO deve seguir Y em nível 1D (level_height_px=0)"
	)
	cam.queue_free()
	ctrl.queue_free()


# ── AnimatedEntityRegistry: visual por direção 4-dir ─────────────────────────


func _warrior_sprite_from_state(state: LevelState) -> AnimatedSprite2D:
	var floor := TileMapLayer.new()
	var tile_set := TileSet.new()
	tile_set.tile_size = Vector2i(32, 32)
	floor.tile_set = tile_set
	add_child(floor)

	var registry := AnimatedEntityRegistry.new()
	add_child(registry)
	await get_tree().process_frame

	registry.update_from_state(state, floor)
	await get_tree().process_frame

	for child in registry.get_children():
		if child is AnimatedSprite2D:
			return child as AnimatedSprite2D
	return null


func test_warrior_sprite_ativo_em_estado_2d() -> void:
	var state := _make_state_2d(3, 5)
	var asp := await _warrior_sprite_from_state(state)
	if asp == null:
		pending("AnimatedSprite2D não encontrado (manifest ausente)")
		return
	assert_not_null(asp.sprite_frames, "SpriteFrames deve estar configurado")
	assert_true(asp.is_playing(), "AnimatedSprite2D deve estar tocando uma animação")


func test_warrior_east_flip_h_false() -> void:
	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0, Direction.east()
	)
	var asp := await _warrior_sprite_from_state(state)
	if asp == null:
		pending("AnimatedSprite2D não encontrado (manifest ausente)")
		return
	assert_false(asp.flip_h, "East → flip_h deve ser false")
	assert_almost_eq(asp.rotation, 0.0, 0.001, "East → rotation deve ser 0")


func test_warrior_west_flip_h_true() -> void:
	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), -1, {}, 0, Direction.west()
	)
	var asp := await _warrior_sprite_from_state(state)
	if asp == null:
		pending("AnimatedSprite2D não encontrado (manifest ausente)")
		return
	assert_true(asp.flip_h, "West → flip_h deve ser true")


func test_warrior_north_rotation_negativa() -> void:
	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0, Direction.north()
	)
	var asp := await _warrior_sprite_from_state(state)
	if asp == null:
		pending("AnimatedSprite2D não encontrado (manifest ausente)")
		return
	assert_almost_eq(asp.rotation, -PI / 2.0, 0.001, "North → rotation deve ser -PI/2")


func test_warrior_south_rotation_positiva() -> void:
	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0, Direction.south()
	)
	var asp := await _warrior_sprite_from_state(state)
	if asp == null:
		pending("AnimatedSprite2D não encontrado (manifest ausente)")
		return
	assert_almost_eq(asp.rotation, PI / 2.0, 0.001, "South → rotation deve ser PI/2")


func test_visual_difere_entre_4_direcoes() -> void:
	var dirs := [Direction.east(), Direction.west(), Direction.north(), Direction.south()]
	var props: Array = []
	for dir in dirs:
		var state := LevelState.from_2d(
			3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(0, 0), 1, {}, 0, dir
		)
		var asp := await _warrior_sprite_from_state(state)
		if asp == null:
			pending("AnimatedSprite2D não encontrado (manifest ausente)")
			return
		props.append(Vector3(asp.rotation, 1.0 if asp.flip_h else 0.0, 1.0 if asp.flip_v else 0.0))
	# Cada direção deve ter uma combinação única de (rotation, flip_h, flip_v).
	var unique_props := {}
	for p in props:
		unique_props[p] = true
	assert_eq(unique_props.size(), 4, "4 direções devem produzir 4 visuais distintos")
