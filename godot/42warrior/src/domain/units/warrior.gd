class_name Warrior
extends Unit
## O herói controlado pela lógica do jogador. Atributos espelham o Ruby Warrior
## (HP 20, ataque 5 corpo-a-corpo). O dano reduzido ao atacar para trás é aplicado
## pela resolução do turno, não aqui.


func _configure() -> void:
	max_health = 20
	attack_power = 5
	attack_range = 1
