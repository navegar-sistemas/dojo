extends GutTest
## Cobre a CONSTRUÇÃO do TurnEvent (T-014) e a EMISSÃO correta dos eventos pelo
## resolver/applier/enemy phase (T-009/T-011/T-013) — o contrato consumido pela
## pontuação (ADR-007) e pela apresentação (ADR-008).

var _resolver: TurnResolver


func before_each() -> void:
	_resolver = TurnResolver.new()


func _find(events: Array, kind: TurnEvent.Kind) -> TurnEvent:
	for event in events:
		if event.kind == kind:
			return event
	return null


# ── T-014: construção ────────────────────────────────────────────────────────


func test_turn_event_carrega_seus_dados() -> void:
	var event := TurnEvent.new(TurnEvent.Kind.ATTACKED, "warrior", 5, 3)
	assert_eq(event.kind, TurnEvent.Kind.ATTACKED)
	assert_eq(event.actor, "warrior")
	assert_eq(event.amount, 5)
	assert_eq(event.position, 3)


# ── Emissão: walk / attack / rest ────────────────────────────────────────────


func test_walk_emite_moved_com_a_posicao_alvo() -> void:
	var result := _resolver.resolve(
		LevelState.new(8, 7, Warrior.new(), 1, 1, {}, 0), WalkAction.new(Direction.forward())
	)
	var moved := _find(result.events, TurnEvent.Kind.MOVED)
	assert_not_null(moved)
	assert_eq(moved.position, 2)


func test_attack_emite_attacked_com_o_dano() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: ThickSludge.new()}, 0)
	var attacked := _find(
		_resolver.resolve(state, AttackAction.new(Direction.forward())).events,
		TurnEvent.Kind.ATTACKED
	)
	assert_not_null(attacked)
	assert_eq(attacked.amount, 5, "dano de ataque do warrior")


func test_matar_emite_enemy_defeated() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Wizard.new()}, 0)
	var events := _resolver.resolve(state, AttackAction.new(Direction.forward())).events
	assert_not_null(_find(events, TurnEvent.Kind.ENEMY_DEFEATED))


func test_rest_emite_rested_com_a_cura() -> void:
	var state := LevelState.new(8, 7, Warrior.new(15), 1, 1, {}, 0)
	var rested := _find(_resolver.resolve(state, RestAction.new()).events, TurnEvent.Kind.RESTED)
	assert_not_null(rested)
	assert_eq(rested.amount, 2, "10% de 20")


# ── Emissão: enemy phase / vitória / derrota ─────────────────────────────────


func test_enemy_phase_emite_damaged() -> void:
	var state := LevelState.new(8, 7, Warrior.new(), 1, 1, {2: Sludge.new()}, 0)
	var damaged := _find(_resolver.resolve(state, RestAction.new()).events, TurnEvent.Kind.DAMAGED)
	assert_not_null(damaged)
	assert_eq(damaged.amount, 3, "dano do sludge")


func test_vitoria_emite_won() -> void:
	var events := (
		_resolver
		. resolve(
			LevelState.new(8, 7, Warrior.new(), 6, 1, {}, 0), WalkAction.new(Direction.forward())
		)
		. events
	)
	assert_not_null(_find(events, TurnEvent.Kind.WON))


func test_derrota_emite_died() -> void:
	var state := LevelState.new(8, 7, Warrior.new(3), 1, 1, {2: Wizard.new()}, 0)
	var events := _resolver.resolve(state, RestAction.new()).events
	assert_not_null(_find(events, TurnEvent.Kind.DIED))
