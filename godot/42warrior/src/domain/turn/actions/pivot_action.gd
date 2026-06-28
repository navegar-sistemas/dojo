class_name PivotAction
extends Action

var direction: Direction


func _init(p_direction: Direction = Direction.backward()) -> void:
	direction = p_direction
