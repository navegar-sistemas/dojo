class_name RangedBehavior
extends UnitBehavior
## Ataca o warrior à distância dentro do alcance, na direção que o inimigo encara e
## se a linha não estiver bloqueada por outra unidade (archer, wizard).


func damage_to_warrior(state: LevelState, self_position: int, unit: Unit) -> int:
	var to_warrior := state.warrior_position() - self_position
	var distance := absi(to_warrior)
	if distance < 1 or distance > unit.attack_range:
		return 0
	if signi(to_warrior) != _facing(state, self_position):
		return 0
	if _line_blocked(state, self_position, state.warrior_position()):
		return 0
	return unit.attack_power


## Facing fixo (fidelidade ao gem): o inimigo encara a entrada do warrior, isto é, o lado
## oposto à escada. Quando o inimigo está exatamente na escada, signi(0)=0 seria inválido;
## nesse caso deriva a direção da posição do warrior (que sempre está do outro lado).
func _facing(state: LevelState, self_position: int) -> int:
	var facing := signi(self_position - state.stairs_position())
	if facing == 0:
		return signi(state.warrior_position() - self_position)
	return facing


func _line_blocked(state: LevelState, from_position: int, to_position: int) -> bool:
	var step := signi(to_position - from_position)
	var position := from_position + step
	while position != to_position:
		if state.unit_at(position) != null:
			return true
		position += step
	return false
