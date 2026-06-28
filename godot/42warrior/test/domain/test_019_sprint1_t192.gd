class_name TestGlitchExploits
extends GutTest
## T-192 (019 Sprint 1) — GlitchExploits: 4 mecânicas de domínio na janela de glitch.
## DoD: ≥4 testes (um por mecânica); efeito só na janela; comportamento normal fora;
## determinístico (mesmo seed+turno → mesmo resultado); 0-RNG; aditivo.
##
## GlitchRuleModel: _PERIOD=7, _DURATION=3. seed=0, turn=0..2 → janela aberta;
## turn=3..6 → fechada.

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


func _make_warrior(health: int = 20) -> Warrior:
	return Warrior.new(health)


## Estado 1D simples (sem glitch) — largura 10, escada em 9.
func _make_state(warrior_pos: int, turn: int, units: Dictionary = {}) -> LevelState:
	return LevelState.new(10, 9, _make_warrior(), warrior_pos, 1, units, turn)


## Estado 1D com glitch ativo. seed=0: janela aberta em turn 0,1,2; fechada em 3,4,5,6.
func _make_glitch_state(warrior_pos: int, turn: int, units: Dictionary = {}) -> LevelState:
	return _make_state(warrior_pos, turn, units).with_glitch_model(GlitchRuleModel.new(), 0)


# ── buffer-overflow → dano dobrado (RF-192) ─────────────────────────────────


func test_buffer_overflow_attack_dano_dobrado_na_janela() -> void:
	# seed=0, turn=0 → janela aberta; Sludge=12HP, power=5 → com glitch=10
	var state := _make_glitch_state(1, 0, {2: Sludge.new()})
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_eq(
		result.state.unit_at(2).health,
		2,
		"buffer-overflow: attack! na janela dobra o dano (12-10=2)"
	)


func test_buffer_overflow_attack_normal_fora_da_janela() -> void:
	# seed=0, turn=3 → janela fechada; Sludge=12HP, power=5 normal
	var state := _make_glitch_state(1, 3, {2: Sludge.new()})
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(2).health, 7, "fora da janela: dano normal (12-5=7)")


func test_buffer_overflow_sem_model_dano_normal() -> void:
	# Sem GlitchRuleModel: comportamento base preservado (aditivo)
	var state := _make_state(1, 0, {2: Sludge.new()})
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(2).health, 7, "sem model: dano normal (legado preservado)")


func test_buffer_overflow_determinismo() -> void:
	# Mesmo seed+turno → mesmo dano em duas execuções independentes
	var state := _make_glitch_state(1, 0, {2: Sludge.new()})
	var r1 := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	var state2 := _make_glitch_state(1, 0, {2: Sludge.new()})
	var r2 := _resolver.resolve(state2, AttackAction.new(Direction.forward()))
	assert_eq(
		r1.state.unit_at(2).health,
		r2.state.unit_at(2).health,
		"determinismo: mesmo seed+turno → mesmo dano restante"
	)


# ── memory-leak → cura dobrada (RF-194) ─────────────────────────────────────


func test_memory_leak_rest_cura_dobrada_na_janela() -> void:
	# warrior HP=15, max=20; heal=10% de 20=2; com glitch=4 → HP=19
	var warrior := Warrior.new(15)
	var state := LevelState.new(10, 9, warrior, 1, 1, {}, 0).with_glitch_model(
		GlitchRuleModel.new(), 0
	)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(
		result.state.warrior().health, 19, "memory-leak: rest! na janela cura o dobro (15+4=19)"
	)


func test_memory_leak_rest_normal_fora_da_janela() -> void:
	# seed=0, turn=3 → janela fechada; cura normal=2
	var warrior := Warrior.new(15)
	var state := LevelState.new(10, 9, warrior, 1, 1, {}, 3).with_glitch_model(
		GlitchRuleModel.new(), 0
	)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 17, "fora da janela: cura normal (15+2=17)")


func test_memory_leak_cura_dobrada_nao_ultrapassa_max() -> void:
	# warrior HP=19, max=20; heal=2 normal, com glitch=4; min(20, 19+4)=20
	var warrior := Warrior.new(19)
	var state := LevelState.new(10, 9, warrior, 1, 1, {}, 0).with_glitch_model(
		GlitchRuleModel.new(), 0
	)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(
		result.state.warrior().health, 20, "memory-leak: cura dobrada respeita o teto de max_health"
	)


