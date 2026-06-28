extends GutTest
## Cobre CameraFollowController: acompanhamento por frame, dead-zone, lookahead
## com histerese, limites de Camera2D e modo estático-centrado.

const VIEWPORT := Vector2(1280.0, 720.0)
const LEVEL_W_LARGE := 2000.0  # maior que viewport → modo dinâmico
const LEVEL_W_SMALL := 800.0  # cabe no viewport → modo estático
const DELTA := 1.0  # forçar lerp total (delta * smooth_speed = 1.0 * 1.0)

var _ctrl: CameraFollowController
var _cam: Camera2D
var _warrior_pos: Vector2


func before_each() -> void:
	_warrior_pos = Vector2.ZERO
	_cam = Camera2D.new()
	add_child(_cam)
	_ctrl = CameraFollowController.new()
	_ctrl.smooth_speed = 1.0
	_ctrl.dead_zone_half_w = 32.0
	_ctrl.lookahead_px = 96.0
	_ctrl.hysteresis_px = 32.0
	add_child(_ctrl)


func after_each() -> void:
	remove_child(_ctrl)
	_ctrl.free()
	remove_child(_cam)
	_cam.free()


func _get_pos() -> Vector2:
	return _warrior_pos


# ── T-110: acompanhamento contínuo por frame ──────────────────────────────────


func test_target_position_reflete_warrior_apos_follow() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	_warrior_pos = Vector2(200.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_eq(_ctrl.target_position.x, 200.0, "target_position deve acompanhar o sprite")


func test_camera_move_quando_warrior_sai_da_dead_zone() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	var cam_x_antes := _cam.global_position.x
	# Deslocar warrior além da dead_zone (>32px)
	_warrior_pos = Vector2(cam_x_antes + 80.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_gt(
		_cam.global_position.x, cam_x_antes, "câmera deve se mover quando warrior sai da dead-zone"
	)


func test_camera_nao_move_dentro_da_dead_zone() -> void:
	_warrior_pos = Vector2(500.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	var cam_x_antes := _cam.global_position.x
	# Deslocar warrior dentro da dead_zone (<32px)
	_warrior_pos = Vector2(cam_x_antes + 10.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_almost_eq(
		_cam.global_position.x,
		cam_x_antes,
		0.01,
		"câmera não deve se mover enquanto warrior está na dead-zone"
	)


# ── T-111: lookahead com histerese ───────────────────────────────────────────


func test_lookahead_dir_positivo_apos_deslocamento_acima_de_histerese() -> void:
	_warrior_pos = Vector2(300.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	_warrior_pos = Vector2(300.0 + 50.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_eq(_ctrl.current_lookahead_dir, 1.0, "lookahead deve apontar para direita")


func test_lookahead_dir_nao_muda_abaixo_de_histerese() -> void:
	_warrior_pos = Vector2(300.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	_warrior_pos = Vector2(300.0 + 50.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	# Inverter menos que a histerese — direção não deve mudar
	_warrior_pos = Vector2(300.0 + 50.0 - 20.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_eq(
		_ctrl.current_lookahead_dir,
		1.0,
		"lookahead não deve inverter com deslocamento abaixo de hysteresis_px"
	)


func test_lookahead_dir_inverte_apos_deslocamento_suficiente() -> void:
	_warrior_pos = Vector2(300.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	_warrior_pos = Vector2(300.0 + 50.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	# Inverter com mais de hysteresis_px (32px)
	_warrior_pos = Vector2(300.0 + 50.0 - 50.0, 0.0)
	_ctrl._follow(_warrior_pos, DELTA)
	assert_eq(
		_ctrl.current_lookahead_dir,
		-1.0,
		"lookahead deve inverter após deslocamento maior que hysteresis_px"
	)


# ── T-112: zoom 1:1 e limites da Camera2D ────────────────────────────────────


func test_zoom_e_1_a_1_em_nivel_grande() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	assert_eq(_cam.zoom, Vector2.ONE, "zoom deve ser 1:1 constante")


func test_zoom_e_1_a_1_em_nivel_pequeno() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_SMALL, VIEWPORT, _get_pos)
	assert_eq(_cam.zoom, Vector2.ONE, "zoom 1:1 também no nível pequeno")


func test_limit_right_configurado_com_largura_do_nivel() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	assert_eq(_cam.limit_right, int(LEVEL_W_LARGE), "limit_right deve igualar a largura do nível")


func test_limit_left_e_zero() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	assert_eq(_cam.limit_left, 0, "limit_left deve ser 0")


# ── T-113: modo estático para nível que cabe no viewport ─────────────────────


func test_modo_estatico_centra_camera_no_nivel() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_SMALL, VIEWPORT, _get_pos)
	assert_almost_eq(
		_cam.global_position.x,
		LEVEL_W_SMALL * 0.5,
		0.01,
		"câmera deve ser centralizada no nível em modo estático"
	)


func test_camera_nao_segue_warrior_em_modo_estatico() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_SMALL, VIEWPORT, _get_pos)
	var cam_x := _cam.global_position.x
	# Atualizar posição e acionar _process (que tem o guard de _static_mode)
	_warrior_pos = Vector2(600.0, 0.0)
	_ctrl._process(DELTA)
	assert_almost_eq(
		_cam.global_position.x,
		cam_x,
		0.01,
		"câmera deve permanecer estática quando nível cabe no viewport"
	)


func test_modo_dinamico_ativo_em_nivel_maior_que_viewport() -> void:
	_warrior_pos = Vector2(100.0, 0.0)
	_ctrl.initialize(_cam, LEVEL_W_LARGE, VIEWPORT, _get_pos)
	var cam_x_antes := _cam.global_position.x
	_warrior_pos = Vector2(cam_x_antes + 100.0, 0.0)
	_ctrl._process(DELTA)
	assert_gt(
		_cam.global_position.x,
		cam_x_antes,
		"câmera deve seguir warrior quando nível excede o viewport"
	)
