class_name Senses
extends RefCounted
## Consultas do warrior sobre um snapshot do nível, sem efeito colateral (CQS).
## Não consome turno e nunca muta o estado.

const LOOK_RANGE := 3

var _state: LevelState


func _init(state: LevelState) -> void:
	_state = state


## Espaço adjacente na direção dada (1D relativa).
func feel(direction: Direction) -> Space:
	return _state.space_at(_state.position_toward(direction, 1))


## Os 3 espaços à frente na direção, do mais próximo ao mais distante (1D).
func look(direction: Direction) -> Array:
	var spaces: Array = []
	for distance in range(1, LOOK_RANGE + 1):
		spaces.append(_state.space_at(_state.position_toward(direction, distance)))
	return spaces


## Espaços que contêm unidades (inimigos/cativos), em ordem de posição.
func listen() -> Array:
	var spaces: Array = []
	for position in _state.unit_positions():
		spaces.append(_state.space_at(position))
	return spaces


func health() -> int:
	return _state.warrior().health


func direction_of_stairs() -> Direction:
	return _direction_to(_state.stairs_position())


## Direção relativa (forward/backward) da posição de uma unidade ouvida.
func direction_of_position(position: int) -> Direction:
	return _direction_to(position)


func _direction_to(target_position: int) -> Direction:
	var delta := target_position - _state.warrior_position()
	var target_sign := signi(delta)
	if target_sign == 0 or target_sign == _state.warrior_facing():
		return Direction.forward()
	return Direction.backward()


# ── API 2D ───────────────────────────────────────────────────────────────────


## Espaço adjacente em direção absoluta cardeal (2D).
func feel_2d(direction: Direction) -> Space:
	return _state.space_at_2d(_state.position_toward_2d(direction, 1))


## Os LOOK_RANGE espaços na direção absoluta, do mais próximo ao mais distante (2D).
func look_2d(direction: Direction) -> Array:
	var spaces: Array = []
	for distance: int in range(1, LOOK_RANGE + 1):
		spaces.append(_state.space_at_2d(_state.position_toward_2d(direction, distance)))
	return spaces


## Direção absoluta (NORTH/SOUTH/EAST/WEST) de target_pos relativo ao warrior.
## Eixo dominante: |Δrow| >= |Δcol| → N/S; |Δcol| > |Δrow| → E/W. Zero → NORTH.
func direction_of_2d(target_pos: Vector2i) -> Direction:
	var d := target_pos - _state.warrior_position_2d()
	if d == Vector2i.ZERO:
		return Direction.north()
	if absi(d.y) > absi(d.x):
		return Direction.east() if d.y > 0 else Direction.west()
	return Direction.south() if d.x > 0 else Direction.north()


## Direção absoluta cardeal da escada em relação ao warrior (2D).
func direction_of_stairs_2d() -> Direction:
	return direction_of_2d(_state.stairs_position_2d())
