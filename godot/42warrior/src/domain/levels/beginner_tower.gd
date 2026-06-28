class_name BeginnerTower
extends RefCounted
## As 9 definições da beginner tower. Fonte canônica ratificada (usuario): o gem
## original ryanb/ruby-warrior, towers/beginner/level_001.rb..level_009.rb. width,
## posições de unidade, escada, time_bonus e ace_score são os literais do código-fonte
## (ancorados pelo teste test_beginner_tower_canonical.gd). O facing por-unidade do
## original é omitido: o combate aqui não depende dele (melee por adjacência, ranged
## por alcance/linha).

const LEVEL_COUNT := 9


static func definitions() -> Array:
	return [
		_level_1(),
		_level_2(),
		_level_3(),
		_level_4(),
		_level_5(),
		_level_6(),
		_level_7(),
		_level_8(),
		_level_9(),
	]


static func definition(index: int) -> LevelDefinition:
	return definitions()[index - 1]


static func _level_1() -> LevelDefinition:
	return (
		LevelDefinition
		. new(
			{
				"index": 1,
				"width": 8,
				"warrior_position": 0,
				"warrior_facing": 1,
				"stairs_position": 7,
				"description": "Um corredor longo com a escada no fim. Nada no caminho.",
				"abilities": PackedStringArray(["walk"]),
				"time_bonus": 15,
				"ace_score": 10,
				"units": {},
			}
		)
	)


static func _level_2() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 2,
			"width": 8,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 7,
			"description": "Escuro demais para ver, mas você sente cheiro de sludge.",
			"abilities": PackedStringArray(["feel", "attack"]),
			"time_bonus": 20,
			"ace_score": 26,
			"units": {4: func() -> Unit: return Sludge.new()},
		}
	)


static func _level_3() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 3,
			"width": 9,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 8,
			"description": "Uma horda de sludge.",
			"abilities": PackedStringArray(["health", "rest"]),
			"time_bonus": 35,
			"ace_score": 71,
			"units":
			{
				2: func() -> Unit: return Sludge.new(),
				4: func() -> Unit: return Sludge.new(),
				5: func() -> Unit: return Sludge.new(),
				7: func() -> Unit: return Sludge.new(),
			},
		}
	)


static func _level_4() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 4,
			"width": 7,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 6,
			"description": "Você ouve cordas de arco sendo esticadas.",
			"abilities": PackedStringArray([]),
			"time_bonus": 45,
			"ace_score": 90,
			"units":
			{
				2: func() -> Unit: return ThickSludge.new(),
				3: func() -> Unit: return Archer.new(),
				5: func() -> Unit: return ThickSludge.new(),
			},
		}
	)


static func _level_5() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 5,
			"width": 7,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 6,
			"description": "Gritos por socorro — há cativos a resgatar.",
			"abilities": PackedStringArray(["rescue"]),
			"time_bonus": 45,
			"ace_score": 123,
			"units":
			{
				2: func() -> Unit: return Captive.new(),
				3: func() -> Unit: return Archer.new(),
				4: func() -> Unit: return Archer.new(),
				5: func() -> Unit: return ThickSludge.new(),
				6: func() -> Unit: return Captive.new(),
			},
		}
	)


static func _level_6() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 6,
			"width": 8,
			"warrior_position": 2,
			"warrior_facing": 1,
			"stairs_position": 7,
			"description": "A parede atrás está mais longe; mais gritos por socorro.",
			"abilities": PackedStringArray([]),
			"time_bonus": 55,
			"ace_score": 105,
			"units":
			{
				0: func() -> Unit: return Captive.new(),
				4: func() -> Unit: return ThickSludge.new(),
				6: func() -> Unit: return Archer.new(),
				7: func() -> Unit: return Archer.new(),
			},
		}
	)


static func _level_7() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 7,
			"width": 6,
			"warrior_position": 5,
			"warrior_facing": 1,
			"stairs_position": 0,
			"description": "Uma parede à frente, uma abertura atrás.",
			"abilities": PackedStringArray(["pivot"]),
			"time_bonus": 30,
			"ace_score": 50,
			"units":
			{
				1: func() -> Unit: return Archer.new(),
				3: func() -> Unit: return ThickSludge.new(),
			},
		}
	)


static func _level_8() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 8,
			"width": 6,
			"warrior_position": 0,
			"warrior_facing": 1,
			"stairs_position": 5,
			"description":
			"Murmúrios de magos — cuidado com as varinhas mortais. Você achou um arco.",
			"abilities": PackedStringArray(["look", "shoot"]),
			"time_bonus": 20,
			"ace_score": 46,
			"units":
			{
				2: func() -> Unit: return Captive.new(),
				3: func() -> Unit: return Wizard.new(),
				4: func() -> Unit: return Wizard.new(),
			},
		}
	)


static func _level_9() -> LevelDefinition:
	return LevelDefinition.new(
		{
			"index": 9,
			"width": 11,
			"warrior_position": 5,
			"warrior_facing": 1,
			"stairs_position": 0,
			"description": "Aplique todas as habilidades. Cuide das suas costas.",
			"abilities": PackedStringArray([]),
			"time_bonus": 40,
			"ace_score": 100,
			"units":
			{
				1: func() -> Unit: return Captive.new(),
				2: func() -> Unit: return Archer.new(),
				7: func() -> Unit: return ThickSludge.new(),
				9: func() -> Unit: return Wizard.new(),
				10: func() -> Unit: return Captive.new(),
			},
		}
	)
