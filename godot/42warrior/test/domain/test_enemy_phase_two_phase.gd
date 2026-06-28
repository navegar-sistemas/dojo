extends GutTest
## Fidelidade ao gem: a fase de inimigos decide sobre o SNAPSHOT do início do turno
## (antes da ação do warrior), não sobre o estado já mutado. Um inimigo à distância
## cuja linha estava bloqueada no início do turno não atira no mesmo turno em que o
## warrior abre a linha (matando/resgatando o bloqueador). Regressão do L8 (2 wizards
## + cativo). Tópico de chat: fidelidade-combate.

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


func test_wizard_nao_atira_no_turno_em_que_o_resgate_abre_a_linha() -> void:
	# warrior@1 (olhando p/ frente), cativo@2 bloqueia a linha do wizard@3 (dist 2, alcance 3).
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Captive.new(), 3: Wizard.new()}, 0)
	var result := _resolver.resolve(state, RescueAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior().health,
		20,
		"wizard decidiu sobre o snapshot (linha bloqueada pelo cativo) e nao atira neste turno"
	)
	assert_null(result.state.unit_at(2), "cativo foi resgatado")


func test_wizard_atira_no_turno_seguinte_com_a_linha_ja_aberta() -> void:
	# Estado pós-resgate: cativo@2 já foi removido, linha do wizard@3 ao warrior@1 está limpa.
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {3: Wizard.new()}, 1)
	var result := _resolver.resolve(state, PivotAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior().health,
		20 - 11,
		"com a linha limpa desde o inicio do turno, o wizard atira (11 de dano)"
	)


func test_um_inimigo_morto_pela_acao_do_warrior_nao_age_no_mesmo_turno() -> void:
	# warrior@1 ataca o wizard@2 (5 de dano mata os 3 HP); o wizard morto não revida.
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Wizard.new()}, 0)
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_null(result.state.unit_at(2), "wizard morre com o ataque")
	assert_eq(result.state.warrior().health, 20, "wizard morto no turno nao causa dano")
