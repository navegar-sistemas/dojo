class_name AttackAction
extends Action
## Atacar corpo-a-corpo a unidade adjacente na direção dada.

var direction: Direction


func _init(p_direction: Direction) -> void:
	direction = p_direction
