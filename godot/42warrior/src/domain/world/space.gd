class_name Space
extends RefCounted
## Visão somente-leitura de um espaço da grade, devolvida pelos sentidos.
## Encapsula o que o jogador pode saber sem expor a unidade mutável diretamente.

var _unit: Unit
var _is_stairs: bool
var _is_wall: bool
var _position: int


func _init(unit: Unit, is_stairs: bool, is_wall: bool, position: int) -> void:
	_unit = unit
	_is_stairs = is_stairs
	_is_wall = is_wall
	_position = position


static func wall(position: int) -> Space:
	return Space.new(null, false, true, position)


static func of(unit: Unit, is_stairs: bool, position: int) -> Space:
	return Space.new(unit, is_stairs, false, position)


## Posição desta casa na grade — usada por direction_of(space).
func position() -> int:
	return _position


func is_wall() -> bool:
	return _is_wall


func is_stairs() -> bool:
	return _is_stairs


## Vazio = sem parede e sem unidade (a escada não conta como unidade).
func is_empty() -> bool:
	return not _is_wall and _unit == null


func is_enemy() -> bool:
	return _unit != null and _unit.is_enemy()


func is_captive() -> bool:
	return _unit != null and _unit.is_captive()


## O tipo da unidade contida (ex.: "Sludge"), ou "" se não houver.
func unit_type() -> String:
	if _unit == null:
		return ""
	return _unit.get_script().get_global_name()
