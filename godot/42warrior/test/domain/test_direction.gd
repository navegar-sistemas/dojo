extends GutTest
## Cobre o VO Direction: sinal relativo e direção oposta.


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
