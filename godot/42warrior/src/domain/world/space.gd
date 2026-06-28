class_name Space
extends RefCounted
## Visão somente-leitura de um espaço da grade, devolvida pelos sentidos.
## Encapsula o que o jogador pode saber sem expor a unidade mutável diretamente.

var _unit: Unit
var _is_stairs: bool
var _is_wall: bool
var _position: int
var _position_2d: Vector2i = Vector2i(-1, -1)
## Campos de detecção de glitch (GlitchDetection T-191). Populados por LevelState
## quando um GlitchRuleModel está configurado; false por padrão (sem regressão).
var _glitch_active: bool = false
var _glitch_next: bool = false


func _init(unit: Unit, is_stairs: bool, is_wall: bool, position: int) -> void:
	_unit = unit
	_is_stairs = is_stairs
	_is_wall = is_wall
	_position = position


static func wall(position: int) -> Space:
	return Space.new(null, false, true, position)


static func of(unit: Unit, is_stairs: bool, position: int) -> Space:
	return Space.new(unit, is_stairs, false, position)


static func wall_2d(pos: Vector2i) -> Space:
	var s := Space.new(null, false, true, -1)
	s._position_2d = pos
	return s


static func of_2d(unit: Unit, is_stairs: bool, pos: Vector2i) -> Space:
	var s := Space.new(unit, is_stairs, false, -1)
	s._position_2d = pos
	return s


## Posição desta casa na grade 1D — usada por direction_of(space).
func position() -> int:
	return _position


## Posição desta casa na grade 2D.
func position_2d() -> Vector2i:
	return _position_2d


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


## true se a janela de glitch está ativa neste turno (populado por LevelState.space_at).
func glitch_active() -> bool:
	return _glitch_active


## true se a janela de glitch abrirá no próximo turno (antecipação ≥1 turno, T-191).
func glitch_next() -> bool:
	return _glitch_next


## Janela de glitch está ativa no turno atual? (GlitchDetection T-191)
func glitch_active() -> bool:
	return _glitch_active


## Janela de glitch estará ativa no PRÓXIMO turno? (antecipação ≥1 turno, CQS)
func glitch_next() -> bool:
	return _glitch_next
