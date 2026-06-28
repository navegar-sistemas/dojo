class_name Direction
extends RefCounted
## Value object de direção relativa ao warrior: FORWARD ou BACKWARD.
##
## A direção é relativa ao sentido para o qual o warrior olha (o facing, mantido
## no LevelState). `relative_sign()` devolve +1 (forward) ou -1 (backward); o passo
## absoluto na grade é `facing * relative_sign()`, calculado por quem conhece o facing.

enum Kind { FORWARD, BACKWARD }

var kind: Kind


func _init(p_kind: Kind) -> void:
	kind = p_kind


static func forward() -> Direction:
	return Direction.new(Kind.FORWARD)


static func backward() -> Direction:
	return Direction.new(Kind.BACKWARD)


func relative_sign() -> int:
	return 1 if kind == Kind.FORWARD else -1


func opposite() -> Direction:
	return Direction.new(Kind.BACKWARD if kind == Kind.FORWARD else Kind.FORWARD)


func equals(other: Direction) -> bool:
	return other != null and other.kind == kind
