class_name MeleeBehavior
extends UnitBehavior
## Ataca o warrior quando ele está adjacente (sludge, thick sludge).


func damage_to_warrior(state: LevelState, self_position: int, unit: Unit) -> int:
	if absi(state.warrior_position() - self_position) == 1:
		return unit.attack_power
	return 0
