extends GutTest
## T-191 (019 Sprint 1) — GlitchDetection: feel/look revelam janela glitch via Space.
## DoD: CQS (não consome turno), ≥1 turno de antecedência via glitch_next(),
## 0-regressão, engine-independente.
##
## GlitchRuleModel usa _PERIOD=7, _DURATION=3 (constantes internas).
## seed=0: janela aberta em turnos 0,1,2 — fechada em 3,4,5,6 — reabre em 7.


func _make_warrior() -> Warrior:
	return Warrior.new()


func _make_state(turn: int) -> LevelState:
	return LevelState.new(6, 5, _make_warrior(), 0, 1, {}, turn)


func _make_state_with_model(turn: int, seed: int) -> LevelState:
	var model := GlitchRuleModel.new()
	return _make_state(turn).with_glitch_model(model, seed)


# ── Space.glitch_active / glitch_next por padrão ────────────────────────────


func test_space_glitch_active_false_por_padrao() -> void:
	var s := Space.of(null, false, 1)
	assert_false(s.glitch_active(), "Space sem glitch: glitch_active() deve ser false")


func test_space_glitch_next_false_por_padrao() -> void:
	var s := Space.of(null, false, 1)
	assert_false(s.glitch_next(), "Space sem glitch: glitch_next() deve ser false")


# ── LevelState.space_at sem model ─────────────────────────────────────────────


func test_space_at_sem_model_glitch_false() -> void:
	var state := _make_state(0)
	var s := state.space_at(1)
	assert_false(s.glitch_active(), "sem model: glitch_active() deve ser false")
	assert_false(s.glitch_next(), "sem model: glitch_next() deve ser false")


# ── LevelState.with_glitch_model → space_at propaga glitch ──────────────────


func test_space_at_turno_na_janela_ativa_glitch_active() -> void:
	# seed=0, turn=0: (0+0)%7=0 < 3 → janela aberta
	var state := _make_state_with_model(0, 0)
	var s := state.space_at(1)
	assert_true(s.glitch_active(), "turno 0 na janela (seed=0): glitch_active() deve ser true")


func test_space_at_turno_fora_da_janela_glitch_active_false() -> void:
	# seed=0, turn=3: (0+3)%7=3 >= 3 → janela fechada
	var state := _make_state_with_model(3, 0)
	var s := state.space_at(1)
	assert_false(
		s.glitch_active(), "turno 3 fora da janela (seed=0): glitch_active() deve ser false"
	)


func test_space_at_glitch_next_prediz_proximo_turno() -> void:
	# seed=0, turn=2: (0+2)%7=2 < 3 → aberta; turn=3: (0+3)%7=3 >= 3 → fechada
	var state := _make_state_with_model(2, 0)
	var s := state.space_at(1)
	assert_true(s.glitch_active(), "turno 2 na janela: glitch_active=true")
	assert_false(s.glitch_next(), "proximo turno (3) fora da janela: glitch_next=false")


func test_space_at_glitch_next_true_quando_proximo_turno_na_janela() -> void:
	# seed=0, turn=6: (0+6)%7=6 >= 3 → fechada; turn=7: (0+7)%7=0 < 3 → aberta
	var state := _make_state_with_model(6, 0)
	var s := state.space_at(1)
	assert_false(s.glitch_active(), "turno 6 fora da janela: glitch_active=false")
	assert_true(
		s.glitch_next(), "proximo turno (7) na janela: glitch_next=true — antecipacao ≥1 turno"
	)


# ── CQS: space_at não muta o estado ────────────────────────────────────────


func test_space_at_cqs_resultado_idempotente() -> void:
	var state := _make_state_with_model(0, 0)
	var s1 := state.space_at(1)
	var s2 := state.space_at(1)
	assert_eq(
		s1.glitch_active(),
		s2.glitch_active(),
		"space_at() idempotente: mesma glitch_active nas duas chamadas (CQS)"
	)
	assert_eq(s1.glitch_next(), s2.glitch_next(), "space_at() idempotente: mesmo glitch_next (CQS)")


# ── space_at_2d propaga glitch ────────────────────────────────────────────────


func test_space_at_2d_sem_model_glitch_false() -> void:
	var model := GlitchRuleModel.new()
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), _make_warrior(), Vector2i(0, 0), 1, {}, 0)
	var s := state.space_at_2d(Vector2i(1, 1))
	assert_false(s.glitch_active(), "2D sem model: glitch_active() false")
	assert_false(s.glitch_next(), "2D sem model: glitch_next() false")


func test_space_at_2d_com_model_propaga_glitch() -> void:
	var model := GlitchRuleModel.new()
	var state := LevelState.from_2d(3, 5, Vector2i(2, 4), _make_warrior(), Vector2i(0, 0), 1, {}, 0)
	var state_g := state.with_glitch_model(model, 0)
	# seed=0, turn=0: janela aberta
	var s := state_g.space_at_2d(Vector2i(1, 1))
	assert_true(s.glitch_active(), "2D com model, turn=0: glitch_active true")


# ── Senses.feel e look expõem glitch via Space ─────────────────────────────


func test_feel_expoe_glitch_active_quando_model_configurado() -> void:
	var model := GlitchRuleModel.new()
	var state := _make_state(0).with_glitch_model(model, 0)
	var senses := Senses.new(state)
	# feel(forward) = espaço à frente do warrior (pos 1)
	var s := senses.feel(Direction.forward())
	assert_true(s.glitch_active(), "Senses.feel() expõe glitch_active via Space (turn=0, seed=0)")


func test_look_expoe_glitch_active_em_todos_os_espacos() -> void:
	var model := GlitchRuleModel.new()
	var state := _make_state(0).with_glitch_model(model, 0)
	var senses := Senses.new(state)
	var spaces: Array = senses.look(Direction.forward())
	for s: Space in spaces:
		assert_true(
			s.glitch_active(), "Senses.look(): todos os espaços devem ter glitch_active (turn=0)"
		)


func test_feel_sem_model_glitch_false() -> void:
	var state := _make_state(0)
	var senses := Senses.new(state)
	var s := senses.feel(Direction.forward())
	assert_false(
		s.glitch_active(), "Senses.feel() sem model: glitch_active false (legado preservado)"
	)


# ── Antecipação ≥1 turno: jogador lê glitch_next ANTES do turno ─────────────


func test_antecipacao_jogador_le_glitch_next_com_1_turno_de_avanco() -> void:
	# No turno 6 (janela fechada), o jogador lê glitch_next=true (turno 7 abre)
	# → pode planejar ação para o próximo turno SEM ser surpreendido
	var state := _make_state_with_model(6, 0)
	var senses := Senses.new(state)
	var s := senses.feel(Direction.forward())
	assert_false(s.glitch_active(), "turno atual (6) sem glitch: nao afeta o jogador agora")
	assert_true(
		s.glitch_next(),
		"jogador le glitch_next=true: glitch abre no proximo turno (antecipacao ≥1t)"
	)


func test_determinismo_glitch_detection_mesmo_seed_turno() -> void:
	var model := GlitchRuleModel.new()
	var s1 := _make_state(0).with_glitch_model(model, 42).space_at(1)
	var s2 := _make_state(0).with_glitch_model(model, 42).space_at(1)
	assert_eq(
		s1.glitch_active(),
		s2.glitch_active(),
		"determinismo: mesmo seed+turno → mesmo glitch_active"
	)
	assert_eq(
		s1.glitch_next(), s2.glitch_next(), "determinismo: mesmo seed+turno → mesmo glitch_next"
	)
