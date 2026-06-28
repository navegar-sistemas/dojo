extends GutTest
## Cobre o PlayerScriptRunner: compila e roda o código do jogador, tolerando erros.

var _runner: PlayerScriptRunner


func before_each() -> void:
	_runner = PlayerScriptRunner.new()


func _facade() -> WarriorFacade:
	return WarriorFacade.new(LevelState.new(6, 5, Warrior.new(), 1, 1, {2: Sludge.new()}, 0))


func test_codigo_valido_produz_a_acao_escolhida() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	if warrior.feel().is_enemy():
		warrior.attack()
	else:
		warrior.walk()
"""
	var instance := _runner.compile(source)
	assert_false(_runner.has_error(), "compila sem erro")
	var action := _runner.play_turn(instance, _facade())
	assert_true(action is AttackAction, "sente o sludge à frente e ataca")


func test_codigo_que_anda_quando_vazio() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	warrior.walk()
"""
	var instance := _runner.compile(source)
	var facade := WarriorFacade.new(LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0))
	assert_true(_runner.play_turn(instance, facade) is WalkAction)


func test_erro_de_compilacao_nao_trava() -> void:
	var instance := _runner.compile("func play_turn(warrior) este codigo é inválido {{{")
	assert_null(instance)
	assert_true(_runner.has_error())


func test_sem_play_turn_e_erro() -> void:
	var instance := _runner.compile("extends RefCounted\nfunc outra():\n\tpass\n")
	assert_null(instance)
	assert_true(_runner.has_error())


func test_turno_sem_acao_e_no_op() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	var _h = warrior.health()
"""
	var instance := _runner.compile(source)
	assert_false(_runner.has_error())
	assert_null(_runner.play_turn(instance, _facade()), "não agir devolve null (no-op)")
