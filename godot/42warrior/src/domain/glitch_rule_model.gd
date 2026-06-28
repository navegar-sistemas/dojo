class_name GlitchRuleModel
extends RefCounted
## Modelo de janela de glitch SEEDADA e DETERMINÍSTICA (T-190, ADR-034).
## window_open(seed, turn) é a única fonte do predicado "janela de glitch aberta";
## build_turn_events publica GLITCH_WINDOW no canal de eventos do turno.
## RefCounted puro — sem RNG, sem Time, sem dependência de engine.

## Comprimento do ciclo de janela em turnos.
const _PERIOD := 7
## Quantos turnos consecutivos a janela permanece aberta dentro do ciclo.
const _DURATION := 3


func window_open(seed: int, turn: int) -> bool:
	return (seed + turn) % _PERIOD < _DURATION


func build_turn_events(seed: int, turn: int) -> Array:
	if not window_open(seed, turn):
		return []
	return [TurnEvent.new(TurnEvent.Kind.GLITCH_WINDOW, "glitch", 0)]
