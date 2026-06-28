extends GutTest
## Cobre o VO Direction: relativas (FORWARD/BACKWARD) e absolutas 4-dir (N/S/E/W).

# ─── Relativas (legado — não regredir) ───────────────────────────────────────


func test_forward_tem_sinal_positivo() -> void:
	assert_eq(Direction.forward().relative_sign(), 1)


func test_backward_tem_sinal_negativo() -> void:
	assert_eq(Direction.backward().relative_sign(), -1)


func test_oposto_de_forward_e_backward() -> void:
	assert_true(Direction.forward().opposite().equals(Direction.backward()))


func test_oposto_de_backward_e_forward() -> void:
	assert_true(Direction.backward().opposite().equals(Direction.forward()))


func test_equals_distingue_direcoes() -> void:
	assert_true(Direction.forward().equals(Direction.forward()))
	assert_false(Direction.forward().equals(Direction.backward()))


# ─── Absolutas: delta 2D ─────────────────────────────────────────────────────


func test_north_delta_e_linha_menos_um() -> void:
	assert_eq(Direction.north().delta(), Vector2i(-1, 0))


func test_south_delta_e_linha_mais_um() -> void:
	assert_eq(Direction.south().delta(), Vector2i(1, 0))


func test_east_delta_e_coluna_mais_um() -> void:
	assert_eq(Direction.east().delta(), Vector2i(0, 1))


func test_west_delta_e_coluna_menos_um() -> void:
	assert_eq(Direction.west().delta(), Vector2i(0, -1))


# ─── Absolutas: pivot (sentido horário N→E→S→W→N) ────────────────────────────


func test_pivot_north_roda_para_east() -> void:
	assert_true(Direction.north().pivot().equals(Direction.east()))


func test_pivot_east_roda_para_south() -> void:
	assert_true(Direction.east().pivot().equals(Direction.south()))


func test_pivot_south_roda_para_west() -> void:
	assert_true(Direction.south().pivot().equals(Direction.west()))


func test_pivot_west_roda_para_north() -> void:
	assert_true(Direction.west().pivot().equals(Direction.north()))


func test_pivot_quatro_rotacoes_retorna_norte() -> void:
	var d := Direction.north()
	d = d.pivot()
	d = d.pivot()
	d = d.pivot()
	d = d.pivot()
	assert_true(d.equals(Direction.north()))


# ─── Absolutas: opposite ─────────────────────────────────────────────────────


func test_oposto_de_north_e_south() -> void:
	assert_true(Direction.north().opposite().equals(Direction.south()))


func test_oposto_de_south_e_north() -> void:
	assert_true(Direction.south().opposite().equals(Direction.north()))


func test_oposto_de_east_e_west() -> void:
	assert_true(Direction.east().opposite().equals(Direction.west()))


func test_oposto_de_west_e_east() -> void:
	assert_true(Direction.west().opposite().equals(Direction.east()))


# ─── Absolutas: equals ───────────────────────────────────────────────────────


func test_equals_absolutas_distingue_direcoes() -> void:
	assert_true(Direction.north().equals(Direction.north()))
	assert_false(Direction.north().equals(Direction.south()))
	assert_false(Direction.north().equals(Direction.east()))
	assert_false(Direction.north().equals(Direction.west()))
