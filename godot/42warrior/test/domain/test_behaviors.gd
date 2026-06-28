extends GutTest
## Cobre os comportamentos de unidade isoladamente.


func _state_with(units: Dictionary, warrior_position: int) -> LevelState:
	return LevelState.new(10, 9, Warrior.new(), warrior_position, 1, units, 0)


func test_melee_ataca_so_adjacente() -> void:
	var sludge := Sludge.new()
	var behavior := MeleeBehavior.new()
	# warrior em 2, sludge em 3 (adjacente) → ataca.
	assert_eq(
		behavior.damage_to_warrior(_state_with({3: sludge}, 2), 3, sludge), sludge.attack_power
	)
	# warrior em 1, sludge em 3 (distante) → não ataca.
	assert_eq(behavior.damage_to_warrior(_state_with({3: sludge}, 1), 3, sludge), 0)


func test_ranged_ataca_dentro_do_alcance() -> void:
	var archer := Archer.new()
	var behavior := RangedBehavior.new()
	# warrior em 0, archer em 3, alcance 3 → ataca.
	assert_eq(
		behavior.damage_to_warrior(_state_with({3: archer}, 0), 3, archer), archer.attack_power
	)


func test_ranged_nao_ataca_fora_do_alcance() -> void:
	var archer := Archer.new()
	var behavior := RangedBehavior.new()
	# warrior em 0, archer em 5, alcance 3 → não ataca.
	assert_eq(behavior.damage_to_warrior(_state_with({5: archer}, 0), 5, archer), 0)


func test_ranged_bloqueado_por_unidade_no_caminho() -> void:
	var archer := Archer.new()
	var behavior := RangedBehavior.new()
	# warrior em 0, sludge em 1 (bloqueia), archer em 3 → não acerta.
	var state := _state_with({1: Sludge.new(), 3: archer}, 0)
	assert_eq(behavior.damage_to_warrior(state, 3, archer), 0)


func test_captive_e_inerte() -> void:
	var captive := Captive.new()
	assert_true(captive.create_behavior() is InertBehavior)
	assert_eq(
		captive.create_behavior().damage_to_warrior(_state_with({2: captive}, 1), 2, captive), 0
	)
