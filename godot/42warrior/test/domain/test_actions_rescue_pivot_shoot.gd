extends GutTest
## Cobre os comandos rescue/pivot/shoot (T-015) e seus efeitos no resolver (T-016).

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


# ── T-015: objetos de comando ────────────────────────────────────────────────


func test_comandos_carregam_tipo_e_direcao() -> void:
	assert_true(RescueAction.new(Direction.forward()) is Action)
	assert_true(PivotAction.new(Direction.backward()) is Action)
	assert_true(ShootAction.new(Direction.forward()) is Action)
	assert_true(ShootAction.new(Direction.forward()).direction.equals(Direction.forward()))


# ── T-016: rescue ────────────────────────────────────────────────────────────


func test_rescue_liberta_cativo_adjacente() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Captive.new()}, 0)
	var result := _resolver.resolve(state, RescueAction.new(Direction.forward()))
	assert_null(result.state.unit_at(2), "cativo libertado some da grade")


func test_rescue_sem_cativo_e_no_op() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Sludge.new()}, 0)
	var result := _resolver.resolve(state, RescueAction.new(Direction.forward()))
	assert_not_null(result.state.unit_at(2), "não resgata inimigo")


# ── T-016: pivot ─────────────────────────────────────────────────────────────


func test_pivot_backward_inverte_o_facing() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 3, 1, {}, 0)
	var result := _resolver.resolve(state, PivotAction.new(Direction.backward()))
	assert_eq(result.state.warrior_facing(), -1)
	assert_eq(result.state.warrior_position(), 3, "pivot não move")


func test_pivot_forward_mantem_o_facing() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 3, 1, {}, 0)
	var result := _resolver.resolve(state, PivotAction.new(Direction.forward()))
	assert_eq(result.state.warrior_facing(), 1)


# ── T-016: shoot ─────────────────────────────────────────────────────────────


func test_shoot_atinge_primeira_unidade_na_linha() -> void:
	# warrior em 0, archer em 2 (dentro do alcance 3).
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {2: Archer.new()}, 0)
	var result := _resolver.resolve(state, ShootAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(2).health, 7 - 3, "archer perde SHOOT_POWER")


func test_shoot_mata_e_remove() -> void:
	# wizard (3 HP) morre com SHOOT_POWER 3.
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {2: Wizard.new()}, 0)
	var result := _resolver.resolve(state, ShootAction.new(Direction.forward()))
	assert_null(result.state.unit_at(2))


func test_shoot_atinge_so_a_primeira_da_linha() -> void:
	# sludge em 1 (mais perto) bloqueia o archer em 3.
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {1: Sludge.new(), 3: Archer.new()}, 0)
	var result := _resolver.resolve(state, ShootAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(1).health, 12 - 3, "acerta o sludge da frente")
	assert_eq(result.state.unit_at(3).health, 7, "archer atrás fica intacto")


func test_shoot_sem_alvo_no_alcance_e_no_op() -> void:
	# sludge em 5, fora do alcance 3.
	var state := LevelState.new(8, 7, Warrior.new(), 0, 1, {5: Sludge.new()}, 0)
	var result := _resolver.resolve(state, ShootAction.new(Direction.forward()))
	assert_eq(result.state.unit_at(5).health, 12)
