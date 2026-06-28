class_name Sludge
extends Unit
## Inimigo corpo-a-corpo básico (HP 12).


func _configure() -> void:
	max_health = 12
	attack_power = 3
	attack_range = 1


func is_enemy() -> bool:
	return true


func create_behavior() -> UnitBehavior:
	return MeleeBehavior.new()
