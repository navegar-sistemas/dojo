class_name ActionApplier
extends RefCounted
## Aplica a ação do warrior a um LevelState, produzindo um novo estado e os
## eventos resultantes. Despacha por tipo de Action (sem if-cadeia de strings).
## Cada método privado trata uma única ação.

const SHOOT_RANGE := 3
const SHOOT_POWER := 3


## Retorna { "state": LevelState, "events": Array }.
func apply(state: LevelState, action: Action) -> Dictionary:
	if action is WalkAction:
		return _walk(state, (action as WalkAction).direction)
	if action is AttackAction:
		return _attack(state, (action as AttackAction).direction)
	if action is RestAction:
		return _rest(state)
	return _apply_extended(state, action)


## Ações introduzidas no Sprint 2 (rescue/pivot/shoot), separadas para manter o
## despacho com no máximo 6 retornos por método (max-returns do gdlint).
func _apply_extended(state: LevelState, action: Action) -> Dictionary:
	if action is RescueAction:
		return _rescue(state, (action as RescueAction).direction)
	if action is PivotAction:
		return _pivot(state, (action as PivotAction).direction)
	if action is ShootAction:
		return _shoot(state, (action as ShootAction).direction)
	return _no_op(state)


func _no_op(state: LevelState) -> Dictionary:
	return {"state": state, "events": []}


func _walk(state: LevelState, direction: Direction) -> Dictionary:
	var target := state.position_toward(direction, 1)
	if not state.space_at(target).is_empty():
		return _no_op(state)
	var moved := state.with_warrior_position(target)
	return {"state": moved, "events": [TurnEvent.new(TurnEvent.Kind.MOVED, "warrior", 0, target)]}


func _attack(state: LevelState, direction: Direction) -> Dictionary:
	var target := state.position_toward(direction, 1)
	var unit := state.unit_at(target)
	if unit == null or unit.is_captive():
		return _no_op(state)
	var power := _attack_power(state.warrior().attack_power, direction)
	var wounded := unit.damaged_by(power)
	var events := [TurnEvent.new(TurnEvent.Kind.ATTACKED, "warrior", power, target)]
	if wounded.is_alive():
		return {"state": state.with_unit_at(target, wounded), "events": events}
	events.append(
		TurnEvent.new(
			TurnEvent.Kind.ENEMY_DEFEATED,
			unit.get_script().get_global_name(),
			unit.max_health,
			target
		)
	)
	return {"state": state.with_unit_at(target, null), "events": events}


## Ataque para trás: ceil(power/2), conforme ruby-warrior (abilities/attack.rb).
func _attack_power(base_power: int, direction: Direction) -> int:
	if direction.relative_sign() < 0:
		return ceili(base_power / 2.0)
	return base_power


func _rest(state: LevelState) -> Dictionary:
	var hero := state.warrior()
	var heal := roundi(hero.max_health * 0.1)
	var new_health := mini(hero.max_health, hero.health + heal)
	var healed := hero.clone_with_health(new_health)
	var restored := new_health - hero.health
	return {
		"state": state.with_warrior(healed),
		"events": [TurnEvent.new(TurnEvent.Kind.RESTED, "warrior", restored, -1)],
	}


func _rescue(state: LevelState, direction: Direction) -> Dictionary:
	var target := state.position_toward(direction, 1)
	var unit := state.unit_at(target)
	if unit == null or not unit.is_captive():
		return _no_op(state)
	return {
		"state": state.with_unit_at(target, null),
		"events": [TurnEvent.new(TurnEvent.Kind.RESCUED, "warrior", 0, target)],
	}


func _pivot(state: LevelState, direction: Direction) -> Dictionary:
	var new_facing := state.warrior_facing() * direction.relative_sign()
	return {"state": state.with_warrior_facing(new_facing), "events": []}


func _shoot(state: LevelState, direction: Direction) -> Dictionary:
	var target := _first_unit_position(state, direction)
	if target == -1:
		return _no_op(state)
	var unit := state.unit_at(target)
	if unit.is_captive():
		return _no_op(state)
	var wounded := unit.damaged_by(SHOOT_POWER)
	var events := [TurnEvent.new(TurnEvent.Kind.SHOT, "warrior", SHOOT_POWER, target)]
	if wounded.is_alive():
		return {"state": state.with_unit_at(target, wounded), "events": events}
	events.append(
		TurnEvent.new(
			TurnEvent.Kind.ENEMY_DEFEATED,
			unit.get_script().get_global_name(),
			unit.max_health,
			target
		)
	)
	return {"state": state.with_unit_at(target, null), "events": events}


## Posição da primeira unidade na linha de tiro (até SHOOT_RANGE), ou -1; para na parede.
func _first_unit_position(state: LevelState, direction: Direction) -> int:
	for distance in range(1, SHOOT_RANGE + 1):
		var position := state.position_toward(direction, distance)
		if state.space_at(position).is_wall():
			return -1
		if state.unit_at(position) != null:
			return position
	return -1
