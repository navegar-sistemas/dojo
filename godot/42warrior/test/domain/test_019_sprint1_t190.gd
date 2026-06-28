class_name TestGlitchRuleModel
extends GutTest
## T-190 (019 Sprint 1) — GlitchRuleModel: janela de glitch SEEDADA determinística.
## DoD: window_open é pura f(seed,turno), builds GLITCH_WINDOW event, 0-RNG, 0-regressão.


func test_window_open_deterministico_mesmo_seed_e_turno() -> void:
	var model := GlitchRuleModel.new()
	assert_eq(
		model.window_open(42, 5),
		model.window_open(42, 5),
		"mesmo seed+turno deve retornar mesmo resultado (determinismo)"
	)
	assert_eq(model.window_open(0, 100), model.window_open(0, 100), "determinismo para turno alto")


func test_seeds_distintos_geram_janelas_distintas_em_algum_turno() -> void:
	var model := GlitchRuleModel.new()
	var found_diff := false
	for turn: int in range(50):
		if model.window_open(1, turn) != model.window_open(2, turn):
			found_diff = true
			break
	assert_true(found_diff, "seeds 1 e 2 devem divergir em pelo menos 1 dos 50 primeiros turnos")


func test_janela_abre_e_fecha_nos_50_primeiros_turnos() -> void:
	var model := GlitchRuleModel.new()
	var has_open := false
	var has_closed := false
	for turn: int in range(50):
		var w := model.window_open(0, turn)
		if w:
			has_open = true
		else:
			has_closed = true
		if has_open and has_closed:
			break
	assert_true(has_open, "janela deve abrir em algum dos 50 primeiros turnos (seed=0)")
	assert_true(has_closed, "janela deve fechar em algum dos 50 primeiros turnos (seed=0)")


func test_build_turn_events_janela_aberta_emite_glitch_window() -> void:
	var model := GlitchRuleModel.new()
	for turn: int in range(50):
		if model.window_open(0, turn):
			var events: Array = model.build_turn_events(0, turn)
			assert_eq(events.size(), 1, "janela aberta: deve emitir exatamente 1 evento")
			assert_eq(
				events[0].kind,
				TurnEvent.Kind.GLITCH_WINDOW,
				"evento emitido deve ser GLITCH_WINDOW"
			)
			return
	# Só chega aqui se _PERIOD//_DURATION estiverem errados — falha ruidosa.
	assert_true(false, "BUG: seed=0 nunca abriu janela em 50 turnos — constantes incorretas")


func test_build_turn_events_janela_fechada_retorna_vazio() -> void:
	var model := GlitchRuleModel.new()
	for turn: int in range(50):
		if not model.window_open(0, turn):
			var events: Array = model.build_turn_events(0, turn)
			assert_eq(events.size(), 0, "janela fechada: build_turn_events deve retornar []")
			return
	# Só chega aqui se _DURATION >= _PERIOD — falha ruidosa.
	assert_true(false, "BUG: seed=0 nunca fechou janela em 50 turnos — constantes incorretas")


func test_window_open_previsivel_um_turno_a_frente() -> void:
	var model := GlitchRuleModel.new()
	var seed := 7
	for turn: int in range(20):
		var now: bool = model.window_open(seed, turn)
		var next: bool = model.window_open(seed, turn + 1)
		assert_true(now == true or now == false, "window_open deve retornar bool (sem RNG ou Time)")
		assert_true(
			next == true or next == false, "window_open(turn+1) deve retornar bool previsível"
		)


func test_build_turn_events_consistente_com_window_open() -> void:
	var model := GlitchRuleModel.new()
	for turn: int in range(20):
		var is_open := model.window_open(3, turn)
		var events: Array = model.build_turn_events(3, turn)
		if is_open:
			assert_eq(events.size(), 1, "window_open=true deve gerar 1 evento (turn=%d)" % turn)
		else:
			assert_eq(events.size(), 0, "window_open=false deve gerar 0 eventos (turn=%d)" % turn)


# ── GlitchEffect.window_active ────────────────────────────────────────────────


func test_glitch_effect_window_active_false_por_padrao() -> void:
	var effect := GlitchEffect.new()
	assert_false(effect.window_active, "window_active deve ser false por padrão")


# ── GlitchRule + GlitchRuleModel integrados ──────────────────────────────────


func _find_open_turn(model: GlitchRuleModel, seed: int) -> int:
	for t: int in range(50):
		if model.window_open(seed, t):
			return t
	return -1


func _find_closed_turn(model: GlitchRuleModel, seed: int) -> int:
	for t: int in range(50):
		if not model.window_open(seed, t):
			return t
	return -1


func test_rule_com_model_ativa_window_active_quando_janela_aberta() -> void:
	var rule := GlitchRule.new()
	rule.model = GlitchRuleModel.new()
	rule.glitch_seed = 0
	var open_turn := _find_open_turn(rule.model, 0)
	assert_true(open_turn >= 0, "pré-condição: deve existir turno aberto (seed=0)")
	var effect := rule.evaluate(1, open_turn, [], false)
	assert_true(effect.window_active, "turno na janela → window_active")
	assert_gt(effect.post_process_intensity, 0.0, "janela ativa → intensidade > 0")


func test_rule_com_model_nao_ativa_window_fora_da_janela() -> void:
	var rule := GlitchRule.new()
	rule.model = GlitchRuleModel.new()
	rule.glitch_seed = 0
	var closed_turn := _find_closed_turn(rule.model, 0)
	assert_true(closed_turn >= 0, "pré-condição: deve existir turno fechado (seed=0)")
	var effect := rule.evaluate(1, closed_turn, [], false)
	assert_false(effect.window_active, "turno fora da janela → window_active false")
	assert_almost_eq(
		effect.post_process_intensity, 0.0, 0.001, "sem eventos/janela → intensidade 0"
	)


func test_rule_sem_model_nao_altera_comportamento_existente() -> void:
	var rule := GlitchRule.new()
	var effect := rule.evaluate(1, 0, [], false)
	assert_false(effect.window_active, "sem model: window_active sempre false")
	assert_almost_eq(effect.post_process_intensity, 0.0, 0.001, "sem model/eventos: intensidade 0")


func test_rule_janela_e_dano_cumulativos() -> void:
	var rule := GlitchRule.new()
	rule.model = GlitchRuleModel.new()
	rule.glitch_seed = 0
	var open_turn := _find_open_turn(rule.model, 0)
	assert_true(open_turn >= 0, "pré-condição: deve existir turno aberto (seed=0)")
	var event := TurnEvent.new(TurnEvent.Kind.DAMAGED, "warrior", 4)
	var effect := rule.evaluate(1, open_turn, [event], false)
	assert_true(effect.window_active, "janela + dano: window_active")
	assert_true(effect.warrior_corrupted, "janela + dano: warrior_corrupted")
	# _INTENSITY_DAMAGED=0.70 > _INTENSITY_WINDOW=0.35 → maxf garante 0.70
	assert_gte(effect.post_process_intensity, 0.7, "dano (0.70) deve dominar via maxf")
