class_name WalkAction
extends Action
## Mover um espaço na direção dada.

var direction: Direction


func _init(p_direction: Direction) -> void:
	direction = p_direction
