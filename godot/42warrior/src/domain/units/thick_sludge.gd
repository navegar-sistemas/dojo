class_name ThickSludge
extends Unit
## Inimigo corpo-a-corpo resistente (HP 24).


func _configure() -> void:
	max_health = 24
	attack_power = 3
	attack_range = 1


func is_enemy() -> bool:
	return true


func create_behavior() -> UnitBehavior:
	return MeleeBehavior.new()