func test_memory_leak_sem_model_cura_normal() -> void:
	var warrior := Warrior.new(15)
	var state := LevelState.new(10, 9, warrior, 1, 1, {}, 0)
	var result := _resolver.resolve(state, RestAction.new())
	assert_eq(result.state.warrior().health, 17, "sem model: cura normal (legado preservado)")


# ── no-clip seedado → atravessa parede corrompida (RF-191) ───────────────────


func test_noclip_walk_atravessa_corrupted_wall_na_janela() -> void:
	# warrior em 3, corrupted_wall em 4, pos 5 livre; seed=0, turn=0 → janela aberta
	# walk!(forward) → target=4 (corrompida), além=5 (empty) → warrior vai para 5
	var state := _make_glitch_state(3, 0).with_corrupted_walls([4])
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior_position(),
		5,
		"no-clip: walk! atravessa parede corrompida (3→5 saltando pos 4)"
	)


func test_noclip_walk_bloqueado_por_corrupted_wall_fora_da_janela() -> void:
	# seed=0, turn=3 → janela fechada → walk! bloqueado
	var state := _make_glitch_state(3, 3).with_corrupted_walls([4])
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior_position(), 3, "fora da janela: corrupted_wall bloqueia normalmente"
	)


func test_noclip_sem_model_corrupted_wall_bloqueia() -> void:
	# Sem glitch model, corrupted_wall comporta-se como parede normal (aditivo)
	var state := _make_state(3, 0).with_corrupted_walls([4])
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(result.state.warrior_position(), 3, "sem model: corrupted_wall bloqueia (legado)")


func test_noclip_bloqueado_quando_alem_e_parede() -> void:
	# corrupted_wall em 4, parede (borda) em 5 (width=5); janela aberta
	# beyond seria position 5 que é parede → warrior não pode pular
	var warrior := _make_warrior()
	var state := (
		LevelState
		. new(5, 4, warrior, 3, 1, {}, 0)
		. with_glitch_model(GlitchRuleModel.new(), 0)
		. with_corrupted_walls([4])
	)
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior_position(),
		3,
		"no-clip: bloqueado se além da parede corrompida não há espaço livre"
	)


# ── inimigo intangível piscante → atravessar a favor (RF-195) ───────────────


func test_intangivel_walk_atravessa_inimigo_na_janela() -> void:
	# warrior em 3, Sludge em 4, pos 5 livre; seed=0, turn=0 → janela aberta
	# walk!(forward) → target=4 (inimigo intangível), além=5 (empty) → warrior vai para 5
	var state := _make_glitch_state(3, 0, {4: Sludge.new()})
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior_position(),
		5,
		"intangível: walk! atravessa inimigo intangível na janela (3→5)"
	)


func test_intangivel_inimigo_permanece_apos_atravessar() -> void:
	# O Sludge permanece na posição 4 após o warrior passar por ele
	var state := _make_glitch_state(3, 0, {4: Sludge.new()})
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_not_null(
		result.state.unit_at(4), "inimigo permanece em sua posição após ser atravessado"
	)


func test_intangivel_walk_bloqueado_por_inimigo_fora_da_janela() -> void:
	# seed=0, turn=3 → janela fechada → walk! bloqueado pelo inimigo
	var state := _make_glitch_state(3, 3, {4: Sludge.new()})
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(result.state.warrior_position(), 3, "fora da janela: inimigo bloqueia normalmente")


func test_intangivel_sem_model_inimigo_bloqueia() -> void:
	var state := _make_state(3, 0, {4: Sludge.new()})
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(result.state.warrior_position(), 3, "sem model: inimigo bloqueia (legado preservado)")


func test_intangivel_bloqueado_quando_alem_e_parede() -> void:
	# inimigo em 4, parede (borda) em 5 (width=5); janela aberta → warrior não pode pular
	var warrior := _make_warrior()
	var state := LevelState.new(5, 4, warrior, 3, 1, {4: Sludge.new()}, 0).with_glitch_model(
		GlitchRuleModel.new(), 0
	)
	var result := _resolver.resolve(state, WalkAction.new(Direction.forward()))
	assert_eq(
		result.state.warrior_position(),
		3,
		"intangível: bloqueado se além do inimigo não há espaço livre"
	)
