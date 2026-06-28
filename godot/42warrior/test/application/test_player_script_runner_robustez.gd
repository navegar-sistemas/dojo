extends GutTest
## Robustez da fronteira de execução (014): código do jogador com erro de RUNTIME
## (RF-141), LOOP INFINITO (RF-142), RECURSÃO INFINITA (RF-143) ou SINTAXE INVÁLIDA
## (RF-140) não crasha nem trava — vira no-op + reporte.


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


func test_recursao_infinita_direta_nao_crasha() -> void:
	# RF-143: play_turn que se chama → sem depth-guard → "Stack overflow" +
	# "Stack underflow Engine Bug" → VM corrompida → crash do app.
	# Com o depth-guard injetado, deve virar no-op + erro reportado.
	var source := """
extends RefCounted
func play_turn(warrior):
	play_turn(warrior)
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null, "recursão só aparece em runtime, compila ok")
	# Se crashasse, o GUT não chegaria à linha abaixo.
	var action: Action = runner.play_turn(instance, _facade())
	assert_null(action, "recursão infinita vira no-op")
	assert_true(runner.has_error(), "o corte de recursão é reportado")


func test_recursao_via_helper_nao_crasha() -> void:
	# Recursão indireta via função auxiliar também deve ser bloqueada.
	var source := """
extends RefCounted
func play_turn(warrior):
	_loop(warrior)
func _loop(w):
	_loop(w)
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null)
	var action: Action = runner.play_turn(instance, _facade())
	assert_null(action, "recursão via helper vira no-op")
	assert_true(runner.has_error(), "o corte de recursão via helper é reportado")


func test_funcao_legitima_com_helper_age_normalmente() -> void:
	# Funções auxiliares legítimas (não recursivas) não devem ser bloqueadas.
	var source := """
extends RefCounted
func play_turn(warrior):
	if _deve_andar(warrior):
		warrior.walk()
func _deve_andar(w):
	return w.health() > 0
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_true(instance != null)
	var action: Action = runner.play_turn(instance, _facade())
	assert_true(action is WalkAction, "helper legítimo não bloqueia a ação")
	assert_false(runner.has_error(), "helper legítimo não dispara o corte")


func test_sintaxe_invalida_vira_null_com_erro() -> void:
	# RF-140 (gap histórico): sintaxe inválida não deve crashar — compile() devolve
	# null e has_error() fica true. Esse gap deixou a 014 passar verde sem proteção.
	var source := """
extends RefCounted
func play_turn(w) walk(
"""
	var runner := PlayerScriptRunner.new()
	var instance := runner.compile(source)
	assert_null(instance, "sintaxe inválida → compile() devolve null")
	assert_true(runner.has_error(), "sintaxe inválida → has_error() true")
