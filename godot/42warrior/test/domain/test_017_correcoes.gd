extends GutTest
## T-171 (017): atacar ou atirar num cativo não conta como inimigo derrotado
## nem pontua — _attack/_shoot respeitam is_captive() como _rescue já fazia.
## T-172 (017): inimigo ranged posicionado exatamente na posição da escada
## calcula facing válido (não-zero) e dispara/causa dano ao warrior no alcance.

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


# ── T-171: cativo não é contado como inimigo ao atacar ─────────────────────


func test_attack_cativo_nao_emite_enemy_defeated() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Captive.new()}, 0)
	var result := _resolver.resolve(state, AttackAction.new(Direction.forward()))
	assert_not_null(result.state.unit_at(2), "cativo permanece após attack")
	for event: TurnEvent in result.events:
		assert_ne(
			event.kind,
			TurnEvent.Kind.ENEMY_DEFEATED,
			"attack num cativo não deve emitir ENEMY_DEFEATED"
		)


func test_shoot_cativo_nao_emite_enemy_defeated() -> void:
	# warrior em 0, cativo em 2 (dentro do alcance SHOOT_RANGE=3).
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {2: Captive.new()}, 0)
	var result := _resolver.resolve(state, ShootAction.new(Direction.forward()))
	assert_not_null(result.state.unit_at(2), "cativo permanece após shoot")
	for event: TurnEvent in result.events:
		assert_ne(
			event.kind,
			TurnEvent.Kind.ENEMY_DEFEATED,
			"shoot num cativo não deve emitir ENEMY_DEFEATED"
		)


# ── T-172: ranged na posição da escada dispara ──────────────────────────────


func test_ranged_na_escada_causa_dano() -> void:
	# Bug #3: archer em pos 7 == stairs 7 → signi(7-7)=0 → facing 0 → não dispara.
	# Fix: _facing cai para warrior_pos quando stairs dá 0.
	# _level_6 do beginner_tower: Archer@7, stairs@7, warrior entrando pela esquerda.
	var archer := Archer.new()
	var behavior := RangedBehavior.new()
	# width=9, stairs=7, warrior_pos=4 (distância 3 == attack_range do archer).
	var state := LevelState.new(9, 7, Warrior.new(), 4, 1, {7: archer}, 0)
	assert_eq(
		behavior.damage_to_warrior(state, 7, archer),
		archer.attack_power,
		"archer na posição da escada deve causar dano ao warrior no alcance"
	)


func test_ranged_fora_da_escada_continua_funcionando() -> void:
	# Regressão: o comportamento normal (não na escada) não deve ser afetado.
	var archer := Archer.new()
	var behavior := RangedBehavior.new()
	# width=10, stairs=9, archer em 3, warrior em 0 (distância 3).
	var state := LevelState.new(10, 9, Warrior.new(), 0, 1, {3: archer}, 0)
	assert_eq(
		behavior.damage_to_warrior(state, 3, archer),
		archer.attack_power,
		"archer fora da escada continua causando dano normalmente"
	)
