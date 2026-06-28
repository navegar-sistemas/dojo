class_name GlitchRule
extends RefCounted
## Regra de glitch DETERMINÍSTICA (ADR-034): dado floor/turn + turn_events + erro
## do código do jogador, decide os efeitos de glitch sem RNG (RNF-150).
## Mesmo estado+parâmetros → mesmo GlitchEffect. Coberto por teste de domínio.

const _INTENSITY_ERROR := 0.90
const _INTENSITY_DIED := 1.00
const _INTENSITY_DAMAGED := 0.70


## floor_index e turn_number fazem parte da assinatura determinística (RF-155 P1 futuro).
func evaluate(
	_floor_index: int, _turn_number: int, events: Array, has_player_error: bool
) -> GlitchEffect:
	var effect := GlitchEffect.new()
	if has_player_error:
		effect.screen_glitch = true
		effect.warrior_corrupted = true
		effect.post_process_intensity = _INTENSITY_ERROR
		return effect
	for event: TurnEvent in events:
		match event.kind:
			TurnEvent.Kind.DIED:
				effect.screen_glitch = true
				effect.warrior_corrupted = true
				effect.post_process_intensity = maxf(effect.post_process_intensity, _INTENSITY_DIED)
			TurnEvent.Kind.DAMAGED:
				effect.warrior_corrupted = true
				effect.post_process_intensity = maxf(
					effect.post_process_intensity, _INTENSITY_DAMAGED
				)
	return effect
