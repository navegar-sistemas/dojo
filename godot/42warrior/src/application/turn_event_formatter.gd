class_name TurnEventFormatter
extends RefCounted
## Converte a lista de TurnEvents de um turno em uma entrada textual legível.
## Isolado para que mudar a redação não mexa na UI (ADR-003).


func format_turn(events: Array, error: String) -> String:
	if events.is_empty():
		if error.is_empty():
			return "sem ação"
		return "erro: " + _first_line(error)
	var parts: PackedStringArray = []
	for event: TurnEvent in events:
		var line := _format_event(event)
		if not line.is_empty():
			parts.append(line)
	var text := " • ".join(parts)
	if not error.is_empty():
		text += "  [erro: " + _first_line(error) + "]"
	return text


func _format_event(event: TurnEvent) -> String:
	var kind := event.kind
	if kind == TurnEvent.Kind.MOVED:
		return "andou"
	if kind == TurnEvent.Kind.ATTACKED:
		return "atacou causando %d de dano" % event.amount
	if kind == TurnEvent.Kind.SHOT:
		return "disparou causando %d de dano" % event.amount
	if kind == TurnEvent.Kind.DAMAGED:
		return "levou %d de dano de %s" % [event.amount, event.actor]
	if kind == TurnEvent.Kind.RESTED:
		return "descansou (+%d HP)" % event.amount
	return _format_event_rare(event)


func _format_event_rare(event: TurnEvent) -> String:
	match event.kind:
		TurnEvent.Kind.RESCUED:
			return "resgatou cativo"
		TurnEvent.Kind.ENEMY_DEFEATED:
			return "%s derrotado" % event.actor
		TurnEvent.Kind.WON:
			return "vitória!"
		TurnEvent.Kind.DIED:
			return "derrota"
	return ""


func _first_line(text: String) -> String:
	var newline := text.find("\n")
	if newline < 0:
		return text.strip_edges()
	return text.left(newline).strip_edges()
