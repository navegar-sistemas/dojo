class_name LevelState
extends RefCounted
## Estado imutável de um nível (grade 1×N). Toda transição produz um NOVO
## LevelState; as consultas são puras e não mutam. O warrior é guardado à parte
## das demais unidades; `units` mapeia posição → Unit (inimigos e cativos).

var _width: int
var _stairs_position: int
var _warrior: Warrior
var _warrior_position: int
## Sentido absoluto que o warrior encara na grade: +1 (direita) ou -1 (esquerda).
var _warrior_facing: int
var _units: Dictionary
var _turn: int


func _init(
	width: int,
	stairs_position: int,
	warrior: Warrior,
	warrior_position: int,
	warrior_facing: int,
	units: Dictionary,
	turn: int
) -> void:
	_width = width
	_stairs_position = stairs_position
	_warrior = warrior
	_warrior_position = warrior_position
	_warrior_facing = warrior_facing
	_units = units
	_turn = turn


# ── Acessores ────────────────────────────────────────────────────────────────


func width() -> int:
	return _width


func warrior() -> Warrior:
	return _warrior


func warrior_position() -> int:
	return _warrior_position


func warrior_facing() -> int:
	return _warrior_facing


func stairs_position() -> int:
	return _stairs_position


func turn() -> int:
	return _turn


## Posições (ordenadas) das unidades vivas no nível, exceto o warrior.
func unit_positions() -> Array:
	var positions := _units.keys()
	positions.sort()
	return positions


func unit_at(position: int) -> Unit:
	return _units.get(position, null)


# ── Consultas espaciais (puras) ──────────────────────────────────────────────


func space_at(position: int) -> Space:
	if position < 0 or position >= _width:
		return Space.wall(position)
	return Space.of(_units.get(position, null), position == _stairs_position, position)


## Passo absoluto na grade para uma direção relativa ao warrior.
func step_of(direction: Direction) -> int:
	return _warrior_facing * direction.relative_sign()


## Posição a `distance` passos do warrior na direção dada.
func position_toward(direction: Direction, distance: int) -> int:
	return _warrior_position + step_of(direction) * distance


# ── Construtores derivados (imutáveis) ───────────────────────────────────────


func _clone_units() -> Dictionary:
	return _units.duplicate()


func with_warrior(new_warrior: Warrior) -> LevelState:
	return LevelState.new(
		_width,
		_stairs_position,
		new_warrior,
		_warrior_position,
		_warrior_facing,
		_clone_units(),
		_turn
	)


func with_warrior_position(new_position: int) -> LevelState:
	return LevelState.new(
		_width, _stairs_position, _warrior, new_position, _warrior_facing, _clone_units(), _turn
	)


func with_warrior_facing(new_facing: int) -> LevelState:
	return LevelState.new(
		_width, _stairs_position, _warrior, _warrior_position, new_facing, _clone_units(), _turn
	)


## Novo estado com a unidade da posição substituída (null remove a unidade).
func with_unit_at(position: int, unit: Unit) -> LevelState:
	var units := _clone_units()
	if unit == null:
		units.erase(position)
	else:
		units[position] = unit
	return LevelState.new(
		_width, _stairs_position, _warrior, _warrior_position, _warrior_facing, units, _turn
	)


## Mapa posição→Unit do início do turno (cópia defensiva). A fase de inimigos o usa
## como percepção de linha de tiro: um bloqueador morto/resgatado neste turno ainda
## bloqueava a linha quando os inimigos decidiram (fidelidade ao prepare_turn do gem).
func units_snapshot() -> Dictionary:
	return _clone_units()


## Novo estado com o mapa de unidades substituído (posição do warrior preservada).
func with_units(new_units: Dictionary) -> LevelState:
	return LevelState.new(
		_width,
		_stairs_position,
		_warrior,
		_warrior_position,
		_warrior_facing,
		new_units.duplicate(),
		_turn
	)


func with_turn(new_turn: int) -> LevelState:
	return LevelState.new(
		_width,
		_stairs_position,
		_warrior,
		_warrior_position,
		_warrior_facing,
		_clone_units(),
		new_turn
	)
