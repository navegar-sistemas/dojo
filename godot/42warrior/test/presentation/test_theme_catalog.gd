class_name TestThemeCatalog
extends GutTest
## Testes do ThemeCatalog — mapeamento evento→mensagem Unix/42 (T-154, RF-154).


func test_message_chave_conhecida() -> void:
	var msg := ThemeCatalog.message("victory")
	assert_false(msg.is_empty(), "victory: mensagem não vazia")
	assert_true(msg.contains("exit 0"), "victory: deve conter 'exit 0'")


func test_message_defeat_contem_sigkill() -> void:
	var msg := ThemeCatalog.message("defeat")
	assert_true(msg.contains("SIGKILL"), "defeat: deve conter 'SIGKILL'")


func test_message_error_compile() -> void:
	var msg := ThemeCatalog.message("error_compile")
	assert_false(msg.is_empty(), "error_compile: mensagem não vazia")


func test_message_error_runtime_contem_segfault() -> void:
	var msg := ThemeCatalog.message("error_runtime")
	assert_true(msg.contains("segfault"), "error_runtime: deve conter 'segfault'")


func test_message_chave_desconhecida_retorna_a_chave() -> void:
	var msg := ThemeCatalog.message("chave_inexistente_xyz")
	assert_eq(msg, "chave_inexistente_xyz", "chave desconhecida deve retornar a própria chave")


func test_message_floor_heading_com_args() -> void:
	var msg := ThemeCatalog.message("floor_heading", [3])
	assert_true(msg.contains("03"), "floor_heading: deve conter '03' formatado")


func test_corruption_for_floor_andar_1() -> void:
	var v := ThemeCatalog.corruption_for_floor(1)
	assert_gt(v, 0.0, "andar 1: corrupção > 0")
	assert_lt(v, 0.5, "andar 1: corrupção baixa")


func test_corruption_for_floor_andar_9_maximo() -> void:
	var v := ThemeCatalog.corruption_for_floor(9)
	assert_almost_eq(v, 1.0, 0.001, "andar 9: corrupção máxima")


func test_corruption_for_floor_fora_dos_limites() -> void:
	assert_almost_eq(ThemeCatalog.corruption_for_floor(0), 0.0, 0.001)
	assert_almost_eq(ThemeCatalog.corruption_for_floor(10), 0.0, 0.001)


func test_corruption_cresce_com_andar() -> void:
	var prev := ThemeCatalog.corruption_for_floor(1)
	for i: int in range(2, 10):
		var cur := ThemeCatalog.corruption_for_floor(i)
		assert_gte(cur, prev, "andar %d deve ter corrupção >= andar %d" % [i, i - 1])
		prev = cur
