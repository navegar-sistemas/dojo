class_name LevelDefinition
extends RefCounted
## Definição declarativa de um nível da beginner tower (ADR-006). Apenas dados:
## layout, unidades (por fábrica, para o loader instanciar frescas), escada, facing
## inicial, descrição, habilidades introduzidas, time bonus e ace score. Sem regra.

var index: int
var width: int
## Número de linhas da grade 2D (default 1 = corredor 1xN).
var rows: int = 1
var warrior_position: int
var warrior_facing: int
var stairs_position: int
## Posição 2D do warrior (válida quando rows > 1).
var warrior_position_2d: Vector2i = Vector2i.ZERO
## Posição 2D da escada (válida quando rows > 1).
var stairs_position_2d: Vector2i = Vector2i.ZERO
## Direção inicial do warrior em grade 2D (null = derivar de warrior_facing).
var warrior_direction: Direction = null
var description: String
var abilities: PackedStringArray
var time_bonus: int
var ace_score: int
var is_sandbox: bool = false
var hint_text: String = ""
## position:int -> Callable que devolve uma Unit nova (modo 1D, legado).
var _unit_makers: Dictionary
## Vector2i -> Callable que devolve uma Unit nova (modo 2D, quando rows > 1).
var _unit_makers_2d: Dictionary


func _init(config: Dictionary) -> void:
	index = config["index"]
	width = config["width"]
	rows = config.get("rows", 1)
	warrior_position = config["warrior_position"]
	warrior_facing = config["warrior_facing"]
	stairs_position = config["stairs_position"]
	warrior_position_2d = config.get("warrior_position_2d", Vector2i.ZERO)
	stairs_position_2d = config.get("stairs_position_2d", Vector2i.ZERO)
	warrior_direction = config.get("warrior_direction", null)
	description = config["description"]
	abilities = config["abilities"]
	time_bonus = config["time_bonus"]
	ace_score = config["ace_score"]
	is_sandbox = config.get("is_sandbox", false)
	hint_text = config.get("hint_text", "")
	_unit_makers = config.get("units", {})
	_unit_makers_2d = config.get("units_2d", {})


## Monta um dicionário fresco {posição: Unit} — instâncias novas a cada carga (1D).
func build_units() -> Dictionary:
	var units := {}
	for position in _unit_makers:
		var make: Callable = _unit_makers[position]
		units[position] = make.call()
	return units


## Monta um dicionário fresco {Vector2i: Unit} — instâncias novas a cada carga (2D).
func build_units_2d() -> Dictionary:
	var units: Dictionary = {}
	for pos: Vector2i in _unit_makers_2d:
		var make: Callable = _unit_makers_2d[pos]
		units[pos] = make.call()
	return units
