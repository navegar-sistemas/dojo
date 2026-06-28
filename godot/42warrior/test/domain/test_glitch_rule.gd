class_name TestGlitchRule
extends GutTest
## Testes do GlitchRule — regra de glitch determinística (T-151, ADR-034).

var _rule: GlitchRule


func before_each() -> void:
	_rule = GlitchRule.new()


func test_sem_eventos_sem_glitch() -> void:
	var effect := _rule.evaluate(1, 1, [], false)
	assert_false(effect.warrior_corrupted, "sem eventos: warrior não corrompido")
	assert_false(effect.screen_glitch, "sem eventos: sem flash de tela")
	assert_almost_eq(effect.post_process_intensity, 0.0, 0.001)


func test_erro_do_jogador_aciona_glitch_de_tela() -> void:
	var effect := _rule.evaluate(1, 1, [], true)
	assert_true(effect.screen_glitch, "erro: screen_glitch deve estar ativo")
	assert_true(effect.warrior_corrupted, "erro: warrior deve estar corrompido")
	assert_gt(effect.post_process_intensity, 0.5, "erro: intensidade deve ser alta")


func test_evento_damaged_corrompe_warrior() -> void:
	var event := TurnEvent.new(TurnEvent.Kind.DAMAGED, "warrior", 4)
	var effect := _rule.evaluate(1, 1, [event], false)
	assert_true(effect.warrior_corrupted, "DAMAGED: warrior corrompido")
	assert_false(effect.screen_glitch, "DAMAGED: sem flash de tela")
	assert_gt(effect.post_process_intensity, 0.5, "DAMAGED: intensidade maior que 0.5")


func test_evento_died_aciona_tela_e_warrior() -> void:
	var event := TurnEvent.new(TurnEvent.Kind.DIED, "warrior", 0)
	var effect := _rule.evaluate(1, 1, [event], false)
	assert_true(effect.screen_glitch, "DIED: screen_glitch ativo")
	assert_true(effect.warrior_corrupted, "DIED: warrior corrompido")
	assert_almost_eq(effect.post_process_intensity, 1.0, 0.001)


func test_determinismo_mesmo_resultado_para_mesmos_parametros() -> void:
	var event := TurnEvent.new(TurnEvent.Kind.DAMAGED, "warrior", 4)
	var e1 := _rule.evaluate(3, 5, [event], false)
	var e2 := _rule.evaluate(3, 5, [event], false)
	assert_eq(e1.warrior_corrupted, e2.warrior_corrupted, "determinismo: warrior_corrupted igual")
	assert_eq(e1.screen_glitch, e2.screen_glitch, "determinismo: screen_glitch igual")
	assert_almost_eq(e1.post_process_intensity, e2.post_process_intensity, 0.001)


func test_erro_sobrescreve_eventos() -> void:
	var event := TurnEvent.new(TurnEvent.Kind.DAMAGED, "warrior", 4)
	var e_erro := _rule.evaluate(1, 1, [event], true)
	var e_sem_erro := _rule.evaluate(1, 1, [event], false)
	assert_gt(
		e_erro.post_process_intensity,
		e_sem_erro.post_process_intensity,
		"erro deve intensidade maior que só DAMAGED"
	)
	assert_true(e_erro.screen_glitch, "erro + evento: screen_glitch ativo")
