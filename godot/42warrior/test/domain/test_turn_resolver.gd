extends GutTest
## Cobre o TurnResolver: determinismo, efeitos das ações, vitória/derrota e a
## reação dos inimigos.

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


func _empty_state(warrior_position: int, width := 8, stairs := 7) -> LevelState:
	return LevelState.new(width, stairs, Warrior.new(), warrior_position, 1, {}, 0)


# ── Determinismo e despacho ──────────────────────────────────────────────────


func test_determinismo_mesma_entrada_mesmo_resultado() -> void:
	var state := _empty_state(1)
	var a := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	var b := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(a.state.warrior_position(), b.state.warrior_position())
	assert_eq(a.outcome, b.outcome)
	assert_eq(a.events.size(), b.events.size())


func test_acao_desconhecida_ou_nula_e_no_op() -> void:
	var state := _empty_state(1)
	var result := _resolver.resolve(state, Action.new())
	assert_eq(result.state.warrior_position(), 1, "estado não muda além do turno")
	assert_eq(result.outcome, TurnResult.Outcome.ONGOING)


# ── Efeitos das ações (T-009) ────────────────────────────────────────────────


func test_walk_avanca_em_espaco_vazio() -> void:
	var result := _resolver.resolve(_empty_state(1), WalkAction.new(Direction.forward()))
	assert_eq(result.state.warrior_position(), 2)


func test_walk_bloqueado_por_parede_nao_move() -> void:
	# warrior em 0, facing +1, walk backward → parede em -1.
	var result := _resolver.resolve(_empty_state(0), WalkAction.new(Direction.backward()))
	assert_eq(result.state.warrior_position(), 0)


func test_attack_frente_causa_dano_cheio() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Sludge.new()}, 0)
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(2).health, 12 - 5, "sludge perde attack_power do warrior")


func test_attack_para_tras_causa_dano_reduzido() -> void:
	# sludge atrás (posição 0), warrior em 1 facing +1 → backward.
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {0: Sludge.new()}, 0)
	var result := _resolver.resolve(state, AttackAction.new(Direction.backward()))
	assert_eq(result.state.unit_at(0).health, 12 - 3, "dano para trás é ceil(5/2)=3 (ruby-warrior)")


func test_attack_que_mata_remove_o_inimigo() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Wizard.new()}, 0)
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_null(result.state.unit_at(2), "wizard (3 HP) morre com 5 de dano")


func test_rest_cura_dez_porcento_sem_passar_do_maximo() -> void:
	var ferido := Warrior.new(15)
	var state := LevelState.new(8, 7, ferido, 1, 1, {}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 17, "15 + 2 (10% de 20)")


func test_rest_no_maximo_nao_ultrapassa() -> void:
	var result := _resolver.resolve(_empty_state(1), RestAction.new())
	assert_eq(result.state.warrior().health, 20)


# ── Vitória e derrota (T-011) ────────────────────────────────────────────────


func test_vitoria_ao_alcancar_a_escada() -> void:
	# warrior em 6, escada em 7 → walk forward chega na escada.
	var result := _resolver.resolve(_empty_state(6), WalkAction.new(Direction.forward()))
	assert_eq(result.outcome, TurnResult.Outcome.VICTORY)


func test_derrota_quando_saude_zera() -> void:
	# warrior com 3 HP, dois sludges adjacentes? Use wizard adjacente (11 dano).
	var fraco := Warrior.new(3)
	var state := LevelState.new(8, 7, fraco, 1, 1, {2: Wizard.new()}, 0)
	# warrior descansa; wizard adjacente ataca 11 → morre.
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.outcome, TurnResult.Outcome.DEFEAT)


# ── Reação dos inimigos (T-013) ──────────────────────────────────────────────


func test_inimigo_adjacente_causa_dano_apos_acao() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Sludge.new()}, 0)
	# warrior descansa (não ataca) → sludge adjacente bate 3.
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 20 - 3)


func test_cativo_nao_causa_dano() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Captive.new()}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 20)


func test_archer_acerta_a_distancia_na_enemy_phase() -> void:
	# warrior em 0, archer em 2 (distância 2, dentro do alcance 3) → acerta.
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {2: Archer.new()}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 20 - 3, "archer atira de longe (dist 2)")


func test_archer_bloqueado_por_unidade_no_caminho_nao_acerta() -> void:
	# warrior em 0, cativo em 1 (bloqueia a linha sem atacar), archer em 3 → não acerta.
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {1: Captive.new(), 3: Archer.new()}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 20, "linha bloqueada pelo cativo")


func test_ranged_nao_atira_pelas_costas() -> void:
	# Fidelidade ao gem: o inimigo à distância encara a entrada do warrior (lado oposto à
	# escada) e só atira nessa direção. archer@3 encara a entrada (escada@7); warrior@5 está
	# do lado da escada → atrás do facing do archer → não leva tiro.
	var state := LevelState.new(8, 7, Warrior.new(), 5, 1, {3: Archer.new()}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(
		result.state.warrior().health, 20, "archer nao atira pelas costas (warrior atras do facing)"
	)


func test_ranged_atira_na_direcao_do_facing() -> void:
	# mesmo archer@3 (encara a entrada), warrior@1 do lado da entrada → na direção do facing → atira.
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {3: Archer.new()}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 20 - 3, "archer atira no warrior à sua frente")


func test_turno_e_incrementado() -> void:
	var result := _resolver.resolve(_empty_state(1), RestAction.new())
	assert_eq(result.state.turn(), 1)
