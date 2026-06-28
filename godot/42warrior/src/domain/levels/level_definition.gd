class_name LevelDefinition
extends RefCounted
## Definição declarativa de um nível da beginner tower (ADR-006). Apenas dados:
## layout, unidades (por fábrica, para o loader instanciar frescas), escada, facing
## inicial, descrição, habilidades introduzidas, time bonus e ace score. Sem regra.

var index: int
var width: int
var warrior_position: int
var warrior_facing: int
var stairs_position: int
var description: String
var abilities: PackedStringArray
var time_bonus: int
var ace_score: int
## position:int -> Callable que devolve uma Unit nova.
var _unit_makers: Dictionary


func _init(config: Dictionary) -> void:
	index = config["index"]
	width = config["width"]
	warrior_position = config["warrior_position"]
	warrior_facing = config["warrior_facing"]
	stairs_position = config["stairs_position"]
	description = config["description"]
	abilities = config["abilities"]
	time_bonus = config["time_bonus"]
	ace_score = config["ace_score"]
	_unit_makers = config["units"]


## Monta um dicionário fresco {posição: Unit} — instâncias novas a cada carga.
func build_units() -> Dictionary:
	var units := {}
	for position in _unit_makers:
		var make: Callable = _unit_makers[position]
		units[position] = make.call()
	return units
