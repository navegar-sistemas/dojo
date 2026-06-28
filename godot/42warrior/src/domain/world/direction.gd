class_name Direction
extends RefCounted
## Value object de direção: absoluta cardeal (NORTH/SOUTH/EAST/WEST) ou relativa ao warrior
## (FORWARD/BACKWARD).
##
## Direções absolutas carregam delta 2D (linha, coluna) e suportam pivot() horário N→E→S→W→N.
## Direções relativas carregam relative_sign() (+1/-1); o passo absoluto na grade é
## `facing * relative_sign()`, calculado por quem conhece o facing no LevelState.

enum Kind { NORTH, SOUTH, EAST, WEST, FORWARD, BACKWARD }

var kind: Kind


func _init(p_kind: Kind) -> void:
	kind = p_kind


# ─── Fábricas absolutas ──────────────────────────────────────────────────────


static func north() -> Direction:
	return Direction.new(Kind.NORTH)


static func south() -> Direction:
	return Direction.new(Kind.SOUTH)


static func east() -> Direction:
	return Direction.new(Kind.EAST)


static func west() -> Direction:
	return Direction.new(Kind.WEST)


# ─── Fábricas relativas ──────────────────────────────────────────────────────


static func forward() -> Direction:
	return Direction.new(Kind.FORWARD)


static func backward() -> Direction:
	return Direction.new(Kind.BACKWARD)


# ─── API absolutas ───────────────────────────────────────────────────────────


## Delta (linha, coluna) na grade 2D. Apenas para direções absolutas.
func delta() -> Vector2i:
	match kind:
		Kind.NORTH:
			return Vector2i(-1, 0)
		Kind.SOUTH:
			return Vector2i(1, 0)
		Kind.EAST:
			return Vector2i(0, 1)
		Kind.WEST:
			return Vector2i(0, -1)
	return Vector2i.ZERO


## Rotação 90° horária: N→E→S→W→N. Apenas para direções absolutas.
func pivot() -> Direction:
	match kind:
		Kind.NORTH:
			return Direction.new(Kind.EAST)
		Kind.EAST:
			return Direction.new(Kind.SOUTH)
		Kind.SOUTH:
			return Direction.new(Kind.WEST)
		Kind.WEST:
			return Direction.new(Kind.NORTH)
	return Direction.new(kind)


# ─── API relativas ───────────────────────────────────────────────────────────


## Sinal +1 (forward) ou -1 (backward). Apenas para direções relativas.
func relative_sign() -> int:
	return 1 if kind == Kind.FORWARD else -1


# ─── API compartilhada ───────────────────────────────────────────────────────


func opposite() -> Direction:
	match kind:
		Kind.NORTH, Kind.SOUTH:
			return Direction.new(Kind.SOUTH if kind == Kind.NORTH else Kind.NORTH)
		Kind.EAST, Kind.WEST:
			return Direction.new(Kind.WEST if kind == Kind.EAST else Kind.EAST)
		_:
			return Direction.new(Kind.BACKWARD if kind == Kind.FORWARD else Kind.FORWARD)


func equals(other: Direction) -> bool:
	return other != null and other.kind == kind
