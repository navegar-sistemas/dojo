class_name Unit
extends RefCounted
## Base imutável de uma unidade do jogo. Subclasses definem os atributos em
## `_configure()`. Mudanças de saúde produzem uma NOVA unidade (imutabilidade),
## preservando o determinismo da resolução de turno.

var max_health: int
var attack_power: int
## Alcance de ataque em espaços: 1 = corpo-a-corpo; >1 = à distância.
var attack_range: int
var health: int


func _init(p_health: int = -1) -> void:
	_configure()
	health = max_health if p_health < 0 else p_health


## Define max_health/attack_power/attack_range. Toda subclasse sobrescreve.
func _configure() -> void:
	push_error("Unit._configure() deve ser sobrescrito pela subclasse")


func is_alive() -> bool:
	return health > 0


func is_enemy() -> bool:
	return false


func is_captive() -> bool:
	return false


## Comportamento de turno desta unidade (polimórfico). Default: inerte.
func create_behavior() -> UnitBehavior:
	return InertBehavior.new()


## Nova unidade do mesmo tipo com a saúde dada (clamp em [0, max]).
func clone_with_health(new_health: int) -> Unit:
	return get_script().new(clampi(new_health, 0, max_health))


## Nova unidade com `amount` de dano aplicado.
func damaged_by(amount: int) -> Unit:
	return clone_with_health(health - amount)
