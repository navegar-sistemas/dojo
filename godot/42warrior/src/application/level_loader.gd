class_name LevelLoader
extends RefCounted
## Monta o LevelState inicial de uma LevelDefinition (ADR-006).


func load_definition(definition: LevelDefinition) -> LevelState:
	if definition.rows > 1:
		return LevelState.from_2d(
			definition.rows,
			definition.width,
			definition.stairs_position_2d,
			Warrior.new(),
			definition.warrior_position_2d,
			definition.warrior_facing,
			definition.build_units_2d(),
			0,
			definition.warrior_direction
		)
	return LevelState.new(
		definition.width,
		definition.stairs_position,
		Warrior.new(),
		definition.warrior_position,
		definition.warrior_facing,
		definition.build_units(),
		0
	)


func load_level(index: int) -> LevelState:
	return load_definition(BeginnerTower.definition(index))
