class_name LevelLoader
extends RefCounted
## Monta o LevelState inicial de uma LevelDefinition (ADR-006).


func load_definition(definition: LevelDefinition) -> LevelState:
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
