class_name Wizard
extends Unit
## Inimigo à distância letal (HP 3, mas ataque alto). Deve ser morto rápido.


func _configure() -> void:
	max_health = 3
	attack_power = 11
	attack_range = 3


func is_enemy() -> bool:
	return true


func create_behavior() -> UnitBehavior:
	return RangedBehavior.new()
