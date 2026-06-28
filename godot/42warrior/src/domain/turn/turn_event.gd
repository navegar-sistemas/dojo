class_name TurnEvent
extends RefCounted
## Descreve algo observável que ocorreu durante um turno — consumido pela
## pontuação e pela apresentação. Imutável.

enum Kind {
	MOVED, ATTACKED, DAMAGED, RESTED, RESCUED, SHOT, ENEMY_DEFEATED, WON, DIED, GLITCH_WINDOW
}

var kind: Kind
## Quem originou o evento: "warrior" ou o tipo do inimigo (ex.: "Sludge").
var actor: String
## Valor associado (dano, cura), ou 0.
var amount: int
## Posição-alvo na grade, ou -1.
var position: int


func _init(p_kind: Kind, p_actor: String, p_amount: int = 0, p_position: int = -1) -> void:
	kind = p_kind
	actor = p_actor
	amount = p_amount
	position = p_position
