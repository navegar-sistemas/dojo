extends GutTest
## Âncora de fidelidade: cada nível bate com os literais de
## ryanb/ruby-warrior towers/beginner/level_00N.rb (fonte ratificada por usuario).

const CANON := {
	1: {"width": 8, "warrior": 0, "stairs": 7, "units": {}},
	2: {"width": 8, "warrior": 0, "stairs": 7, "units": {4: "Sludge"}},
	3:
	{
		"width": 9,
		"warrior": 0,
		"stairs": 8,
		"units": {2: "Sludge", 4: "Sludge", 5: "Sludge", 7: "Sludge"},
	},
	4:
	{
		"width": 7,
		"warrior": 0,
		"stairs": 6,
		"units": {2: "ThickSludge", 3: "Archer", 5: "ThickSludge"}
	},
	5:
	{
		"width": 7,
		"warrior": 0,
		"stairs": 6,
		"units": {2: "Captive", 3: "Archer", 4: "Archer", 5: "ThickSludge", 6: "Captive"},
	},
	6:
	{
		"width": 8,
		"warrior": 2,
		"stairs": 7,
		"units": {0: "Captive", 4: "ThickSludge", 6: "Archer", 7: "Archer"},
	},
	7: {"width": 6, "warrior": 5, "stairs": 0, "units": {1: "Archer", 3: "ThickSludge"}},
	8: {"width": 6, "warrior": 0, "stairs": 5, "units": {2: "Captive", 3: "Wizard", 4: "Wizard"}},
	9:
	{
		"width": 11,
		"warrior": 5,
		"stairs": 0,
		"units": {1: "Captive", 2: "Archer", 7: "ThickSludge", 9: "Wizard", 10: "Captive"},
	},
}


func test_cada_nivel_bate_com_o_gem_canonico() -> void:
	for index in CANON:
		var canon: Dictionary = CANON[index]
		var definition := BeginnerTower.definition(index)
		assert_eq(definition.width, canon["width"], "L%d width" % index)
		assert_eq(definition.warrior_position, canon["warrior"], "L%d warrior_position" % index)
		assert_eq(definition.warrior_facing, 1, "L%d facing east" % index)
		assert_eq(definition.stairs_position, canon["stairs"], "L%d stairs" % index)
		_assert_units(definition, canon["units"], index)


func _assert_units(definition: LevelDefinition, expected: Dictionary, index: int) -> void:
	var units: Dictionary = definition.build_units()
	assert_eq(units.size(), expected.size(), "L%d nº de unidades" % index)
	for position in expected:
		assert_true(units.has(position), "L%d unidade em x%d" % [index, position])
		var type_name: String = units[position].get_script().get_global_name()
		assert_eq(type_name, expected[position], "L%d tipo em x%d" % [index, position])
