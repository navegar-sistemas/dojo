extends GutTest
## Robustez da fronteira de execução (014): código do jogador com erro de RUNTIME
## (RF-141) ou LOOP INFINITO (RF-142) não crasha nem trava — vira no-op + reporte.
## Erro de SINTAXE (RF-140): coberto por test_player_script_runner.gd.


func _facade() -> WarriorFacade:
	return WarriorFacade.new(LevelState.new(6, 5, Warrior.new(), 1, 1, {}, 0))


func test_runtime_metodo_inexistente_nao_crasha_vira_no_op() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	warrior.metodo_que_nao_existe()
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null, "compila — o erro só aparece em runtime")
	# Se o erro de runtime crashasse o processo, o teste não chegaria à asserção.
	var action: Action = runner.play_turn(instance, _facade())
	assert_null(action, "erro de runtime aborta o turno → no-op")


func test_runtime_acesso_a_null_nao_crasha() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	var x = null
	x.alguma_coisa()
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null)
	var action: Action = runner.play_turn(instance, _facade())
	assert_null(action, "acesso a null vira no-op sem crash")


func test_loop_infinito_e_cortado_sem_travar() -> void:
	var source := """
extends RefCounted
func play_turn(warrior):
	while true:
		pass
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null)
	# Sem a guarda de iteração injetada, esta chamada penduraria a suíte para sempre.
	var action: Action = runner.play_turn(instance, _facade())
	assert_null(action, "loop infinito vira no-op")
	assert_true(runner.has_error(), "o corte do loop é reportado")


func test_while_legitimo_termina_e_age_normalmente() -> void:
	# A instrumentação NÃO pode quebrar um laço legítimo (que termina sozinho).
	var source := """
extends RefCounted
func play_turn(warrior):
	var passos = 0
	while passos < 3:
		passos += 1
	warrior.walk()
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null)
	var action: Action = runner.play_turn(instance, _facade())
	assert_true(action is WalkAction, "o laço termina e a ação seguinte é registrada")
	assert_false(runner.has_error(), "laço legítimo não dispara o corte")
