extends GutTest
## Robustez da fronteira de execução (014): código do jogador com erro de RUNTIME
## (método inexistente, acesso a null) NÃO crasha o jogo — o turno vira no-op (RF-141).
## Erro de SINTAXE: coberto por test_player_script_runner.gd (RF-140).
## Loop/recursão infinita (RF-142): NÃO coberto — sem mecanismo seguro em GDScript
## single-thread (síncrono trava; Thread crasha com Bus error). Ver doc do runner.


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
