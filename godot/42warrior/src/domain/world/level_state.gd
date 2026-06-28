class_name LevelState
extends RefCounted
## Estado imutável de um nível. Toda transição produz um NOVO LevelState;
## as consultas são puras e não mutam. O warrior é guardado à parte das
## demais unidades; `units` mapeia posição → Unit (inimigos e cativos).
##
## API 1D (legado/beginner): _init aceita ints; posições e unidades são inteiros.
## API 2D: from_2d() aceita grade R×C com Vector2i; use space_at_2d/warrior_position_2d.

var _width: int
var _stairs_position: int
var _warrior: Warrior
var _warrior_position: int
## Sentido absoluto que o warrior encara na grade: +1 (direita) ou -1 (esquerda).
var _warrior_facing: int
var _units: Dictionary
var _turn: int

## Campos 2D (preenchidos via from_2d(); em LevelStates 1D ficam em -1/null).
var _rows: int = -1
var _cols: int = -1
var _stairs_2d: Vector2i = Vector2i(-1, -1)
var _warrior_pos_2d: Vector2i = Vector2i(-1, -1)
## Unidades 2D: Vector2i → Unit (usado só em from_2d()).
var _units_2d: Dictionary = {}


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


## Constrói um LevelState em grade R×C com posições 2D (Vector2i).
## warrior_facing: int ±1 (legado); unidades: {Vector2i: Unit}.
## 1×N com R=1 comporta-se identicamente ao corredor 1D (subcaso do modelo unificado).
static func from_2d(
	rows: int,
	cols: int,
	stairs_pos: Vector2i,
	warrior: Warrior,
	warrior_pos: Vector2i,
	warrior_facing: int,
	units: Dictionary,
	turn: int
) -> LevelState:
	var s := LevelState.new(cols, stairs_pos.y, warrior, warrior_pos.y, warrior_facing, {}, turn)
	s._rows = rows
	s._cols = cols
	s._stairs_2d = stairs_pos
	s._warrior_pos_2d = warrior_pos
	s._units_2d = units.duplicate()
	return s


# ── Acessores 1D (legado) ─────────────────────────────────────────────────────


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


# ── Acessores 2D ─────────────────────────────────────────────────────────────


func rows() -> int:
	return _rows if _rows >= 0 else 1


func cols() -> int:
	return _cols if _cols >= 0 else _width


func warrior_position_2d() -> Vector2i:
	return _warrior_pos_2d if _rows >= 0 else Vector2i(0, _warrior_position)


func stairs_position_2d() -> Vector2i:
	return _stairs_2d if _rows >= 0 else Vector2i(0, _stairs_position)


# ── Consultas espaciais (puras) ──────────────────────────────────────────────


func space_at(position: int) -> Space:
	if position < 0 or position >= _width:
		return Space.wall(position)
	return Space.of(_units.get(position, null), position == _stairs_position, position)


## Consulta espacial 2D: retorna parede se pos estiver fora de [0,rows-1]×[0,cols-1].
func space_at_2d(pos: Vector2i) -> Space:
	var r := rows()
	var c := cols()
	if pos.x < 0 or pos.x >= r or pos.y < 0 or pos.y >= c:
		return Space.wall(0)
	var unit: Unit = _units_2d.get(pos, null)
	var is_stairs: bool = pos == stairs_position_2d()
	return Space.of(unit, is_stairs, 0)


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


## Novo estado 2D com posição do warrior alterada (produz LevelState 2D).
func with_warrior_position_2d(new_pos: Vector2i) -> LevelState:
	var result := LevelState.from_2d(
		rows(),
		cols(),
		stairs_position_2d(),
		_warrior,
		new_pos,
		_warrior_facing,
		_units_2d.duplicate(),
		_turn
	)
	return result
