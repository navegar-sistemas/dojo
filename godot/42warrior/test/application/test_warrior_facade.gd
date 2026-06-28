extends GutTest
## Cobre a WarriorFacade: 1ª ação vence, sentidos delegam, isolamento.


func _facade() -> WarriorFacade:
	# warrior em 1 (facing +1), sludge em 2, escada em 5.
	return WarriorFacade.new(LevelState.new(6, 5, Warrior.new(), 1, 1, {2: Sludge.new()}, 0))


func test_primeira_acao_vence() -> void:
	var facade := _facade()
	facade.walk(Direction.forward())
	facade.attack(Direction.forward())
	assert_true(facade.chosen_action() is WalkAction, "a 1ª ação registrada prevalece")


func test_sem_acao_devolve_null() -> void:
	assert_null(_facade().chosen_action())


func test_sentidos_delegam_e_nao_gastam_turno() -> void:
	var facade := _facade()
	assert_true(facade.feel(Direction.forward()).is_enemy(), "sente o sludge à frente")
	assert_eq(facade.health(), 20)
	assert_true(facade.direction_of_stairs().equals(Direction.forward()))
	assert_null(facade.chosen_action(), "consultar não registra ação")


func test_direction_of_usa_a_posicao_do_space() -> void:
	var facade := _facade()
	var spaces := facade.listen()
	assert_eq(spaces.size(), 1)
	assert_true(facade.direction_of(spaces[0]).equals(Direction.forward()))


func test_superficie_publica_tem_so_a_api() -> void:
	# A superfície pública = sentidos + ações + chosen_action; nada de LevelState/units.
	var esperado := [
		"feel",
		"look",
		"listen",
		"health",
		"direction_of_stairs",
		"direction_of",
		"walk",
		"attack",
		"rest",
		"rescue",
		"pivot",
		"shoot",
		"chosen_action",
	]
	var facade := _facade()
	var publicos: Array = []
	for m in facade.get_method_list():
		var nome: String = m.name
		if not nome.begins_with("_") and not nome.begins_with("@"):
			publicos.append(nome)
	# Todo método público da API esperada existe; e nenhum vaza estado do mundo.
	for nome in esperado:
		assert_true(publicos.has(nome), "expõe %s" % nome)
	# Não expõe acessos ao mundo:
	for proibido in ["unit_at", "space_at", "warrior", "with_warrior", "_chosen_action"]:
		assert_false(publicos.has(proibido), "não vaza %s" % proibido)
