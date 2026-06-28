class_name Archer
extends Unit
## Inimigo à distância (HP 7, alcance 3). Perigoso para descansar por perto.


func _configure() -> void:
	max_health = 7
	attack_power = 3
	attack_range = 3


func is_enemy() -> bool:
	return true


func create_behavior() -> UnitBehavior:
	return RangedBehavior.new()
