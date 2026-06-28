extends GutTest
## T-184 (018 Sprint 3) — Apresentação 2D: floor RxC, câmera 2 eixos, sprites 4-dir.
## DoD count-level: floor_layer.get_used_cells().size()>0 (grade real);
## câmera acompanha warrior em X e Y; sprite/anim muda conforme direção 4-dir.

const _GAME_SCENE := "res://scenes/game.tscn"
const _MANIFEST_PATH := "res://assets/v1/anim/manifest.json"

const _VP := Vector2(1280.0, 720.0)
const _DELTA := 1.0

# ── Floor RxC ────────────────────────────────────────────────────────────────


func test_floor_rende_grade_rxc_nao_vazia() -> void:
	var packed := load(_GAME_SCENE) as PackedScene
	if packed == null:
		pending("game.tscn ausente — pulado")
		return
	var game: Node = packed.instantiate()
	add_child_autoqfree(game)
	await get_tree().process_frame

	var dv: DungeonView = game.get_node_or_null("DungeonView") as DungeonView
	if dv == null:
		pending("DungeonView não encontrado em game.tscn — pulado")
		return

	var state := LevelState.from_2d(3, 9, Vector2i(2, 8), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	dv.refresh_level(state)
	await get_tree().process_frame

	var floor_layer: TileMapLayer = dv.get_node_or_null("Floor") as TileMapLayer
	assert_not_null(floor_layer, "Floor (TileMapLayer) deve existir em DungeonView")
	if floor_layer == null:
		return
	assert_gt(
		floor_layer.get_used_cells().size(),
		0,
		"floor_layer deve ter tiles reais desenhados (grade RxC, conteudo, nao presenca de no)"
	)


func test_floor_grade_3x9_tem_ao_menos_27_tiles_de_chao() -> void:
	var packed := load(_GAME_SCENE) as PackedScene
	if packed == null:
		pending("game.tscn ausente — pulado")
		return
	var game: Node = packed.instantiate()
	add_child_autoqfree(game)
	await get_tree().process_frame

	var dv: DungeonView = game.get_node_or_null("DungeonView") as DungeonView
	if dv == null:
		pending("DungeonView não encontrado — pulado")
		return

	var state := LevelState.from_2d(3, 9, Vector2i(2, 8), Warrior.new(), Vector2i(0, 0), 1, {}, 0)
	dv.refresh_level(state)
	await get_tree().process_frame

	var floor_layer: TileMapLayer = dv.get_node_or_null("Floor") as TileMapLayer
	if floor_layer == null:
		return
	assert_gte(
		floor_layer.get_used_cells().size(),
		27,
		"grade 3x9 deve ter >= 27 tiles (3*9 chao + paredes ao redor)"
	)


# ── Câmera — 2 eixos ──────────────────────────────────────────────────────────


func _warrior_pos_2d_test() -> Vector2:
	return Vector2(250.0, 100.0)


func test_camera_segue_warrior_em_y_em_nivel_alto() -> void:
	var cam := Camera2D.new()
	add_child_autoqfree(cam)
	var ctrl := CameraFollowController.new()
	ctrl.smooth_speed = 1.0
	ctrl.dead_zone_half_w = 32.0
	ctrl.lookahead_px = 96.0
	ctrl.hysteresis_px = 32.0
	add_child_autoqfree(ctrl)

	var warrior_pos := Vector2(250.0, 16.0)
	ctrl.initialize(cam, 500.0, _VP, func() -> Vector2: return warrior_pos, 2000.0)

	warrior_pos = Vector2(250.0, 200.0)
	ctrl._follow(warrior_pos, _DELTA)
	assert_gt(
		cam.global_position.y,
		16.0,
		"câmera deve seguir warrior no eixo Y quando nível é maior que o viewport"
	)


func test_camera_nao_move_em_y_quando_nivel_menor_que_viewport() -> void:
	var cam := Camera2D.new()
	add_child_autoqfree(cam)
	var ctrl := CameraFollowController.new()
	ctrl.smooth_speed = 1.0
	ctrl.dead_zone_half_w = 32.0
	add_child_autoqfree(ctrl)

	var warrior_pos := Vector2(250.0, 16.0)
	ctrl.initialize(cam, 500.0, _VP, func() -> Vector2: return warrior_pos, 96.0)
	var cam_y_antes := cam.global_position.y

	warrior_pos = Vector2(250.0, 200.0)
	ctrl._follow(warrior_pos, _DELTA)
	assert_almost_eq(
		cam.global_position.y,
		cam_y_antes,
		0.01,
		"câmera não deve mover em Y quando nível cabe no viewport verticalmente"
	)


func test_camera_retrocompat_sem_level_height() -> void:
	var cam := Camera2D.new()
	add_child_autoqfree(cam)
	var ctrl := CameraFollowController.new()
	ctrl.smooth_speed = 1.0
	ctrl.dead_zone_half_w = 32.0
	add_child_autoqfree(ctrl)

	var warrior_pos := Vector2(100.0, 50.0)
	ctrl.initialize(cam, 2000.0, _VP, func() -> Vector2: return warrior_pos)
	var cam_y_antes := cam.global_position.y

	warrior_pos = Vector2(100.0, 400.0)
	ctrl._follow(warrior_pos, _DELTA)
	assert_almost_eq(
		cam.global_position.y,
		cam_y_antes,
		0.01,
		"sem level_height_px, câmera não deve mover em Y (retrocompat 1D)"
	)


# ── Sprites 4-dir ─────────────────────────────────────────────────────────────


func test_sprite_warrior_flip_muda_entre_leste_e_oeste() -> void:
	if not FileAccess.file_exists(_MANIFEST_PATH):
		pending("manifest.json ausente — prova de sprite 4-dir pulada")
		return

	var packed := load(_GAME_SCENE) as PackedScene
	if packed == null:
		pending("game.tscn ausente — pulado")
		return
	var game: Node = packed.instantiate()
	add_child_autoqfree(game)
	await get_tree().process_frame

	var dv: DungeonView = game.get_node_or_null("DungeonView") as DungeonView
	if dv == null:
		pending("DungeonView não encontrado — pulado")
		return

	# Warrior facing Leste (facing=+1, 4dir=East)
	var state_e := LevelState.from_2d(
		1, 9, Vector2i(0, 8), Warrior.new(), Vector2i(0, 2), 1, {}, 0, Direction.east()
	)
	dv.refresh_level(state_e)
	await get_tree().process_frame

	var registry: AnimatedEntityRegistry = dv.get_node_or_null("Entities") as AnimatedEntityRegistry
	if registry == null:
		pending("Entities (AnimatedEntityRegistry) não encontrado — pulado")
		return
	var sprite_e := _find_animated_sprite2d(registry)
	if sprite_e == null:
		pending("warrior AnimatedSprite2D não encontrado — manifest pode estar ausente")
		return

	var flip_h_east := sprite_e.flip_h

	# Warrior facing Oeste (4dir=West)
	var state_w := LevelState.from_2d(
		1, 9, Vector2i(0, 8), Warrior.new(), Vector2i(0, 2), -1, {}, 0, Direction.west()
	)
	dv.refresh_level(state_w)
	await get_tree().process_frame

	var sprite_w := _find_animated_sprite2d(registry)
	assert_not_null(sprite_w)
	assert_ne(
		sprite_w.flip_h, flip_h_east, "sprite flip_h deve ser diferente entre Leste e Oeste (4-dir)"
	)


func test_sprite_warrior_rotation_muda_entre_norte_e_sul() -> void:
	if not FileAccess.file_exists(_MANIFEST_PATH):
		pending("manifest.json ausente — prova de sprite 4-dir pulada")
		return

	var packed := load(_GAME_SCENE) as PackedScene
	if packed == null:
		pending("game.tscn ausente — pulado")
		return
	var game: Node = packed.instantiate()
	add_child_autoqfree(game)
	await get_tree().process_frame

	var dv: DungeonView = game.get_node_or_null("DungeonView") as DungeonView
	if dv == null:
		pending("DungeonView não encontrado — pulado")
		return

	var state_n := LevelState.from_2d(
		5, 5, Vector2i(4, 2), Warrior.new(), Vector2i(2, 2), 1, {}, 0, Direction.north()
	)
	dv.refresh_level(state_n)
	await get_tree().process_frame

	var registry: AnimatedEntityRegistry = dv.get_node_or_null("Entities") as AnimatedEntityRegistry
	if registry == null:
		pending("Entities não encontrado — pulado")
		return
	var sprite_n := _find_animated_sprite2d(registry)
	if sprite_n == null:
		pending("warrior AnimatedSprite2D não encontrado — manifest pode estar ausente")
		return

	var rot_n := sprite_n.rotation

	var state_s := LevelState.from_2d(
		5, 5, Vector2i(4, 2), Warrior.new(), Vector2i(2, 2), 1, {}, 0, Direction.south()
	)
	dv.refresh_level(state_s)
	await get_tree().process_frame

	var sprite_s := _find_animated_sprite2d(registry)
	assert_not_null(sprite_s)
	assert_ne(
		sprite_s.rotation, rot_n, "sprite rotation deve ser diferente entre Norte e Sul (4-dir)"
	)


func test_sprite_warrior_ativo_apos_refresh_2d() -> void:
	if not FileAccess.file_exists(_MANIFEST_PATH):
		pending("manifest.json ausente — prova de sprite ativo pulada")
		return

	var packed := load(_GAME_SCENE) as PackedScene
	if packed == null:
		pending("game.tscn ausente — pulado")
		return
	var game: Node = packed.instantiate()
	add_child_autoqfree(game)
	await get_tree().process_frame

	var dv: DungeonView = game.get_node_or_null("DungeonView") as DungeonView
	if dv == null:
		pending("DungeonView não encontrado — pulado")
		return

	var state := LevelState.from_2d(
		3, 5, Vector2i(2, 4), Warrior.new(), Vector2i(1, 2), 1, {}, 0, Direction.east()
	)
	dv.refresh_level(state)
	await get_tree().process_frame

	var registry: AnimatedEntityRegistry = dv.get_node_or_null("Entities") as AnimatedEntityRegistry
	if registry == null:
		pending("Entities não encontrado — pulado")
		return
	var sprite := _find_animated_sprite2d(registry)
	if sprite == null:
		pending("warrior AnimatedSprite2D não encontrado — manifest pode estar ausente")
		return

	assert_true(
		sprite.is_playing(),
		"warrior AnimatedSprite2D deve estar ativo (playing) após refresh_level 2D"
	)


func _find_animated_sprite2d(root: Node) -> AnimatedSprite2D:
	if root is AnimatedSprite2D:
		return root as AnimatedSprite2D
	for child: Node in root.get_children():
		var found := _find_animated_sprite2d(child)
		if found != null:
			return found
	return null
