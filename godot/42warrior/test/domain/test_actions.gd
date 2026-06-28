extends GutTest
## Cobre os objetos de comando Action (tipo e direção).


func test_walk_carrega_direcao() -> void:
	var action := WalkAction.new(Direction.forward())
	assert_true(action is WalkAction)
	assert_true(action.direction.equals(Direction.forward()))


func test_attack_carrega_direcao() -> void:
	var action := AttackAction.new(Direction.backward())
	assert_true(action is AttackAction)
	assert_true(action.direction.equals(Direction.backward()))


func test_rest_nao_tem_direcao() -> void:
	assert_true(RestAction.new() is RestAction)


func test_actions_sao_subtipos_de_action() -> void:
	assert_true(WalkAction.new(Direction.forward()) is Action)
	assert_true(AttackAction.new(Direction.forward()) is Action)
	assert_true(RestAction.new() is Action)
