class_name Captive
extends Unit
## Refém não-hostil (HP 1). Nunca ataca; deve ser resgatado, jamais atacado.


func _configure() -> void:
	max_health = 1
	attack_power = 0
	attack_range = 0


func is_captive() -> bool:
	return true
